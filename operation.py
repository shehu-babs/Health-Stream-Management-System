import subprocess
import sys
from idlelib import tree
from tkinter import PhotoImage
from PIL import Image, ImageTk
from PIL._tkinter_finder import tk
import time
import tkinter as tkk

from matplotlib.backend_tools import cursors
from matplotlib.pyplot import title
from mysql.connector import cursor
import mysql.connector
from reportlab.lib.colors import HexColor

from config import Config
import mysql.connector
from datetime import datetime
from tkinter import ttk, messagebox
from customtkinter import CTkImage
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,Image as imm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import datetime
from tkinter import filedialog
from PIL import Image, ImageGrab
import customtkinter as ctk
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from openpyxl import Workbook


today = datetime.date.today()



# connect to database
def connect_to_database():
    """
        Establishes and returns a connection to the MySQL database.

        This function uses the configuration settings from the `Config` class (e.g., host, user,
        password, and database) to establish a connection to the MySQL database using the
        `mysql.connector` library.

        Returns:
        mysql.connector.connection.MySQLConnection: A connection object to interact with the database.

        Raises:
        mysql.connector.Error: If a connection error occurs (e.g., incorrect credentials,
                                unavailable database, etc.), an exception will be raised.
        """
    conn = mysql.connector.connect(
        host=Config.db_host,
        user=Config.user,
        password=Config.password,
        database=Config.database)
    return conn


# conn = connect_to_database()
# cursor = conn.cursor()


class Style():
    page_heading = ('San Francisco', 25, 'bold')
    page_heading_color = '#6A0032'
    subheading_color = '#424242'
    subheading = ('San Francisco', 12, 'bold')
    caption = ('Arial', 10)
    level_one_subheading_color = '#424242'
    level_one_subheading = ('Poppins', 15, 'bold')
    level_three_subheading = ('Poppins', 13)
    page_heading_genova = ('Geneva', 30, 'bold')
    page_heading_geneva2 = ('Geneva', 16, 'bold')



def resize_image(size, image_url):
    """ Function to resize an image.
    Args:
    size (tuple): size of the image
    image_url (str): url of the image
    Returns:Resized image
    """
    # Load the original image
    original_image = Image.open(f'{image_url}')
    resized_image = original_image.resize((size[0], size[1]))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image


def resize_image2(size, image_url):
    """ Function to resize an image for use with CustomTkinter's CTkImage.
    Args:
        size (tuple): Desired (width, height) size of the image.
        image_url (str): Path or URL to the image file.
    Returns:
        CTkImage: Resized image compatible with CustomTkinter.
    """
    # Load the original image
    original_image = Image.open(image_url)

    # Resize the image to the specified size
    resized_image = original_image.resize(size)

    # Create a CTkImage object with the resized image
    ctk_image = CTkImage(light_image=resized_image, dark_image=resized_image, size=size)

    return ctk_image


# Function to update the datetime display
def update_time(label):
    """
      Updates a label widget with the current date and time, refreshing every second.

      This function retrieves the current date and time, formats it as 'YYYY-MM-DD HH:MM:SS',
      and sets it as the text of the specified label widget. It then schedules itself
      to run again after 1000 milliseconds, maintaining an updated timestamp display.

      Parameters:
      label (tkinter.Label): The label widget to update with the current date and time.
      """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label.config(text=f'Date Time: {current_time}')
    # Schedule the update_time function to run again after 1000 milliseconds (1 second)
    label.after(1000, update_time, label)


# authenticate students if credentials are valid
def authenticate_user(userid, password):
    """
       Authenticates a user based on a provided user ID and password.

       This function checks if the given password is empty. If so, it returns a
       tuple indicating failed authentication with an error message. If the credentials
       match predefined values (user ID as 'admin' and password as 'mypass'), it returns
       a tuple indicating successful authentication. Otherwise, it returns a tuple
       indicating failed authentication due to invalid credentials.

       Parameters:
       userid (str): The user ID to authenticate.
       password (str): The password associated with the user ID.

       Returns:
       tuple: A tuple containing a boolean (authentication success status) and a
              string message explaining the result.
       """
    if password == "":
        return (False, "Empty Password")
    if userid == "admin" and password == "mypass":
        return (True, "Logged In")
    else:
        return (False, "Invalid user")


