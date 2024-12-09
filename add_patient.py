from datetime import datetime,date
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from operation import connect_to_database, resize_image, show_frame, resize_image2, Style
from tkcalendar import DateEntry
from PIL import Image, ImageGrab
import subprocess
import customtkinter as ctk
import os
from tkinter import filedialog


# def Add_Patient(event):
global datdatewarning_lb

def show_add_patient():
    show_frame(frame1)
    show_frame(frame2)


def show_update_patient():
    show_frame(frame3)
    show_frame(frame4)
    update_tk()


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


# Function to add staff to the database
def submit_patient_details():
    # Get input from the entry fields
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    address = entry_staff_address.get("1.0", tk.END)
    dob = entry_dob.get()
    age = entry_age.get()
    phone = entry_phone.get()
    gender = gender_var.get()  # Radio button value
    clinic_id = on_clinic_selected()
    contact_name = entry_contact_name.get()
    contact_phone = entry_contact_phone.get()
    name = first_name + " " + last_name
    USERID = ""

    if not all([first_name, last_name, address, dob, age, phone, gender, clinic_id, contact_name, contact_phone]):
        messagebox.showwarning("Input Error", "All fields are required")
        return

    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Insert Patient Data
        sql = """
            INSERT INTO Patient (First_Name, Last_Name, Address, DateOfBirth, Age, PhoneNumber, Gender, ClinicID, Emergency_Contact_Name, Emergency_Contact, USERID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            first_name, last_name, address, dob, age, phone, gender, clinic_id, contact_name, contact_phone, USERID))
        conn.commit()

        # Retrieve the auto-incremented Patient_ID
        sql = """
            SELECT Patient_ID,Updated_AT
            FROM Patient 
            WHERE PhoneNumber = %s
        """
        cursor.execute(sql, (phone,))  # Pass phone as a tuple
        result = cursor.fetchone()

        if result:
            # Extract the Patient_ID from the result
            patient_id = result[0]
            card_date = result[1]
            print("patient id is" f"{patient_id}")

            # Generate the formatted USERID, padding with leading zeros if necessary
            formatted_id = f"P{str(patient_id).zfill(4)}"  # Output: PA00007
            # create_id_card_window(formatted_id, card_date)

            # Update the Patient table with the formatted USERID
            sql = """
                UPDATE Patient 
                SET USERID = %s
                WHERE PhoneNumber = %s
            """
            cursor.execute(sql, (formatted_id, phone))
            conn.commit()

            sql = """UPDATE clinic 
                    SET Number_of_Patient = Number_of_Patient + 1 
                    WHERE Clinic_ID = %s;
                        """
            cursor.execute(sql, (clinic_id,))
            conn.commit()

            # Success message
            messagebox.showinfo("Success", f"Patient added successfully with USERID: {formatted_id}!")
            subprocess.Popen(
                ['python3', 'id_card.py', name, formatted_id, str(dob), gender, clinic_id, address, str(card_date)])

        else:
            messagebox.showerror("Error", "Patient could not be found after insertion.")

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error inserting data: {err}")

    label_info2.configure(text="Registration Successful !", text_color="green")

    # Clear the fields
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_staff_address.delete("1.0", tk.END)
    entry_dob.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_contact_name.delete(0, tk.END)
    entry_contact_phone.delete(0, tk.END)

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

        datewarning_lb.place(x=200, y=400)


# Create a new window (popup) for adding staff
add_patient_window = tk.Tk()
# add_patient_window.attributes('-topmost', True)
add_patient_window.title("Patient Registration Form")
add_patient_window.configure(bg="gray81")
add_patient_window.focus_force()
add_patient_window.resizable(False, False)
add_patient_window.iconphoto(True, resize_image((90, 90), 'images/HSMS.png'))

# Center-aligning the window on the screen
window_width = 1320
window_height = 600
screen_width = add_patient_window.winfo_screenwidth()
screen_height = add_patient_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
add_patient_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Right NAV
frame1 = ctk.CTkFrame(add_patient_window, fg_color="khaki")
frame1.grid(row=0, column=1, pady=(80, 0), padx=(10, 20), sticky="nsew")
# LEFT NAV
frame2 = ctk.CTkFrame(add_patient_window, width=500, height=500, fg_color="khaki4", corner_radius=10)
frame2.grid(row=0, column=0, pady=(40, 0), padx=(20, 10), sticky="nsew")

lef_nav_image = resize_image2((450, 450), "images/addp.jpg")
label_show_user = ctk.CTkLabel(frame2, text="", image=lef_nav_image)
label_show_user.place(x=25, y=25)

# Right NAV for update
frame3 = ctk.CTkFrame(add_patient_window, fg_color="gray99")
frame3.grid(row=0, column=1, pady=(80, 0), padx=(10, 20), sticky="nsew")
# LEFT NAV for update
frame4 = ctk.CTkFrame(add_patient_window, width=500, height=500, fg_color="gray61", corner_radius=10)
frame4.grid(row=0, column=0, pady=(40, 0), padx=(20, 10), sticky="nsew")

label_info = ctk.CTkLabel(frame3, text="Enter Patient ID to Update Records", font=Style.level_one_subheading)
label_info.place(x=50, y=10)
label_info2 = ctk.CTkLabel(frame1, text="New Patient Registration Form", font=Style.level_one_subheading)
label_info2.place(x=50, y=10)


def update_tk():
    """
        Initializes the Tkinter GUI window for updating patient information.

        This function sets up a form for updating patient details, including fields for
        the patient's name, address, date of birth, phone number, gender, and emergency contact
        details. The function contains the following nested functions:

        - submit_patient_update: Updates patient data in the database based on input from the form.
          Before proceeding, it prompts the user for confirmation as the action cannot be reversed.
          If any required fields are empty, it displays an error message and halts the update.

        - patient_search: Searches for a patient using a provided PatientID. If found, it populates
          the form fields with the patient's details; otherwise, it displays a warning message.

        GUI Elements:
        - Label and Entry widgets for input fields (e.g., First Name, Last Name, Address, Phone Number).
        - Date picker for the Date of Birth field.
        - Combobox for Clinic selection.
        - Radio buttons for Gender selection.
        - Buttons for searching by PatientID and submitting updates.

        Upon successful update or search, a message is displayed to inform the user of the outcome.

        Parameters:
        None

        Returns:
        None
        """
    datewarning_lb.place_forget()
    def submit_patient_update():
        """
            This function is used to update the patient information in the database.

            It collects user input from various entry fields like first name, last name,
            address, date of birth, age, phone number, gender, clinic ID, and emergency contacts.

            Steps:
            1. Asks for user confirmation before proceeding with the update.
            2. Validates that all required fields are filled.
            3. Updates the patient information in the database using the provided USERID.
            4. Displays success or error messages based on the result.
            5. Clears the input fields after the operation.

            Parameters:
            None (Inputs are collected from form widgets like entry fields and comboboxes).

            Returns:
            None (But displays message dialogs for success/failure).
            """
        if not messagebox.askyesno("Confirm Update",
                                   "This action cannot be reversed. Are you sure you want to proceed?"):
            return  # Exit the function if the user chooses "No"

        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        address = entry_staff_address.get("1.0", tk.END).strip()  # Use strip to remove extra spaces/newlines
        dob = entry_dob.get()
        age = entry_age.get()
        phone = entry_phone.get()
        gender = gender_var.get()  # Radio button value
        clinic_id = on_clinic_selected()
        # clinic_id = combobox_clinic_id.get()
        contact_name = entry_contact_name.get()
        contact_phone = entry_contact_phone.get()
        USERID = entry_PatientID.get()  # This should be set appropriately, possibly from another input
        patient_id = ""  # Get the PatientID that you want to update

        # Check for empty fields
        if not all([first_name, last_name, address, dob, age, phone, gender, clinic_id, contact_name, contact_phone]):
            messagebox.showwarning("Input Error", "All fields are required")
            return

        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Update Patient Data
            sql = """
                UPDATE Patient 
                SET First_Name = %s, 
                    Last_Name = %s, 
                    Address = %s, 
                    DateOfBirth = %s, 
                    Age = %s, 
                    PhoneNumber = %s, 
                    Gender = %s, 
                    ClinicID = %s, 
                    Emergency_Contact_Name = %s, 
                    Emergency_Contact = %s
                WHERE USERID = %s;
            """
            cursor.execute(sql, (
                first_name, last_name, address, dob, age, phone, gender, clinic_id, contact_name, contact_phone,
                USERID))
            conn.commit()

            if cursor.rowcount > 0:
                label_info.configure(text="Update Successful", text_color='red')
                messagebox.showinfo("Success", "Patient updated successfully.")
            else:
                label_info.configure(text="Patient update was not successful \n ask for Help.", text_color='red')
                messagebox.showerror("Error", "Patient update was not successful \n ask for Help.")

            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating data: {err}")

        # Clear the fields
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_staff_address.delete("1.0", tk.END)
        entry_dob.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_contact_name.delete(0, tk.END)
        entry_contact_phone.delete(0, tk.END)

    def patient_search():
        """Retrieve patient details based on the provided PatientID and populate entry fields."""
        search_pid = entry_PatientID.get().strip()  # Get the PatientID from the input field and remove any extra spaces
        if not search_pid:
            label_info.configure(text="Please enter a PatientID.", text_color="red")
            messagebox.showwarning("Input Error", "Please enter a PatientID.")
            return

        try:
            conn = connect_to_database()  # Establish database connection
            cursor = conn.cursor()

            # Query to retrieve patient details
            sql = """
                SELECT 
                    First_Name, Last_Name, Address, DateOfBirth, Age, 
                    PhoneNumber, Gender, ClinicID, Emergency_Contact_Name, Emergency_Contact
                FROM 
                    Patient 
                WHERE 
                    USERID = %s
            """
            cursor.execute(sql, (search_pid,))
            patient_data = cursor.fetchone()

            if patient_data:
                # Populate entry fields with patient data
                entry_first_name.delete(0, tk.END)
                entry_first_name.insert(0, patient_data[0])

                entry_last_name.delete(0, tk.END)
                entry_last_name.insert(0, patient_data[1])

                entry_staff_address.delete("1.0", tk.END)
                entry_staff_address.insert("1.0", patient_data[2])

                entry_dob.set_date(patient_data[3])

                entry_age.delete(0, tk.END)
                entry_age.insert(0, patient_data[4])

                entry_phone.delete(0, tk.END)
                entry_phone.insert(0, patient_data[5])

                gender_var.set(patient_data[6])

                # Select clinic by name from the dropdown
                clinic_id = patient_data[7]
                clinic_name = next((name for cid, name in clinic_data if cid == clinic_id), "")
                combobox_clinic_id.set(clinic_name)

                entry_contact_name.delete(0, tk.END)
                entry_contact_name.insert(0, patient_data[8])

                entry_contact_phone.delete(0, tk.END)
                entry_contact_phone.insert(0, patient_data[9])

                label_info.configure(text="Patient details loaded successfully", text_color="green")

            else:
                label_info.configure(text="No patient found with the provided PatientID.", text_color="red")
                # messagebox.showwarning("Not Found", "No patient found with the provided PatientID.")

            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error retrieving patient data: {err}")

    lef_nav_image = resize_image2((450, 450), "images/update-user.jpg")
    label_show_user = ctk.CTkLabel(frame4, text="", image=lef_nav_image)
    label_show_user.place(x=25, y=25)

    image_path = "images/search.png"  # Provide the path to your image
    image = ctk.CTkImage(Image.open(image_path), size=(15, 15))  # Resize the image
    image_path_update = "images/update.png"  # Provide the path to your image
    image2 = ctk.CTkImage(Image.open(image_path_update), size=(40, 40))  # Resize the image

    # Search PatientID
    label_PatientID = ctk.CTkLabel(frame3, text="PatientID", font=Style.level_three_subheading)
    label_PatientID.grid(row=0, column=2, padx=0, pady=10, sticky="w")
    global entry_PatientID
    entry_PatientID = ctk.CTkEntry(frame3, font=(Style.level_three_subheading))
    entry_PatientID.grid(row=0, column=2, sticky="w", padx=(70, 0))
    search_icon = ctk.CTkButton(frame3, text="", image=image, width=15, height=15, command=patient_search)
    search_icon.grid(row=0, column=2, padx=(177, 0), pady=15, sticky='w')

    # Staff Name
    label_first_name = ctk.CTkLabel(frame3, text="First Name:", font=Style.level_three_subheading)
    label_first_name.grid(row=1, column=0, padx=(30, 5), pady=10, sticky="w")
    entry_first_name = ctk.CTkEntry(frame3, font=(Style.level_three_subheading))
    entry_first_name.grid(row=1, column=1, padx=5, pady=10, sticky="w")

    label_last_name = ctk.CTkLabel(frame3, text="Last Name:", font=(Style.level_three_subheading))
    label_last_name.grid(row=2, column=0, padx=(30, 5), pady=10, sticky="w")
    entry_last_name = ctk.CTkEntry(frame3, font=(Style.level_three_subheading))
    entry_last_name.grid(row=2, column=1, padx=5, pady=10, sticky="w")

    # Staff Address
    label_staff_address = ctk.CTkLabel(frame3, text="Address:", font=Style.level_three_subheading)
    label_staff_address.grid(row=3, column=0, padx=(30, 5), pady=10, sticky="w")
    entry_staff_address = ctk.CTkTextbox(frame3, font=Style.level_three_subheading, width=200, height=80,
                                         border_width=2)
    entry_staff_address.grid(row=3, column=1, padx=5, pady=10, sticky="w")

    # Date of Birth
    label_dob = ctk.CTkLabel(frame3, text="Date of Birth:", font=(Style.level_three_subheading))
    label_dob.grid(row=4, column=0, padx=(30, 5), pady=10, sticky="w")
    entry_dob = DateEntry(frame3, font=(Style.level_three_subheading), width=18, background='blue', foreground='black',
                          borderwidth=2, date_pattern='y-mm-dd')
    entry_dob.grid(row=4, column=1, padx=5, pady=10, sticky="w")

    # Age
    label_age = ctk.CTkLabel(frame3, text="Age:", font=(Style.level_three_subheading))
    label_age.grid(row=5, column=0, padx=(30, 5), pady=10, sticky="w")
    entry_age = ctk.CTkEntry(frame3, font=(Style.level_three_subheading))
    entry_age.grid(row=5, column=1, padx=5, pady=10, sticky="w")

    # Phone Number
    label_phone = ctk.CTkLabel(frame3, text="Phone Number:", font=Style.level_three_subheading)
    label_phone.grid(row=6, column=0, padx=(30, 5), pady=10, sticky="w")
    entry_phone = ctk.CTkEntry(frame3, font=Style.level_three_subheading)
    entry_phone.grid(row=6, column=1, padx=5, pady=10, sticky="w")

    # Gender
    label_gender = ctk.CTkLabel(frame3, text="Gender:", font=Style.level_three_subheading)
    label_gender.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    gender_var = tk.StringVar(value="Male")
    ctk.CTkRadioButton(frame3, text="Male", variable=gender_var, value="Male").grid(row=1, column=3, sticky="w")
    ctk.CTkRadioButton(frame3, text="Female", variable=gender_var, value="Female").grid(row=1, column=3, padx=(80, 0),
                                                                                        sticky="w")

    # Clinic Name Label
    label_clinic_id = ctk.CTkLabel(frame3, text="Clinic Name:", font=(Style.level_three_subheading))
    label_clinic_id.grid(row=2, column=2, padx=10, pady=10, sticky="w")
    # Fetch clinic data (IDs and Names)
    clinic_data = fetch_clinic_ids()  # Fetch clinic data from the database
    # Create a dictionary: {clinic_name: clinic_id}
    clinic_ids = {row[1]: str(row[0]) for row in clinic_data}
    # Extract clinic names from the dictionary keys
    clinic_names = list(clinic_ids.keys())
    # Create the combobox to display clinic names
    combobox_clinic_id = ctk.CTkComboBox(frame3, values=clinic_names, font=Style.level_three_subheading,state="readonly", width=200)
    combobox_clinic_id.grid(row=2, column=3, padx=10, pady=10, sticky="w")

    # Function to handle clinic selection and fetch clinic ID based on selected name
    def on_clinic_selected():
        """Update the selected clinic ID based on the selected clinic name."""
        selected_clinic_name = combobox_clinic_id.get()
        selected_clinic_id = clinic_ids.get(selected_clinic_name)  # Fetch the clinic ID from the dictionary
        return selected_clinic_id

    # Bind the combobox selection event to the handler function
    combobox_clinic_id.bind("<<ComboboxSelected>>", on_clinic_selected)

    # emergency contact Phone Number
    label_contact_name = ctk.CTkLabel(frame3, text="Emergency Contact Name:", font=(Style.level_three_subheading))
    label_contact_name.grid(row=3, column=2, padx=10, pady=10, sticky="w")
    entry_contact_name = ctk.CTkEntry(frame3, font=(Style.level_three_subheading))
    entry_contact_name.grid(row=3, column=3, padx=10, pady=10, sticky="w")

    # emergency contact Phone Number
    label_contact_phone = ctk.CTkLabel(frame3, text="Emergency Phone Number:", font=(Style.level_three_subheading))
    label_contact_phone.grid(row=4, column=2, padx=10, pady=10, sticky="w")
    entry_contact_phone = ctk.CTkEntry(frame3, font=(Style.level_three_subheading))
    entry_contact_phone.grid(row=4, column=3, padx=10, pady=10, sticky="w")

    submit__update_button = ctk.CTkButton(frame3, image=image2, fg_color='gray61', text="Submit Record", text_color="black",
                                          hover_color="PeachPuff2", command=submit_patient_update)
    submit__update_button.grid(row=7, column=3)


# Staff Name
label_first_name = ctk.CTkLabel(frame1, text="First Name:", font=(Style.level_three_subheading))
label_first_name.grid(row=0, column=0, padx=(30, 5), pady=(50, 10), sticky="w")
entry_first_name = ctk.CTkEntry(frame1, font=(Style.level_three_subheading))
entry_first_name.grid(row=0, column=1, padx=5, pady=(50, 10), sticky="w")

label_last_name = ctk.CTkLabel(frame1, text="Last Name:", font=Style.level_three_subheading)
label_last_name.grid(row=1, column=0, padx=(30, 5), pady=10, sticky="w")
entry_last_name = ctk.CTkEntry(frame1, font=Style.level_three_subheading)
entry_last_name.grid(row=1, column=1, padx=5, pady=10, sticky="w")

# Staff Address
label_staff_address = ctk.CTkLabel(frame1, text="Address:", font=Style.level_three_subheading)
label_staff_address.grid(row=2, column=0, padx=(30, 5), pady=10, sticky="w")
entry_staff_address = ctk.CTkTextbox(frame1, font=Style.level_three_subheading, width=200, height=60, border_width=2)
entry_staff_address.grid(row=2, column=1, padx=5, pady=10, sticky="w")

# Date of Birth
label_dob = ctk.CTkLabel(frame1, text="Date of Birth:", font=Style.level_three_subheading)
label_dob.grid(row=3, column=0, padx=(30, 5), pady=10, sticky="w")
entry_dob = DateEntry(frame1, font=('Geneva',14,'normal'), width=18, background='black', foreground='black',
                      borderwidth=2,
                      date_pattern='y-mm-dd')
entry_dob.grid(row=3, column=1, padx=5, pady=10, sticky="w")
datewarning_lb = ctk.CTkLabel(frame1,text="Invalid date format. Use YYYY-MM-DD.", text_color='red',font=('Geneva', 12, 'bold'))
entry_dob.bind('<Return>', lambda event: get_age_value())
entry_dob.bind('<FocusOut>', lambda event: get_age_value())
entry_dob.bind('<KeyRelease>', lambda event: get_age_value())

# Age
label_age = ctk.CTkLabel(frame1, text="Age:", font=Style.level_three_subheading)
label_age.grid(row=4, column=0, padx=(30, 5), pady=10, sticky="w")
entry_age = ctk.CTkEntry(frame1, font=Style.level_three_subheading)
entry_age.grid(row=4, column=1, padx=5, pady=10, sticky="w")

# Phone Number
label_phone = ctk.CTkLabel(frame1, text="Phone Number:", font=(Style.level_three_subheading))
label_phone.grid(row=5, column=0, padx=(30, 5), pady=10, sticky="w")
entry_phone = ctk.CTkEntry(frame1, font=(Style.level_three_subheading))
entry_phone.grid(row=5, column=1, padx=5, pady=10, sticky="w")

# Gender
label_gender = ctk.CTkLabel(frame1, text="Gender:", font=(Style.level_three_subheading))
label_gender.grid(row=0, column=2, padx=10, pady=(50, 10), sticky="w")
gender_var = ctk.StringVar(value="Male")
ctk.CTkRadioButton(frame1, text="Male", variable=gender_var, value="Male").grid(row=0, column=3, sticky="w",
                                                                                pady=(50, 10))
ctk.CTkRadioButton(frame1, text="Female", variable=gender_var, value="Female").grid(row=0, column=3, padx=(80, 0),
                                                                                    sticky="w", pady=(50, 10))

# Clinic ID
# label_clinic_id = ctk.CTkLabel(frame1, text="Clinic ID:", font=(Style.level_three_subheading))
# label_clinic_id.grid(row=6, column=0, padx=10, pady=10, sticky="w")
# clinic_ids = fetch_clinic_ids()  # Fetch clinic IDs from the database
# combobox_clinic_id = ttk.Combobox(frame1, values=clinic_ids, font=(Style.level_three_subheading), state="readonly")
# combobox_clinic_id.grid(row=6, column=1, padx=10, pady=10)
label_clinic_id = ctk.CTkLabel(frame1, text="Clinic Name:", font=(Style.level_three_subheading))
label_clinic_id.grid(row=1, column=2, padx=10, pady=10, sticky="w")
clinic_data = fetch_clinic_ids()  # Fetch clinic IDs from the database
# Create a dictionary: {clinic_name: clinic_id}
clinic_ids = {row[1]: str(row[0]) for row in clinic_data}
clinic_names = list(clinic_ids)
combobox_clinic_id = ctk.CTkComboBox(frame1, values=clinic_names, font=(Style.level_three_subheading), state="readonly",width=200)
combobox_clinic_id.grid(row=1, column=3, padx=10, pady=10, sticky="w")


def on_clinic_selected():
    """Update the selected clinic ID based on the selected clinic name."""
    selected_clinic_name = combobox_clinic_id.get()
    selected_clinic_id = clinic_ids.get(selected_clinic_name)  # Fetch the clinic ID from the dictionary
    return selected_clinic_id


# Bind the combobox selection event to the handler function
combobox_clinic_id.bind("<<ComboboxSelected>>", on_clinic_selected)

# emergency contact Phone Number
label_contact_name = ctk.CTkLabel(frame1, text="Emergency Contact Name:", font=(Style.level_three_subheading))
label_contact_name.grid(row=2, column=2, padx=10, pady=10, sticky="w")
entry_contact_name = ctk.CTkEntry(frame1, font=(Style.level_three_subheading))
entry_contact_name.grid(row=2, column=3, padx=10, pady=10, sticky="w")

# emergency contact Phone Number
label_contact_phone = ctk.CTkLabel(frame1, text="Emergency Phone Number:", font=(Style.level_three_subheading))
label_contact_phone.grid(row=3, column=2, padx=10, pady=10, sticky="w")
entry_contact_phone = ctk.CTkEntry(frame1, font=(Style.level_three_subheading))
entry_contact_phone.grid(row=3, column=3, padx=10, pady=10, sticky="w")

image3 = resize_image2((40, 40), "images/add.png")
submit__update_button = ctk.CTkButton(frame1, image=image3,fg_color='khaki4', text="ADD Patient", text_color="white",
                                      hover_color="PeachPuff2", command=submit_patient_details)
submit__update_button.grid(row=7, column=3, pady=(30, 0))

# Submit Button
submit_button = ctk.CTkButton(add_patient_window, text="Add \n Patient Record",fg_color='gray10', hover_color="sienna3",
                              command=lambda: show_add_patient())
submit_button.place(x=1150, y=20)

submit_button = ctk.CTkButton(add_patient_window, text="Update \n Patient Record",fg_color='gray10', hover_color="sienna3",
                              command=lambda: show_update_patient())
submit_button.place(x=1000, y=20)

show_add_patient()
add_patient_window.mainloop()
