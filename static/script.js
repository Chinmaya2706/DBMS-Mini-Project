document.addEventListener("DOMContentLoaded", () => {
    // Navigation setup
    const navLinks = document.querySelectorAll('.nav-links a');
    const sections = document.querySelectorAll('.content-section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('data-target');
            
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            link.classList.add('active');
            document.getElementById(targetId).classList.add('active');

            // Automatically load patients when switching to display section
            if (targetId === 'display-section') {
                document.querySelector('.display-tab-btn[data-tab="disp-patient"]').click();
            }
        });
    });

    // Add Records Tabs
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-tab');
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(target).classList.add('active');
        });
    });

    // Display Records Tabs
    const dispTabBtns = document.querySelectorAll('.display-tab-btn');
    
    dispTabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            dispTabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const tabId = btn.getAttribute('data-tab');
            if (tabId === 'disp-patient') loadTableData('patients');
            if (tabId === 'disp-report') loadTableData('urine_test_reports');
            if (tabId === 'disp-result') loadTableData('analyte_results');
        });
    });

    // Utility: Show Alert Message
    function showAlert(message, isSuccess = true) {
        const alertBox = document.getElementById('alert-box');
        alertBox.textContent = message;
        alertBox.className = `alert ${isSuccess ? 'success' : 'error'}`;
        
        // Hide after 5 seconds
        setTimeout(() => alertBox.className = 'alert hidden', 5000);
    }

    // A. Add Patient Form Submit
    document.getElementById('form-patient').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            first_name: document.getElementById('p_first_name').value,
            last_name: document.getElementById('p_last_name').value,
            dob: document.getElementById('p_dob').value,
            gender: document.getElementById('p_gender').value,
            contact_no: document.getElementById('p_contact').value
        };

        try {
            const response = await fetch('/api/patients', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            
            if (response.ok) {
                showAlert(`Success: ${result.message} (Patient ID: ${result.patient_id})`);
                e.target.reset(); // Clear form
            } else {
                showAlert(`Error: ${result.error}`, false);
            }
        } catch (error) {
            showAlert(`Network error: ${error.message}`, false);
        }
    });

    // B. Add Report Form Submit
    document.getElementById('form-report').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            patient_id: parseInt(document.getElementById('r_patient_id').value),
            test_date: document.getElementById('r_test_date').value,
            sample_id: document.getElementById('r_sample_id').value,
            lab_technician: document.getElementById('r_technician').value,
            diagnosis_status: document.getElementById('r_status').value
        };

        try {
            const response = await fetch('/api/reports', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            
            if (response.ok) {
                showAlert(`Success: ${result.message} (Report ID: ${result.report_id})`);
                e.target.reset();
            } else {
                showAlert(`Error: ${result.error}`, false);
            }
        } catch (error) {
            showAlert(`Network error: ${error.message}`, false);
        }
    });

    // C. Add Analyte Result Form Submit
    document.getElementById('form-result').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            report_id: parseInt(document.getElementById('a_report_id').value),
            analyte_name: document.getElementById('a_name').value,
            concentration: parseFloat(document.getElementById('a_concentration').value),
            unit: document.getElementById('a_unit').value,
            reference_range: document.getElementById('a_range').value
        };

        try {
            const response = await fetch('/api/results', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            
            if (response.ok) {
                showAlert(`Success: ${result.message} (Result ID: ${result.result_id})`);
                e.target.reset();
            } else {
                showAlert(`Error: ${result.error}`, false);
            }
        } catch (error) {
            showAlert(`Network error: ${error.message}`, false);
        }
    });

    // D. Fetch and Display Records
    async function loadTableData(tableName) {
        try {
            const response = await fetch(`/api/records/${tableName}`);
            const data = await response.json();
            
            const thead = document.getElementById('display-thead');
            const tbody = document.getElementById('display-tbody');
            
            thead.innerHTML = '';
            tbody.innerHTML = '';

            if (data.error) {
                showAlert(`Error loading data: ${data.error}`, false);
                return;
            }

            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="100%" style="text-align:center; padding: 2rem;">No records found.</td></tr>';
                return;
            }

            // Create Table Headers dynamically based on object keys
            const keys = Object.keys(data[0]);
            keys.forEach(key => {
                const th = document.createElement('th');
                th.textContent = key.replace(/_/g, ' '); // Format column names nicely
                thead.appendChild(th);
            });

            // Create Table Rows
            data.forEach(row => {
                const tr = document.createElement('tr');
                keys.forEach(key => {
                    const td = document.createElement('td');
                    // Format null or undefined as empty string
                    td.textContent = row[key] !== null ? row[key] : '';
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
        } catch (error) {
            showAlert(`Failed to load data for ${tableName}: ${error.message}`, false);
        }
    }

    // E. Search Patient Records
    document.getElementById('form-search').addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = document.getElementById('search_query').value;
        const resultsContainer = document.getElementById('search-results-container');
        resultsContainer.innerHTML = '<p>Searching...</p>';

        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const patients = await response.json();

            resultsContainer.innerHTML = '';

            if (patients.error) {
                showAlert(`Search Error: ${patients.error}`, false);
                return;
            }

            if (patients.length === 0) {
                resultsContainer.innerHTML = '<div class="card"><p>No matching patients found.</p></div>';
                return;
            }

            // Render nested related data
            patients.forEach(patient => {
                let html = `
                    <div class="patient-result-card">
                        <div class="patient-header">
                            <h3>Patient: ${patient.First_Name} ${patient.Last_Name} (ID: ${patient.Patient_ID})</h3>
                            <p>DOB: ${patient.Date_of_Birth} | Gender: ${patient.Gender} | Contact: ${patient.Contact_No}</p>
                        </div>
                `;

                if (patient.reports && patient.reports.length > 0) {
                    patient.reports.forEach(report => {
                        html += `
                            <div class="report-section">
                                <h4>Test Report ID: ${report.Report_ID} | Date: ${report.Test_Date}</h4>
                                <p>Sample ID: ${report.Sample_ID} | Technician: ${report.Lab_Technician} | Status: <strong>${report.Diagnosis_Status}</strong></p>
                        `;

                        if (report.results && report.results.length > 0) {
                            html += `
                                <table class="results-table">
                                    <thead>
                                        <tr>
                                            <th>Analyte Name</th>
                                            <th>Concentration</th>
                                            <th>Unit</th>
                                            <th>Reference Range</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                            `;
                            report.results.forEach(res => {
                                html += `
                                    <tr>
                                        <td>${res.Analyte_Name}</td>
                                        <td>${res.Concentration}</td>
                                        <td>${res.Unit}</td>
                                        <td>${res.Reference_Range}</td>
                                    </tr>
                                `;
                            });
                            html += `</tbody></table>`;
                        } else {
                            html += `<p style="margin-top:0.5rem; color: #888;"><em>No analyte results recorded for this report.</em></p>`;
                        }
                        html += `</div>`; // Close report section
                    });
                } else {
                    html += `<p><em>No test reports found for this patient.</em></p>`;
                }

                html += `</div>`; // Close patient card
                resultsContainer.innerHTML += html;
            });
        } catch (error) {
            resultsContainer.innerHTML = '';
            showAlert(`Search failed: ${error.message}`, false);
        }
    });
});
