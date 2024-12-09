import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector
from operation import connect_to_database, resize_image,show_frame,fetch_services_data,fetching_service_option
import customtkinter as ctk
from PIL import Image, ImageTk

# global username
username = sys.argv[1]


# def add_service():




def add_service():
    """Update the password for a specific username or phone number in the database."""
    service_name = service_name_entry.get()

    cost = cost_entry.get()
    description = description_entry.get("1.0", tk.END).strip()

    if not all([service_name, cost, description]):
        warnings_label.configure(text='❌ All Filed is Required ‼️')
        return
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Update password for the given username or phone number, and set the username if it's empty
        sql = """
            INSERT INTO Services (Service_Name,  Cost, Description, CreatedBy) VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (service_name, cost, description, username))
        conn.commit()

        # cursor.execute("SELECT * FROM Services WHERE Service_Name = %s", (service_name))
        # result = cursor.fetchone()
        get_service_id = cursor.lastrowid
        # if result:
        if get_service_id:
            # get_service_id = str(result[1])
            service_code = f"SV{str(get_service_id).zfill(4)}"

            sql = """UPDATE Services 
                    SET Service_Code = %s
                    WHERE ServiceID = %s """
            cursor.execute(sql, (service_code, get_service_id,))
            conn.commit()

            # Success message
            messagebox.showinfo("Success", f"Thank {username} for adding {service_name} as a Service ✅")

            clear_entries()

        else:
            messagebox.showerror("Error", "Check Error.")

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error inserting data: {err}")
        return

def update_service_data():
    """Update service data based on the input fields."""
    service_code = service_code_entry2.get()
    service_name = service_name_entry2.get()
    cost = cost_entry2.get()
    description = description_entry2.get("1.0", tk.END).strip()

    if not all([service_code, service_name, cost, description]):
        warnings_label.configure(text="😅All Filed is Required")
        return False

    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Update service details
        sql = """
            UPDATE Services SET Service_Name = %s, Cost = %s, Description = %s 
            WHERE Service_Code = %s
        """
        cursor.execute(sql, (service_name, cost, description, service_code))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Service data updated successfully ✅")
        else:
            messagebox.showerror("Error", "Service not found or data unchanged ⚠️")

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error updating data: {err}")
        return

def delete_service_data():
    """Update service data based on the input fields."""
    service_code = service_code_entry2.get()

    confirm_delete = messagebox.askyesno('HEY‼️','Do you really want to Delete⁉️')
    if confirm_delete:
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Update service details
            sql = """
                DELETE FROM Services WHERE Service_Code = %s
            """
            cursor.execute(sql, (service_code,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Service data deleted successfully‼️")
            else:
                messagebox.showerror("Error", "Service not found‼️")

            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating data: {err}")
            return

def pull_and_update_service():
    service_code = service_code_entry2.get()
    all_data = fetching_service_option()
    selected_details = [row for row in all_data if row[2] == service_code]

    # Print the selected details
    for detail in selected_details:
        if detail:
            clear_entries()

            # Insert data into entry fields
            service_name_entry2.insert(0, str(detail[1]))  # Assuming `Service_Name` is in index 1
            cost_entry2.insert(0, str(detail[3]))  # Assuming `Cost` is in index 3
            description_entry2.insert("1.0", str(detail[4]))  # Assuming `Description` is in index 4
        else:
            messagebox.showinfo("No Record Found", "No service found with the given Service Code ⚠️")
    return

def clear_entries():
    # Clear existing text in entry fields
    service_name_entry2.delete(0, tk.END)
    cost_entry2.delete(0, tk.END)
    description_entry2.delete("1.0", tk.END)

    # Clear the input fields after the success message
    service_name_entry.delete(0, tk.END)  # Clear service name entry
    cost_entry.delete(0, tk.END)  # Clear cost entry
    description_entry.delete("1.0", tk.END)  # Clear description text box

# Set up the password update window
update_window = tk.Tk()
update_window.title('Services Update')
update_window.focus_force()
update_window.geometry("400x300")
# favicon = resize_image((90, 90), 'images/HSMS.png')
update_window.iconphoto(True, resize_image((90, 90), 'images/HSMS.png'))

# Center-aligning the window on the screen
window_width = 500
window_height = 500
screen_width = update_window.winfo_screenwidth()
screen_height = update_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
update_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Image frame
imageframe = ctk.CTkFrame(update_window, fg_color='gray', width=100, height=70)
imageframe.place(x=200, y=30)
tk_image = resize_image((70, 70), 'images/manage_service.png')  # Adjusted to return PhotoImage
doctor_patient_image = tk.Label(imageframe, image=tk_image)
doctor_patient_image.grid()

# ADD frame
frame1 = tk.Frame(update_window, width=350, height=400)
frame1.place(x=70, y=110)

# Update frame
frame2 = tk.Frame(update_window, width=350, height=400)
frame2.place(x=70, y=110)

for frame in (frame1, frame2):
    frame.grid_propagate(False)

# Set frame1 as the default frame to display
frame1.tkraise()

warnings_label = ctk.CTkLabel(update_window,text='', text_color='Black', font=('Geneva',18,'bold'))
warnings_label.place(x=140, y=450)

# Entry fields
service_name_label = ctk.CTkLabel(frame1, text="Enter Service Name:", font=('Geneva', 12))
service_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
service_name_entry = ctk.CTkEntry(frame1, width=210)
service_name_entry.grid(row=1, column=1, sticky='w')

s_code = 'Service Code is Auto Generated'
service_code_label = ctk.CTkLabel(frame1, text="Service Code:", font=('Geneva', 12))
service_code_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
service_code_entry = ctk.CTkButton(frame1, text=s_code, fg_color='black', state='disabled', width=210)
service_code_entry.grid(row=2, column=1, sticky='w')

cost_label = ctk.CTkLabel(frame1, text="Cost:", font=('Geneva', 12))
cost_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
cost_entry = ctk.CTkEntry(frame1, width=210)
cost_entry.grid(row=3, column=1, sticky='w')

description_label = ctk.CTkLabel(frame1, text="Description:", font=('Geneva', 12))
description_label.grid(row=4, column=0, padx=10, pady=10, sticky='ne')
description_entry = ctk.CTkTextbox(frame1, height=100, width=210)
description_entry.grid(row=4, column=1, sticky='n')

# Submit button
update_button = ctk.CTkButton(frame1, text="Add Service", command=add_service)
update_button.grid(row=5, column=1, pady=20, sticky='e', padx=0)

def frame_item2():
    clear_entries()
    show_frame(frame2)
# Update button
update_button = ctk.CTkButton(update_window, text="Update Service", command=lambda: frame_item2(), fg_color='red3')
update_button.place(x=350, y=10)

back_image = resize_image((20, 20), 'images/back.png')  # Adjusted to return PhotoImage
def frame_item1():
    clear_entries()
    show_frame(frame1)
back_icon = ctk.CTkButton(update_window, text="", image=back_image, width=20, height=20,command=lambda:frame_item1())
back_icon.place(x=310, y=10)

search_icon_image = resize_image((20, 20), 'images/search.png')  # Adjusted to return PhotoImage
search_icon = ctk.CTkButton(frame2, text="", image=search_icon_image, width=20, height=20, command=pull_and_update_service)
search_icon.place(x=290, y=10)

# -----Widget-for-frame-2-(Update-Service)------#
# Entry fields
service_code_label2 = ctk.CTkLabel(frame2, text="Service Code:", font=('Geneva', 12))
service_code_label2.grid(row=0, column=0, padx=10, pady=10, sticky='e')
services = fetch_services_data()
codes = ['Select Code',]
for row in services:
    if row[2]:
        codes.append(row[2])
service_code_entry2 = ctk.CTkOptionMenu(frame2, values=codes, width=150, fg_color='gray96', text_color='black')
service_code_entry2.grid(row=0, column=1, sticky='w')
service_code_entry2.bind("<Button-1>", lambda event: pull_and_update_service())

service_name_label2 = ctk.CTkLabel(frame2, text="Enter Service Name:", font=('Geneva', 12))
service_name_label2.grid(row=1, column=0, padx=10, pady=10, sticky='e')
service_name_entry2 = ctk.CTkEntry(frame2, width=210)
service_name_entry2.grid(row=1, column=1, sticky='w')

cost_label2 = ctk.CTkLabel(frame2, text="Cost:", font=('Geneva', 12))
cost_label2.grid(row=2, column=0, padx=10, pady=10, sticky='e')
cost_entry2 = ctk.CTkEntry(frame2, width=210)
cost_entry2.grid(row=2, column=1, sticky='w')

description_label2 = ctk.CTkLabel(frame2, text="Description:", font=('Geneva', 12))
description_label2.grid(row=3, column=0, padx=10, pady=10, sticky='ne')
description_entry2 = ctk.CTkTextbox(frame2, height=100, width=210)
description_entry2.grid(row=3, column=1, sticky='n')

# Submit button
update_button2 = ctk.CTkButton(frame2, text="Update", command=update_service_data)
update_button2.grid(row=4, column=1, pady=20, sticky='e', padx=0)

delete_button2 = ctk.CTkButton(frame2, text="Delete Service", command=delete_service_data)
delete_button2.grid(row=4, column=0, pady=20, sticky='e', padx=0)

# Bind Enter key to pull_service_data function

# service_name_entry2.bind("<Return>", lambda event: update_service_data())
# cost_entry2.bind("<Return>", lambda event: update_service_data())
# description_entry2.bind("<Return>", lambda event: update_service_data())

update_window.mainloop()
