#Final Project in ACP
''' Medication Tracking System.

    This system is designed to help users manage and monitor their medication efficiently. 
It provides a simple yet effective way to record prescriptions, track intake history, 
and view a summary of the user’s medication schedule.'''

import tkinter as tk
import json
import os

# ------ FILE NAME ------
DATA_FILE = "meds_data.json"

# ------ LOAD DATA ------
def load_data():
    # If file does not exist, return empty dictionary
    if not os.path.exists(DATA_FILE):
        return {}
    
    # Open file and read JSON data
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# ------ SAVE DATA ------
def save_data():
    # Save current data to JSON file
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# ------ GLOBAL VARIABLES ------
data = load_data()     # stores all users data
current_user = None    # current logged in user

# ------ CLEAR SCREEN ------
def clear_screen():
    # Remove all widgets from the window
    for widget in root.winfo_children():
        widget.destroy()

# ------ LOGIN SCREEN ------
def login_screen():
    clear_screen()

    tk.Label(root, text="Medication Tracker").pack(pady=10)

    # Username input
    tk.Label(root, text="Enter Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    # Password input
    tk.Label(root, text="Password (minimum of 5 characters)").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    message = tk.Label(root, text="")
    message.pack()

    # Login function
    def login():
        global current_user

        username = username_entry.get()
        password = password_entry.get()

        # Check empty fields
        if username == "" or password == "":
            message.config(text="Fill in all fields")
            return

        # Check password length
        if len(password) < 5:
            message.config(text="Password too short. Input atleast 5 characters.")
            return

        # If user exists
        if username in data:
            if data[username]["password"] == password:
                current_user = username
                main_screen()
            else:
                message.config(text="Wrong password.")
        else:
            # Create new account
            data[username] = {"password": password, "meds": []}
            save_data()
            current_user = username
            main_screen()

    tk.Button(root, text="Login / Create", command=login).pack(pady=10)

# ------ MAIN SCREEN ------
def main_screen():
    clear_screen()

    tk.Label(root, text="Welcome " + current_user).pack(pady=10)

    meds = data[current_user]["meds"]

    # If no medicines
    if len(meds) == 0:
        tk.Label(root, text="No meds to take").pack()

    # Loop through medicines
    for i in range(len(meds)):
        med = meds[i]

        # Compute interval
        if med["times"] > 0:
            interval = 24 // med["times"]
        else:
            interval = 0

        # Determine status
        if med["days"] <= 0:
            status = "Done Taking"
        else:
            status = "Ongoing"

        # Display medicine info
        info = (
            med["name"]
            + " | Every " + str(interval) + " hrs"
            + " | Days: " + str(med["days"])
            + " | Taken: " + str(med["taken_today"]) + "/" + str(med["times"])
            + " | " + status
        )

        tk.Label(root, text=info).pack()

        # ------ TAKE BUTTON LOGIC ------
        if med["days"] <= 0:
            # If done, show message only
            tk.Label(root, text="Done Taking").pack()
        else:
            # If still ongoing, allow taking
            tk.Button(root, text="Take",
                      command=lambda i=i: take_medicine(i)).pack()

        # ------ DELETE BUTTON ------
        if med["days"] <= 0:
            tk.Button(root, text="Delete",
                      command=lambda i=i: delete_medicine(i)).pack()

        tk.Label(root, text="----------------").pack()

    # Bottom buttons
    tk.Button(root, text="Add Medicine", command=add_screen).pack(pady=5)
    tk.Button(root, text="Logout", command=login_screen).pack()

# ------ ADD MEDICINE ------
def add_screen():
    clear_screen()

    tk.Label(root, text="Add Medicine").pack(pady=10)

    # Name input
    tk.Label(root, text="Medicine Name").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Times input
    tk.Label(root, text="Times per day").pack()
    times_entry = tk.Entry(root)
    times_entry.pack()

    # Days input
    tk.Label(root, text="Days to take").pack()
    days_entry = tk.Entry(root)
    days_entry.pack()

    # Saves function
    def save():
        name = name_entry.get()
        times = times_entry.get()
        days = days_entry.get()

        # Check empty
        if name == "" or times == "" or days == "":
            return

        # Convert to numbers safely
        try:
            times = int(times)
            days = int(days)
        except:
            return

        # Create medicine
        med = {
            "name": name,
            "times": times,
            "days": days,
            "taken_today": 0
        }

        # Add to list
        data[current_user]["meds"].append(med)
        save_data()

        main_screen()

    tk.Button(root, text="Save", command=save).pack(pady=5)
    tk.Button(root, text="Back", command=main_screen).pack()

# ------ TAKE MEDICINE ------
def take_medicine(index):
    med = data[current_user]["meds"][index]

    # Prevent taking if already done
    if med["days"] <= 0:
        return

    # Increase taken count
    if med["taken_today"] < med["times"]:
        med["taken_today"] += 1

    # If completed daily intake
    if med["taken_today"] == med["times"]:
        med["days"] -= 1
        med["taken_today"] = 0

    save_data()
    main_screen()

# ------ DELETE MEDICINE ------
def delete_medicine(index):
    del data[current_user]["meds"][index]
    save_data()
    main_screen()

# ------ RUN PROGRAM ------
root = tk.Tk()
root.title("Medication Tracker")
root.geometry("400x500")

login_screen()
root.mainloop()
