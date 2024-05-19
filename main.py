import tkinter as tk
from tkinter import font
import sqlite3

#database connection
conn = sqlite3.connect('rrs.db')

def query1():
    first_name = field1.get()
    last_name = field2.get()
    query = f"Select train_name from trains where train_number IN (SELECT train_number FROM bookings JOIN passengers ON bookings.passenger_ssn = passengers.ssn WHERE passengers.first_name='{first_name}' AND passengers.last_name='{last_name}');"
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    result.delete(0, tk.END)
    if len(rows) >= 1:
        for row in rows:
            result.insert(tk.END, row)
    else:
        result.insert(tk.END, "Nothing to show")


def query2():
    date = field3.get()
    query = f"SELECT first_name, last_name, train_number, ticket_type FROM bookings JOIN passengers ON bookings.passenger_ssn = passengers.ssn WHERE bookings.train_number in (Select train_number from trains Join train_status on trains.train_name=train_status.train_name where train_status.train_date='{date}')"
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    result.delete(0, tk.END)
    if len(rows) >= 1:
        for row in rows:
            result.insert(tk.END, row)
    else:
        result.insert(tk.END, "Nothing to show")


def query3():
    age = int(field4.get())
    if age>=50 and age<=60:
        query = f"SELECT bookings.train_number, train_name, source_station, destination_station, first_name, last_name, address, ticket_type, status FROM bookings JOIN passengers ON bookings.passenger_ssn = passengers.ssn JOIN trains ON bookings.train_number = trains.train_number WHERE (julianday('now') - julianday(bdate))/365.25 BETWEEN 50 AND 60"
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        result.delete(0, tk.END)
        if len(rows)>=1:
            for row in rows:
               result.insert(tk.END, row)
        else:
           result.insert(tk.END, "Nothing to show")
    else:
       result.insert(tk.END, "Nothing to show")


def query4():
    query = "SELECT train_name, COUNT(*) FROM bookings JOIN trains ON bookings.train_number = trains.train_number GROUP BY train_name"
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    result.delete(0, tk.END)
    if len(rows) >= 1:
        for row in rows:
           result.insert(tk.END, row)
    else:
       result.insert(tk.END, "Nothing to show")


def query5():
    trainName = field5.get()
    print(trainName)
    query = f"SELECT first_name, last_name, address, ticket_type, status FROM bookings JOIN passengers ON bookings.passenger_ssn = passengers.ssn WHERE bookings.train_number IN (SELECT train_number from trains where train_name = '{trainName}') AND bookings.status = 'Booked';"
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    result.delete(0, tk.END)
    if len(rows) >= 1:
        for row in rows:
           result.insert(tk.END, row)
    else:
       result.insert(tk.END, "Nothing to show")

def query6():
    p_ssn = field6.get()
    cursor = conn.cursor()
    result.delete(0, tk.END)
    query = f"SELECT * FROM bookings WHERE passenger_ssn = '{p_ssn}' AND status = 'Booked'"
    cursor.execute(query)
    bookingRecord = cursor.fetchone()
    if bookingRecord is None:
       result.insert(tk.END, "Nothing to show")
    else:
        query = f"SELECT * FROM trains WHERE train_number = {bookingRecord[1]}"
        cursor.execute(query)
        trainRecord = cursor.fetchone()

        query = f"DELETE FROM bookings WHERE passenger_ssn = '{p_ssn}'"
        cursor.execute(query)
        conn.commit()

        query = f"SELECT * FROM bookings WHERE train_number = {bookingRecord[1]} AND status = 'WaitL'"
        cursor.execute(query)
        waitingList = cursor.fetchall()

        if len(waitingList) > 0:
            firstPassenger = waitingList[0]

            query = f"DELETE FROM bookings WHERE Passenger_ssn = {firstPassenger[0]}"
            cursor.execute(query)
            conn.commit()

            query = f"INSERT INTO bookings (train_number, passenger_ssn, ticket_type, status) VALUES ({trainRecord[0]}, {firstPassenger[0]}, '{firstPassenger[2]}', 'Confirmed')"
            cursor.execute(query)
            conn.commit()

            query = f"SELECT * FROM passengers WHERE ssn = {firstPassenger[0]}"
            cursor.execute(query)
            passengerRecord = cursor.fetchone()
            result.insert(tk.END,f"Passenger {passengerRecord[1]} {passengerRecord[2]}'s ticket got confirmed")

#GUI window
root = tk.Tk()
root.title("Railway Reservation System")

bold_font = font.Font(family='Helvetica', size=10, weight='bold')

title1 = tk.Label(root, text="**Query1**", font=bold_font)
title1.grid(row=0, column=0)
label1 = tk.Label(root, text="Enter Passenger's First Name:")
label1.grid(row=1, column=0)
field1 = tk.Entry(root)
field1.grid(row=1, column=1)

label2 = tk.Label(root, text="Enter Passenger's Last Name:")
label2.grid(row=2, column=0)
field2 = tk.Entry(root)
field2.grid(row=2, column=1)

button1 = tk.Button(root, text="Find Booked Trains", command=query1)
button1.grid(row=3, column=0)

title2 = tk.Label(root, text="**Query2**", font=bold_font)
title2.grid(row=5, column=0)
label3 = tk.Label(root, text="Enter Date (YYYY-MM-DD):")
label3.grid(row=6, column=0)
field3 = tk.Entry(root)
field3.grid(row=6, column=1)
button2 = tk.Button(root, text="List Confirmed Passengers", command=query2)
button2.grid(row=7, column=0)


title3 = tk.Label(root, text="**Query3**", font=bold_font)
title3.grid(row=9, column=0)
label4 = tk.Label(root, text="Enter Age (50-60):")
label4.grid(row=10, column=0)
field4 = tk.Entry(root)
field4.grid(row=10, column=1)
button3 = tk.Button(root, text="Find Passengers By Age", command=query3)
button3.grid(row=11, column=0)

title4 = tk.Label(root, text="**Query4**", font=bold_font)
title4.grid(row=13, column=0)
button4 = tk.Button(root, text="List Train Passenger Counts", command=query4)
button4.grid(row=14, column=0)


title5 = tk.Label(root, text="**Query5**", font=bold_font)
title5.grid(row=16, column=0)
label5 = tk.Label(root, text="Enter Train Name:")
label5.grid(row=17, column=0)
field5 = tk.Entry(root)
field5.grid(row=17, column=1)
button5 = tk.Button(root, text="List Confirmed Passengers By Train", command=query5)
button5.grid(row=18, column=0)

title6 = tk.Label(root, text="**Query6**", font=bold_font)
title6.grid(row=20, column=0)
label6 = tk.Label(root, text="Enter Passenger SSN to cancel ticket:")
label6.grid(row=21, column=0)
field6 = tk.Entry(root)
field6.grid(row=21, column=1)
button6 = tk.Button(root, text="Cancel Ticket", command=query6)
button6.grid(row=22, column=0)

title6 = tk.Label(root, text="**Result**", font=bold_font)
title6.grid(row=24, column=0)
result = tk.Listbox(root)
result.grid(row=40, columnspan=25)

#start the GUI
root.mainloop()

