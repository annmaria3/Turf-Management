import mysql.connector
import datetime
import os
import csv

# Database Connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0123",  # Using the password from your original context
        database="turf_management"  # Using the database name from your original context
    )
    cursor = db.cursor()
    print("Database connection established successfully.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# These are typically for initial setup and should be run once, then commented out or removed.
# "CREATE DATABASE TURF_MANAGEMENT;"
# "USE TURF_MANAGEMENT;"

"""CREATE TABLE turf (
turf_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255) NOT NULL,
rate DECIMAL(10, 2) NOT NULL
);"""

"""CREATE TABLE bookings (
booking_id INT AUTO_INCREMENT PRIMARY KEY,
customer_name VARCHAR(255) NOT NULL,
contact VARCHAR(50) NOT NULL,
booking_date DATE NOT NULL,
time_slot VARCHAR(50) NOT NULL,
turf_id INT NOT NULL,
pin_code INT NOT NULL,
FOREIGN KEY (turf_id) REFERENCES turf(turf_id) ON DELETE CASCADE
);"""

username = 'admin'
passw = 'password'

REPORT_DIR = "reports"

if not os.path.exists(REPORT_DIR):
    try:
        os.makedirs(REPORT_DIR)
        print(f"Directory '{REPORT_DIR}' created.")
    except OSError as e:
        print(f"Error creating directory '{REPORT_DIR}': {e}")
        exit(1) # Exit if report directory cannot be created

def log_action(action):
    try:
        with open("booking_log.txt", "a") as log_file:
            log_file.write(f"{datetime.datetime.now()} - {action}\n")
    except IOError as e:
        print(f"Error writing to log file: {e}")

def generate_booking_report():
    print("\n--- Generating Booking Report ---")
    report_path = os.path.join(REPORT_DIR, "booking_report.csv")

    try:
        cursor.execute("SELECT booking_id, customer_name, contact, booking_date, time_slot, turf_id FROM bookings")
        bookings = cursor.fetchall()

        if bookings:
            with open(report_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Booking ID", "Customer Name", "Contact", "Booking Date", "Time Slot", "Turf ID"])
                writer.writerows(bookings) # Use writerows for multiple rows
            print(f"Booking report generated: {report_path}")
            log_action("Generated booking report.")
        else:
            print("No bookings available to generate report.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

def generate_turf_report():
    print("\n--- Generating Turf Report ---")
    report_path = os.path.join(REPORT_DIR, "turf_report.csv")

    try:
        cursor.execute("SELECT turf_id, name, rate FROM turf")
        turfs = cursor.fetchall()

        if turfs:
            with open(report_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Turf ID", "Turf Name", "Hourly Rate"])
                writer.writerows(turfs) # Use writerows for multiple rows
            print(f"Turf report generated: {report_path}")
            log_action("Generated turf report.")
        else:
            print("No turfs available to generate report.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

def generate_revenue_report():
    print("\n--- Generating Revenue Report ---")
    report_path = os.path.join(REPORT_DIR, "revenue_report.txt")

    try:
        cursor.execute("""
            SELECT t.name, COUNT(b.booking_id) as total_bookings, SUM(t.rate) as revenue
            FROM bookings b
            JOIN turf t ON b.turf_id = t.turf_id
            GROUP BY b.turf_id
        """)
        revenue_data = cursor.fetchall()

        if revenue_data:
            with open(report_path, mode="w") as file:
                file.write("Turf Revenue Report\n")
                file.write("-" * 60 + "\n")
                file.write(f"{'Turf Name':<20} | {'Total Bookings':<15} | {'Total Revenue':<15}\n")
                file.write("-" * 60 + "\n") # Adjusted line length for consistency

                for row in revenue_data:
                    # Ensure row[2] is treated as a float for formatting
                    file.write(f"{row[0]:<20} | {row[1]:<15} | ${float(row[2]):<15.2f}\n") # Format revenue as currency

            print(f"Revenue report generated: {report_path}")
            log_action("Generated revenue report.")
        else:
            print("No revenue data available to generate report.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except IOError as e:
        print(f"Error writing to TXT file: {e}")

def report_menu():
    while True:
        print("\n--- Report Menu ---")
        print("1. Generate Booking Report")
        print("2. Generate Turf Report")
        print("3. Generate Revenue Report")
        print("4. Exit to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            generate_booking_report()
        elif choice == '2':
            generate_turf_report()
        elif choice == '3':
            generate_revenue_report()
        elif choice == '4':
            break
        else:
            print("Invalid choice! Please try again.")

def view_available_time_slots(turf_id, booking_date):
    available_time_slots = ['08:00-10:00', '10:00-12:00', '12:00-14:00',
                            '14:00-16:00', '16:00-18:00', '18:00-20:00']

    try:
        cursor.execute("""
            SELECT time_slot FROM bookings
            WHERE turf_id = %s AND booking_date = %s
        """, (turf_id, booking_date))

        booked_slots = cursor.fetchall()
        booked_time_slots = [slot[0] for slot in booked_slots]

        available_slots = [slot for slot in available_time_slots if slot not in booked_time_slots]
        return available_slots

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

def add_booking():
    print("\n--- Add Booking ---")
    customer_name = input("Enter your name: ")
    contact = input("Enter your contact number: ")
    booking_date = input("Enter the booking date (YYYY-MM-DD): ")
    print('Turf_ID 1 : FOOTBALL, Turf_ID 2 : CRICKET')
    turf_id = int(input("Enter the turf ID (1 or 2): "))
    pin_code = input("Enter a 4-digit PIN code for booking: ")

    available_slots = view_available_time_slots(turf_id, booking_date)

    if available_slots:
        print(f"\nAvailable time slots for Turf ID {turf_id} on {booking_date}:")
        for index, slot in enumerate(available_slots, start=1):
            print(f"{index}. {slot}", end=' ')
        print()

        try:
            slot_choice = int(input("Select a time slot by entering the corresponding number: ")) - 1

            if 0 <= slot_choice < len(available_slots):
                time_slot = available_slots[slot_choice]

                cursor.execute("""
                    SELECT * FROM bookings
                    WHERE turf_id = %s AND booking_date = %s AND time_slot = %s
                """, (turf_id, booking_date, time_slot))

                result = cursor.fetchone()

                if result:
                    print(f"Error: The selected time slot {time_slot} on {booking_date} is already booked for Turf ID {turf_id}.")
                else:
                    cursor.execute("""
                        INSERT INTO bookings (turf_id, customer_name, contact, booking_date, time_slot, pin_code)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (turf_id, customer_name, contact, booking_date, time_slot, pin_code))

                    db.commit()
                    booking_id = cursor.lastrowid
                    log_action(f"Booking added for {customer_name} on {booking_date} at {time_slot} (Turf ID: {turf_id})")
                    print(f"Booking added successfully! Your Booking ID is: {booking_id}")
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    else:
        print(f"\nNo available time slots for Turf ID {turf_id} on {booking_date}.")

def remove_booking():
    print("\n--- Remove Booking ---")
    booking_id = input("Enter the booking ID: ")
    pin_code = input("Enter the 4-digit PIN code: ")

    try:
        cursor.execute("SELECT booking_id FROM bookings WHERE booking_id = %s AND pin_code = %s", (booking_id, pin_code))
        if cursor.fetchone():
            cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
            db.commit()
            log_action(f"Booking ID {booking_id} removed.")
            print("Booking removed successfully!")
        else:
            print("Invalid booking ID or PIN code!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def update_booking():
    print("\n--- Update Booking ---")
    booking_id = input("Enter the booking ID: ")
    pin_code = input("Enter the 4-digit PIN code: ")

    try:
        cursor.execute("SELECT booking_id FROM bookings WHERE booking_id = %s AND pin_code = %s", (booking_id, pin_code))
        if cursor.fetchone():
            new_date = input("Enter the new booking date (YYYY-MM-DD): ")
            new_time_slot = input("Enter the new time slot (e.g., 10:00-12:00): ")

            cursor.execute("UPDATE bookings SET booking_date = %s, time_slot = %s WHERE booking_id = %s",
                           (new_date, new_time_slot, booking_id))
            db.commit()
            log_action(f"Booking ID {booking_id} updated to {new_date} at {new_time_slot}.")
            print("Booking updated successfully!")
        else:
            print("Invalid booking ID or PIN code!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def search_booking():
    print("\n--- Search Booking ---")
    contact = input("Enter your contact number: ")

    try:
        cursor.execute("SELECT booking_id, customer_name, booking_date, time_slot FROM bookings WHERE contact = %s", (contact,))
        results = cursor.fetchall()

        if results:
            print("Your Bookings:")
            for row in results:
                print(f"Booking ID: {row[0]}, Name: {row[1]}, Date: {row[2]}, Time Slot: {row[3]}")
        else:
            print("No bookings found for this contact.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def list_current_bookings():
    print("\n--- Current Bookings ---")
    try:
        cursor.execute("SELECT booking_id, customer_name, booking_date, time_slot FROM bookings")
        bookings = cursor.fetchall()

        if bookings:
            for row in bookings:
                print(f"Booking ID: {row[0]}, Customer Name: {row[1]}, Date: {row[2]}, Time Slot: {row[3]}")
        else:
            print("No current bookings available.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def list_all_turfs():
    print("\n--- List of All Turfs ---")
    try:
        cursor.execute("SELECT turf_id, name, rate FROM turf")
        turfs = cursor.fetchall()

        if turfs:
            for row in turfs:
                print(f"Turf ID: {row[0]}, Turf Name: {row[1]}, Hourly Rate: ${row[2]:.2f}")
        else:
            print("No turfs available.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def view_available_slots():
    print("\n--- View Available Slots ---")
    try:
        turf_id = int(input("Enter the turf ID (1 or 2): "))
        booking_date = input("Enter the date (YYYY-MM-DD): ")

        # Reusing the existing view_available_time_slots for consistency
        available_slots = view_available_time_slots(turf_id, booking_date)

        if available_slots:
            print("Available Time Slots:")
            for slot in available_slots:
                print(slot)
        else:
            print("No available slots for the selected date and turf.")
    except ValueError:
        print("Invalid input. Please enter a valid turf ID.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def location_and_contact():
    print("\n--- Location and Contact ---")
    print()
    print("Location: 123 Turf Avenue, Sports City")
    print()
    print("""Contact:
Phone : 04822-261336, 9487569325
Email : contact@sportsarena.com""")

def admin_panel():
    user = input('Enter Admin Username: ')
    password = input('Enter Admin Password: ')

    if user == username and password == passw:
        while True:
            print("\n--- Admin Panel ---")
            print("1. Remove Booking without PIN")
            print("2. Update Booking without PIN")
            print("3. Add Turf")
            print("4. Remove Turf")
            print("5. Change Rate")
            print("6. Exit to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                remove_booking_without_pin()
            elif choice == '2':
                update_booking_without_pin()
            elif choice == '3':
                add_turf()
            elif choice == '4':
                remove_turf()
            elif choice == '5':
                change_rate()
            elif choice == '6':
                break
            else:
                print("Invalid choice! Please try again.")
    else:
        print('Invalid username or password!')

def remove_booking_without_pin():
    print("\n--- Remove Booking (Admin) ---")
    list_current_bookings()
    booking_id = input("Enter the booking ID: ")

    try:
        cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
        db.commit()
        log_action(f"Admin removed booking ID {booking_id}.")
        print("Booking removed successfully by admin!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def update_booking_without_pin():
    print("\n--- Update Booking (Admin) ---")
    list_current_bookings()
    booking_id = input("Enter the booking ID: ")

    try:
        new_date = input("Enter the new booking date (YYYY-MM-DD): ")
        new_time_slot = input("Enter the new time slot (e.g., 10:00-12:00): ")

        cursor.execute("UPDATE bookings SET booking_date = %s, time_slot = %s WHERE booking_id = %s",
                       (new_date, new_time_slot, booking_id))
        db.commit()
        log_action(f"Admin updated booking ID {booking_id} to {new_date} at {new_time_slot}.")
        print("Booking updated successfully by admin!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def add_turf():
    print("\n--- Add Turf ---")
    name = input("Enter turf name: ")
    try:
        rate = float(input("Enter hourly rate: "))
        cursor.execute("INSERT INTO turf (name, rate) VALUES (%s, %s)", (name, rate))
        db.commit()
        log_action(f"Admin added new turf: {name} with rate {rate}.")
        print("Turf added successfully!")
    except ValueError:
        print("Invalid input for rate. Please enter a number.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def remove_turf():
    print("\n--- Remove Turf ---")
    list_all_turfs()
    try:
        turf_id = int(input("Enter the turf ID to remove: "))
        cursor.execute("DELETE FROM turf WHERE turf_id = %s", (turf_id,))
        db.commit()
        log_action(f"Admin removed turf ID {turf_id}.")
        print("Turf removed successfully!")
    except ValueError:
        print("Invalid input for turf ID. Please enter a number.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def change_rate():
    print("\n--- Change Turf Rate ---")
    list_all_turfs()
    try:
        turf_id = int(input("Enter the turf ID: "))
        new_rate = float(input("Enter the new hourly rate: "))

        cursor.execute("UPDATE turf SET rate = %s WHERE turf_id = %s", (new_rate, turf_id))
        db.commit()
        log_action(f"Admin changed rate of turf ID {turf_id} to {new_rate}.")
        print("Rate changed successfully!")
    except ValueError:
        print("Invalid input for turf ID or rate. Please enter numbers.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def main_menu():
    while True:
        print("\nWELCOME TO SPORTS ARENA")
        print("1. Add Booking")
        print("2. Remove Booking")
        print("3. Update Booking")
        print("4. Search Booking")
        print("5. View Available Time Slots") # This now correctly calls view_available_slots()
        print("6. Location and Contact")
        print("7. Admin Panel")
        print("8. Reports")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_booking()
        elif choice == '2':
            remove_booking()
        elif choice == '3':
            update_booking()
        elif choice == '4':
            search_booking()
        elif choice == '5':
            view_available_slots() # This function handles its own input
        elif choice == '6':
            location_and_contact()
        elif choice == '7':
            admin_panel()
        elif choice == '8':
            report_menu()
        elif choice == '9':
            db.close()
            print("Goodbye!")
            break # Correctly breaks the loop to exit the application
        else:
            print("Invalid choice! Please try again.")

# Call the main menu to start the application
if __name__ == "__main__":
    main_menu()
