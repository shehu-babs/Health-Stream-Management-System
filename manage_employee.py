import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from operation import Style, resize_image, connect_to_database, sort_column
import customtkinter as ctk
import subprocess
from add_staff import Add_Staff


# def call_employee_screen(event):
def staff_details():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT First_Name ,Last_Name, Staff_Address, DateOfBirth, Age, PhoneNumber, Gender, ClinicID FROM STAFF")
        results = cursor.fetchall()

        # Insert results into the tree
        for result in results:
            tree.insert("", tk.END, values=result)
        conn.close()


def staff_search():
    search_term1 = search_var1.get()  # The search term from the input field
    search_term2 = search_criteria.get()  # The search criteria (e.g., first_name, last_name)

    conn = connect_to_database()  # Establish the database connection
    if conn:
        cursor = conn.cursor()

        # Dynamically adjust the SQL based on the selected search criteria
        if search_term2 == "Staff_ID":
            sql = """
            SELECT first_name, last_name, email, date
            FROM STAFF
            WHERE staff_id LIKE %s

            """
            cursor.execute(sql, (f'%{search_term1}%',))
        elif search_term2 == "Name":
            sql = """
            SELECT first_name, last_name, email, date
            FROM STAFF
            WHERE first_name LIKE %s OR last_name LIKE %s

            """
            cursor.execute(sql, (f'%{search_term1}%', f'%{search_term1}%'))
        elif search_term2 == "Email":
            sql = """
            SELECT first_name, last_name, email, date
            FROM STAFF
            WHERE email LIKE %s

            """
            cursor.execute(sql, (f'%{search_term1}%',))
        elif search_term2 == "Date":
            sql = """
            SELECT first_name, last_name, email, date
            FROM STAFF
            WHERE date LIKE %s

            """
            cursor.execute(sql, (f'%{search_term1}%',))

        results = cursor.fetchall()

        # Clear the tree view before populating it with new results
        for item in tree.get_children():
            tree.delete(item)

        # Insert the query results into the tree view
        for result in results:
            tree.insert("", tk.END, values=result)

        # Close the database connection
        conn.close()


def clear():
    # Clear all entries in tree and search entries
    for item in tree.get_children():
        tree.delete(item)

    search_entry1.delete(0, tk.END)


# Function to update the search label based on selected radio button value
def update_selected_search_label(*args):
    selected_value = search_criteria.get()
    search_label.config(text=selected_value)


def on_logout_label_click(event):
    result = messagebox.askyesno("Question", "Are you sure you want to sign out?")
    if result:
        subprocess.Popen(["Python3", "main.py"])
        manage_emp_window.destroy()



# Creating the main window
manage_emp_window = tk.Tk()
manage_emp_window.title("Manage Staff Profile")
manage_emp_window.geometry("1000x600")
# manage_emp_window.iconphoto(True, resize_image((90, 90), 'images/HSMS.png'))

# Center-aligning the window on the screen
window_width = 1000
window_height = 600
screen_width = manage_emp_window.winfo_screenwidth()
screen_height = manage_emp_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
manage_emp_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Label for Search Criteria
criteria_label = tk.Label(manage_emp_window, text="Select Search Criteria:", font=Style.subheading)
criteria_label.grid(row=0, column=0, columnspan=4, pady=(20, 10), padx= 30, sticky="w")

# Radio button options
search_criteria = tk.StringVar(value="Name")  # Default selection
criteria_options = [("Date", "Date"), ("Name", "Name"), ("Staff_ID", "Staff_ID"), ("Email", "Email")]

for idx, (text, value) in enumerate(criteria_options):
    tk.Radiobutton(
        manage_emp_window, text=text, variable=search_criteria, value=value,
        command=update_selected_search_label  # Corrected to reference function without parentheses
    ).grid(row=1, column=idx, padx=10, pady=(0, 10), sticky="w")

# Frame for organizing All Staff View
frame1 = tk.LabelFrame(manage_emp_window, text="Search Area")
frame1.grid(row=2, column=0, columnspan=4, pady=20, padx=20, sticky="nsew")

# Frame for Search Records
frame2 = tk.Frame(manage_emp_window, bg="#00CCCC")
frame2.grid(row=3, column=0, columnspan=4, pady=20, padx=20, sticky="nsew")

# Search label and entry in All Staff frame
search_var1 = tk.StringVar()
search_label = tk.Label(frame1, text=search_criteria.get())
search_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

search_entry1 = tk.Entry(frame1, textvariable=search_var1)
search_entry1.grid(row=0, column=1, sticky="w")

# Button to search
search_button = tk.Button(frame1, text="Search", command=staff_search)
search_button.grid(row=0, column=2, sticky="e")

# Button to view all staff records
record_button = tk.Button(frame1, text="View All Staff", command=staff_details)
record_button.grid(row=0, column=3, padx=5, pady=5, sticky="w")

# Treeview for displaying staff records
# columns = ("first_name", "last_name", "email", "date")
# tree = ttk.Treeview(frame1, columns=columns, show="headings")
# tree.heading("first_name", text="First Name")
# tree.heading("last_name", text="Last Name")
# tree.heading("email", text="Email")
# tree.heading("date", text="Date")
# tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Treeview for displaying staff records
columns = ("First_name", "Last_name", "Staff_Address", "DateOfBirth", "Age", "PhoneNumber", "Gender", "ClinicID")
tree = ttk.Treeview(frame1, columns=columns, show="headings")
tree.heading("First_name", text="First Name", command=lambda: sort_column(tree, "First_name", False))
tree.heading("Last_name", text="Last Name", command=lambda: sort_column(tree, "Last_name", False))
tree.heading("Staff_Address", text="Staff_Address", command=lambda: sort_column(tree, "Staff_Address", False))
tree.heading("DateOfBirth", text="DateOfBirth", command=lambda: sort_column(tree, "DateOfBirth", False))
tree.heading("Age", text="Age", command=lambda: sort_column(tree, "Age", False))
tree.heading("PhoneNumber", text="PhoneNumber", command=lambda: sort_column(tree, "PhoneNumber", False))
tree.heading("Gender", text="Gender", command=lambda: sort_column(tree, "Gender", False))
tree.heading("ClinicID", text="ClinicID", command=lambda: sort_column(tree, "ClinicID", False))

tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Configuring row and column weights for resizing
manage_emp_window.grid_rowconfigure(2, weight=1)
manage_emp_window.grid_rowconfigure(3, weight=1)
manage_emp_window.grid_columnconfigure(0, weight=1)
frame1.grid_rowconfigure(1, weight=1)
frame1.grid_columnconfigure(1, weight=1)
frame2.grid_rowconfigure(1, weight=1)
frame2.grid_columnconfigure(1, weight=1)



manage_emp_window.mainloop()

    # return

