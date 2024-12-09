import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from operation import connect_to_database, resize_image, update_time, fetch_services_data, show_frame, Style,show_notification,print_card
import customtkinter as ctk
import sys
from decimal import Decimal, InvalidOperation

username = sys.argv[1]

full_name = []


# def run_diagnosis(event):
# Function to fetch patient details based on Patient Number
def fetch_patient():
    patient_id = entry_patient_id.get()

    if not patient_id:
        messagebox.showwarning("Input Error", "Please enter a Patient Number.")
        return

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "SELECT * FROM Patient WHERE USERID = %s"
        cursor.execute(sql, (patient_id,))
        record = cursor.fetchone()
        if record:
            print(record[1], record[2], record[8])
            global clinicID
            clinicID = record[8]

            # global full_name
            # full_name = f'{record[1] + " " + record[2]}'
            full_name.append(record[1] + " " + record[2])
            show_name.config(text=record[1] + " " + record[2])
            show_gender.config(text=record[7])
            show_age.config(text=record[5])
            show_phone.config(text=record[6])
            show_address.config(text=record[3])
            # p_name.config(text=record[1] + " " + record[2])


        else:
            messagebox.showerror("Database Error", "No patient found")

        conn.close()
        return
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")


# Function to submit the diagnosis along with selected services
def submit_diagnosis():
    patient_id = entry_patient_id.get()
    diagnosis = diagnostic_text.get(1.0, tk.END).strip()
    symptom = symptom_text.get(1.0, tk.END).strip()
    selected_services = []
    # Collect selected services

    # selected_services = StringVar()
    for var, service in zip(service_vars, services):
        if var.get():
            selected_services.append(service)

    selected_services_string = ", ".join(selected_services)

    if not patient_id or not diagnosis.strip() or not selected_services or not symptom:
        messagebox.showwarning("Input Error", "Please fill all required fields!")
        return

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "INSERT INTO PatientVisit (Patient_ID, Clinic_ID, Diagnosis, Symptoms, Services, CheckInBy) VALUES (%s, %s, %s, %s,%s, %s) "
        cursor.execute(sql,
                       (patient_id.upper(), clinicID, diagnosis, symptom, selected_services_string.strip(), username,))
        conn.commit()

        today_date = datetime.datetime.now().date()
        sql = """ SELECT p.VisitID
                        FROM PatientVisit p
                        WHERE p.Patient_ID = %s
                        AND p.VisitDate = %s
                        ORDER BY p.VisitID DESC
			            LIMIT 1;"""
        cursor.execute(sql, (patient_id, today_date))
        results = cursor.fetchone()
        TotalCost = float(0.00)
        sql = "INSERT INTO Bills (VisitID, TotalCost ) VALUES (%s, %s) "
        cursor.execute(sql, (results[0], TotalCost,))
        conn.commit()

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Inserting data: {err}")

    # Here you can write code to save the diagnosis and selected services to the database
    messagebox.showinfo("Success",
                        f"Diagnosis submitted for Patient {patient_id}\nServices: {', '.join(selected_services)}")
    billterm()
    billframe()


def billterm():
    try:
        patient_id = entry_patient_id.get()
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "SELECT Services FROM PatientVisit p WHERE p.Patient_ID = %s ORDER BY VisitID DESC LIMIT 1"
        cursor.execute(sql, (patient_id,))
        data = cursor.fetchall()
        print(data)

        # return data

        sevis = {row[0]: str(row[1]) for row in fetch_services_data()}
        itemlist = []
        tcost = []
        for row in data:
            for item in row[0].split(', '):
                print(item)
                itemlist.append(item)
                print(sevis.get(item))
                tcost.append(sevis.get(item))

        total = sum(float(cost) for cost in tcost)
        print(total)

        cursor = conn.cursor()
        sql = """ UPDATE Bills 
                SET TotalCost = %s 
                WHERE VisitID = (
                    SELECT VisitID 
                    FROM PatientVisit 
                    WHERE Patient_ID = %s 
                    ORDER BY VisitID DESC 
                    LIMIT 1)  """
        cursor.execute(sql, (total, patient_id,))
        conn.commit()
        conn.close()
        return sevis
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")


