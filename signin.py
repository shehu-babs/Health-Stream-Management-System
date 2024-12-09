import tkinter as tk
import customtkinter as ctk
import mysql
from operation import Style, resize_image
from operation import authenticate_user, connect_to_database, days_count
import subprocess
import sys
from tkinter import messagebox
import json
from datetime import datetime

# from pass_change import passwordchange


def reset_form():
    """
    Resets the login form or restarts the application based on entry fields' content.
    If either `userid_entry` or `password_entry` contains text, the function clears these fields.
    If both fields are empty, it launches the main application file (`main.py`) and closes
    the current sign-in window.
    Args:
        None
    Returns:
        None
    """
    if (userid_entry.get() != "") or (password_entry.get() != ""):
        userid_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        # auth_form_message.config(text = "")
    else:
        subprocess.Popen(["python3", "main.py"])
        signin_window.withdraw()


# def user_details(username):
#     username = userid_entry.get()
#     return username


def show_password():
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
    if show_password_var.get():
        password_entry.configure(show="")
    else:
        password_entry.configure(show="•")


def authenticate():
    """Authenticate user login from the database."""
    username = userid_entry.get()
    password = password_entry.get()

    if not all([username, password]):
        messagebox.showwarning("Fields Empty", " 😅\nEnter a Valid \nUser Name and Password")
        return
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Check the username and password in the database
        sql = ("SELECT * FROM STAFF "
               "WHERE (PhoneNumber = %s OR User_Name = %s) "
               "AND password = %s")
        cursor.execute(sql, (username, username, password))
        result = cursor.fetchone()


        if result:
            psw = result[10]
            if psw == 'mypass':
                messagebox.showinfo("Password Change", f"Password change required for {result[3]}\nWeak Password!!!")
                # passwordchange()  # Open the password change window
                on_pass_change()
                signin_window.withdraw()
                return

            role = result[3]  # Assuming role is in the 3rd index
            if role == 'admin':
                messagebox.showinfo("Login Successful", f"Login successful! Role: {role}")
                signin_window.withdraw()
                subprocess.Popen(['python3', 'dashboard_admin.py', username, result[1], result[2]])
            elif role == 'staff':
                messagebox.showinfo("Login Successful", f"Login successful! Role: {role}")
                signin_window.withdraw()
                subprocess.Popen(['python3', 'dashboard_staff.py', username])

                # inserting into log table
            userid = result[0]
            uname = result[11]
            role = result[3]
            print(f"{result}")

            print(f"Inserting into log table: UserID={userid}, User_Name={uname}, Role={role}")

            sql = """
                    INSERT INTO UserLoginLog 
                    (UserID, User_Name, Role)
                    VALUES ( %s, %s, %s)"""

            cursor.execute(sql, (userid, uname, role))
            conn.commit()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            return

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return


def on_hover(event):
    reset_pass.configure(text_color="blue", cursor="hand2")  # Change text color and cursor


# Function to reset label color when mouse leaves
def on_leave(event):
    reset_pass.configure(text_color="black", cursor="arrow")

def on_pass_change():
    # signin_window.attributes('-topmost', True)
    subprocess.run(["python3", "pass_change.py"])
    # signin_window.deiconify()
    signin_window.destroy()

    # signin_window.attributes('-topmost', False)


signin_window = tk.Tk()
signin_window.title('SignIn')
# signin_window.resizable(400, 500)
signin_window.config(background="#ffc107")
signin_window.geometry("400x500")
signin_window.focus_force()
signin_window.resizable(False, False)

window_width = 400
window_height = 500
screen_width = signin_window.winfo_screenwidth()
screen_height = signin_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
signin_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# signin_window.bind('<Escape>', lambda event: signin_window.withdraw())

signin_title_frame = tk.Frame(signin_window).grid(padx=20)

signin_frame = tk.Frame(signin_window).grid()

signin_button_frame = tk.Frame(signin_window).grid(padx=20)

# signup_link_frame = tk.Frame(signin_window, bd=1, relief='solid')
# signup_link_frame.grid(padx=10, pady=(20, 50))


# ------------------------------------------------------------------------------------------------------------------
singin_text = 'Sign In'
signin_title = tk.Label(signin_title_frame, text=singin_text, bg=None, font=Style.page_heading,
                        fg=Style.page_heading_color, background="#ffc107")
signin_title.grid(row=0, column=0, padx=20, pady=20, sticky="E")
tk_image = resize_image((70, 70), 'images/userlogo.png')
# Create a Label widget with the resized image
signin_image = tk.Label(signin_title_frame, image=tk_image, background="#ffc107")
signin_image.grid(row=0, column=1, pady=20, padx=20, sticky="E")

signin_form_message = tk.Label(signin_title_frame, font=('helvetica', 12), fg="red", background="#ffc107")
signin_form_message.grid(row=1, column=1, columnspan=2, pady=(10, 0))

userid_label = tk.Label(signin_frame, text="Username:", background="#ffc107")
userid_label.grid(row=2, column=0, padx=(20, 5), sticky='E')
userid_entry = ctk.CTkEntry(signin_frame, width=200)
userid_entry.grid(row=2, column=1, padx=(5, 20), pady=10, sticky='W')

password_label = tk.Label(signin_frame, text="Password:", background="#ffc107")
password_label.grid(row=3, column=0, padx=(20, 5), ipady=5, sticky='E')
password_entry = ctk.CTkEntry(signin_frame, width=200, show="•", font=('arial', 12, 'bold'))
password_entry.grid(row=3, column=1, padx=(5, 20), pady=10, sticky='E')
password_entry.bind('<Return>',lambda event: authenticate())

show_password_var = tk.IntVar()
show_password_checkbox = tk.Checkbutton(signin_frame, text="Show Password", variable=show_password_var,
                                        command=show_password, bg="#ffc107")
show_password_checkbox.grid(row=4, column=1, sticky='e', padx=20)

signin_button = ctk.CTkButton(signin_button_frame, text="Login", command=authenticate)
# signin_button.grid(row=5, column=0, padx=(90,5), sticky="E")
signin_button.place(x=70, y=280)

reset_button = ctk.CTkButton(signin_button_frame, text="Reset/Back", command=reset_form)

# reset_button.grid(row=5, column=1,  padx=(5, 20), sticky="E")
reset_button.place(x=230, y=280)

reset_pass = ctk.CTkLabel(signin_button_frame, text="Forgot password - Reset password", font=("", 12))
reset_pass.place(x=105, y=460)
reset_pass.bind("<Button-1>", lambda event: on_pass_change())
# reset_pass.bind("<Button-1>", lambda event: passwordchange())
reset_pass.bind("<Enter>", on_hover)
reset_pass.bind("<Leave>", on_leave)

signin_window.mainloop()
