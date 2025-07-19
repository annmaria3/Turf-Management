# Turf-Management
A Python + MySQL based Turf Booking Management System
# Turf Management System

A command-line based Turf Booking Management System built using Python and MySQL.

This project allows administrators to manage turf bookings, view availability, update and remove bookings, and generate reports — all through a simple and efficient Python-based interface.

---

## ?? Features

- ? Admin login with credentials
- ??? Add, update, delete turf bookings
- ?? Check real-time availability of turfs
- ?? View daily/weekly booking reports
- ??? Backend connected with MySQL database

---

## ?? Technologies Used

| Component        | Tech Used             |
|------------------|------------------------|
| Programming      | Python                 |
| Database         | MySQL (via mysql-connector-python) |
| UI               | CLI (Command-line Interface) |
| Storage          | MySQL Tables (Turf Bookings, Users, etc.) |

---

Install Requirements
pip install mysql-connector-python

Set Up the Database
* Open MySQL Workbench or phpMyAdmin
* Import the provided turf_db.sql (if available) or create tables manually
* Update DB credentials in db_connect.py file:
* 
conn = mysql.connector.connect(
    host="localhost",
    user="your-username",
    password="your-password",
    database="your-db-name"
)

?? How to Run
python turf.py


?? Project Structure

Turf-Management/
?
??? turf.py             # Main script to run the management system
??? db_connect.py       # Handles MySQL connection
??? web/                # Web-based practice or subprojects (optional)
?   ??? index.html
??? README.md           # Project description (this file)
??? turf_db.sql         # SQL script for database schema (if included)
??? .gitignore          # Files/folders to be ignored by Git

?? Contribution
????? Ann Maria Joby
Email: u2203048@rajagiri.edu.in

?? License
This project is open-source and free to use under the MIT License.

?? Give a Star!
If you found this project helpful or inspiring, feel free to ? the repo!

-----

