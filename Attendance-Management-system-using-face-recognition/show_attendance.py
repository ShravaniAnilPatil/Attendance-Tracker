import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return
        
        # Define the directory path
        subject_dir = f"Attendance\\{Subject}"
        
        # Check if directory exists
        if not os.path.exists(subject_dir):
            t = f"The directory for {Subject} does not exist."
            text_to_speech(t)
            return
        
        # Find all CSV files for the given subject
        filenames = glob(f"{subject_dir}\\{Subject}*.csv")
        
        # Check if any CSV files are found
        if not filenames:
            t = f"No CSV files found for {Subject}."
            text_to_speech(t)
            return
        
        # Read CSV files into DataFrames
        df = [pd.read_csv(f) for f in filenames]
        
        # Ensure the DataFrame list is not empty
        if not df:
            t = 'Error: No valid data found in CSV files.'
            text_to_speech(t)
            return
        
        # Merge the DataFrames
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        
        # Fill any missing values with 0
        newdf.fillna(0, inplace=True)
        
        # Calculate attendance
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
        
        # Save the final DataFrame to CSV
        attendance_csv_path = f"{subject_dir}\\attendance.csv"
        newdf.to_csv(attendance_csv_path, index=False)

        # Display the result in a new Tkinter window
        root = tkinter.Tk()
        root.title(f"Attendance of {Subject}")
        root.configure(background="black")
        
        # Check if the saved CSV exists
        if not os.path.exists(attendance_csv_path):
            t = 'Error: Attendance CSV not found.'
            text_to_speech(t)
            return
        
        # Display the attendance data in the Tkinter window
        with open(attendance_csv_path) as file:
            reader = csv.reader(file)
            for r, row in enumerate(reader):
                for c, cell in enumerate(row):
                    label = tkinter.Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, " bold "),
                        bg="black",
                        text=cell,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
        
        root.mainloop()
        print(newdf)

    # Tkinter UI setup
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    
    titl = tk.Label(subject, text="Which Subject of Attendance?", bg="black", fg="green", font=("arial", 25))
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

    attf = tk.Button(subject, text="Check Sheets", command=Attf, bd=7, font=("times new roman", 15), bg="black", fg="yellow", height=2, width=10, relief=RIDGE)
    attf.place(x=360, y=170)

    sub = tk.Label(subject, text="Enter Subject", width=10, height=2, bg="black", fg="yellow", bd=5, relief=RIDGE, font=("times new roman", 15))
    sub.place(x=50, y=100)

    tx = tk.Entry(subject, width=15, bd=5, bg="black", fg="yellow", relief=RIDGE, font=("times", 30, "bold"))
    tx.place(x=190, y=100)

    fill_a = tk.Button(subject, text="View Attendance", command=calculate_attendance, bd=7, font=("times new roman", 15), bg="black", fg="yellow", height=2, width=12, relief=RIDGE)
    fill_a.place(x=195, y=170)
    
    subject.mainloop()