def get_user_info(username):
    """
        Retrieves information for a specified user from the 'admin_credentials' database table.

        This function executes a SQL query to select all columns from the 'admin_credentials' table
        where the username matches the provided value. It fetches and returns the first matching
        record.

        Parameters:
        username (str): The username to look up in the 'admin_credentials' table.

        Returns:
        tuple or None: A tuple containing user information if a matching record is found;
                       otherwise, None if no match exists.
        """
    query = 'SELECT * FROM admin_credentials WHERE username = %s;'
    cursor.execute(query, (username,))
    user_info = cursor.fetchone()
    return user_info


def fetch_patient_gender_data():
    """
        Fetches patient data grouped by gender from the 'PATIENTS' database table.

        This function connects to a database, executes a SQL query to count the number
        of patients grouped by gender, and retrieves the results. The database connection
        is closed after fetching the data. If a database error occurs, an error message
        is displayed, and an empty list is returned.

        Returns:
        list of tuples: A list of tuples where each tuple contains a gender and the count
                        of patients of that gender, or an empty list if an error occurs.
        """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "SELECT Gender, COUNT(*) FROM PATIENTS GROUP BY Gender"
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []


def fetch_billing_data():
    """
        Fetches billing data grouped by clinic from the 'BILLING' database table.

        This function connects to a database, executes a SQL query to count the number
        of billing records grouped by clinic, and retrieves the results. The database
        connection is closed after fetching the data. If a database error occurs, an
        error message is displayed, and an empty list is returned.

        Returns:
        list of tuples: A list of tuples where each tuple contains a clinic name and the
                        count of billing records for that clinic, or an empty list if an
                        error occurs.
        """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "SELECT Clinic, COUNT(*) FROM BILLING "
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []


def fetch_services_data():
    """
        Fetches service details from the 'Services' database table.

        This function connects to a database, executes a SQL query to retrieve the
        service name, cost, and service code for each service in the 'Services' table,
        and retrieves the results. The database connection is closed after fetching the
        data. If a database error occurs, an error message is displayed, and an empty
        list is returned.

        Returns:
        list of tuples: A list of tuples where each tuple contains the service name,
                        cost, and service code for a service, or an empty list if an
                        error occurs.
        """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "SELECT Service_Name,  Cost, Service_Code FROM Services "
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []


def fetch_visit_count_data():
    """
        Fetches visit counts grouped by clinic from the 'PatientVisit' and 'clinic' database tables.

        This function connects to a database, executes a SQL query that joins the 'PatientVisit'
        and 'clinic' tables to count the number of visits for each clinic, and retrieves the results.
        The database connection is closed after fetching the data. If a database error occurs, an
        error message is displayed, and an empty list is returned.

        Returns:
        list of tuples: A list of tuples where each tuple contains a clinic name and the count of
                        visits to that clinic, or an empty list if an error occurs.
        """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = """SELECT Name, COUNT(VisitID) 
                FROM PatientVisit
                JOIN clinic ON PatientVisit.Clinic_ID = clinic.Clinic_ID
                GROUP BY Name;"""
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []
def fetch_bill_sum_data():
    """
        Fetches the total billing amount grouped by clinic from the 'Bills' and related tables.

        This function connects to a database, executes a SQL query to calculate the total billing
        amount for each clinic by joining the 'Bills', 'PatientVisit', and 'clinic' tables, and
        retrieves the results sorted by the total cost in descending order. The database connection
        is closed after fetching the data. If a database error occurs, an error message is displayed,
        and an empty list is returned.

        Returns:
        list of tuples: A list of tuples where each tuple contains a clinic name and the total billing
                        amount for that clinic, or an empty list if an error occurs.
        """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = """SELECT Name, sum(TotalCost), sum(Netpay), sum(Tax), sum(Subtotal), SUM(CASE WHEN Bills.PaymentType = 'NotPaid' THEN 1 ELSE 0 END) as Payment FROM BIS698W_29.Bills
                    join BIS698W_29.PatientVisit on Bills.VisitID = PatientVisit.VisitID
                    join BIS698W_29.clinic on PatientVisit.Clinic_ID=clinic.Clinic_ID
                    group by Name
                    order by sum(TotalCost) desc;"""
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []

