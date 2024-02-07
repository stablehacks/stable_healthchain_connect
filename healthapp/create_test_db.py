import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('appointments.db')
c = conn.cursor()

# # Create appointments table
# c.execute('''CREATE TABLE IF NOT EXISTS appointments (
#                 id INTEGER PRIMARY KEY,
#                 doctor_id INTEGER NOT NULL,
#                 patient_name TEXT NOT NULL,
#                 appointment_details TEXT NOT NULL,
#                 UNIQUE(doctor_id, appointment_details)
#              )''')
# Create appointments table
c.execute('''select * from appointments;
             ''')
# Commit changes and close connection
conn.commit()
conn.close()


