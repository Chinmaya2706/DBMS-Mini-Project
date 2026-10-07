import random
from datetime import datetime, timedelta
from database import get_db_connection

def seed_database():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database.")
        return
    
    cursor = conn.cursor()

    first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    genders = ["Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female"]
    
    try:
        for i in range(10):
            # 1. Insert Patient
            first_name = first_names[i]
            last_name = last_names[i]
            dob = (datetime.now() - timedelta(days=random.randint(7000, 25000))).strftime('%Y-%m-%d')
            gender = genders[i]
            contact_no = f"555010{random.randint(1000, 9999)}"
            
            cursor.execute(
                "INSERT INTO Patients (First_Name, Last_Name, Date_of_Birth, Gender, Contact_No) VALUES (%s, %s, %s, %s, %s)",
                (first_name, last_name, dob, gender, contact_no)
            )
            patient_id = cursor.lastrowid
            
            # 2. Insert Urine Test Report
            test_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            sample_id = f"SMP2023{random.randint(10000, 99999)}"
            lab_technician = random.choice(["Tech A", "Tech B", "Tech C"])
            diagnosis_status = random.choice(["Normal", "Abnormal", "Needs Review"])
            
            cursor.execute(
                "INSERT INTO Urine_Test_Reports (Patient_ID, Test_Date, Sample_ID, Lab_Technician, Diagnosis_Status) VALUES (%s, %s, %s, %s, %s)",
                (patient_id, test_date, sample_id, lab_technician, diagnosis_status)
            )
            report_id = cursor.lastrowid
            
            # 3. Insert Analyte Results
            analytes = [
                ("Glucose", round(random.uniform(0.0, 30.0), 2), "mg/dL", "0-15"),
                ("Protein", round(random.uniform(0.0, 25.0), 2), "mg/dL", "0-14"),
                ("pH", round(random.uniform(4.5, 8.0), 2), "", "4.5-8.0"),
                ("Ketones", round(random.uniform(0.0, 5.0), 2), "mg/dL", "0-5")
            ]
            
            for analyte in analytes:
                cursor.execute(
                    "INSERT INTO Analyte_Results (Report_ID, Analyte_Name, Concentration, Unit, Reference_Range) VALUES (%s, %s, %s, %s, %s)",
                    (report_id, analyte[0], analyte[1], analyte[2], analyte[3])
                )
        
        conn.commit()
        print("Successfully seeded 10 patient records along with their reports and analyte results!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_database()