def fetch_clinic_data():
    """
        Fetches clinic information, including clinic names and the number of patients,
        from the 'clinic' database table.

        This function connects to a database, executes a SQL query to retrieve each clinic's
        name and the corresponding number of patients from the 'clinic' table, and retrieves
        the results. The database connection is closed after fetching the data. If a database
        error occurs, an error message is displayed, and an empty list is returned.

        Returns:
        list of tuples: A list of tuples where each tuple contains a clinic name and the
                        number of patients in that clinic, or an empty list if an error occurs.
        """
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "SELECT Name, Number_of_Patient FROM clinic; "
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []


def sort_column(tree, col, reverse):
    """
       Sorts the items in a Treeview widget column in ascending or descending order.

       This function retrieves all data from the specified column in the Treeview widget,
       sorts it in ascending or descending order based on the `reverse` parameter, and
       rearranges the items in the Treeview accordingly. After sorting, it updates the
       column header command to toggle the sorting order when clicked again.

       Parameters:
       tree (tkinter.ttk.Treeview): The Treeview widget containing the data to be sorted.
       col (str): The column identifier to sort by.
       reverse (bool): A boolean flag indicating the sort order; if True, sorts in descending
                       order; if False, sorts in ascending order.
       """
    # Fetch all data in the treeview
    data = [(tree.set(child, col), child) for child in tree.get_children('')]

    # Sort the data
    data.sort(reverse=reverse)

    # Rearrange items in sorted positions
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)

    # Toggle the sorting order on next click
    tree.heading(col, command=lambda _col=col: sort_column(tree, _col, not reverse))


def show_frame(frame):
    """
        Brings the specified frame to the front in a Tkinter application.

        This function raises the given frame, making it the active frame in the
        Tkinter window by placing it at the top of the stacking order. This is
        useful when switching between different frames or views in a multi-frame layout.

        Parameters:
        frame (tkinter.Frame): The frame to be raised and displayed in the window.
        """
    frame.tkraise()


def show_notification(root, message, duration=30000, bg_color="green",x=50, y=50, width=600,height=100, ):
    """
    Function to display a notification for a given duration.

    :param root: The root Tkinter window where the notification should appear
    :param message: The message to display in the notification
    :param duration: Time in milliseconds to display the notification (default is 30 seconds)
    :param bg_color: Background color for the notification (default is green)
    :param text_color: Text color for the notification (default is white)

    Args:
        x:
        y:
        width:
        height:

    """
    # Create a new frame for the notification
    notification_frame = ctk.CTkFrame(root, fg_color=bg_color, height=height, width=width, corner_radius=10)
    notification_frame.place(x=x, y=y)
    notification_label = ctk.CTkLabel(notification_frame, text=message, font=('Geneva', 12, 'bold'))
    notification_label.place(x=10, y=1)

    show_frame(root)

    root.after(duration, notification_frame.destroy)


# Function to generate PDF
def generate_pdf(bill_title,patient_name, billid, check_by, patient_idd,paddress,
                 pservices, cost, ncost,clinicname,clinicaddress,visitid):

    # Retrieve form data
    save_folder = "/Users/shehuibrahim/Downloads/BIS698/HSMS_BIS698/Bills"  # Replace this with your desired folder path
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)  # Create the folder if it doesn't exist
    # total = float(quantity) * float(price)

    # Get current date
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a PDF file
    file_name = f"{billid}_bill.pdf"
    file_path = os.path.join(save_folder, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Set title and date
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, height - 100, f"{bill_title}")
    c.line(100, height - 105, 500, height - 105)  # Horizontal line
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 130, f"Today's Date: {date}")

    # Bill details
    c.drawString(100, height - 160, f"{billid}")
    c.drawString(100, height - 180, f"{visitid}")
    c.drawString(100, height - 200, f"{clinicname}")
    c.drawString(100, height - 220, f"{clinicaddress}")
    c.drawString(100, height - 240, f"{check_by}")

    # Customer details
    c.drawString(100, height - 300, f"{patient_idd}")
    c.drawString(100, height - 320, f"{patient_name}")
    c.drawString(100, height - 340, f"{paddress}")

    # Services details
    c.drawString(100, height - 380, f"{pservices}")
    c.drawString(100, height - 400, f"{cost}")
    c.drawString(100, height - 420, f"{ncost}")

    # c.drawString(100, height - 280, f"Total: ${total:.2f}")

    # Footer
    c.drawString(100, height - 460, "Thank you for your visit \n Get well soon ❤!")
    c.line(100, height - 465, 500, height - 465)  # Horizontal line

    # Save PDF
    c.save()
    messagebox.showinfo("PDF Saved", f"PDF bill saved as {billid}")

    # Open the PDF file after saving
    try:
        os.system(f'open "{file_path}"')
        os.startfile(file_path)  # This will work on Windows
    except AttributeError:
        # Use 'open' command for macOS or 'xdg-open' for Linux
        if os.name == 'posix':
            os.system(f'open "{file_path}"')  # macOS
            # os.system(f'xdg-open "{file_path}"')  # Uncomment for Linux


