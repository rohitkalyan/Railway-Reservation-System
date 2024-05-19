import csv
import sqlite3
import tkinter as tk
from tkinter import ttk

# Create a SQLite database
conn = sqlite3.connect('rrs.db')

# Create tables for each CSV file
with open('Passenger.csv', newline='') as f:
    passenger_reader = csv.DictReader(f)
    conn.execute('''CREATE TABLE passengers
                     (first_name text, last_name text, address text, city text, county text, phone text, ssn text, bdate text)''')
    for row in passenger_reader:
        parts = row['bdate'].split("/")
        if len(parts[0])==1:
            parts[0] = '0'+parts[0]
        if len(parts[1])==1:
            parts[1] = '0'+parts[1]
        date = '19'+parts[2]+'-'+parts[0]+'-'+parts[1]
        conn.execute("INSERT INTO passengers VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (row['ï»¿first_name'], row['last_name'], row['address'], row['city'], row['county'], row['phone'], row['SSN'], date))
    conn.commit()

with open('Train.csv', newline='') as f:
    train_reader = csv.DictReader(f)
    conn.execute('''CREATE TABLE trains
                     (train_number text, train_name text, premium_fare real, general_fare real, source_station text, destination_station text)''')
    for row in train_reader:
        conn.execute("INSERT INTO trains VALUES (?, ?, ?, ?, ?, ?)",
                     (row['TrainNumber'], row['TrainName'], row['PremiumFare'], row['GeneralFare'], row['SourceStation'], row['DestinationStation']))
    conn.commit()

with open('Train_status.csv', newline='') as f:
    status_reader = csv.DictReader(f)
    conn.execute('''CREATE TABLE train_status
                     (train_date text, train_name text, premium_seats_available integer, gen_seats_available integer, premium_seats_occupied integer, gen_seats_occupied integer)''')
    for row in status_reader:
        conn.execute("INSERT INTO train_status VALUES (?, ?, ?, ?, ?, ?)",
                     (row['TrainDate'], row['TrainName'], row['PremiumSeatsAvailable'], row['GenSeatsAvailable'], row['PremiumSeatsOccupied'], row['GenSeatsOccupied']))
    conn.commit()

with open('booked.csv', newline='') as f:
    booked_reader = csv.DictReader(f)
    conn.execute('''CREATE TABLE bookings
                     (passenger_ssn text, train_number text, ticket_type text, status text)''')
    for row in booked_reader:
        conn.execute("INSERT INTO bookings VALUES (?, ?, ?, ?)",
                     (row['ï»¿Passenger_ssn'], row['Train_Number'], row['Ticket_Type'], row['Status']))
    conn.commit()
