import mysql.connector

def connect_db():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Default username for XAMPP MySQL
        password="",  # Default password for XAMPP MySQL is empty
        database="vehicle_management"
    )
    return conn

def close_db(conn):
    # Close the database connection
    conn.close()
def add_vehicle(vehicle_number, owner_name, vehicle_type, registration_date):
    conn = connect_db()
    cursor = conn.cursor()
    
    query = "INSERT INTO vehicles (vehicle_number, owner_name, vehicle_type, registration_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (vehicle_number, owner_name, vehicle_type, registration_date))
    
    conn.commit()  # Commit the transaction
    print("Vehicle added successfully.")
    close_db(conn)
def add_fine(vehicle_number, fine_type, fine_amount, fine_date):
    conn = connect_db()
    cursor = conn.cursor()
    
    query = "INSERT INTO fines (vehicle_number, fine_type, fine_amount, fine_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (vehicle_number, fine_type, fine_amount, fine_date))
    
    conn.commit()  # Commit the transaction
    print("Fine added successfully.")
    close_db(conn)
def calculate_fines(vehicle_number):
    conn = connect_db()
    cursor = conn.cursor()
    
    query = "SELECT fine_type, fine_amount, fine_date FROM fines WHERE vehicle_number = %s"
    cursor.execute(query, (vehicle_number,))
    
    fines = cursor.fetchall()
    
    if fines:
        total_fine = 0
        print(f"Fines for Vehicle {vehicle_number}:")
        for fine in fines:
            print(f"Type: {fine[0]}, Amount: {fine[1]}, Date: {fine[2]}")
            total_fine += fine[1]
        print(f"Total Fine: {total_fine}")
    else:
        print(f"No fines for Vehicle {vehicle_number}.")
    
    close_db(conn)
