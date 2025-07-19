import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0123",  # Use your correct password
        database="turf_booking"  # Ensure this matches exactly
    )
    print("Connected successfully!")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
