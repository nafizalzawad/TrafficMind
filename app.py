from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import mysql.connector

app = Flask(__name__)
socketio = SocketIO(app)

# MySQL connection function
def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vehicle_management"
    )
    return conn

# Route to serve the home page with HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route for Admin page to show added vehicles and fines
@app.route('/admin')
def admin():
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch all vehicles
    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()

    # Fetch all fines
    cursor.execute("SELECT * FROM fines")
    fines = cursor.fetchall()

    conn.close()

    return render_template('admin.html', vehicles=vehicles, fines=fines)

# Add Vehicle route
@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    vehicle_number = request.form['vehicle_number']
    owner_name = request.form['owner_name']
    vehicle_type = request.form['vehicle_type']
    registration_date = request.form['registration_date']

    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO vehicles (vehicle_number, owner_name, vehicle_type, registration_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (vehicle_number, owner_name, vehicle_type, registration_date))
    conn.commit()
    conn.close()

    # Emit real-time update
    socketio.emit('vehicle_added', {
        "vehicle_number": vehicle_number,
        "owner_name": owner_name,
        "vehicle_type": vehicle_type,
        "registration_date": registration_date
    })

    return jsonify({"status": "success"})

# Add Fine route
@app.route('/add_fine', methods=['POST'])
def add_fine():
    vehicle_number = request.form['vehicle_number']
    fine_type = request.form['fine_type']
    fine_amount = request.form['fine_amount']
    fine_date = request.form['fine_date']

    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO fines (vehicle_number, fine_type, fine_amount, fine_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (vehicle_number, fine_type, fine_amount, fine_date))
    conn.commit()
    conn.close()

    # Emit real-time update
    socketio.emit('fine_added', {
        "vehicle_number": vehicle_number,
        "fine_type": fine_type,
        "fine_amount": fine_amount,
        "fine_date": fine_date
    })

    return jsonify({"status": "success"})

# Search fines route
@app.route('/search_fines', methods=['GET'])
def search_fines():
    vehicle_number = request.args.get('vehicle_number')

    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT fine_type, fine_amount, fine_date FROM fines WHERE vehicle_number = %s"
    cursor.execute(query, (vehicle_number,))
    fines = cursor.fetchall()
    conn.close()

    return jsonify(fines)

# Edit Vehicle route
@app.route('/edit_vehicle', methods=['POST'])
def edit_vehicle():
    vehicle_id = request.form['vehicle_id']
    vehicle_number = request.form['vehicle_number']
    owner_name = request.form['owner_name']
    vehicle_type = request.form['vehicle_type']
    registration_date = request.form['registration_date']

    conn = connect_db()
    cursor = conn.cursor()
    query = "UPDATE vehicles SET vehicle_number = %s, owner_name = %s, vehicle_type = %s, registration_date = %s WHERE id = %s"
    cursor.execute(query, (vehicle_number, owner_name, vehicle_type, registration_date, vehicle_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

# Edit Fine route
@app.route('/edit_fine', methods=['POST'])
def edit_fine():
    fine_id = request.form['fine_id']
    vehicle_number = request.form['vehicle_number']
    fine_type = request.form['fine_type']
    fine_amount = request.form['fine_amount']
    fine_date = request.form['fine_date']

    conn = connect_db()
    cursor = conn.cursor()
    query = "UPDATE fines SET vehicle_number = %s, fine_type = %s, fine_amount = %s, fine_date = %s WHERE id = %s"
    cursor.execute(query, (vehicle_number, fine_type, fine_amount, fine_date, fine_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

if __name__ == '__main__':
    socketio.run(app, debug=True)