# Function to generate PDF
def auto_pdf(items, filename, title):
    # Retrieve form data
    global last_H
    save_folder = "/Users/shehuibrahim/Downloads/BIS698/HSMS_BIS698/Bills"  # Replace this with your desired folder path
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)  # Create the folder if it doesn't exist

    # Get current date and time
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a PDF file
    file_name = f"{filename}_bill.pdf"
    file_path = os.path.join(save_folder, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Set title and date
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, height - 100, title)
    c.line(100, height - 105, 500, height - 105)  # Horizontal line
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 130, f"Today's Date: {date}")

    # Add items to the PDF
    initialH = 160
    for row in items:
        if row is None:
            continue
        c.drawString(20, height - initialH, f"{row}")
        initialH += 20

    last_H = initialH


    # Add closing message
    c.drawString(100, height - last_H, "Thank you for your visit. Get well soon ❤!")

    # Save PDF
    c.save()
    messagebox.showinfo("PDF Saved", f"PDF bill saved as {filename}")

    # Open the PDF file after saving
    try:
        os.system(f'open "{file_path}"')  # macOS
        # os.startfile(file_path)  # Windows
    except AttributeError:
        if os.name == 'posix':
            os.system(f'open "{file_path}"')  # macOS
            # os.system(f'xdg-open "{file_path}"')  # Uncomment for Linux

def print_card(window,file_name):
    """
        Captures the content of a Tkinter window and saves it as an image for printing.

        This function retrieves the geometry of the given window, captures the window's
        content as an image using the `ImageGrab` module, and prompts the user to specify
        a location to save the image file. After saving the image as a PNG file, the function
        opens the image and triggers the print dialog for the user to print the ID card.

        Parameters:
        window (tkinter.Tk or tkinter.Toplevel): The Tkinter window to capture as an ID card.
        """
    # Get the ID card window geometry
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    width = window.winfo_width() + x
    height = window.winfo_height() + y

    # Capture the window content as an image
    image = ImageGrab.grab(bbox=(x, y, width, height))

    # Ask the user where to save the image (optional, for saving as a file)
    # save_path = filedialog.asksaveasfilename(defaultextension=".png",
    #                                          filetypes=[("PNG files", "*.png")])
    save_directory = "/Users/shehuibrahim/Downloads/BIS698/HSMS_BIS698/receipts"  # Replace with your desired path
    filename = f"{today}_{file_name}.png"  # Replace with your desired filename
    save_path = os.path.join(save_directory, filename)

    if save_path:
        image.save(save_path)
        try:
            os.system(f'open "{save_path}"')
            os.startfile(save_path, "print")  # Trigger the print dialog to print the saved image
        except Exception as e:
            print(e)

def create_bar_chart(root):
    """
     Creates and displays a bar chart of patient visits for each clinic.

     This function fetches patient visit data using the `fetch_visit_count_data` function,
     processes the data to extract clinic names and visit counts, and creates a bar chart
     using Matplotlib. The chart is embedded in a Tkinter window using `FigureCanvasTkAgg`.

     The bar chart displays the number of patient visits for each clinic, with custom titles
     and axis labels. The chart is drawn on a Tkinter root window and placed at the top-left
     corner of the window.

     Parameters:
     root (tkinter.Tk or tkinter.Toplevel): The Tkinter root window or frame where the
                                             bar chart will be displayed.

     """
    data = fetch_visit_count_data()
    Clinics = [(' '.join(row[0].split()[:-2])) for row in data]
    Visits = [row[1] for row in data]

    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(Clinics, Visits, color="skyblue")
    ax.set_title("Patient Visit Bar Chart", font="Geneva", fontsize=18, fontweight='bold', color='darkblue')
    ax.set_xlabel("Clinics", font="Geneva", fontsize=12, fontweight='bold', color='darkred')
    ax.set_ylabel("Visits", font="Geneva", fontsize=12, fontweight='bold', color='darkred')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=0, y=0)  # Adjust padding as needed

