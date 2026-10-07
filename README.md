# DBMS Mini Project - Lab Management System

A simple healthcare/laboratory database management system for storing and retrieving patient urine-test information.
Built with Python Flask, HTML/CSS/JS, and MySQL.

## 1. Required Software
- Python 3.8+
- MySQL Server (e.g., XAMPP, WAMP, or standalone MySQL)
- Web browser (Chrome, Firefox, etc.)

## 2. How to create the MySQL database
1. Open your MySQL client (e.g., MySQL Workbench, phpMyAdmin, or terminal).
2. Ensure the MySQL server is running.

## 3. How to run schema.sql
You can run the `schema.sql` file to create the database and tables automatically.
Via terminal:
```bash
mysql -u root -p < schema.sql
```
Or simply open `schema.sql` in MySQL Workbench/phpMyAdmin and execute all the queries.

## 4. How to configure .env
1. Copy the `.env.example` file and rename it to `.env`.
2. Update the variables inside with your MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=lab_db
```

## 5. How to install Python dependencies
It's recommended to use a virtual environment.
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
```

## 6. How to start Flask
Run the application by executing:
```bash
python app.py
```
The server should start on `http://127.0.0.1:5000/`.

## 7. How to access the website
Open your web browser and go to:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## 8. Example test operations
- **Add Patient:** Go to the Add Records section, select the Patient tab, fill the form, and save.
- **Add Report:** Provide the ID of the patient you just created and fill out the report form.
- **Add Analyte:** Provide the ID of the newly created report and add analyte details.
- **Display Records:** Switch to the Display Records section to view everything from the tables.
- **Search:** Go to Search Records and search for the patient by ID or Name to see a nested view of their data!
