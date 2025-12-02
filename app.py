from flask import Flask, render_template_string, request, jsonify
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # UPDATE THIS
    'database': 'phase1'
}


def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def get_actual_table_name(connection, table_name):
    """Get the actual table name from database (handles case sensitivity)"""
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES FROM `phase1`")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()

        # Try exact match first
        if table_name in tables:
            return table_name

        # Try case-insensitive match
        for table in tables:
            if table.lower() == table_name.lower():
                return table

        return table_name  # Return original if not found
    except:
        return table_name


# HTML Template with embedded CSS and JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airport Management System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .nav-tabs {
            display: flex;
            background: #f8f9fa;
            padding: 10px;
            gap: 10px;
            flex-wrap: wrap;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .tab-btn {
            padding: 12px 24px;
            border: none;
            background: white;
            cursor: pointer;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .tab-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .tab-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .content {
            padding: 30px;
        }
        
        .controls {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }
        
        .search-box {
            flex: 1;
            min-width: 250px;
            position: relative;
        }
        
        .search-box input {
            width: 100%;
            padding: 12px 40px 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .search-icon {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: #999;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        .btn-success {
            background: #10b981;
            color: white;
        }
        
        .btn-danger {
            background: #ef4444;
            color: white;
        }
        
        .btn-warning {
            background: #f59e0b;
            color: white;
        }
        
        .btn-secondary {
            background: #6b7280;
            color: white;
        }
        
        .table-container {
            overflow-x: auto;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }
        
        thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .actions {
            display: flex;
            gap: 8px;
        }
        
        .icon-btn {
            padding: 8px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 16px;
            max-width: 600px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            position: relative;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }
        
        .modal-header h2 {
            color: #667eea;
        }
        
        .close-btn {
            background: none;
            border: none;
            font-size: 1.5em;
            cursor: pointer;
            color: #999;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .form-actions {
            display: flex;
            gap: 12px;
            margin-top: 25px;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }
        
        .empty-state-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .alert {
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .alert.show {
            display: block;
        }
        
        .alert-success {
            background: #d1fae5;
            color: #065f46;
            border-left: 4px solid #10b981;
        }
        
        .alert-error {
            background: #fee2e2;
            color: #991b1b;
            border-left: 4px solid #ef4444;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                ✈️ Airport Management System
            </h1>
            <p>King Saud University - Database Systems Project</p>
        </div>
        
        <div class="nav-tabs" id="navTabs">
            <button class="tab-btn active" onclick="switchTable('Airport')" data-table="Airport">
                🏢 Airports
            </button>
            <button class="tab-btn" onclick="switchTable('AirLine')" data-table="AirLine">
                ✈️ Airlines
            </button>
            <button class="tab-btn" onclick="switchTable('Aircraft')" data-table="Aircraft">
                🛩️ Aircraft
            </button>
            <button class="tab-btn" onclick="switchTable('Flight')" data-table="Flight">
                🛫 Flights
            </button>
            <button class="tab-btn" onclick="switchTable('Passenger')" data-table="Passenger">
                👤 Passengers
            </button>
            <button class="tab-btn" onclick="switchTable('Ticket')" data-table="Ticket">
                🎫 Tickets
            </button>
            <button class="tab-btn" onclick="switchTable('Employee')" data-table="Employee">
                👨‍💼 Employees
            </button>
            <button class="tab-btn" onclick="switchTable('Employee_Address')" data-table="Employee_Address">
                📍 Addresses
            </button>
        </div>
        
        <div class="content">
            <div id="alertBox" class="alert"></div>
            
            <div class="controls">
                <div class="search-box">
                    <input type="text" id="searchInput" placeholder="Search..." onkeyup="filterTable()">
                    <span class="search-icon">🔍</span>
                </div>
                <button class="btn btn-primary" onclick="openAddModal()">
                    ➕ Add New
                </button>
                <button class="btn btn-secondary" onclick="refreshData()">
                    🔄 Refresh
                </button>
            </div>
            
            <div class="table-container">
                <table id="dataTable">
                    <thead id="tableHead"></thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
        </div>
    </div>
    
    <div id="formModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Add New Record</h2>
                <button class="close-btn" onclick="closeModal()">✕</button>
            </div>
            <form id="dataForm" onsubmit="submitForm(event)">
                <div id="formFields"></div>
                <div class="form-actions">
                    <button type="submit" class="btn btn-success">💾 Save</button>
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        let currentTable = 'Airport';
        let currentData = [];
        let editingRecord = null;
        let foreignKeyCache = {};
        
        const tableConfigs = {
            'Airport': {
                fields: ['Airport_iD', 'Airport_Name', 'City', 'Country', 'Code', 'Capacity'],
                labels: ['ID', 'Airport Name', 'City', 'Country', 'Code', 'Capacity'],
                types: ['number', 'text', 'text', 'text', 'text', 'number']
            },
            'AirLine': {
                fields: ['Airline_iD', 'Airline_Name', 'Country', 'Founded_Year'],
                labels: ['ID', 'Airline Name', 'Country', 'Founded Year'],
                types: ['number', 'text', 'text', 'date']
            },
            'Aircraft': {
                fields: ['Aircraft_iD', 'FK_Airline_iD', 'Model', 'Manufacturer', 'Capacity'],
                labels: ['ID', 'Airline', 'Model', 'Manufacturer', 'Capacity'],
                types: ['number', 'select', 'text', 'text', 'number'],
                foreignKeys: { FK_Airline_iD: 'AirLine' }
            },
            'Flight': {
                fields: ['Flight_iD', 'FK_Aircraft_iD', 'Dep_Airport_iD', 'Arr_Airport_iD', 'Flight_Number', 'Departure_time', 'Arrival_time', 'Status'],
                labels: ['ID', 'Aircraft', 'Departure Airport', 'Arrival Airport', 'Flight Number', 'Departure Time', 'Arrival Time', 'Status'],
                types: ['number', 'select', 'select', 'select', 'number', 'text', 'text', 'text'],
                foreignKeys: { 
                    FK_Aircraft_iD: 'Aircraft',
                    Dep_Airport_iD: 'Airport',
                    Arr_Airport_iD: 'Airport'
                }
            },
            'Passenger': {
                fields: ['Passenger_iD', 'First_Name', 'Last_Name', 'Gender', 'Nationality', 'Phone', 'Email'],
                labels: ['ID', 'First Name', 'Last Name', 'Gender', 'Nationality', 'Phone', 'Email'],
                types: ['number', 'text', 'text', 'text', 'text', 'text', 'email']
            },
            'Ticket': {
                fields: ['Ticket_iD', 'Flight_Flight_iD', 'Flight_FK_Aircraft_iD', 'FK_Passenger_iD', 'Seat_Number', 'Price', 'Class'],
                labels: ['ID', 'Flight ID', 'Aircraft ID', 'Passenger', 'Seat Number', 'Price', 'Class'],
                types: ['number', 'number', 'number', 'select', 'number', 'number', 'text'],
                foreignKeys: { FK_Passenger_iD: 'Passenger' }
            },
            'Employee': {
                fields: ['Employee_iD', 'FK_Airport_iD', 'First_Name', 'Last_Name', 'Jop_title', 'Salary'],
                labels: ['ID', 'Airport', 'First Name', 'Last Name', 'Job Title', 'Salary'],
                types: ['number', 'select', 'text', 'text', 'text', 'number'],
                foreignKeys: { FK_Airport_iD: 'Airport' }
            },
            'Employee_Address': {
                fields: ['Address_iD', 'FK_Employee_iD', 'Street', 'City', 'Zip_Code'],
                labels: ['ID', 'Employee', 'Street', 'City', 'Zip Code'],
                types: ['number', 'select', 'text', 'text', 'text'],
                foreignKeys: { FK_Employee_iD: 'Employee' }
            }
        };
        
        async function switchTable(tableName) {
            currentTable = tableName;
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            await loadData();
        }
        
        async function loadData() {
            try {
                const response = await fetch(`/api/data/${currentTable}`);
                const result = await response.json();
                if (result.success) {
                    currentData = result.data;
                    renderTable();
                } else {
                    showAlert('Error loading data: ' + result.error, 'error');
                }
            } catch (error) {
                showAlert('Error loading data: ' + error.message, 'error');
            }
        }
        
        function renderTable() {
            const config = tableConfigs[currentTable];
            const thead = document.getElementById('tableHead');
            const tbody = document.getElementById('tableBody');
            
            thead.innerHTML = '<tr>' + 
                config.labels.map(label => `<th>${label}</th>`).join('') +
                '<th>Actions</th></tr>';
            
            if (currentData.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="${config.fields.length + 1}">
                            <div class="empty-state">
                                <div class="empty-state-icon">📭</div>
                                <h3>No records found</h3>
                                <p>Click "Add New" to create your first record</p>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }
            
            tbody.innerHTML = currentData.map(row => {
                const cells = config.fields.map(field => {
                    let value = row[field];
                    if (value === null || value === undefined) value = '-';
                    return `<td>${value}</td>`;
                }).join('');
                
                return `
                    <tr>
                        ${cells}
                        <td>
                            <div class="actions">
                                <button class="icon-btn btn-warning" onclick='editRecord(${JSON.stringify(row)})'>✏️</button>
                                <button class="icon-btn btn-danger" onclick="deleteRecord('${row[config.fields[0]]}')">🗑️</button>
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        }
        
        function filterTable() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const rows = document.querySelectorAll('#tableBody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        }
        
        async function openAddModal() {
            editingRecord = null;
            document.getElementById('modalTitle').textContent = `Add New ${currentTable}`;
            await renderForm();
            document.getElementById('formModal').classList.add('active');
        }
        
        async function editRecord(record) {
            editingRecord = record;
            document.getElementById('modalTitle').textContent = `Edit ${currentTable}`;
            await renderForm(record);
            document.getElementById('formModal').classList.add('active');
        }
        
        async function renderForm(data = null) {
            const config = tableConfigs[currentTable];
            const formFields = document.getElementById('formFields');
            
            if (config.foreignKeys) {
                for (const [field, refTable] of Object.entries(config.foreignKeys)) {
                    if (!foreignKeyCache[refTable]) {
                        await loadForeignKeyData(refTable);
                    }
                }
            }
            
            formFields.innerHTML = config.fields.map((field, index) => {
                const label = config.labels[index];
                const type = config.types[index];
                const value = data ? data[field] : '';
                const isId = index === 0;
                const disabled = isId && data ? 'disabled' : '';
                
                if (type === 'select') {
                    const refTable = config.foreignKeys[field];
                    const options = foreignKeyCache[refTable] || [];
                    
                    if (options.length === 0) {
                        return `
                            <div class="form-group">
                                <label>${label} *</label>
                                <select name="${field}" required ${disabled}>
                                    <option value="">No ${refTable} records found - Add ${refTable} first!</option>
                                </select>
                            </div>
                        `;
                    }
                    
                    // Get all keys and find the ID field (usually ends with _iD or _ID)
                    const keys = Object.keys(options[0]);
                    const idField = keys.find(k => k.toLowerCase().includes('_id')) || keys[0];
                    const nameField = keys.find(k => k.toLowerCase().includes('name')) || keys[1] || keys[0];
                    
                    console.log('Foreign Key Debug:', {refTable, idField, nameField, sample: options[0]});
                    
                    return `
                        <div class="form-group">
                            <label>${label} *</label>
                            <select name="${field}" required ${disabled}>
                                <option value="">Select ${label}</option>
                                ${options.map(opt => {
                                    const id = opt[idField];
                                    const name = opt[nameField];
                                    return `<option value="${id}" ${value == id ? 'selected' : ''}>
                                        ${id} - ${name}
                                    </option>`;
                                }).join('')}
                            </select>
                        </div>
                    `;
                }
                
                return `
                    <div class="form-group">
                        <label>${label} *</label>
                        <input type="${type}" name="${field}" value="${value}" required ${disabled}>
                    </div>
                `;
            }).join('');
        }
        
        async function loadForeignKeyData(tableName) {
            try {
                const response = await fetch(`/api/data/${tableName}`);
                const result = await response.json();
                if (result.success) {
                    foreignKeyCache[tableName] = result.data;
                }
            } catch (error) {
                console.error('Error loading foreign key data:', error);
            }
        }
        
        async function submitForm(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const data = Object.fromEntries(formData.entries());
            
            const config = tableConfigs[currentTable];
            const idField = config.fields[0];
            
            try {
                let response;
                if (editingRecord) {
                    data[idField] = editingRecord[idField];
                    response = await fetch(`/api/data/${currentTable}/${editingRecord[idField]}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                } else {
                    response = await fetch(`/api/data/${currentTable}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                }
                
                const result = await response.json();
                if (result.success) {
                    showAlert(result.message, 'success');
                    closeModal();
                    await loadData();
                } else {
                    showAlert('Error: ' + result.error, 'error');
                }
            } catch (error) {
                showAlert('Error: ' + error.message, 'error');
            }
        }
        
        async function deleteRecord(id) {
            if (!confirm('Are you sure you want to delete this record?')) return;
            
            try {
                const response = await fetch(`/api/data/${currentTable}/${id}`, {
                    method: 'DELETE'
                });
                const result = await response.json();
                if (result.success) {
                    showAlert(result.message, 'success');
                    await loadData();
                } else {
                    showAlert('Error: ' + result.error, 'error');
                }
            } catch (error) {
                showAlert('Error: ' + error.message, 'error');
            }
        }
        
        function closeModal() {
            document.getElementById('formModal').classList.remove('active');
            document.getElementById('dataForm').reset();
        }
        
        function showAlert(message, type) {
            const alertBox = document.getElementById('alertBox');
            alertBox.className = `alert alert-${type} show`;
            alertBox.textContent = message;
            setTimeout(() => {
                alertBox.classList.remove('show');
            }, 5000);
        }
        
        async function refreshData() {
            await loadData();
            showAlert('Data refreshed successfully', 'success');
        }
        
        // Initialize
        loadData();
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/data/<table_name>', methods=['GET'])
def get_data(table_name):
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'})

    try:
        actual_table = get_actual_table_name(connection, table_name)
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM `phase1`.`{actual_table}`"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({'success': True, 'data': data})
    except Error as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/data/<table_name>', methods=['POST'])
def insert_data(table_name):
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'})

    try:
        data = request.json
        actual_table = get_actual_table_name(connection, table_name)

        # Debug: Print the data being inserted
        print(f"Inserting into {actual_table}: {data}")

        columns = ', '.join([f'`{k}`' for k in data.keys()])
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO `phase1`.`{actual_table}` ({columns}) VALUES ({placeholders})"

        cursor = connection.cursor()
        cursor.execute(query, list(data.values()))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Record added successfully'})
    except Error as e:
        print(f"Database Error: {e}")
        error_msg = str(e)
        if "foreign key constraint fails" in error_msg.lower():
            return jsonify({'success': False, 'error': 'Foreign key error: Make sure the related record exists (e.g., Airline must exist before adding Aircraft)'})
        return jsonify({'success': False, 'error': error_msg})


@app.route('/api/data/<table_name>/<record_id>', methods=['PUT'])
def update_data(table_name, record_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'})

    try:
        data = request.json
        actual_table = get_actual_table_name(connection, table_name)
        id_field = list(data.keys())[0]

        set_clause = ', '.join(
            [f'`{k}` = %s' for k in data.keys() if k != id_field])
        query = f"UPDATE `phase1`.`{actual_table}` SET {set_clause} WHERE `{id_field}` = %s"

        values = [v for k, v in data.items() if k != id_field] + [record_id]

        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Record updated successfully'})
    except Error as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/data/<table_name>/<record_id>', methods=['DELETE'])
def delete_data(table_name, record_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'})

    try:
        actual_table = get_actual_table_name(connection, table_name)

        # Get the primary key field name
        cursor = connection.cursor()
        cursor.execute(
            f"SHOW KEYS FROM `phase1`.`{actual_table}` WHERE Key_name = 'PRIMARY'")
        result = cursor.fetchone()
        id_field = result[4] if result else None

        if not id_field:
            return jsonify({'success': False, 'error': 'Primary key not found'})

        query = f"DELETE FROM `phase1`.`{actual_table}` WHERE `{id_field}` = %s"
        cursor.execute(query, (record_id,))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Record deleted successfully'})
    except Error as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