def create_bar_chart_sum_income(root):
    """
        Creates and displays a bar chart of total income per clinic.

        This function fetches billing data using the `fetch_bill_sum_data` function,
        processes the data to extract clinic names and the corresponding total income,
        and creates a bar chart using Matplotlib. The chart is embedded in a Tkinter window
        using `FigureCanvasTkAgg`.

        The bar chart displays the sum of income for each clinic, with custom titles
        and axis labels. The chart is drawn on a Tkinter root window and placed at the
        top-left corner of the window.

        Parameters:
        root (tkinter.Tk or tkinter.Toplevel): The Tkinter root window or frame where the
                                                bar chart will be displayed.
        """
    data = fetch_bill_sum_data()
    Clinics = [(' '.join(row[0].split()[:-2])) for row in data]
    Visits = [row[2] for row in data]

    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(Clinics, Visits, color="skyblue")
    ax.set_title("Sum of Income By clinic", font="Geneva", fontsize=18, fontweight='bold', color='darkblue')
    ax.set_xlabel("Clinics", font="Geneva", fontsize=12, fontweight='bold', color='darkred')
    ax.set_ylabel("Amount", font="Geneva", fontsize=12, fontweight='bold', color='darkred')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=0, y=0)  # Adjust padding as needed


def plot_billing_distribution(frame):
    data = fetch_billing_data()
    Clinic = [row[0] for row in data]
    counts = [row[1] for row in data]

    # Create a pie chart
    figure = plt.Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.pie(counts, labels=Clinic, autopct='%1.1f%%', startangle=90)
    ax.set_title("Billings Overview")

    # Embed the chart in the Tkinter frame
    chart = FigureCanvasTkAgg(figure, frame)
    chart.get_tk_widget().grid(row=0, column=0, pady=(0, 30))


def plot_clinic_distribution(frame):
    """
        Creates and displays a pie chart showing the distribution of patients across clinics.

        This function fetches clinic data using the `fetch_clinic_data` function, processes
        the data to extract clinic names and the corresponding patient counts, and creates
        a pie chart using Matplotlib. The chart is embedded in a Tkinter frame using
        `FigureCanvasTkAgg`.

        The pie chart visualizes the percentage distribution of patients across clinics
        and includes labels showing the clinic name and the percentage of patients.

        Parameters:
        frame (tkinter.Frame): The Tkinter frame where the pie chart will be displayed.
        """
    data = fetch_clinic_data()
    Clinic = [row[0] for row in data]
    Patients = [row[1] for row in data]

    # Create a pie chart
    figure = plt.Figure(figsize=(6.5, 4), dpi=110)
    ax = figure.add_subplot(111)
    ax.pie(Patients, labels=Clinic, autopct='%1.1f%%', startangle=90)
    ax.set_title("Clinic Patient Count", font="Geneva", fontsize=18, fontweight='bold')

    # Embed the chart in the Tkinter frame
    chart = FigureCanvasTkAgg(figure, frame)
    chart.get_tk_widget().grid(row=0, column=0, pady=(0, 20))
    return


def fetching_service_option():
    """
        Fetches all service records from the 'Services' table in the database.

        This function connects to the database, executes a SQL query to retrieve all records
        from the 'Services' table, and returns the fetched data.

        Returns:
        list of tuples: A list of tuples where each tuple contains data for a service, or
                        an empty list if no records are found or an error occurs.
        """
    conn = connect_to_database()
    cursor = conn.cursor()
    # Update password for the given username or phone number, and set the username if it's empty
    sql = """
                SELECT * FROM Services 
            """
    cursor.execute(sql)
    record = cursor.fetchall()

    return record


