import mysql.connector
from operation import Style, resize_image, connect_to_database, sort_column, show_frame, export_tree_to_excel
import customtkinter as ctk
import subprocess
from operation import update_time
from PIL import Image
# from add_patient import Add_Patient
import sys

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

username = 'sys.argv[1]'


def Add_Patient():
    subprocess.Popen(['python3', 'add_patient.py'])
    # Add_Patient()
    search_patient_window.withdraw()


def clear():
    # Clear all entries in tree and search entries
    for item in tree.get_children():
        tree.delete(item)

    for item in tree2.get_children():
        tree2.delete(item)

    for item in tree1.get_children():
        tree1.delete(item)

    # search_entry.delete(0, tk.END)


# def call_search_patient_screen(event):
def search_patient_all():
    clear()
    show_frame(frame3)
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT 
                    p.USERID, 
                    CONCAT(p.First_Name, ' ', p.Last_Name) AS Full_Name,
                    p.Address,
                    p.DateOfBirth,
                    p.Age,
                    p.PhoneNumber,
                    p.Gender,
                    c.Name AS ClinicName
                FROM 
                    Patient p
                JOIN 
                    clinic c ON p.ClinicID = c.Clinic_ID;
             """)
        results = cursor.fetchall()

        # Insert results into the tree
        for result in results:
            tree.insert("", tk.END, values=result)
        conn.close()


global patient_id


def search_patient_one():
    clear()
    patient_id = search_entry.get()

    # entry_patient_id = tk.Entry(frame1, font=("Geneva", 12))

    if not patient_id:
        messagebox.showwarning("Input Error", "Please enter a Patient Number.")
        return

    clear()
    show_frame(frame5)

    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """SELECT 
                        p.USERID, 
                        CONCAT(p.First_Name, ' ', p.Last_Name) AS Full_Name,
                        p.Address,
                        p.DateOfBirth,
                        p.Age,
                        p.PhoneNumber,
                        p.Gender,
                        c.Name AS ClinicName
                    FROM 
                        Patient p
                    JOIN 
                        clinic c ON p.ClinicID = c.Clinic_ID
                    WHERE p.USERID = %s;
                 """
            cursor.execute(sql, (patient_id,))
            results = cursor.fetchall()
            # checking if result found if not display message and return
            if not results:
                messagebox.showwarning('No data', 'Patient does not exist or check PID')
                return
            # Insert results into the tree
            for result in results:
                tree2.insert("", tk.END, values=result)

        except Exception as e:
            print("Error while executing query:", e)

        finally:
            cursor.close()  # Ensure the cursor is closed
            conn.close()  # Ensure the connection is closed


def search_patient_visit():
    clear()
    patient_id = search_entry.get()

    # entry_patient_id = tk.Entry(frame1, font=("Geneva", 12))

    if not patient_id:
        messagebox.showwarning("Input Error", "Please enter a Patient Number.")
        return
    clear()
    show_frame(frame4)
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """SELECT 
                        p.Patient_ID,VisitDate,c.Name, Diagnosis, Services, Symptoms, CheckInBy
                        FROM 
                            PatientVisit p
                        JOIN 
                            clinic c on p.Clinic_ID = c.Clinic_ID
                        WHERE p.Patient_ID = %s;
                 """
            cursor.execute(sql, (patient_id,))
            results = cursor.fetchall()
            # checking if result found if not display message and return
            if not results:
                messagebox.showwarning('No data', 'Patient does not exist or check PID')
                return
            # Insert results into the tree
            for result in results:
                tree1.insert("", tk.END, values=result)

        except Exception as e:
            print("Error while executing query:", e)

        finally:
            cursor.close()  # Ensure the cursor is closed
            conn.close()  # Ensure the connection is closed


def staff_search():
    search_pid = search_entry.get()  # The search term from the input field
    conn = connect_to_database()  # Establish the database connection
    if conn:
        cursor = conn.cursor()
        sql = """SELECT 
                    p.USERID, 
                    CONCAT(p.First_Name, ' ', p.Last_Name) AS Full_Name,
                    p.Address,
                    p.DateOfBirth,
                    p.Age,
                    p.PhoneNumber,
                    p.Gender,
                    c.Name AS ClinicName
                FROM 
                    Patient p
                JOIN 
                    clinic c ON p.ClinicID = c.Clinic_ID
                WHERE p.USERID = %s;
             """
        cursor.execute(sql, search_pid)
        results = cursor.fetchall()

        # Insert results into the tree
        for result in results:
            tree.insert("", tk.END, values=result)
        conn.close()


# Function to update the search label based on selected radio button value


# Creating the main window
search_patient_window = tk.Tk()
search_patient_window.title("Manage Patient Profile")
search_patient_window.geometry("800x600")
search_patient_window.focus_force()
search_patient_window.iconphoto(True, resize_image((90, 90), 'images/HSMS.png'))

# Center-aligning the window on the screen
window_width = 1000
window_height = 700
screen_width = search_patient_window.winfo_screenwidth()
screen_height = search_patient_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
search_patient_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Load an image using PIL
image_path = "images/search.png"  # Provide the path to your image
image = ctk.CTkImage(Image.open(image_path), size=(20, 20))  # Resize the image
image2_path = "images/add.png"  # Provide the path to your image
image2 = ctk.CTkImage(Image.open(image2_path), size=(20, 20))  # Resize the image
image3_path = "images/visits.png"  # Provide the path to your image
image3 = ctk.CTkImage(Image.open(image3_path), size=(20, 20))  # Resize the image
image4_path = "images/files.png"  # Provide the path to your image
image4 = ctk.CTkImage(Image.open(image4_path), size=(20, 20))  # Resize the image

# Frame for organizing All Staff View
frame1 = tk.Frame(search_patient_window, bg="gray80", width=800, height=100)
frame1.grid(row=0, column=0, pady=0, padx=0, columnspan=2, sticky="nsew")

# Frame for Search Records
frame2 = tk.Frame(search_patient_window, bg="gray90", width=760, height=200)
frame2.grid(row=1, column=0, pady=0, padx=0, columnspan=2, sticky="nsew")
# Frame for Search Records
frame3 = tk.Frame(search_patient_window, bg="gray80", height=200)
frame3.grid(row=2, column=0, pady=0, padx=(20, 0), columnspan=2, sticky="nsew")
# Frame for Search Records
frame4 = tk.Frame(search_patient_window, bg="red", height=600)
frame4.grid(row=2, column=0, pady=0, padx=0, columnspan=2, sticky="nsew")

frame5 = tk.Frame(search_patient_window, bg="gray80", height=600)
frame5.grid(row=2, column=0, pady=0, padx=(20, 0), columnspan=2, sticky="nsew")

# for frame in (frame4, frame3):
#     frame.grid(row=2, column=0, pady=0, padx=(0, 0), columnspan=2, sticky="nsew")

# Label for Search Criteria
criteria_label = ctk.CTkLabel(frame1, text="Patient Records", font=('Monaco', 30))
criteria_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

time_label = tk.Label(frame1, font=("Gabriola", 10), fg="blue", bg="gray80")
time_label.grid(row=0, column=0, sticky='se', pady=(55, 0))
update_time(time_label)

search_lable = ctk.CTkLabel(frame2, text="Search", font=('Geneva', 15)).grid(row=0, column=0, padx=10, pady=10, )
search_entry = ctk.CTkEntry(frame2)
search_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
search_icon = ctk.CTkButton(frame2, text="", image=image, width=30, height=20,fg_color='turquoise2', command=lambda: search_patient_one())
search_icon.grid(row=0, column=1, padx=(155, 0), pady=10, sticky='w')
search_button = ctk.CTkButton(frame2, text="Search All", image=image4, command=lambda: search_patient_all())
search_button.grid(row=0, column=2, padx=10, pady=10, sticky='w')
tree_title = 'All Patient Records'
add_button = ctk.CTkButton(frame2, text="Export Data", image=image2)
add_button.grid(row=0, column=4, padx=10, pady=10, sticky='w')
add_button.bind("<Button-1>", command=lambda event: export_tree_to_excel(tree,tree_title))
visit_button = ctk.CTkButton(frame2, text="Visits", image=image3, command=lambda: search_patient_visit())
visit_button.grid(row=0, column=3, padx=10, pady=10, sticky='w')
exit_button = ctk.CTkButton(search_patient_window, text="❌",command=lambda: close(), width=30,fg_color='gray90')
exit_button.place(x=960,y=10)

def close():
    search_patient_window.destroy()

# Treeview for displaying patient records
columns = ("IDNumber", "Name", "Address", "DateOfBirth", "Age", "PhoneNumber", "Gender", "Clinic Name")
tree = ttk.Treeview(frame3, columns=columns, show="headings")
tree.heading("IDNumber", text="ID Number", command=lambda: sort_column(tree, "IDNumber", False))
tree.heading("Name", text="Name", command=lambda: sort_column(tree, "Name", False))
tree.heading("Address", text="Address", command=lambda: sort_column(tree, "Address", False))
tree.heading("DateOfBirth", text="DOB", command=lambda: sort_column(tree, "DateOfBirth", False))
tree.heading("Age", text="Age", command=lambda: sort_column(tree, "Age", False))
tree.heading("PhoneNumber", text="Phone Number", command=lambda: sort_column(tree, "PhoneNumber", False))
tree.heading("Gender", text="Gender", command=lambda: sort_column(tree, "Gender", False))
tree.heading("Clinic Name", text="Clinic Name", command=lambda: sort_column(tree, "Clinic Name", False))
# Configure column widths
tree.column("IDNumber", width=50)
tree.column("Name", width=100)
tree.column("Address", width=100)
tree.column("DateOfBirth", width=80)
tree.column("Age", width=30)
tree.column("PhoneNumber", width=100)
tree.column("Gender", width=40)
tree.column("Clinic Name", width=80)
# Grid the Treeview into the frame
tree.grid(row=0, column=0, sticky="nsew")
# Add a vertical scrollbar
scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

# Treeview for displaying patient single records
columns = ("IDNumber", "Name", "Address", "DateOfBirth", "Age", "PhoneNumber", "Gender", "Clinic Name")
tree2 = ttk.Treeview(frame5, columns=columns, show="headings")
tree2.heading("IDNumber", text="ID Number", command=lambda: sort_column(tree2, "IDNumber", False))
tree2.heading("Name", text="Name", command=lambda: sort_column(tree2, "Name", False))
tree2.heading("Address", text="Address", command=lambda: sort_column(tree2, "Address", False))
tree2.heading("DateOfBirth", text="DOB", command=lambda: sort_column(tree2, "DateOfBirth", False))
tree2.heading("Age", text="Age", command=lambda: sort_column(tree2, "Age", False))
tree2.heading("PhoneNumber", text="Phone Number", command=lambda: sort_column(tree2, "PhoneNumber", False))
tree2.heading("Gender", text="Gender", command=lambda: sort_column(tree2, "Gender", False))
tree2.heading("Clinic Name", text="Clinic Name", command=lambda: sort_column(tree2, "Clinic Name", False))
# Configure column widths
tree2.column("IDNumber", width=50)
tree2.column("Name", width=100)
tree2.column("Address", width=100)
tree2.column("DateOfBirth", width=80)
tree2.column("Age", width=30)
tree2.column("PhoneNumber", width=80)
tree2.column("Gender", width=40)
tree2.column("Clinic Name", width=100)
# Grid the Treeview into the frame
tree2.grid(row=0, column=0, sticky="nsew")
# Add a vertical scrollbar
scrollbar = ttk.Scrollbar(frame5, orient="vertical", command=tree2.yview)
tree2.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

# --------------------------------
# Treeview for displaying visits records
columns = ("IDNumber", "Visit Date", "Clinic", "Diagnosis", "Services", "Symptoms", "CheckInBy")
tree1 = ttk.Treeview(frame4, columns=columns, show="headings")
tree1.heading("IDNumber", text="ID Number", command=lambda: sort_column(tree1, "IDNumber", False))
tree1.heading("Visit Date", text="Visit Date", command=lambda: sort_column(tree1, "Visit Date", False))
tree1.heading("Clinic", text="Clinic", command=lambda: sort_column(tree1, "Clinic", False))
tree1.heading("Diagnosis", text="Diagnosis", command=lambda: sort_column(tree1, "Diagnosis", False))
tree1.heading("Services", text="Services", command=lambda: sort_column(tree1, "Services", False))
tree1.heading("Symptoms", text="Symptoms", command=lambda: sort_column(tree1, "Symptoms", False))
tree1.heading("CheckInBy", text="CheckInBy", command=lambda: sort_column(tree1, "CheckInBy", False))

# Configure column widths
tree1.column("IDNumber", width=30)
tree1.column("Visit Date", width=50)
tree1.column("Clinic", width=50)
tree1.column("Diagnosis", width=100)
tree1.column("Services", width=100)
tree1.column("Symptoms", width=50)
tree1.column("CheckInBy", width=50)
# Grid the Treeview into the frame
tree1.grid(row=0, column=0, sticky="nsew")

# Add a vertical scrollbar
scrollbar = ttk.Scrollbar(frame4, orient="vertical", command=tree1.yview)
tree1.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

# Configuring row and column weights for resizing
search_patient_window.grid_rowconfigure(2, weight=1)
search_patient_window.grid_rowconfigure(3, weight=1)
search_patient_window.grid_columnconfigure(0, weight=1)
frame1.grid_rowconfigure(1, weight=1)
frame1.grid_columnconfigure(1, weight=1)
frame2.grid_rowconfigure(1, weight=1)
frame2.grid_columnconfigure(1, weight=1)
frame3.grid_rowconfigure(0, weight=1)
frame3.grid_columnconfigure(0, weight=1)
frame4.grid_rowconfigure(0, weight=1)
frame4.grid_columnconfigure(0, weight=1)
frame5.grid_rowconfigure(0, weight=1)
frame5.grid_columnconfigure(0, weight=1)

search_patient_all()
search_patient_window.mainloop()
