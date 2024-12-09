import sys
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from customtkinter import CTkLabel
from matplotlib.backend_tools import cursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from numpy.ma.core import count
from collections import Counter
import re


from operation import (connect_to_database, update_time, fetch_patient_gender_data, fetch_clinic_data,
                       fetch_billing_data, sort_column, Style, show_frame, resize_image, print_card,
                       plot_clinic_distribution,
                       create_bar_chart, create_bar_chart_sum_income, fetch_bill_sum_data, fetch_visit_count_data,
                       export_tree_to_excel, auto_pdf, load_treeview_shades, create_pdf_report)
import customtkinter as ctk


global patient_count,visit_all_data,p_rec_count,clinic_frame,main_frame2,patient_id_entry,clinic_entry,notice_label,\
    entry_for_frame3,combo_for_frame3,bill_all_data,names_of_clinics,main_frame,tree1_title,log_entry,combo_for_frame4,tree3,\
    combo2_frame4,main_frame4,display_log_data_count,notice_label2,pending_on_frame1

loger = sys.argv[1]
loger_username1 = sys.argv[2]
loger_username2 = sys.argv[3]
loger_username = loger_username1+' '+loger_username2

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
    chart.get_tk_widget().grid(row=0, column=0)




def get_billing_details(tree):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT CONCAT(First_Name,'   ',Last_Name) as PName, BillDate,Services,TotalCost,Tax,Subtotal,Netpay,PaymentType,Patient.USERID, Name
                            FROM BIS698W_29.Bills
                            JOIN PatientVisit ON Bills.VisitID = PatientVisit.VisitID
                            JOIN Patient ON PatientVisit.Patient_ID = Patient.USERID
                            JOIN clinic ON Patient.ClinicID = clinic.Clinic_ID;""")
        results = cursor.fetchall()
        # Clear the tree before inserting new data
        for row in tree.get_children():
            tree.delete(row)

        # Insert results into the tree
        for result in results:
            tag = load_treeview_shades(tree,shade2='#E8F4FA')
            tree.insert("", tk.END, values=result,tags=tag)

        total_cost_for_services = 0
        for i in results:
            total_cost_for_services +=i[6]

        Discounts = 0
        for i in results:
            Discounts += i[6]-i[5]



        Tax = 0
        for i in results:
            Tax += i[4]

        paystatus = 0
        for i in results:
            if str(i[7]) =='NotPaid':
                paystatus +=1

        print(f' Total Tax received is: {Tax}')

        print(f' Total Discount Issued is: {Discounts}')
        print(f' Total Cost for Service is: {total_cost_for_services}')

        notice_label2.configure(text=f'Search By All \nTaxes ${Tax} \nDiscounts: ${Discounts} \nIncome: ${total_cost_for_services} \nPending Payment: {paystatus}')
        pending_on_frame1.configure(text=f'Pending Payment: {paystatus}')

        return results
    conn.close()

def get_bill_data_by_id(tree):
    global entry_for_frame3,combo_for_frame3,bill_all_data
    entered_value = entry_for_frame3.get().upper()

    if entered_value:
        bills = [v for v in bill_all_data]
        # print(bills)

        fill_tree = []

        for v in bills:
            # print(v)
            if str(v[8]) == entered_value:
                fill_tree.append(v)
                print(v)

        for row in tree.get_children():
            tree.delete(row)

        # Insert results into the tree
        for result in fill_tree:
            tag = load_treeview_shades(tree, shade2='#E8F4FA')
            tree.insert("", tk.END, values=result,tags=tag)

        total_cost_for_services = 0
        for i in fill_tree:
            total_cost_for_services += i[6]

        Discounts = 0
        for i in fill_tree:
            Discounts += i[6]-i[5]

        Tax = 0
        for i in fill_tree:
            Tax += i[4]

        paystatus = 0
        for i in fill_tree:
            if str(i[7]) == 'NotPaid':
                paystatus += 1

        notice_label2.configure(
            text=f'Search By \n{entered_value} \nTaxes ${Tax} \nDiscounts: ${Discounts} \nIncome: ${total_cost_for_services} \nPending Payment: {paystatus}')

    else:
        get_billing_details(tree)



def get_bill_data_by_clinic(tree):
    global entry_for_frame3, combo_for_frame3, bill_all_data
    entered_value = combo_for_frame3.get()
    bills = [v for v in bill_all_data]

    fill_tree = [i for i in bills if i[9] == entered_value ]
    print(fill_tree)

    for row in tree.get_children():
        tree.delete(row)

    for result in fill_tree:
        tag = load_treeview_shades(tree, shade2='#E8F4FA')
        tree.insert('',tk.END,values=result,tags=tag)

    total_cost_for_services = 0
    for i in fill_tree:
        total_cost_for_services += i[6]

    Discounts = 0
    for i in fill_tree:
        Discounts += i[6]-i[5]

    Tax = 0
    for i in fill_tree:
        Tax += i[4]

    paystatus = 0
    for i in fill_tree:
        if str(i[7]) == 'NotPaid':
            paystatus += 1



    notice_label2.configure(
        text=f'Search By \n{entered_value} \nTaxes ${Tax} \nDiscounts: ${Discounts} \nIncome: ${total_cost_for_services} \nPending Payment: {paystatus}')


def get_bill_data_non_paid(tree):
    global entry_for_frame3, combo_for_frame3, bill_all_data
    # entered_value = combo_for_frame3.get()
    bills = [v for v in bill_all_data]

    fill_tree = [i for i in bills if i[7] == 'NotPaid' ]
    print(fill_tree)

    for row in tree.get_children():
        tree.delete(row)

    for result in fill_tree:
        tag = load_treeview_shades(tree, shade2='#E8F4FA')
        tree.insert('',tk.END,values=result,tags=tag)

    total_cost_for_services = 0
    for i in fill_tree:
        total_cost_for_services += i[3]

    Discounts = 0
    for i in fill_tree:
        Discounts += i[6]-i[5]

    Tax = 0
    for i in fill_tree:
        Tax += i[4]

    paystatus = 0
    for i in fill_tree:
        if str(i[7]) == 'NotPaid':
            paystatus += 1

    notice_label2.configure(
        text=f'Search By \n Non Payment \nEst. Amount\nReceivable –${total_cost_for_services} \nPending Payment: {paystatus}')


def get_bill_data_by_date(tree):
    global entry_for_frame3, combo_for_frame3, bill_all_data
    combo_value = entry_for_frame3.get()
    bills = [v for v in bill_all_data]
    pattern = r'^\d{4}-\d{2}-\d{2}$'

    if re.match(pattern, combo_value):
        try:
            fill_tree = [i for i in bills if i[1].strftime("%Y-%m-%d") == combo_value]

            for row in tree.get_children():
                tree.delete(row)

            for result in fill_tree:
                tag = load_treeview_shades(tree,shade2='#E8F4FA')
                tree.insert('',tk.END,values=result,tags=tag)

            total_cost_for_services = 0
            for i in fill_tree:
                total_cost_for_services += i[6]

            Discounts = 0
            for i in fill_tree:
                Discounts += i[6]-i[5]

            Tax = 0
            for i in fill_tree:
                Tax += i[4]

            paystatus = 0
            for i in fill_tree:
                if str(i[7]) == 'NotPaid':
                    paystatus += 1


            notice_label2.configure(
                text=f'Search By {combo_value} \nTaxes ${Tax} \nDiscounts: ${Discounts} \nIncome: ${total_cost_for_services} \nPending Payment: {paystatus}')
        except Exception as e:
            print(e)
            return
    else:
        # print('Only accepts YYYY-MM-DD Format \n Re-Enter date!')
        messagebox.showinfo('Hey','Only accepts YYYY-MM-DD Format \n Re-Enter date!')
        return


def get_service_details(tree1):
    global main_frame,tree1_title
    try:
        conn = connect_to_database()

        cursor = conn.cursor()
        cursor.execute("SELECT Service_Name, Service_Code, Cost, Description, CreatedBy, CreatedDate FROM Services")
        results = cursor.fetchall()

        # Clear the tree before inserting new data
        for row in tree1.get_children():
            tree1.delete(row)


        # Insert results into the tree
        for result in results:
            tag = load_treeview_shades(tree1,shade2='#E8F4FA')
            tree1.insert("", tk.END, values=result,tags=tag)


        formatted_rows =[]
        service_pdf_report = [('Service Name', 'Service Code', 'Cost', 'Description', 'CreateBy', 'CreatedDate')]
        for row in results:
            service_pdf_report.append(row)

        auto_pdf_btn_tree1 = ctk.CTkButton(main_frame, text='Export Service Data as PDF', fg_color='black',
                                           hover_color='black', height=20,
                                           command=lambda: create_pdf_report(heading_name='Service Data',data=service_pdf_report,generated_by=loger,name=loger_username)).place(x=850,
                                                                                                            y=250)

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error inserting data: {err}")


def get_visit_details(tree2):
    global notice_label
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT CONCAT(First_Name,"  ",Last_Name) as Patient_Name, VisitDate,CheckInBy,Name,Clinic_Address
                            FROM PatientVisit
                            JOIN Patient ON PatientVisit.Patient_ID = Patient.USERID
                            join clinic ON Patient.ClinicID = clinic.Clinic_ID;""")
        results = cursor.fetchall()


        # Clear the tree before inserting new data
        for row in tree2.get_children():
            tree2.delete(row)

        # Insert results into the tree
        counter = 0
        for result in results:
            tag = load_treeview_shades(tree2, shade2='#E8F4FA')
            tree2.insert("", tk.END, values=result,tags=tag)
            counter +=1
        global notice_label
        notice_label.configure(text=f'Visit found: {counter}')

        return results

    conn.close()