def days_count(entry_date):
    """Calculate the days since `entry_date`."""
    # if isinstance(entry_date, str):
    #     entry_date = datetime.strptime(entry_date, "%Y-%m-%d")  # Adjust format if needed
    # return (datetime.now() - entry_date).days
    # If `entry_date` is a date, convert it to a datetime for comparison with `now`
    if isinstance(entry_date, datetime.date) and not isinstance(entry_date, datetime.datetime):
        entry_date = datetime.datetime.combine(entry_date, datetime.datetime.min.time())

    # Calculate the difference in days
    return (datetime.datetime.now() - entry_date).days

def fetch_patient_bill_history(pnumber,vdate):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = """
            SELECT PatientVisit.VisitID, PatientVisit.Patient_ID, VisitDate, Diagnosis, Services,
            Symptoms, CheckInBy, First_Name, Last_Name, Address, DateOfBirth,
            PhoneNumber, Name, Clinic_Address, BillID, TotalCost, BillDate, Netpay
            FROM BIS698W_29.PatientVisit
            join Patient on PatientVisit.Patient_ID = Patient.USERID
            join clinic on PatientVisit.Clinic_ID = clinic.Clinic_ID
            join Bills on PatientVisit.VisitID = Bills.VisitID
            where PatientVisit.Patient_ID = %s and VisitDate = %s
            ORDER BY PatientVisit.VisitID DESC
			LIMIT 1;
            """
        cursor.execute(sql,(pnumber,vdate,))
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []



def export_tree_to_excel(tree, title):
    # Ask the user where to save the Excel file

    file_path = f"/Users/shehuibrahim/Downloads/BIS698/HSMS_BIS698/Reports/{today}_{title}.xlsx"
    try:
        # Create a new Excel workbook and active worksheet
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = title

        # Write the header (column names) to the Excel sheet
        column_names = [tree.heading(col)["text"] for col in tree["columns"]]
        sheet.append(column_names)

        # Write each row of data
        for child in tree.get_children():
            row_data = [tree.item(child)["values"][i] for i in range(len(column_names))]
            sheet.append(row_data)

        # Save the Excel workbook
        workbook.save(file_path)
        messagebox.showinfo("Export Successful", f"Data successfully exported to {file_path}")

        os.system(f'open "{file_path}"')
        # os.startfile(file_path)

    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred: {e}")

def submit_payment(amount,taxvalue,netvalue,paymenttype,billid ):
    conn = connect_to_database()
    try:
        cursor = conn.cursor()
        sql = """UPDATE BIS698W_29.Bills 
                 SET Netpay = %s, Tax = %s, Subtotal = %s, PaymentType = %s
                 WHERE BillID = %s """
        cursor.execute(sql, (float(amount),float(taxvalue),float(netvalue),str(paymenttype),int(billid)))


    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Updating data: {err}")

    finally:
        conn.commit()
        conn.close()
        return []

def fetch_employee_data_one(userid):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = """
            SELECT First_Name, Last_Name, Role, Staff_Address, DateOfBirth, PhoneNumber, Gender, 
            User_Name, Created_At, USERID, Name, Clinic_Address, Supervisor,is_active
            FROM BIS698W_29.STAFF
            join clinic on STAFF.ClinicID = clinic.Clinic_ID
            WHERE USERID = %s;
            """
        cursor.execute(sql,(userid,))
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []

def fetch_employee_data_all():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = """
            SELECT First_Name, Last_Name, Role, Staff_Address, DateOfBirth, PhoneNumber, Gender, 
            User_Name, Created_At, USERID, Name, Clinic_Address, Supervisor,is_active
            FROM BIS698W_29.STAFF
            join clinic on STAFF.ClinicID = clinic.Clinic_ID;
            """
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []
# print(fetch_employee_data_all())



def message_user(username,to,text_msg):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = """
            SELECT USERID
            FROM BIS698W_29.STAFF
            WHERE User_Name = %s;
            """
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        sender_id = data[0]
        sql = """
                    INSERT INTO Message 
                    SET Sender = %s, Receiver = %s, Message_Content = %s ;
                    """
        cursor.execute(sql, (sender_id,to,text_msg))
        conn.commit()
        conn.close()
        return sender_id
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []

def get_user_msg(userid):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = """
            SELECT * 
            FROM Message
            WHERE Receiver = %s;
            """
        cursor.execute(sql, (userid,))
        data = cursor.fetchall()
        conn.close()
        return data

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return []

