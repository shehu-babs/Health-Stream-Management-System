import tkinter as tk
from datetime import datetime,date

import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from operation import connect_to_database,resize_image
from tkcalendar import DateEntry
import re
import subprocess


def Add_Staff(event):
    phone_pattern = r'^\d{10,15}$'
    name_pattern = r'^[A-Za-z]+$'  # Only alphabets
    age_pattern = r'^\d{1,2}$' # Only numbers limit to 2

    def fetch_clinic_ids():
        """Fetch Clinic_IDs and Names from the Clinic table."""
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT Clinic_ID, Name FROM clinic")
            clinic_data = cursor.fetchall()  # Fetch both ID and Name
            conn.close()
            return clinic_data
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching clinic IDs: {err}")
            return []

    # def get_age_value():
    #     # Assuming dob_value is in the format 'YYYY-MM-DD'
    #     dob_value = entry_dob.get().strip()  # Get the date of birth input and remove leading/trailing spaces
    #     # Parse the date of birth string into a date object
    #     dob_date = datetime.strptime(dob_value, '%Y-%m-%d').date()
    #     # Get the current date
    #     current_date = date.today()
    #     # Calculate age
    #     age_value = current_date.year - dob_date.year
    #     # Adjust if the birthday hasn't occurred yet this year
    #     if (current_date.month, current_date.day) < (dob_date.month, dob_date.day):
    #         age_value -= 1
    #         entry_age.insert(0, str(age_value))
    #         warning_label.configure(text=f"Age{age_value}", text_color='red', font=('Geneva', 16, 'bold'))
    #
    #     return


    def get_age_value(event=None):
        # Assuming dob_value is in the format 'YYYY-MM-DD'
        dob_value = entry_dob.get().strip()  # Get the date of birth input and remove leading/trailing spaces
        try:
            # Parse the date of birth string into a date object
            dob_date = datetime.strptime(dob_value, '%Y-%m-%d').date()
            # Get the current date
            current_date = date.today()
            # Calculate age
            age_value = current_date.year - dob_date.year
            # Adjust if the birthday hasn't occurred yet this year
            if (current_date.month, current_date.day) < (dob_date.month, dob_date.day):
                age_value -= 1

            entry_age.delete(0, tk.END)  # Clear the existing content
            entry_age.insert(0, str(age_value))  # Insert the calculated age
        except ValueError:
            # Handle invalid date format error
            warning_label.configure(text="Invalid date format. Use YYYY-MM-DD.", text_color='red',
                                    font=('Geneva', 16, 'bold'))

    # Function to add staff to the database
    def submit_staff_details():
        # Get input from the entry fields
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        staff_address = entry_staff_address.get()
        dob = entry_dob.get()
        age = entry_age.get()
        phone = entry_phone.get()
        gender = gender_var.get()  # Radio button value
        clinic_id = on_clinic_selected()
        role = role_var.get()
        password = 'mypass'

        if not all([first_name, last_name, staff_address, dob, age, phone, gender, clinic_id]):
            # messagebox.showwarning("Input Error", "All fields are required")
            warning_label.configure(text="All fields are required", text_color='red', font=('Geneva', 16, 'bold'))
            return False
        if not re.match(name_pattern,first_name):
            warning_label.configure(text="Enter a valid First Name",text_color='red', font=('Geneva', 16, 'bold'))
            return False
        if not re.match(name_pattern,last_name):
            warning_label.configure(text="Enter a valid Last Name",text_color='red', font=('Geneva', 16, 'bold'))
            return False
        if not re.match(age_pattern,age):
            warning_label.configure(text="Enter a valid Age Number",text_color='red', font=('Geneva', 16, 'bold'))
            return False
        elif len(age)>2:
            warning_label.configure(text="check your age",text_color='red', font=('Geneva', 16, 'bold'))
            return False
        if not re.match(phone_pattern,phone):
            warning_label.configure(text="Enter only Numbers 0-9 as Phone number",text_color='red', font=('Geneva', 16, 'bold'))
            return False
        elif len(phone)<10 or len(phone)>10:
            warning_label.configure(text="Phone Number Must be 10 Digits",text_color='red', font=('Geneva', 16, 'bold'))
            return False

        try:
            # Step 1: Connect to the database
            conn = connect_to_database()
            cursor = conn.cursor()

            # Step 2: Insert staff information
            sql = """
                INSERT INTO STAFF (First_Name, Last_Name, Role, Staff_Address, DateOfBirth, Age, PhoneNumber, Gender, ClinicID, Password) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql,
                           (first_name, last_name, role, staff_address, dob, age, phone, gender, clinic_id, password))
            conn.commit()

            # Step 3: Retrieve the auto-incremented Staff_ID (assuming it is the primary key)
            sql = """
                SELECT Staff_ID
                FROM STAFF 
                WHERE PhoneNumber = %s
            """
            cursor.execute(sql, (phone,))  # No need for pattern matching with LIKE; phone numbers should be unique
            result = cursor.fetchone()

            if result:
                # Extract the Staff_ID from the result
                staff_id = result[0]

                # Step 4: Generate the formatted USERID, padding with leading zeros if necessary
                formatted_id = f"S{str(staff_id).zfill(4)}"  # Output: S0007S

                # Step 5: Update the STAFF table with the formatted USERID
                sql = """
                    UPDATE STAFF 
                    SET USERID = %s
                    WHERE PhoneNumber = %s
                """
                cursor.execute(sql, (formatted_id, phone))
                conn.commit()

                # Success message
                messagebox.showinfo("Success", f"Staff added successfully with USERID: {formatted_id}!")
            else:
                messagebox.showerror("Error", "Staff could not be found after insertion.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data: {err}")

        # Clear the fields
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_staff_address.delete(0, tk.END)
        entry_dob.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_phone.delete(0, tk.END)

    # Create a new window (popup) for adding staff
    add_staff_window = tk.Toplevel()
    add_staff_window.title("Add / Update Staff")
    add_staff_window.focus_force()
    add_staff_window.geometry("600x500")
    add_staff_window.configure(background='#c3d6db')
    add_staff_window.iconphoto(True, resize_image((90, 90), 'images/HSMS.png'))

    # Center-aligning the window on the screen
    window_width = 540
    window_height = 550
    screen_width = add_staff_window.winfo_screenwidth()
    screen_height = add_staff_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    add_staff_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    frame1 = ctk.CTkFrame(add_staff_window, fg_color='#c3d6db')
    frame1.grid(row=0, column=0, pady=(40, 20),padx=(80,100), sticky="nsew")

    # warinig label
    warning_label = ctk.CTkLabel(add_staff_window, text='Add New Staff',text_color='black', font=('Geneva', 20, 'bold'))
    warning_label.place(x=200, y=5)


    # Staff Name
    label_first_name = ctk.CTkLabel(frame1, text="First Name:", font=("Arial", 12))
    label_first_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_first_name = ctk.CTkEntry(frame1, font=("Arial", 12))
    entry_first_name.grid(row=0, column=1, padx=10, pady=10)

    label_last_name = ctk.CTkLabel(frame1, text="Last Name:", font=("Arial", 12))
    label_last_name.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_last_name = ctk.CTkEntry(frame1, font=("Arial", 12))
    entry_last_name.grid(row=1, column=1, padx=10, pady=10)

    # Staff Address
    label_staff_address = ctk.CTkLabel(frame1, text="Staff Address:", font=("Arial", 12))
    label_staff_address.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_staff_address = ctk.CTkEntry(frame1, font=("Arial", 12))
    entry_staff_address.grid(row=2, column=1, padx=10, pady=10)

    # Date of Birth
    label_dob = ctk.CTkLabel(frame1, text="Date of Birth:", font=("Arial", 12))
    label_dob.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    entry_dob = DateEntry(frame1, font=("Arial", 12), width=18, background='darkblue', foreground='black',
                          borderwidth=2, date_pattern='y-mm-dd',)
    entry_dob.grid(row=3, column=1, padx=10, pady=10)



    # Age
    label_age = ctk.CTkLabel(frame1, text="Age:", font=("Arial", 12))
    label_age.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    entry_age = ctk.CTkEntry(frame1, font=("Arial", 12))
    entry_age.grid(row=4, column=1, padx=10, pady=10)
    entry_dob.bind('<Return>', lambda event: get_age_value())
    entry_dob.bind('<FocusOut>', lambda event: get_age_value())
    entry_dob.bind('<KeyRelease>', lambda event: get_age_value())

    # Phone Number
    label_phone = ctk.CTkLabel(frame1, text="Phone Number:", font=("Arial", 12))
    label_phone.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    entry_phone = ctk.CTkEntry(frame1, font=("Arial", 12))
    entry_phone.grid(row=5, column=1, padx=10, pady=10)

    # Gender
    label_gender = ctk.CTkLabel(frame1, text="Gender:", font=("Arial", 12))
    label_gender.grid(row=6, column=0, padx=10, pady=10, sticky="w")
    gender_var = tk.StringVar(value="Male")
    ctk.CTkRadioButton(frame1, text="Male", variable=gender_var, value="Male").grid(row=6, column=1, sticky="w")
    ctk.CTkRadioButton(frame1, text="Female", variable=gender_var, value="Female").grid(row=6, column=2, sticky="w")

    # Clinic ID
    # label_clinic_id = tk.Label(frame1, text="Clinic ID:", font=("Arial", 12))
    # label_clinic_id.grid(row=6, column=0, padx=10, pady=10, sticky="w")
    # clinic_ids = fetch_clinic_ids()  # Fetch clinic IDs from the database
    # combobox_clinic_id = ttk.Combobox(frame1, values=clinic_ids, font=("Arial", 12), state="readonly")
    # combobox_clinic_id.grid(row=6, column=1, padx=10, pady=10)
    label_clinic_id = ctk.CTkLabel(frame1, text="Clinic Name:", font=("Arial", 12))
    label_clinic_id.grid(row=7, column=0, padx=10, pady=10, sticky="w")
    clinic_data = fetch_clinic_ids()  # Fetch clinic IDs from the database
    clinic_ids = {row[1]: str(row[0]) for row in clinic_data}
    clinic_names = list(clinic_ids)
    # clinic_ids = [str(row[0]) for row in clinic_data]  # Get only the IDs
    # clinic_names = [row[1] for row in clinic_data]  # Get only the Names
    combobox_clinic_id = ctk.CTkComboBox(frame1, values=clinic_names, font=("Arial", 12), state="readonly")
    combobox_clinic_id.grid(row=7, column=1, padx=10, pady=10)

    def on_clinic_selected():
        """Update the selected clinic ID based on the selected clinic name."""
        selected_clinic_name = combobox_clinic_id.get()
        selected_clinic_id = clinic_ids.get(selected_clinic_name)  # Fetch the clinic ID from the dictionary
        return selected_clinic_id

    combobox_clinic_id.bind("<<ComboboxSelected>>", on_clinic_selected)

    # Role
    label_role = ctk.CTkLabel(frame1, text="Set Staff Role to:", font=("Arial", 12))
    label_role.grid(row=8, column=0, padx=10, pady=10, sticky="w")
    role_var = tk.StringVar(value="staff")
    ctk.CTkRadioButton(frame1, text="admin", variable=role_var, value="admin").grid(row=8, column=1, sticky="w")
    ctk.CTkRadioButton(frame1, text="staff", variable=role_var, value="staff").grid(row=8, column=2, sticky="w")

    # Submit Button
    submit_button = ctk.CTkButton(frame1, text="+ Add Staff", command=submit_staff_details,fg_color='black', font=("Arial", 12))
    submit_button.grid(row=9, column=0, padx=10, pady=20, sticky="w")

    add_staff_window.mainloop()

    return

