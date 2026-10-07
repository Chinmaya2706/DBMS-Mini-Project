CREATE DATABASE IF NOT EXISTS lab_db;
USE lab_db;

CREATE TABLE IF NOT EXISTS Patients (
    Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Date_of_Birth DATE NOT NULL,
    Gender VARCHAR(10),
    Contact_No VARCHAR(15) UNIQUE
);

CREATE TABLE IF NOT EXISTS Urine_Test_Reports (
    Report_ID INT PRIMARY KEY AUTO_INCREMENT,
    Patient_ID INT,
    Test_Date DATE NOT NULL,
    Sample_ID VARCHAR(30) UNIQUE,
    Lab_Technician VARCHAR(100),
    Diagnosis_Status VARCHAR(50),
    FOREIGN KEY (Patient_ID) REFERENCES Patients(Patient_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Analyte_Results (
    Result_ID INT PRIMARY KEY AUTO_INCREMENT,
    Report_ID INT,
    Analyte_Name VARCHAR(50) NOT NULL,
    Concentration DECIMAL(10,2),
    Unit VARCHAR(20),
    Reference_Range VARCHAR(50),
    FOREIGN KEY (Report_ID) REFERENCES Urine_Test_Reports(Report_ID) ON DELETE CASCADE
);

-- Insert sample dummy data for testing
INSERT INTO Patients (First_Name, Last_Name, Date_of_Birth, Gender, Contact_No) VALUES
('John', 'Doe', '1980-05-15', 'Male', '1234567890'),
('Jane', 'Smith', '1992-11-20', 'Female', '0987654321');

INSERT INTO Urine_Test_Reports (Patient_ID, Test_Date, Sample_ID, Lab_Technician, Diagnosis_Status) VALUES
(1, '2023-10-01', 'SMP001', 'Tech A', 'Normal'),
(2, '2023-10-02', 'SMP002', 'Tech B', 'Abnormal');

INSERT INTO Analyte_Results (Report_ID, Analyte_Name, Concentration, Unit, Reference_Range) VALUES
(1, 'Glucose', 0.0, 'mg/dL', '0-15'),
(1, 'Protein', 10.5, 'mg/dL', '0-14'),
(2, 'Glucose', 50.0, 'mg/dL', '0-15');