def billframe():
    patient_id = entry_patient_id.get()
    if not patient_id:
        messagebox.showinfo("Empty ID Field","Please enter Patient ID and try again")
        show_notification(diagnosis_window, "Please enter Patient ID", duration=5000, bg_color="pale green",x=320, y=25,height=30, width=150)

        return
    else:
        print_btn()
        bill_structure()
        show_frame(frame2)


# Main window setup
diagnosis_window = tk.Tk()
diagnosis_window.title("Patient Medical Records")
diagnosis_window.focus_force()
diagnosis_window.iconphoto(True, resize_image((90, 90), 'images/HSMS.png'))


# Center-aligning the window on the screen
window_width = 700
window_height = 600
screen_width = diagnosis_window.winfo_screenwidth()
screen_height = diagnosis_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
diagnosis_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")


frame2 = ctk.CTkFrame(diagnosis_window, fg_color='gray90', height=500, width=500)
frame2.place(x=140, y=40)
frame2_bill_to = ctk.CTkFrame(frame2, fg_color='gray96', height=90, width=480)
frame2_bill_to.place(x=10, y=30)
frame2_bill_items = ctk.CTkFrame(frame2, fg_color='gray96', height=150, width=480)
frame2_bill_items.place(x=10, y=130)
frame2_bill_final = ctk.CTkFrame(frame2, fg_color='gray96', height=100, width=480)
frame2_bill_final.place(x=10, y=380)

frame1_anex = ctk.CTkFrame(diagnosis_window, fg_color='gray92', height=500, width=500)
frame1_anex.place(x=140, y=40)

frame1 = ctk.CTkFrame(frame1_anex, fg_color='gray92', height=500, width=500)
frame1.place(x=0, y=0)

frame3 = tk.Frame(diagnosis_window)
frame3.place(x=430, y=500)

frame4 = ctk.CTkFrame(frame1, fg_color='gray98', width=300, height=130)
frame4.place(x=100, y=50)

tk_image = resize_image((70, 70), 'images/doctor-patient.png')
# Create a Label widget with the resized image
doctor_patient_image = tk.Label(diagnosis_window, image=tk_image)
doctor_patient_image.place(x=40, y=40)

# Patient ID (Search Field)
label_patient_id = tk.Label(frame1, text="Patient ID:", font=("Geneva", 12))
label_patient_id.grid(row=0, column=0, padx=10, pady=(10, 140), sticky="w")
entry_patient_id = tk.Entry(frame1, font=("Geneva", 12))
entry_patient_id.grid(row=0, column=1, padx=10, pady=(10, 140))

# Fetch Patient Button
fetch_button = tk.Button(frame1, text="Fetch Patient", command=fetch_patient, font=("Geneva", 12),
                         fg="black")
fetch_button.grid(row=0, column=2, padx=10, pady=(10, 140))

# Time Update label
# Label to display the current datetime
time_label = tk.Label(diagnosis_window, font=("Geneva", 12), fg="blue")
time_label.place(x=300, y=5)
update_time(time_label)

show_nam_var = "BABA"

# Patient Name
label_name = tk.Label(frame4, text="Name:", font=("Geneva", 12), bg='gray98')
label_name.grid(row=1, column=0, padx=10, pady=0, sticky="ws")
show_name = tk.Label(frame4, text="", font=("Geneva", 12), bg='gray98')
show_name.grid(row=1, column=1, padx=10, pady=0, sticky='ws')

# Patient Age
label_age = tk.Label(frame4, text="Age:", font=("Geneva", 12), bg='gray98')
label_age.grid(row=2, column=0, padx=10, pady=0, sticky="wn")
show_age = tk.Label(frame4, text="", font=("Geneva", 12), bg='gray98')
show_age.grid(row=2, column=1, padx=10, pady=0, sticky='wn')