def get_visit_details_by_date(tree2):
    global visit_all_data
    p_id = patient_id_entry.get()
    pattern = r'^\d{4}-\d{2}-\d{2}$'

    if re.match(pattern,p_id):
        # iterating to get a list
        key_to_visit_data = [i for i in visit_all_data]

        # creating a list of tuples
        fill_tree2 = [v for v in key_to_visit_data if str(v[1])== p_id]

        if not fill_tree2:
            messagebox.showinfo('Hey','No Date Matched',)
            # print('No Date Matched')
        else:
            for row in tree2.get_children():
                tree2.delete(row)

            # Insert results into the tree
            counter = 0
            for result in fill_tree2:
                tag = load_treeview_shades(tree2, shade2='#E8F4FA')
                tree2.insert("", tk.END, values=result,tags=tag)
                counter+=1
            notice_label.configure(text=f'Visit found: {counter}')

        return
    else:
        # print('Only accepts YYYY-MM-DD Format \n Re-Enter date!')
        messagebox.showinfo('Hey','Only accepts YYYY-MM-DD Format \n Re-Enter date!')
        return

def get_visit_by_clinic(tree2):
    global notice_label
    c_name = clinic_entry.get()

    key_to_get_clinic = [i for i in visit_all_data]

    fill_tree2 = [v for v in key_to_get_clinic if str(v[3]) == c_name]

    if not fill_tree2:
        messagebox.showinfo('Hey', 'Please Select Clinic!', )
    else:
        for row in tree2.get_children():
            tree2.delete(row)

        # Insert results into the tree
        counter = 0
        for result in fill_tree2:
            tag = load_treeview_shades(tree2, shade2='#E8F4FA')
            tree2.insert("", tk.END, values=result,tags=tag)
            counter+=1
        notice_label.configure(text=f'Visit found: {counter}')
    return




def single_visit_id_get(tree2):
    global notice_label
    p_id = patient_id_entry.get()
    conn = connect_to_database()
    try:
        cursor = conn.cursor()
        if p_id:
            sql = """SELECT CONCAT(First_Name,"  ",Last_Name) as Patient_Name, VisitDate,CheckInBy,Name,Clinic_Address
                                            FROM Bills
                                            JOIN PatientVisit ON Bills.VisitID = PatientVisit.VisitID
                                            JOIN Patient ON PatientVisit.Patient_ID = Patient.USERID
                                            join clinic ON Patient.ClinicID = clinic.Clinic_ID
                                            Where PatientVisit.Patient_ID = %s;"""
            cursor.execute(sql, (p_id,))
            results = cursor.fetchall()

            # Clear the tree before inserting new data
            for row in tree2.get_children():
                tree2.delete(row)

            # Insert results into the tree
            for result in results:
                tag = load_treeview_shades(tree2,shade2='#E8F4FA')
                tree2.insert("", tk.END, values=result,tags=tag)

        else:
            get_visit_details(tree2)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Fetching data ❌: {err}")

    finally:
        conn.close()