def confirm_read(msg_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = """
            UPDATE Message
            SET Is_Read = '1'
            WHERE Message_ID = %s;
            """
        cursor.execute(sql, (int(msg_id),))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")


def load_treeview_shades(tree, state={"current": "normal"},shade1='white', shade2='lightgray'):
    # Configure row styles (run this once for the tree)
    tree.tag_configure('normal', background=shade1)
    tree.tag_configure('gray', background=shade2)

    # Alternate tag state
    if state["current"] == "normal":
        state["current"] = 'gray'
    else:
        state["current"] = "normal"

    return state["current"]

col = ("Name", "Age", "Department", "Location")
tb_data = [
    col,
    ["Alice", "30", "HR", "New York"],
    ["Bob", "25", "IT", "San Francisco"],
    ["Charlie", "35", "Finance", "Chicago"]
]

tb2_data = [
    col,
    ["baba", "30", "HR", "New York"],
    ["Ben", "25", "IT", "San Francisco"],
    ["Came", "35", "Finance", "Chicago"]
]
def create_pdf_report(heading_name="Employee Report", other_labels=None, data = tb_data, pg_size='portrait', generated_by='Admin',name=None ):
    # Define the directory and file name
    if other_labels is None:
        other_labels = ['']
    output_directory = "/Users/shehuibrahim/Downloads/BIS698/HSMS_BIS698/Reports"

    output_file = os.path.join(output_directory, f"{today}_{heading_name}.pdf")

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Define the PDF document based on page size
    if pg_size == 'portrait':
        pdf = SimpleDocTemplate(output_file, pagesize=letter)
    elif pg_size == 'landscape':
        pdf = SimpleDocTemplate(output_file, pagesize=landscape(letter))
    else:
        # Default to portrait letter size if pg_size is invalid
        pdf = SimpleDocTemplate(output_file, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    label_style = styles['Normal']
    doc_name_style = ParagraphStyle(
        'Heading1Centered',
        parent=styles['Heading1'],  # Start with the Heading1 style
        alignment=1,  # 1 stands for center alignment
        textColor=HexColor('#6A0032')  # Optional: set text color if needed
    )
    # Add a logo image
    logo_path = "/Users/shehuibrahim/Downloads/BIS698/HSMS_BIS698/images/HSMS.png"
    try:
        # print(f"Attempting to load logo from: {logo_path}")
        logo = imm(logo_path)
        logo.drawHeight = 50  # Adjust logo height
        logo.drawWidth = 50  # Adjust logo width
        # print("Logo loaded successfully!")
    except Exception as e:
        print(f"Error loading logo: {e}")
        logo = None  # Handle case where logo can't be loaded

    # Adding heading
    doc_name = Paragraph('Health Stream Management Report', doc_name_style)
    heading = Paragraph(heading_name, title_style)



    # Adding label
    labels = [
        Paragraph(f"This report contains details about {heading_name.lower()}.", label_style),
        Paragraph(f'Generated by: {generated_by}', label_style),
        Paragraph(f'Name: {name}', label_style),
        Paragraph(f'Generated On: {today}', label_style),
    ]

    new_items = []
    if other_labels:
        for item in other_labels:
            new_items.append(Paragraph(f'{item}',label_style))


    # Spacer for spacing between elements
    spacer = Spacer(1, 12)

    # Table data



    # Create a Table object
    table = Table(data)

    # Style the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header row
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header row
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Body background
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Grid lines
    ])
    table.setStyle(style)

    # Build the PDF
    elements = []
    if logo:  # Add logo only if it was loaded successfully
        elements.append(logo)
    elements.extend([doc_name, spacer, heading, spacer])
    elements.extend(labels)  # Add all labels
    elements.append(spacer)
    elements.extend(new_items)
    elements.append(spacer)
    elements.append(table)
    pdf.build(elements)

    print(f"PDF report generated: {output_file}")

    # Open the PDF using the default viewer
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(output_file)
        elif os.name == 'posix':  # For macOS/Linux
            subprocess.run(['open', output_file], check=True)
    except Exception as e:
        print(f"Could not open the PDF automatically: {e}")

# Generate the PDF
# create_pdf_report(data=tb2_data)