# Gender
label_gender = tk.Label(frame4, text="Gender:", font=("Geneva", 12), bg='gray98')
label_gender.grid(row=3, column=0, padx=10, pady=0, sticky="nw")
show_gender = tk.Label(frame4, text="", font=("Geneva", 12), bg='gray98')
show_gender.grid(row=3, column=1, padx=10, pady=0, sticky='wn')

# Phone Number
label_phone = tk.Label(frame4, text="Phone Number:", font=("Geneva", 12), bg='gray98')
label_phone.grid(row=4, column=0, padx=10, pady=0, sticky="wn")
show_phone = tk.Label(frame4, text="", font=("Geneva", 12), bg='gray98')
show_phone.grid(row=4, column=1, padx=10, pady=0, sticky='nw')

# Address
label_phone = tk.Label(frame4, text="Address:", font=("Geneva", 12), bg='gray98')
label_phone.grid(row=5, column=0, padx=10, pady=(0, 0), sticky="wn")
show_address = tk.Label(frame4, text="", font=("Geneva", 12), bg='gray98')
show_address.grid(row=5, column=1, padx=10, pady=(0, 0), sticky='wn')

# Symptom Field (Multiline)
label_symptom = tk.Label(frame1, text="Symptoms", font=("Geneva", 12))
label_symptom.grid(row=6, column=0, padx=10, pady=10, sticky="wn")
symptom_text = ctk.CTkTextbox(frame1, height=100, width=300, font=("Geneva", 12))
symptom_text.grid(row=6, column=1, padx=10, pady=10, columnspan=2, sticky="wn")
# diagnostic_text.config(state='readonly')

# Diagnostic Field (Multiline)
label_diagnosis = tk.Label(frame1, text="Diagnosis:", font=("Geneva", 12))
label_diagnosis.grid(row=7, column=0, padx=10, pady=10, sticky="wn")
diagnostic_text = ctk.CTkTextbox(frame1, height=100, width=300, font=("Geneva", 12))
diagnostic_text.grid(row=7, column=1, padx=10, pady=10, columnspan=2, sticky='wn')

# Services Checkboxes
label_services = tk.Label(frame1, text="Services:", font=("Geneva", 12))
label_services.grid(row=8, column=0, padx=10, sticky="wn")

# services = ["X-ray", "Scan", "Blood Test", "ECG", "MRI", "Surgery", "Regular Check ups"]
service_dic = {row[0]: (str(row[1]), row[2]) for row in fetch_services_data()}

services = []
service_vars = []
for row in fetch_services_data():
    services.append(row[0])
    service_vars = [tk.BooleanVar() for _ in services]