def get_log_details(tree3):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT CONCAT(First_Name ,"   " ,Last_Name) as Staff_Name,LastLogin, STAFF.Role, Name
                            FROM UserLoginLog
                            JOIN STAFF ON UserLoginLog.UserID = STAFF.Staff_ID
                            JOIN clinic ON STAFF.ClinicID = clinic.Clinic_ID;""")
        results = cursor.fetchall()

        # Clear the tree before inserting new data
        for row in tree3.get_children():
            tree3.delete(row)

        # Insert results into the tree
        for result in results:
            tag= load_treeview_shades(tree3,shade2='#E8F4FA')
            tree3.insert("", tk.END, values=result,tags=tag)

        conn.close()
        return results



def sorting_log_data(tree3):
    global display_log_data_count
    # Get the selected filter type and search value
    filter_type = combo_for_frame4.get()
    search_val = log_entry.get().strip().replace(" ", "").lower()
    cli_nic = combo2_frame4.get()
    search_values = ['Search All', 'By Staff', 'By Log Date', 'By Role', 'By Clinic']

    # Clear the treeview before populating it with filtered data
    for row in tree3.get_children():
        tree3.delete(row)

    # Load the alternating row styles


    match_found = False  # Flag to track if any matches are found
    counter = 0
    if filter_type == search_values[0]:  # Search All
        for log in log_data:
            tag = load_treeview_shades(tree3, shade2='#E8F4FA')
            tree3.insert("", tk.END, values=log, tags=tag)
            counter+=1
            match_found = True
            display_log_data_count.place(x=950, y=280)

    elif filter_type == search_values[1]:  # By Staff
        for log in log_data:
            if log[0].replace(" ", "").lower() == search_val:
                tag = load_treeview_shades(tree3, shade2='#E8F4FA')
                tree3.insert("", tk.END, values=log, tags=tag)
                counter += 1
                display_log_data_count.place(x=910, y=280)
                match_found = True

    elif filter_type == search_values[2]:  # By Log Date
        for log in log_data:
            if str(log[1].date()).lower() == search_val:
                tag = load_treeview_shades(tree3, shade2='#E8F4FA')
                tree3.insert("", tk.END, values=log, tags=tag)
                counter += 1
                display_log_data_count.place(x=910, y=280)
                match_found = True

    elif filter_type == search_values[3]:  # By Role
        for log in log_data:
            if log[2].strip().lower() == search_val:
                tag = load_treeview_shades(tree3, shade2='#E8F4FA')
                tree3.insert("", tk.END, values=log, tags=tag)
                counter += 1
                display_log_data_count.place(x=950, y=280)
                match_found = True

    elif filter_type == search_values[4]:  # By Clinic
        for log in log_data:
            if log[3].strip().lower() == cli_nic.lower():
                tag = load_treeview_shades(tree3, shade2='#E8F4FA')
                tree3.insert("", tk.END, values=log, tags=tag)
                counter += 1
                display_log_data_count.place(x=900, y=280)
                match_found = True

    if not match_found:  # If no results match the criteria
        messagebox.showinfo("No Results", "No records found matching the search criteria.")

    print(f"Filtered log data for '{filter_type}' with value '{search_val}'.")
    display_log_data_count.configure(text=f'{filter_type} \n{log_entry.get() or combo2_frame4.get()} \nCount: {counter} ')









def get_patient_details(tree4):
    try:
        conn = connect_to_database()

        cursor = conn.cursor()
        cursor.execute("""SELECT USERID, CONCAT(First_Name ,"  ", Last_Name) as Patient_Name,Age,PhoneNumber,
                            Emergency_Contact_Name,Emergency_Contact,Address, Name
                            FROM Patient
                            JOIN clinic ON Patient.ClinicID = clinic.Clinic_ID;""")
        results = cursor.fetchall()

        # Clear the tree before inserting new data
        for row in tree4.get_children():
            tree4.delete(row)

        # Insert results into the tree
        for result in results:
            tag = load_treeview_shades(tree4, shade2='#E8F4FA')
            tree4.insert("", tk.END, values=result, tags=tag)

        conn.close()
        p_rec_count.configure(text=f" Patient Records: {len(results)} ")

        clinic_names = [patient[-1] for patient in results]

        # Count occurrences of each clinic
        clinic_counts = Counter(clinic_names)

        # Print results
        row_index = 1
        for clinic, count in clinic_counts.items():
            # print(f"{clinic}: {count} patients")
            tk.Label(clinic_frame, text=f"{clinic} \nPatient Records {count}",
                     font=("Gabriola", 12), background='azure').grid(row=row_index, column=0, padx=10 )
            row_index +=2

        return []

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error inserting data: {err}")

# Dashboard window setup
global log_data,combo2_frame4
def create_dashboard():
    global p_rec_count,visit_all_data,clinic_frame,bill_all_data,names_of_clinics,main_frame,tree1_title,log_data, main_frame4,display_log_data_count
    dashboard_window = ctk.CTk()
    dashboard_window.title("Clinic Report Dashboard")
    dashboard_window.focus_force()
    dashboard_window.geometry("1300x900")
    dashboard_window.iconphoto(True, resize_image((90, 90), 'images/HSMS.png'))
    # dashboard_window.attributes("-fullscreen", True)
    # dashboard_window.bind('<Escape>', lambda e: dashboard_window.attributes("-fullscreen", False))

    # Center-aligning the window on the screen
    window_width = 1500
    window_height = 900
    screen_width = dashboard_window.winfo_screenwidth()
    screen_height = dashboard_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    dashboard_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    time_label = tk.Label(dashboard_window, font=("Gabriola", 14), fg="blue")
    time_label.grid(row=0, column=0, sticky='n')
    update_time(time_label)

    # ------Frames-section--------
    global main_frame2
    # Frame for clinic Distribution Chart
    main_frame = ctk.CTkFrame(dashboard_window, width=1250, height=750)
    main_frame.place(x=200, y=80)
    main_frame2 = ctk.CTkFrame(dashboard_window, width=1250, height=750, )
    main_frame2.place(x=200, y=80)
    main_frame3 = ctk.CTkFrame(dashboard_window, width=1250, height=750, )
    main_frame3.place(x=200, y=80)
    main_frame4 = ctk.CTkFrame(dashboard_window, width=1250, height=750, )
    main_frame4.place(x=200, y=80)
    main_frame5 = ctk.CTkFrame(dashboard_window, width=1250, height=750, )
    main_frame5.place(x=200, y=80)

    for frame in (main_frame, main_frame2,main_frame3,main_frame4,main_frame5):
        frame.grid_propagate(False)

    main_frame.tkraise()
    # Frame for service tree view
    service_frame = ctk.CTkFrame(main_frame,)
    service_frame.place(x=10, y=20)
    # Frame for clinic Distribution Chart
    clinic_patient_count_frame = ctk.CTkLabel(main_frame, font=("Gabriola", 14))
    clinic_patient_count_frame.place(x=10, y=280)
    # Frame for billing cost center
    bill_cost_frame = ctk.CTkFrame(main_frame, fg_color="azure", width=300, height=500)
    bill_cost_frame.place(x=975, y=440)
    # Frame for clinic details
    clinic_frame = ctk.CTkFrame(main_frame, fg_color="azure", width=500)
    clinic_frame.place(x=740, y=300)
    # Frame for reports
    report_frame = ctk.CTkFrame(main_frame, fg_color="azure")
    report_frame.place(x=980, y=280)
    # bar chart frame and def call for visit count
    visit_bar_frame=ctk.CTkFrame(main_frame2, width=600,height=400, border_width=10)
    visit_bar_frame.place(x=10, y=240)
    create_bar_chart(visit_bar_frame)
    # frame for visit count
    visit_count_frame = ctk.CTkFrame(main_frame2, width=300, height=300, fg_color='gray99')
    visit_count_frame.place(x=620, y=300)
    # bar chart frame and def call for bill sum
    sum_income_bar_frame = ctk.CTkFrame(main_frame3, width=600, height=400, border_width=10)
    sum_income_bar_frame.place(x=10, y=280)
    create_bar_chart_sum_income(sum_income_bar_frame)
    #frame for exact amount
    sum_exact_amount_frame = ctk.CTkFrame(main_frame3, width=300, height=300, fg_color='gray99')
    sum_exact_amount_frame.place(x=615, y=320)

    sum_tax_amount_frame = ctk.CTkFrame(main_frame3, width=300, height=300, fg_color='gray99')
    sum_tax_amount_frame.place(x=825, y=320)

    sum_paymenttype_frame = ctk.CTkFrame(main_frame3, width=300, height=300, fg_color='gray99')
    sum_paymenttype_frame.place(x=1035, y=320)




    # ----Left-Nav-Button-and-labels------
    tk.Label(dashboard_window,text="Health Stream Management System",font=Style.page_heading_genova,foreground=Style.page_heading_color).place(x=470, y=20)
    bt1_image = resize_image((50, 50), 'images/clinic-report.png')  # Adjusted to return PhotoImage
    Button1 = ctk.CTkButton(dashboard_window, text="Clinic \n Report", image=bt1_image, fg_color='#ECECEC',text_color='black',hover_color='#ECECEC',width=160, height=100, corner_radius=10, command=lambda: show_frame(main_frame))
    Button1.place(x=20, y=120)
    bt2_image = resize_image((50, 50), 'images/visit-report.png')  # Adjusted to return PhotoImage
    Button2 = ctk.CTkButton(dashboard_window, text="Visit \n Report", width=160, image=bt2_image,fg_color='#ECECEC',hover_color='#ECECEC',text_color='black', height=100, corner_radius=10,command=lambda: show_frame(main_frame2))
    Button2.place(x=20, y=240)
    bt3_image = resize_image((50, 50), 'images/billing-report.png')  # Adjusted to return PhotoImage
    Button3 = ctk.CTkButton(dashboard_window, text="Billing \n Report",image=bt3_image, width=160,fg_color='#ECECEC',text_color='black',hover_color='#ECECEC', height=100, corner_radius=10,command=lambda: show_frame(main_frame3))
    Button3.place(x=20, y=360)
    bt4_image = resize_image((50, 50), 'images/log-report.png')  # Adjusted to return PhotoImage
    Button4 = ctk.CTkButton(dashboard_window, text="Log \n Report",image=bt4_image, width=160, height=100,fg_color='#ECECEC',text_color='black',hover_color='#ECECEC', corner_radius=10,command=lambda: show_frame(main_frame4))
    Button4.place(x=20, y=480)
    bt5_image = resize_image((50, 50), 'images/patient-report.png')  # Adjusted to return PhotoImage
    Button5 = ctk.CTkButton(dashboard_window, text="Patient \n Report", image=bt5_image, width=160, height=100,fg_color='#ECECEC',text_color='black',hover_color='#ECECEC', corner_radius=10,command=lambda: show_frame(main_frame5))
    Button5.place(x=20, y=600)
    log_search_image = resize_image((400,400),'images/file_search3.png')
    ctk.CTkLabel(main_frame4, text='', image=log_search_image).place(x=840,y=30)
    footer1_image = resize_image((1250, 100), 'images/footer1.png')
    ctk.CTkLabel(main_frame2, text='', image=footer1_image).place(x=0, y=650)
    visit_image = resize_image((390, 400), 'images/visit1.jpg')
    ctk.CTkLabel(main_frame2, text='', image=visit_image).place(x=850, y=240)
    footer2_image = resize_image((1240, 75), 'images/footer1.png')
    ctk.CTkLabel(main_frame3, text='', image=footer2_image).place(x=5, y=680)


    # Frame for billing tree view
    # billing_frame = tk.LabelFrame(main_frame, text="Billing Details Records", font=("Gabriola", 14))
    # billing_frame.grid(row=0, column=0, padx=(20, 0), pady=(10, 0))


    # plot_billing_distribution(billing_frame)

# Data on report_frame report
    ctk.CTkLabel(report_frame, text="Total Clinics Record Count", font=("Gabriola", 18,'bold'), text_color='darkblue').grid(row=0,column=0,padx=10, pady=10)
    p_rec_count = tk.Label(report_frame, text='', font=("Gabriola", 12), background='azure')
    p_rec_count.grid(row=1, column=0, padx=10, pady=5)
    sum_of_visit = 0
    for x in fetch_visit_count_data():
        sum_of_visit += x[1]
    print(fetch_visit_count_data())
    ctk.CTkLabel(report_frame, text=f" Visits made: {sum_of_visit} ", font=("Gabriola", 12)).grid(row=2, column=0, padx=10, pady=5)
    global pending_on_frame1
    pending_on_frame1 = ctk.CTkLabel(report_frame, text=" Pending Payment: X ", font=("Gabriola", 12))
    pending_on_frame1.grid(row=3, column=0, padx=10, pady=5)




# visit report section on frame
    visit_date = fetch_visit_count_data()
    row_index = 2
    for row in visit_date:
        # print(f"{row[0]}: {row[1]} visits")
        tk.Label(clinic_frame, text=f"Visit Records {row[1]}",
                 font=("Gabriola", 12), background='azure').grid(row=row_index, column=0, sticky='n', pady=(0, 10))
        row_index += 2

    tk.Label(clinic_frame, text=" Break Down By Clinics ", font=("Gabriola", 18, 'bold'), background='azure').grid(row=0,column=0,padx=10, pady=10)


# cost breakdown details
    clinic_amount = fetch_bill_sum_data()
    row_index = 1
    ctk.CTkLabel(bill_cost_frame, text='Total Revenue Break Down', font=("Gabriola", 18, 'bold'),
              text_color='darkblue').grid(row=0, column=0, padx=10, pady=(5, 0))
    for row in clinic_amount:
        ctk.CTkLabel(bill_cost_frame, text=f'{row[0]} \n $ {row[2]}', font=("Gabriola", 12, 'bold'),
                 ).grid(
            row=row_index, column=0, padx=10, pady=(2, 12))
        row_index += 1





# -------Preview-for-services-----------#
    columns = ('Service Name', 'Service Code', 'Cost', 'Description', 'CreateBy', 'CreatedDate')
    tree1 = ttk.Treeview(service_frame, columns=columns, show="headings")
    tree1.heading("Service Name", text="Service Name", command=lambda: sort_column(tree1, "Service Name", False))
    tree1.heading("Service Code", text="Service Code", command=lambda: sort_column(tree1, "Service Code", False))
    tree1.heading("Cost", text="Cost", command=lambda: sort_column(tree1, "Cost", False))
    tree1.heading("Description", text="Description", command=lambda: sort_column(tree1, "Description", False))
    tree1.heading("CreateBy", text="CreateBy", command=lambda: sort_column(tree1, "CreateBy", False))
    tree1.heading("CreatedDate", text="CreatedDate", command=lambda: sort_column(tree1, "CreatedDate", False))
    tree1.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
    for i in columns:
        tree1.column(f'{i}', anchor='center')
    tree1_title = 'Services Data'
    ctk.CTkButton(main_frame,text='Export Service Data as xl',fg_color='black',hover_color='black',height=20,command=lambda: export_tree_to_excel(tree1,tree1_title)).place(x=1050,y=250)


# Treeview for displaying Visits records
    columns = ("Patient_Name", "VisitDate","CheckInBy","Clinic_Name","Clinic_Address")
    tree2 = ttk.Treeview(main_frame2, columns=columns, show="headings")
    tree2.heading("Patient_Name", text="Patient_Name", command=lambda: sort_column(tree2, "Patient_Name", False))
    tree2.heading("VisitDate", text="VisitDate", command=lambda: sort_column(tree2, "VisitDate", False))
    tree2.heading("CheckInBy", text="CheckInBy", command=lambda: sort_column(tree2, "CheckInBy", False))
    tree2.heading("Clinic_Name", text="Clinic_Name", command=lambda: sort_column(tree2, "Clinic_Name", False))
    tree2.heading("Clinic_Address", text="Clinic_Address", command=lambda: sort_column(tree2, "Clinic_Address", False))
    tree2.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")


    for i in columns:
        tree2.column(f'{i}', anchor='center')
    tree2_title = 'Patient Visit Data'

    def t2_pdf_report(tree2):
        t2_items_to_pdf = [["Patient_Name", "VisitDate","CheckInBy","Clinic_Name","Clinic_Address"]]
        for item in tree2.get_children():
            item_data = tree2.item(item)  # Get item data
            t2_items_to_pdf.append(item_data['values'])
        create_pdf_report(heading_name=tree2_title, data=t2_items_to_pdf,generated_by=loger, name=loger_username)
        print(t2_items_to_pdf)

    ctk.CTkButton(main_frame2, text='Export Patient Visit xml',fg_color='black',hover_color='black',height=20,command=lambda: export_tree_to_excel(tree2, tree2_title)).place(x=650, y=240)
    ctk.CTkButton(main_frame2, text='Export Patient Visit PDF',fg_color='black',hover_color='black',height=20,command=lambda: t2_pdf_report(tree2)).place(x=650, y=270)




    ## Treeview for displaying bills records
    columns = ("Name", "BillDate", "Services",  "TotalCost","Tax","Subtotal","Netpay", "PaymentType")
    tree = ttk.Treeview(main_frame3, columns=columns, show="headings",height=12)
    tree.heading("Name", text="Name", command=lambda: sort_column(tree, "Name", False))
    tree.heading("BillDate", text="Bill Date", command=lambda: sort_column(tree, "BillDate", False))
    tree.heading("Services", text="Services", command=lambda: sort_column(tree, "Services", False))
    tree.heading("TotalCost", text="Total Cost", command=lambda: sort_column(tree, "TotalCost", False))
    tree.heading("Tax", text="Tax", command=lambda: sort_column(tree, "Tax", False))
    tree.heading("Subtotal", text="Sub-total", command=lambda: sort_column(tree, "Subtotal", False))
    tree.heading("Netpay", text="Net pay", command=lambda: sort_column(tree, "Netpay", False))
    tree.heading("PaymentType", text="Payment Type", command=lambda: sort_column(tree, "PaymentType", False))
    tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
    tree_title = 'All Bill Records'
    ctk.CTkButton(main_frame3, text='Export Bill Data as xl', fg_color='black',font=('',10,'normal'), hover_color='black', height=10,
                  command=lambda: export_tree_to_excel(tree, tree_title)).place(x=880, y=260)
    def t_pdf_report(tree):
        global notice_label2
        t_items_to_pdf = [["Name", "BillDate", "Services",  "TotalCost","Tax","Subtotal","Netpay", "PaymentType"]]
        for item in tree.get_children():
            item_data = tree.item(item)  # Get item data
            values = item_data['values']  # Extract values of the item
            t_items_to_pdf.append(values[:8])
        get_text_labels = notice_label2.cget('text')
        new_labels = get_text_labels.split('\n')
        print(new_labels)
        create_pdf_report(heading_name=tree_title, data=t_items_to_pdf, other_labels=new_labels,generated_by=loger,name=loger_username)
        # print(t_items_to_pdf)
    ctk.CTkButton(main_frame3, text='Export Bill Data as PDF', fg_color='black',font=('',10,'normal'), hover_color='black', height=10,
                  command=lambda: t_pdf_report(tree)).place(x=730, y=260)




# -------Preview-for-Logs-----------#
    columns = ("Staff_Name","LastLogin", "Role", "Clinic Name")
    tree3 = ttk.Treeview(main_frame4, columns=columns, show="headings", height=38)
    tree3.heading("Staff_Name", text="Staff_Name", command=lambda: sort_column(tree3, "Staff_Name", False))
    tree3.heading("LastLogin", text="LastLogin", command=lambda: sort_column(tree3, "LastLogin", False))
    tree3.heading("Role", text="Role", command=lambda: sort_column(tree3, "Role", False))
    tree3.heading("Clinic Name", text="Clinic Name", command=lambda: sort_column(tree3, "Clinic Name", False))
    tree3.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
    for i in columns:
        tree3.column(f'{i}', anchor='center')
    tree3_title = 'Log History'
    ctk.CTkButton(main_frame4, text='Export Log Record to XL', fg_color='black', hover_color='black', height=25,
                  command=lambda: export_tree_to_excel(tree3, tree3_title)).place(x=870, y=705)
    def t3_pdf_report(tree3):
        global notice_label2
        t3_items_to_pdf = [["Staff_Name","LastLogin", "Role", "Clinic Name"]]
        for item in tree3.get_children():
            item_data = tree3.item(item)  # Get item data
            values = item_data['values']  # Extract values of the item
            t3_items_to_pdf.append(values[:8])
        get_text_labels = display_log_data_count.cget('text')
        new_labels = get_text_labels.split('\n')
        print(new_labels)
        create_pdf_report(heading_name=tree3_title, data=t3_items_to_pdf, other_labels=new_labels,generated_by=loger, name=loger_username)
        # print(t_items_to_pdf)
    ctk.CTkButton(main_frame4, text='Export Log Record to PDF', fg_color='black', hover_color='black', height=25,
                  command=lambda: t3_pdf_report(tree3)).place(x=950, y=665)


# -------Preview-for-Patient-----------#
    columns = ("PatientID","Patient Name","Age","Phone Number","Emergency Person","Emergency Contact","Address", "Clinic Name")
    tree4 = ttk.Treeview(main_frame5, columns=columns, show="headings",height=35,)
    tree4.heading("PatientID", text="PatientID", command=lambda: sort_column(tree4, "PatientID", False))
    tree4.heading("Patient Name", text="Patient Name", command=lambda: sort_column(tree4, "Patient Name", False))
    tree4.heading("Age", text="Age", command=lambda: sort_column(tree4, "Age", False))
    tree4.heading("Phone Number", text="Phone Number", command=lambda: sort_column(tree4, "Phone Number", False))
    tree4.heading("Emergency Person", text="Emergency Person", command=lambda: sort_column(tree4, "Emergency Person", False))
    tree4.heading("Address", text="Address", command=lambda: sort_column(tree4, "Address", False))
    tree4.heading("Clinic Name", text="Clinic Name", command=lambda: sort_column(tree4, "Clinic Name", False))
    tree4.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
    for ci in columns:
        tree4.column(ci,width=153,anchor='center')

    tree4_title = 'Patiend Records'
    ctk.CTkButton(main_frame5, text='Export Patient Record to XL', fg_color='black', hover_color='black',
                  command=lambda: export_tree_to_excel(tree4, tree4_title)).place(x=840, y=700)

    def t4_pdf_report(tree4):
        global notice_label2
        t4_items_to_pdf = [["PatientID","Patient Name","Age","Phone Number","Emergency Person","Emergency Contact","Address", "Clinic Name"]]
        for item in tree4.get_children():
            item_data = tree4.item(item)  # Get item data
            values = item_data['values']  # Extract values of the item
            t4_items_to_pdf.append(values[:8])
        get_text_labels = display_log_data_count.cget('text')
        new_labels = get_text_labels.split('\n')
        print(new_labels)
        create_pdf_report(heading_name=tree4_title, data=t4_items_to_pdf, other_labels=None, pg_size='landscape', generated_by=loger, name=loger_username)

    ctk.CTkButton(main_frame5, text='Export Patient Record to PDF', fg_color='black', hover_color='black',
                  command=lambda: t4_pdf_report(tree4)).place(x=640, y=700)





# -------Exact-amount-data-in-frame-3-----------#
    clinic_amount = fetch_bill_sum_data()
    row_index = 1
    tk.Label(sum_exact_amount_frame, text='Income By Clinic', font=("Geneva", 16, 'bold'),
             background='gray99',foreground='darkblue').grid(row=0, column=0, padx=10, pady=(5,0))
    for row in clinic_amount:
        tk.Label(sum_exact_amount_frame, text=f'{row[0]} \n $ {row[2]}', font=("Geneva", 12, 'bold'),background='gray99').grid(
            row=row_index, column=0, padx=10, pady=(2,12))
        row_index +=1

    tk.Label(sum_tax_amount_frame, text='Taxes By Clinic', font=("Geneva", 16, 'bold'),
             background='gray99', foreground='darkblue').grid(row=0, column=0, padx=10, pady=(5, 0))
    for row in clinic_amount:
        tk.Label(sum_tax_amount_frame, text=f'{row[0]} \n $ {row[3]}', font=("Geneva", 12, 'bold'),
                 background='gray99').grid(
            row=row_index, column=0, padx=10, pady=(2, 12))
        row_index += 1


    tk.Label(sum_paymenttype_frame, text='Payment Status', font=("Geneva", 16, 'bold'),
             background='gray99', foreground='darkblue').grid(row=0, column=0, padx=10, pady=(5, 0))
    for row in clinic_amount:
        tk.Label(sum_paymenttype_frame, text=f'{row[0]} \nPending Payment: {row[5]}', font=("Geneva", 12, 'bold'),
                 background='gray99').grid(
            row=row_index, column=0, padx=10, pady=(2, 12))
        row_index += 1



    # -------Visit-count-by-clinics-----------#
    def visit_count_to_frame():

        row_index = 1
        visits = fetch_visit_count_data()

        tk.Label(visit_count_frame, text='Visits Count By Clinic', font=("Geneva", 18, 'bold'),
                 background='gray99', foreground='darkblue').grid(row=0, column=0, padx=10, pady=(5, 0))
        global visit_all_data
        City = 0
        Downtown = 0
        Westside=0
        East=0
        Northview=0
        global names_of_clinics
        print(names_of_clinics)
        for row in visit_all_data:
            if row[3] == names_of_clinics[0]:
                City +=1
            elif row[3] == names_of_clinics[1]:
                Westside +=1
            elif row[3] == names_of_clinics[2]:
                Downtown+=1
            elif row[3] == names_of_clinics[3]:
                East+=1
            elif row[3] == names_of_clinics[4]:
                Northview+=1
                break
        item_to_display = [(City,names_of_clinics[0]),(Downtown,names_of_clinics[2]),(Westside,names_of_clinics[1]),
                           (East,names_of_clinics[3]),(Northview,names_of_clinics[4])]

        for i in item_to_display:
            tk.Label(visit_count_frame, text=f'{i[1]} \n Number of Visits {i[0]}', font=("Geneva", 14, 'bold'),
                     background='gray99').grid(
                row=row_index, column=0, padx=10, pady=(2, 12))
            row_index += 1






    global patient_id_entry,clinic_entry,entry_for_frame3,combo_for_frame3,names_of_clinics
#-----------Entry fields--------
    patient_id_entry = ctk.CTkEntry(main_frame2, placeholder_text='Enter 🔦', width=100)
    patient_id_entry.place(x=1020, y=10)

    names_of_clinics = ['City Health Clinic','Westside Community Clinic','Downtown Medical Center','East End Health Services','Northview Family Clinic']
    clinic_entry = ctk.CTkComboBox(main_frame2, values=names_of_clinics, width=225,state='readonly')
    clinic_entry.place(x=1020, y=70)
    clinic_entry.set('Select Clinic')

    # for frame 3
    entry_for_frame3 = ctk.CTkEntry(main_frame3, placeholder_text='Enter 🔦', width=100)
    entry_for_frame3.place(x=1025, y=10)

    combo_for_frame3 = ctk.CTkComboBox(main_frame3, values=names_of_clinics, width=220,state='readonly')
    combo_for_frame3.place(x=1025, y=70)
    combo_for_frame3.set('Select Clinic')
    combo_for_frame3.bind('<<Button-1>>',lambda: get_visit_by_clinic(tree2))
    combo_for_frame3.bind('<<ComboboxSelected>>', lambda: get_visit_by_clinic(tree2))
    combo_for_frame3.bind('<FocusOut>', lambda : get_visit_by_clinic(tree2))
    combo_for_frame3.bind('<Return>', lambda : get_visit_by_clinic(tree2))

    search_label__ = ctk.CTkLabel(main_frame4, text='', font=Style.page_heading_geneva2)
    search_label__.place(x=1000, y=450)

    global combo_for_frame4, log_entry,combo2_frame4
    search_values = ['Search All', 'By Staff', 'By Log Date', 'By Role', 'By Clinic']

    combo_for_frame4 = ttk.Combobox(main_frame4, values=search_values, width=17, state='readonly')
    combo_for_frame4.place(x=995, y=430)
    combo_for_frame4.set('Search All')

    combo2_frame4 = ctk.CTkComboBox(main_frame4, values=names_of_clinics, width=150, state='readonly')

    log_entry = ctk.CTkEntry(main_frame4)
    log_entry.place(x=890, y=490)

    def activate_combobox(event):
        cbox = combo_for_frame4.get()
        print(cbox)
        log_entry.delete(0,tk.END)
        combo2_frame4.place_forget()
        # Conditional logic based on the selected value
        if cbox == search_values[0]:  # "Search All"
            search_label__.configure(text='Search All')
            # Hide or destroy any other widgets if necessary
            print('1')
        elif cbox == search_values[1]:  # "By Staff"
            search_label__.configure(text='Enter Staff Name')
            print('2')
        elif cbox == search_values[2]:  # "By Log Date"
            search_label__.configure(text='📅YYYY-MM-DD')
            print('3')
        elif cbox == search_values[3]:  # "By Role"
            search_label__.configure(text='Enter Role')
            print('4')
        elif cbox == search_values[4]:  # "By Clinic"
            search_label__.configure(text='Select Clinic')
            combo2_frame4.place(x=890, y=490)
            combo2_frame4.tkraise()
        else:
            print('No value to search')



    # combo_for_frame4.bind('<<Button-1>>', activate_combobox)
    # Correct event binding
    combo_for_frame4.bind('<<ComboboxSelected>>', activate_combobox)
    # combo_for_frame4.bind('<<ComboboxSelected>>',lambda : activate_combobox)
    # combo_for_frame4.bind('<FocusOut>', activate_combobox)
    # combo_for_frame4.bind('<Return>', activate_combobox)






# ------------------Labels-------area
    global notice_label, display_log_data_count,notice_label2
    notice_label = ctk.CTkLabel(main_frame2, text_color='blue', text='', font=('Geneva', 30, 'normal'))
    notice_label.place(x=1020, y=150)

    notice_label2 = ctk.CTkLabel(main_frame3, text_color='blue', text='', font=('Geneva', 15, 'normal'))
    notice_label2.place(x=1050, y=150)

    ctk.CTkLabel(main_frame4,text='Select Filter:', font=Style.page_heading_geneva2).place(x=895, y=427)

    ctk.CTkLabel(main_frame4, text='LOG RECORDS 🗂️ ', font=Style.page_heading_genova, text_color='black').place(x=910, y=10)
    ctk.CTkLabel(main_frame4, text='All Records Count ', font=Style.page_heading_genova, text_color='black').place(x=900, y=55)
    display_log_data_count = ctk.CTkLabel(main_frame4, text='', font=('geneva',14,'bold'), text_color='blue')
    display_log_data_count.place(x=920, y=280)




#-------Buttons------Buttons-------Buttons`
    btn_get_id = ctk.CTkButton(main_frame2, text='Search by ID 🔍', width=100, hover_color='black', fg_color='black',
                               command=lambda: single_visit_id_get(tree2))
    btn_get_id.place(x=1130, y=10)
    ctk.CTkButton(main_frame2, text=' Date 🔍', width=115, fg_color='black', hover_color='black',
                               command=lambda: get_visit_details_by_date(tree2)).place(x=1130, y=40)

    ctk.CTkButton(main_frame2, text='By Clinic 🔍', width=115, fg_color='black', hover_color='black',
                               command=lambda: get_visit_by_clinic(tree2)).place(x=1130, y=100)

    patient_id_entry.bind('<Return>', lambda event: single_visit_id_get(tree2))


    #frame 3
    ctk.CTkButton(main_frame3, text='Search by ID 🔍', width=100, hover_color='black', fg_color='black',
                               command=lambda: get_bill_data_by_id(tree)).place(x=1130, y=10)

    ctk.CTkButton(main_frame3, text=' Date 🔍', width=115, fg_color='black', hover_color='black',
                  command=lambda: get_bill_data_by_date(tree)).place(x=1130, y=40)

    ctk.CTkButton(main_frame3, text='By Clinic 🔍', width=115, fg_color='black', hover_color='black',
                  command=lambda: get_bill_data_by_clinic(tree)).place(x=1130, y=100)

    ctk.CTkButton(main_frame3, text='Non Paid 🔍', width=100, fg_color='black', hover_color='black',
                  command=lambda: get_bill_data_non_paid(tree)).place(x=1025, y=100)


    print_image = resize_image((20, 20), 'images/printer.png')  # Adjusted to return PhotoImage
    bt_print = ctk.CTkButton(main_frame, text='Print', image=print_image,fg_color='black',
                             command=lambda: print_card(main_frame,file_name='dashboard_1')).place(x=1050, y=700)
    print_image = resize_image((20, 20), 'images/printer.png')  # Adjusted to return PhotoImage
    bt_print = ctk.CTkButton(main_frame2, text='Print', image=print_image,fg_color='black',
                             command=lambda: print_card(main_frame2,file_name='dashboard_2')).place(x=1050, y=700)
    print_image = resize_image((20, 20), 'images/printer.png')  # Adjusted to return PhotoImage
    bt_print = ctk.CTkButton(main_frame3, text='Print', image=print_image,fg_color='black',
                             command=lambda: print_card(main_frame3,file_name='dashboard_3')).place(x=1050, y=700)
    print_image = resize_image((20, 20), 'images/printer.png')  # Adjusted to return PhotoImage
    bt_print = ctk.CTkButton(main_frame4, text='Print', image=print_image,fg_color='black',
                             command=lambda: print_card(main_frame4,file_name='dashboard_4')).place(x=1050, y=700)
    print_image = resize_image((20, 20), 'images/printer.png')  # Adjusted to return PhotoImage
    bt_print = ctk.CTkButton(main_frame5, text='Print', image=print_image,fg_color='black',
                             command=lambda: print_card(main_frame5,file_name='dashboard_5')).place(x=1050, y=700)

    # Refresh Button to update the dashboard
    refresh_button = tk.Button(dashboard_window, text="Refresh Data", font=("Gabriola", 12),
                               command=lambda: refresh_data())
    refresh_button.place(x=1300,y=850)

    btn_log_search = ctk.CTkButton(main_frame4,text='🔍 Search', fg_color='black',hover_color='black', command=lambda: sorting_log_data(tree3))
    btn_log_search.place(x=1055, y=490)


# -------Buttons------Buttons-------Buttons


# ---------Calling------functions------area

    bill_all_data = get_billing_details(tree)
    get_service_details(tree1)
    visit_all_data = get_visit_details(tree2)
    log_data = get_log_details(tree3)
    get_patient_details(tree4)
    # Call functions to plot charts and data
    plot_clinic_distribution(clinic_patient_count_frame)
    visit_count_to_frame()
# ---------Calling------functions------area


#---Configuring row and column weights for resizing
    dashboard_window.grid_rowconfigure(2, weight=1)
    dashboard_window.grid_rowconfigure(3, weight=1)
    dashboard_window.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    tree.column('Name',width=200,anchor='center')
    tree.column('TotalCost',width=100,anchor='center')
    tree.column('BillDate',width=100,anchor='center')
    tree.column('Tax',width=100,anchor='center')
    tree.column('Subtotal',width=100,anchor='center')
    tree.column('Netpay',width=100,anchor='center')
    tree.column('PaymentType',width=110,anchor='center')

    def refresh_data():
        bill_all_data = get_billing_details(tree)
        get_service_details(tree1)
        visit_all_data = get_visit_details(tree2)
        log_data = get_log_details(tree3)
        get_patient_details(tree4)
        # Call functions to plot charts and data
        plot_clinic_distribution(clinic_patient_count_frame)
        visit_count_to_frame()





    dashboard_window.mainloop()


# Run the dashboard
create_dashboard()
