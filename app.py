from flask import Flask, request, jsonify, render_template
from database import get_db_connection
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# API Endpoints
# A. Add Patient
@app.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.json
    required_fields = ['first_name', 'last_name', 'dob', 'gender', 'contact_no']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO Patients (First_Name, Last_Name, Date_of_Birth, Gender, Contact_No)
            VALUES (%s, %s, %s, %s, %s)
        """
        # Parameterized query to prevent SQL injection
        cursor.execute(query, (data['first_name'], data['last_name'], data['dob'], data['gender'], data['contact_no']))
        conn.commit()
        return jsonify({'message': 'Patient added successfully', 'patient_id': cursor.lastrowid}), 201
    except mysql.connector.IntegrityError as e:
        return jsonify({'error': 'Duplicate contact number or invalid data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# B. Add Urine Test Report
@app.route('/api/reports', methods=['POST'])
def add_report():
    data = request.json
    required_fields = ['patient_id', 'test_date', 'sample_id', 'lab_technician', 'diagnosis_status']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        
        # Foreign Key check is automatically handled by MySQL, but we can verify explicitly 
        # or rely on the IntegrityError
        query = """
            INSERT INTO Urine_Test_Reports (Patient_ID, Test_Date, Sample_ID, Lab_Technician, Diagnosis_Status)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data['patient_id'], data['test_date'], data['sample_id'], data['lab_technician'], data['diagnosis_status']))
        conn.commit()
        return jsonify({'message': 'Report added successfully', 'report_id': cursor.lastrowid}), 201
    except mysql.connector.IntegrityError as e:
        return jsonify({'error': 'Duplicate sample ID, invalid Patient ID, or invalid data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# C. Add Analyte Result
@app.route('/api/results', methods=['POST'])
def add_result():
    data = request.json
    required_fields = ['report_id', 'analyte_name', 'concentration', 'unit', 'reference_range']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO Analyte_Results (Report_ID, Analyte_Name, Concentration, Unit, Reference_Range)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data['report_id'], data['analyte_name'], data['concentration'], data['unit'], data['reference_range']))
        conn.commit()
        return jsonify({'message': 'Analyte result added successfully', 'result_id': cursor.lastrowid}), 201
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Invalid Report ID or invalid data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# D. Display Records
@app.route('/api/records/<table_name>', methods=['GET'])
def get_records(table_name):
    allowed_tables = ['patients', 'urine_test_reports', 'analyte_results']
    if table_name not in allowed_tables:
        return jsonify({'error': 'Invalid table'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        # Using string formatting for table name is safe here because it's validated against allowed_tables
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        
        # Serialize dates and decimals for JSON compatibility
        for row in records:
            for key, value in row.items():
                if hasattr(value, 'isoformat'):
                    row[key] = value.isoformat()
                elif hasattr(value, 'to_eng_string'):  
                    row[key] = float(value)
        return jsonify(records), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# E. Search
@app.route('/api/search', methods=['GET'])
def search_patient():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Search by ID or Name using Parameterized queries
        search_sql = """
            SELECT * FROM Patients
            WHERE Patient_ID = %s OR First_Name LIKE %s OR Last_Name LIKE %s
        """
        
        patient_id = query if query.isdigit() else None
        like_query = f"%{query}%"
        
        cursor.execute(search_sql, (patient_id, like_query, like_query))
        patients = cursor.fetchall()
        
        # Fetch related reports and results for each patient
        for patient in patients:
            if hasattr(patient['Date_of_Birth'], 'isoformat'):
                patient['Date_of_Birth'] = patient['Date_of_Birth'].isoformat()
                
            cursor.execute("SELECT * FROM Urine_Test_Reports WHERE Patient_ID = %s", (patient['Patient_ID'],))
            reports = cursor.fetchall()
            for report in reports:
                if hasattr(report['Test_Date'], 'isoformat'):
                    report['Test_Date'] = report['Test_Date'].isoformat()
                    
                cursor.execute("SELECT * FROM Analyte_Results WHERE Report_ID = %s", (report['Report_ID'],))
                results = cursor.fetchall()
                for result in results:
                    if hasattr(result['Concentration'], 'to_eng_string'):
                        result['Concentration'] = float(result['Concentration'])
                report['results'] = results
            patient['reports'] = reports

        return jsonify(patients), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
