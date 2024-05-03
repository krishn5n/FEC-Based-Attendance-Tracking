import csv
import serial

# Sample dictionary mapping UID to student ID
uid_dict = {
    "E3D21811": "22MIS1001",
    "0106E7F0": "22BCE1665",
    "3162DEDF": "22BCE1258"
}

try:
    # Open serial port (change 'COM5' to your Arduino's port)
    with serial.Serial('COM5', 9600) as ser, open('data.csv', 'r+', newline='') as csv_file:
        # Read existing data from CSV file
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)
        fieldnames = csv_reader.fieldnames
        
        # Update attendance in memory based on RFID detection
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"Received from Arduino: {line}")

                if line == "Access Denied, You are not part of this Class!":
                    print("Access Denied, Not a part of this class")
                else:
                    uid = line
                    student_id = uid_dict.get(uid, "Unknown")
                    
                    # Update attendance for the student
                    for row in rows:
                        if row['RegisterNo'] == student_id:
                            row['Attendance'] = str(int(row.get('Attendance', 0)) + 1)
                            break
                    
                    # Write updated data back to CSV file
                    csv_file.seek(0)
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                    csv_file.truncate()
                    
                    print(f"UID received: {uid}, StudentID: {student_id}, Attendance Updated")

except KeyboardInterrupt:
    print("Interrupted")
except serial.SerialException as e:
    print(f"Serial Exception: {e}")

print("Finished")
