import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from operation import connect_to_database
import customtkinter as ctk



# def passwordchange():
    # def update_password():
    #     """Update the password for a specific username or phone number in the database."""
    #     username = username_entry.get()
    #     new_username = new_username_entry.get()
    #     new_password = new_password_entry.get()
    #
    #     conn = connect_to_database()
    #     cursor = conn.cursor()
    #
    #     sql = "SELECT User_Name FROM STAFF"
    #     cursor.execute(sql)
    #     result = cursor.fetchall()
    #     print(result)
    #     cleaned_user_db = [user[0] for user in result if user[0] is not None]
    #     print(cleaned_user_db)
    #
    #     if username in cleaned_user_db:
    #         messagebox.showwarning("Registration Failed", "Username already exists.")
    #         return
    #     else:
    #         # Update password for the given username or phone number, and set the username if it's empty
    #         sql = """
    #             UPDATE STAFF
    #             SET Password = %s, User_Name = %s,
    #                 User_Name = CASE WHEN User_Name = '' THEN %s ELSE User_Name END
    #             WHERE (User_Name = %s OR PhoneNumber = %s)
    #         """
    #         cursor.execute(sql, (new_password, new_username, new_username, username, username))
    #         conn.commit()
    #
    #         if cursor.rowcount > 0:
    #             messagebox.showinfo("Success", "Password updated successfully!")
    #         else:
    #             messagebox.showerror("Error", "Username or phone number not found, Make sure to enter the correct info\n password unchanged.")
    #
    #         cursor.close()
    #         conn.close()
    #
    #     # subprocess.Popen(['python3', 'signin.py'])
    #     update_window.withdraw()
    #     return

def show_passwordd():
    """
    Toggles the visibility of the password entry field.
    If `show_password_var` is set to True, the function displays the password
    in the `password_entry` field as plain text. If `show_password_var` is
    set to False, the password is obscured by asterisks.

    Args:
        None

    Returns:
        None
    """
    if update_window.winfo_exists():  # Ensure the window still exists
        if show_password_varr.get():
            new_password_entry.configure(show="")
            new_password_entry2.configure(show="")
        if show_password_varr.get():
            new_password_entry.configure(show="")
            new_password_entry2.configure(show="")

        else:
            new_password_entry.configure(show="•")
            new_password_entry2.configure(show="•")

def update_password():
    """Update the password for a specific username or phone number in the database."""
    username = username_entry.get()
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()

    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        # Step 1: Check if the new username already exists in the database
        sql = "SELECT User_Name FROM STAFF WHERE User_Name = %s"
        cursor.execute(sql, (new_username,))
        result = cursor.fetchone()

        if result:
            messagebox.showwarning("Registration Failed", "Username already exists.")
            new_username_entry.delete(0, tk.END)
            return

        new_username = new_username_entry.get()
        # Step 2: Update password and set the username if it's currently empty
        sql = """
            UPDATE STAFF 
            SET Password = %s, 
                User_Name = %s  
            WHERE (User_Name = %s OR PhoneNumber = %s)
        """
        cursor.execute(sql, (new_password, new_username, username, username))
        conn.commit()

        # Step 3: Provide feedback based on the result of the update
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Password updated successfully!")
            subprocess.Popen(['python3', 'signin.py'])

        else:
            messagebox.showerror("Error",
                                 "Username or phone number not found. Please enter the correct information. Password unchanged.")
    except Exception as e:
        # Error handling in case of unexpected issues
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()

    # Close the update window
    update_window.destroy()
    return



# Set up the password update window
update_window = tk.Tk()
update_window.title('Update Password')
update_window.geometry("400x300")
update_window.focus_force()
update_window.configure(background='#ffc107')

# Center-aligning the window on the screen
window_width = 400
window_height = 300
screen_width = update_window.winfo_screenwidth()
screen_height = update_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
update_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")


# Username/password entry
username_label = ctk.CTkLabel(update_window, text="Enter Your Phone Number:")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = ctk.CTkEntry(update_window,placeholder_text='☎️ 000-000-0000')
username_entry.grid(row=0, column=1)

# New Username entry
new_username_label = ctk.CTkLabel(update_window, text="Set Your New User Name:")
new_username_label.grid(row=1, column=0, pady=10)
new_username_entry = ctk.CTkEntry(update_window, placeholder_text='🧑‍💻 User Name')
new_username_entry.grid(row=1, column=1)


# New password entry
new_password_label1 = ctk.CTkLabel(update_window, text="New Password:")
new_password_label1.grid(row=2, column=0, padx=10, pady=10)
new_password_entry = ctk.CTkEntry(update_window, show="•",placeholder_text='🔐 Password')
new_password_entry.grid(row=2, column=1)

new_password_label2 = ctk.CTkLabel(update_window, text="Repeat Password:")
new_password_label2.grid(row=3, column=0, padx=10, pady=10)
new_password_entry2 = ctk.CTkEntry(update_window, show="•",placeholder_text='🔐 Password')
new_password_entry2.grid(row=3, column=1)




show_password_varr = tk.IntVar()
show_password_checkboxx = tk.Checkbutton(update_window, text="Show Password", variable=show_password_varr,
                                        command=show_passwordd, bg="#ffc107")
show_password_checkboxx.grid(row=4, column=1, sticky='e', padx=20)

# Update password button
update_button = ctk.CTkButton(update_window, text="Update Password", command=update_password)
update_button.grid(row=5, column=1, pady=20)

update_window.mainloop()
    # return