for i, service in enumerate(services):
    chk = ctk.CTkCheckBox(frame1, text=service, variable=service_vars[i], font=("Geneva", 12))
    chk.grid(row=8 + i // 3, column=1 + i % 3, sticky="wn")
    # chk.grid_columnconfigure(0, minsize=10)

# Submit Diagnosis Button
submit_button = ctk.CTkButton(diagnosis_window, text="Submit Diagnosis", command=submit_diagnosis, font=("Geneva", 12))
submit_button.place(x=400, y=550)

Bill_button = ctk.CTkButton(diagnosis_window, text="Get Bill Diagnosis", command=lambda: billframe(),
                            font=("Geneva", 12))
# Bill_button.place(x=250, y=550)

def print_btn():

    print_button = ctk.CTkButton(diagnosis_window, text="Print Bill", command=lambda: print_bill(), font=("Geneva", 12))
    print_button.place(x=400, y=550)



# --------BILLING-SCREEN-TO-PRINT-BILL--SUBMIT-TO-ACCOUNTING-------------------------

def bill_structure():
    def dis_set():
        ftotal_dis = bill_data()
        selected_value = discount.get()
        # print(f"Selected value: {selected_value}")

        try:
            discount_value = Decimal(selected_value.strip('%')) / 100
            applying_dis = discount_value * Decimal(ftotal_dis)
            subtracting_dis = Decimal(ftotal_dis) - applying_dis

            final_total.configure(text=f'${subtracting_dis:.2f}')
            show_notification(diagnosis_window, f'{selected_value} has been applied', duration=5000, bg_color="pale green", x=320,
                              y=305, text_color="black", height=30, width=150)

        except (ValueError, InvalidOperation) as e:
            print(f"Error converting discount value: {e}")

    def bill_data():
        global view_more_btn, apply_dis_btn
        try:
            patient_id = entry_patient_id.get()
            conn = connect_to_database()
            cursor = conn.cursor()
            sql = """SELECT BillID, PatientVisit.Patient_ID, CONCAT(First_Name,"  ", Last_Name) as F_Name ,Address,PhoneNumber,BillDate,TotalCost
                                FROM Bills 
                                JOIN PatientVisit 
                                ON  Bills.VisitID = PatientVisit.VisitID
                                JOIN Patient
                                ON PatientVisit.Patient_ID = Patient.USERID
                                JOIN clinic
                                ON PatientVisit.Clinic_ID = clinic.Clinic_ID
                                WHERE PatientVisit.Patient_ID = %s
                                ORDER BY BillID desc
                                limit 1;
                            """
            cursor.execute(sql, (patient_id,))
            record = cursor.fetchone()
            if record:
                print(record[3].strip(), record[6])
                print(record)

                b_id.configure(text=f'BILL ID #00{record[0]}')
                p_id.configure(text=record[1])
                p_name.configure(text=record[2].upper())
                p_address.configure(text=record[3].strip())
                p_phone.configure(text=record[4].strip())
                p_date.configure(text=record[5])
                p_service_total.configure(text=record[6])
                general_charge = 120
                p_diag_total.configure(text=general_charge)
                medication = 'See your \nPharmacist'
                p_med_total.configure(text=medication)


                # Convert values to Decimal
                subTotal = Decimal(record[6]) + Decimal(general_charge)
                sub_total.configure(text=f'${subTotal}')

                get_tax = subTotal * Decimal('2.75') / Decimal('100')
                taxes.configure(text=f'${get_tax:.2f}')

                ftotal = get_tax + subTotal
                final_total.configure(text=f'${ftotal:.2f}')

                return ftotal
            else:
                messagebox.showerror("Database Error", "No patient found")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")

    # , , , Diagnosis, Services, Symptoms, CheckInBy, Patient_ID, First_Name, Last_Name, , DateOfBirth, Age, PhoneNumber, Gender, ClinicID, Emergency_Contact_Name, Emergency_Contact, USERID, Created_At, Updated_At
    ctk.CTkLabel(frame2, text="Patient Bill", font=Style.page_heading, text_color=Style.page_heading_color).place(x=180,
                                                                                                                  y=1)
    b_id = ctk.CTkLabel(frame2, text="Bill ID #2302", font=Style.level_three_subheading,
                        text_color=Style.page_heading_color)
    b_id.place(x=20, y=1)
    p_id = ctk.CTkLabel(frame2, text="Patien ID #2302", font=Style.level_three_subheading,
                        text_color=Style.page_heading_color)
    p_id.place(x=380, y=1)

    ctk.CTkLabel(frame2_bill_to, text="BILL TO", font=('Geneva', 9, 'italic')).place(x=5, y=0)
    p_name = ctk.CTkLabel(frame2_bill_to, text="Shehu Ibrahim ", font=Style.level_one_subheading)
    p_name.place(x=10, y=20)
    p_address = ctk.CTkLabel(frame2_bill_to, text="12 main st Mount Pleasant MI")
    p_address.place(x=10, y=40)
    p_phone = ctk.CTkLabel(frame2_bill_to, text="9999999999")
    p_phone.place(x=10, y=60)
    ctk.CTkLabel(frame2_bill_to, text="BILL DATE", font=('Geneva', 9, 'italic')).place(x=420, y=0)
    p_date = ctk.CTkLabel(frame2_bill_to, text="2024-11-05", font=Style.level_three_subheading)
    p_date.place(x=400, y=19)

    ctk.CTkLabel(frame2_bill_items, text="BIll Name", font=('Geneva', 9, 'italic')).place(x=5, y=0)
    ctk.CTkLabel(frame2_bill_items, text="Amount", font=('Geneva', 9, 'italic')).place(x=420, y=0)

    p_services = ctk.CTkLabel(frame2_bill_items, text="Services", font=Style.level_one_subheading)
    p_services.place(x=10, y=30)
    p_service_total = ctk.CTkLabel(frame2_bill_items, text="$1505.00", font=("Geneva", 12))
    p_service_total.place(x=400, y=30)
    p_diag = ctk.CTkLabel(frame2_bill_items, text="Diagnosis", font=Style.level_one_subheading)
    p_diag.place(x=10, y=60)
    p_diag_total = ctk.CTkLabel(frame2_bill_items, text="$1005.00", font=("Geneva", 12))
    p_diag_total.place(x=400, y=60)
    p_med = ctk.CTkLabel(frame2_bill_items, text="Medication(0)", font=Style.level_one_subheading)
    p_med.place(x=10, y=90)
    p_med_total = ctk.CTkLabel(frame2_bill_items, text="$1005.00", font=("Geneva", 12))
    p_med_total.place(x=400, y=90)
    view_more_btn = ctk.CTkButton(frame2, text="View More", text_color="blue", border_width=1, fg_color='gray96',
                                  border_color='black', command=lambda: view_more())
    view_more_btn.place(x=180, y=266)

    ctk.CTkLabel(frame2, text="Additional Note(Optional)", font=("Geneva", 9)).place(x=15, y=280)
    bill_note = ctk.CTkTextbox(frame2, width=250, height=70).place(x=10, y=305)

    percentages = ['0%','5%','10%', '15%', '20%', '25%']
    ctk.CTkLabel(frame2, text="Discount", font=("Geneva", 12)).place(x=280, y=300)
    discount = ctk.CTkComboBox(frame2, values=percentages, width=100, state="readonly")
    discount.place(x=280, y=325)

    apply_dis_btn = ctk.CTkButton(frame2, text="Apply Dis.", width=20, command=lambda: dis_set())
    apply_dis_btn.place(x=400, y=325)

    ctk.CTkLabel(frame2_bill_final, text="SubTotal", font=("Geneva", 12)).place(x=10, y=10)
    sub_total = ctk.CTkLabel(frame2_bill_final, text="$1505.00", font=("Geneva", 12))
    sub_total.place(x=400, y=10)
    ctk.CTkLabel(frame2_bill_final, text="TAX", font=("Geneva", 12)).place(x=10, y=35)
    taxes = ctk.CTkLabel(frame2_bill_final, text="$1005.00", font=("Geneva", 12))
    taxes.place(x=400, y=35)
    ctk.CTkLabel(frame2_bill_final, text="Total", font=Style.level_one_subheading).place(x=10, y=60)
    final_total = ctk.CTkLabel(frame2_bill_final, text="$1005.00", font=("Geneva", 12))
    final_total.place(x=400, y=60)
    bill_data()



def print_bill():
    patient_id = entry_patient_id.get()
    print_card(frame2,patient_id)
    return

def show_notification_message():
    show_notification(diagnosis_window, "Task completed successfully!", duration=5000)
def view_more():
    messagebox.showinfo("Note\n",'This is temporarily not available')

diagnosis_window.rowconfigure(1, weight=1)
diagnosis_window.columnconfigure(1, weight=1)

# frame1.grid_rowconfigure(1, weight=1)
# frame1.grid_columnconfigure(1, weight=1)

# Run the Tkinter main loop
diagnosis_window.mainloop()
