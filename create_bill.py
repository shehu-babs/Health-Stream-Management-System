import subprocess
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation
from datetime import datetime
from customtkinter import CTkEntry
from numpy.ma.core import subtract
from reportlab.lib.colors import yellow
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from operation import  fetch_patient_bill_history, Style, generate_pdf,show_notification,show_frame,auto_pdf
# from search_patient import patient_id


# from search_patient import patient_id


def close_out():
    # messagebox.showwarning('Close','Doy you want to close out')
    root.destroy()

def pop_data():
    pid = id_entry.get()
    date = dated.get()
    if not all([pid,date]):
        messagebox.showinfo('Entry Error','🚫\n Enter Patient ID and Date')
        return
    details = fetch_patient_bill_history(pid,date)

    list_detail = []
    for row in details:
        for item in row:
            list_detail.append(item)

    print(details)
    print(list_detail)

    global patient_name
    global cost
    global paddress
    global pservices
    global checkby
    global patient_idd
    global ncost
    global billid
    global bill_title
    global clinicname
    global clinicaddress
    global visitid
    global visitdate
    global cost_value
    global phone_number
    global net_due
    global ppp_id
    global bill_idd
    ppp_id =   f'{list_detail[1]}'
    bill_idd = f'{list_detail[14]}'


    cost_value = list_detail[15]

    bill_title = 'Patient Bill'
    patient_name = f'Patient Name: {list_detail[7]} {list_detail[8]}'
    cost = f'Total Cost of Service: ${list_detail[15]}'
    paddress = f'Address: {list_detail[9].strip()}'
    pservices = f'Services Charged: {list_detail[4]}'
    billid = f'BILL ID: #00{list_detail[14]}'
    checkby = f'Checked In By: {list_detail[6]}'
    patient_idd = f'Patient ID: {list_detail[1]}'
    ncost = f'Net Payment Due: ${list_detail[17]}'
    clinicname = f'Clinic Name: {list_detail[12]}'
    clinicaddress = f'Clinic Address: {list_detail[13]}'
    visitid = f'Visit ID: #VS00{list_detail[0]}'
    visitdate = f'Visit Date: {list_detail[2]}'
    phone_number = f'Phone Number: {list_detail[11]}'

    bill_id.configure(text=f'BILL ID: #00{list_detail[14]}')
    bill_date.configure(text=f'Bill Date: {list_detail[16]}')
    check_by.configure(text=f'Checked In By: {list_detail[6]}')
    check_by2.configure(text=f'Checked In By: {list_detail[6]}')
    p_id.configure(text=f'Patient ID: {list_detail[1]}')
    p_name.configure(text=f'Name: {list_detail[7]} {list_detail[8]}')
    p_address.configure(text=f'Address: {list_detail[9]}')
    p_phone.configure(text=f'Phone Number: {list_detail[11]}')
    c_name.configure(text=f'Clinic Name: {list_detail[12]}')
    c_address.configure(text=f'Clinic Address: {list_detail[13]}')
    c_visitdate.configure(text=f'Visit Date: {list_detail[2]}')
    p_visitid.configure(text=f'Visit ID: #VS00{list_detail[0]}')
    p_services.configure(text=f'Service Provided {list_detail[4]}')
    p_netpay.configure(text=ncost)



    bill_data()



global currentdate
now = datetime.now()
currentdate = now.date()

# Tkinter window setup
root = ctk.CTk()
root.title("Billing System")
root.geometry('700x500')
root.resizable(False,False)
root.focus_force()
# Center the entire window on the screen
window_width = 700
window_height = 580
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# bill_data = []
#
# for row in fetch_patient_bill_history():
#     for item in row:
#         bill_data.append(item)
#
#
# print(bill_data[2])
mainframe = ctk.CTkFrame(root, 600,460, fg_color="gray85")
mainframe.place(x=50 , y=60)
frame2 = ctk.CTkFrame(root, 600,460, fg_color="gray97")
frame2.place(x=50 , y=60)
patient_info = ctk.CTkFrame(mainframe, width=500, height=120, fg_color='gray93')
patient_info.place(x=50, y=80)
clinic_info = ctk.CTkFrame(mainframe, width=500, height=120, fg_color='gray93')
clinic_info.place(x=50, y=205)
visit_info = ctk.CTkFrame(mainframe, width=500, height=120, fg_color='gray93')
visit_info.place(x=50, y=330)

ctk.CTkLabel(root,text='Enter Patient ID Number', font=Style.page_heading_geneva2).place(x=60,y=10)
id_entry = ctk.CTkEntry(root,placeholder_text='Enter Patient ID', placeholder_text_color='black')
id_entry.place(x=250,y=10)
dated = ctk.CTkEntry(root,placeholder_text='📆YYYY-MM-DD', placeholder_text_color='black')
dated.place(x=395,y=10)
get_id_data = ctk.CTkButton(root,text='🧾Get Info',text_color='black', hover_color='red',fg_color='gray60', command=pop_data).place(x=540,y=10)

ctk.CTkLabel(mainframe, text='Patient Bill', font=Style.page_heading).place(x=230, y=5)
bill_id = ctk.CTkLabel(mainframe, text='Bill #', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
bill_id.place(x=20, y=1)
bill_date = ctk.CTkLabel(mainframe, text='Bill YYYY-MM-DD', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
bill_date.place(x=20, y=25)
check_by = ctk.CTkLabel(mainframe, text='Checked In By:', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
check_by.place(x=20, y=45)

p_id = ctk.CTkLabel(patient_info, text='Patient ID #',font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
p_id.place(x=20, y=1)
p_name = ctk.CTkLabel(patient_info, text='Patient Name', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
p_name.place(x=20, y=25)
p_address = ctk.CTkLabel(patient_info, text='Address', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
p_address.place(x=20, y=45)
p_phone = ctk.CTkLabel(patient_info, text='000-000-0000:', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
p_phone.place(x=20, y=65)

c_name = ctk.CTkLabel(clinic_info, text='Clinic', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
c_name.place(x=20, y=1)
c_address = ctk.CTkLabel(clinic_info, text='Address', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
c_address.place(x=20, y=25)
c_visitdate = ctk.CTkLabel(clinic_info, text='0000-00-00', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
c_visitdate.place(x=20, y=45)
check_by2 = ctk.CTkLabel(clinic_info, text='Checked In By:', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
check_by2.place(x=20, y=65)
# p_name = ctk.CTkLabel()

p_visitid = ctk.CTkLabel(visit_info, text='VisitID #', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
p_visitid.place(x=20, y=0)
p_services = ctk.CTkLabel(visit_info, text='Services', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
p_services.place(x=20, y=20)
p_tcost = ctk.CTkLabel(visit_info, text='TotalCost', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
p_tcost.place(x=20, y=40)
p_billdate = ctk.CTkLabel(visit_info, text=f'Todays Date: {str(currentdate)}', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
p_billdate.place(x=20, y=65)
p_netpay = ctk.CTkLabel(visit_info, text='Netpay', font=('Geneva',12,'bold',),text_color=Style.page_heading_color)
p_netpay.place(x=20, y=87)

# def pdf_gen():
#     try:
#         item_to_pdf = [
#             bill_title,
#             patient_name,
#             billid,
#             checkby,
#             patient_idd,
#             paddress,
#             pservices,
#             cost,
#             ncost,
#             clinicname,
#             clinicaddress,
#             visitid
#         ]
#         auto_pdf(item_to_pdf, filename=billid, title=bill_title)
#     except Exception as e:
#         messagebox.showinfo('Oops', f'No patient record selected:')
#         return

print_btn =ctk.CTkButton(root, text='🖨️ Print Bill', command=lambda: generate_pdf(bill_title,patient_name, billid, checkby, patient_idd,paddress, pservices, cost, cal_cost,clinicname,clinicaddress,visitid)).place(x=280, y=531)
pay_btn =ctk.CTkButton(root, text='🄳🄴🅃🄰🄸🄻 🄿🄰🅈', command=lambda: show_frame2()).place(x=430, y=531)
close_btn =ctk.CTkButton(root, text='❌',width=50, command=close_out).place(x=580, y=531)
# auto_btn =ctk.CTkButton(root, text='📃',width=50, command=pdf_gen).place(x=180, y=521)
# pdf_btn =ctk.CTkButton(root, text='📄',width=50, command=lambda: generate_pdf(bill_title,patient_name, billid, checkby, patient_idd,paddress, pservices, cost, ncost,clinicname,clinicaddress,visitid)).place(x=220, y=521)


def show_frame2():
    show_frame(frame2)
    bill_data()




# , , , Diagnosis, Services, Symptoms, CheckInBy, Patient_ID, First_Name, Last_Name, , DateOfBirth, Age, PhoneNumber, Gender, ClinicID, Emergency_Contact_Name, Emergency_Contact, USERID, Created_At, Updated_At
ctk.CTkLabel(frame2, text="Patient Bill", font=Style.page_heading, text_color=Style.page_heading_color).place(x=230, y=5)
bb_id = ctk.CTkLabel(frame2, text="Bill ID #", font=Style.level_three_subheading,
                    text_color=Style.page_heading_color)
bb_id.place(x=20, y=5)
pp_id = ctk.CTkLabel(frame2, text="Patien ID #", font=Style.level_three_subheading,
                    text_color=Style.page_heading_color)
pp_id.place(x=480, y=5)

ctk.CTkLabel(frame2, text="BILL TO", font=('Geneva', 10, 'italic')).place(x=20, y=25)
pp_name = ctk.CTkLabel(frame2, text="Name", font=Style.level_one_subheading)
pp_name.place(x=20, y=45)
pp_address = ctk.CTkLabel(frame2, text="Address")
pp_address.place(x=20, y=65)
pp_phone = ctk.CTkLabel(frame2, text="000-000-0000")
pp_phone.place(x=20, y=85)
ctk.CTkLabel(frame2, text="BILL DATE", font=('Geneva', 10, 'italic')).place(x=480, y=25)
pp_date = ctk.CTkLabel(frame2, text="0000-00-00", font=Style.level_three_subheading)
pp_date.place(x=440, y=45)



pp_date_now = ctk.CTkLabel(frame2, text=f'Date: {str(currentdate)}', font=Style.level_three_subheading)
pp_date_now.place(x=440, y=65)

ctk.CTkLabel(frame2, text="BIll Items", font=('Geneva', 10, 'italic')).place(x=130, y=120)
ctk.CTkLabel(frame2, text="Amount", font=('Geneva', 10, 'italic')).place(x=420, y=120)

pp_services = ctk.CTkLabel(frame2, text="Services", font=Style.level_one_subheading)
pp_services.place(x=150, y=140)
pp_service_total = ctk.CTkLabel(frame2, text="$0.00", font=("Geneva", 12))
pp_service_total.place(x=400, y=140)
pp_diag = ctk.CTkLabel(frame2, text="System Charge", font=Style.level_one_subheading)
pp_diag.place(x=150, y=170)
pp_diag_total = ctk.CTkLabel(frame2, text="$0.00", font=("Geneva", 12))
pp_diag_total.place(x=400, y=170)
pp_med = ctk.CTkLabel(frame2, text="Medication(0)", font=Style.level_one_subheading)
pp_med.place(x=150, y=200)
pp_med_total = ctk.CTkLabel(frame2, text="$0.00", font=("Geneva", 12))
pp_med_total.place(x=400, y=200)
view_more_btn = ctk.CTkButton(frame2, text="View More", text_color="blue", border_width=1, fg_color='gray96',
                              border_color='black', command=lambda: view_more())
view_more_btn.place(x=230, y=246)

ctk.CTkLabel(frame2, text="Additional Note(Optional)", font=("Geneva", 10)).place(x=45, y=280)
bill_note = ctk.CTkTextbox(frame2, width=250, height=70, border_color='black', border_width=2).place(x=70, y=305)

percentages = ['0%','5%','10%', '15%', '20%', '25%']
ctk.CTkLabel(frame2, text="Discount", font=("Geneva", 12)).place(x=330, y=300)
discount = ctk.CTkComboBox(frame2, values=percentages, width=100, state="readonly")
discount.place(x=330, y=325)

apply_dis_btn = ctk.CTkButton(frame2, text="Apply Dis.", width=20, command=lambda: dis_set())
apply_dis_btn.place(x=440, y=325)
apply_pay_btn = ctk.CTkButton(frame2, text="💵Pay💵", width=20, command=lambda: payment_Screen())
apply_pay_btn.place(x=520, y=325)


ctk.CTkLabel(frame2, text="SubTotal", font=("Geneva", 12)).place(x=150, y=380)
sub_total = ctk.CTkLabel(frame2, text="$0.00", font=("Geneva", 12))
sub_total.place(x=400, y=380)
ctk.CTkLabel(frame2, text="TAX", font=("Geneva", 12)).place(x=150, y=400)
taxes = ctk.CTkLabel(frame2, text="$0.00", font=("Geneva", 12))
taxes.place(x=400, y=400)
ctk.CTkLabel(frame2, text="Total", font=Style.level_one_subheading).place(x=150, y=420)
final_total = ctk.CTkLabel(frame2, text="$0.00", font=("Geneva", 12))
final_total.place(x=400, y=420)



# def bill_structure():
def dis_set():
    # ftotal_dis = bill_data()

    # print(f"Selected value: {selected_value}")

    try:
        # ftotal_dis = cost_value
        ftotal = bill_data()
        ftotal_dis = ftotal[0]
        selected_value = discount.get()

        if selected_value == 0:
            subtracting_dis = ftotal[0]
        else:
            discount_value = Decimal(selected_value.strip('%')) / 100
            applying_dis = discount_value * Decimal(ftotal_dis)

            subtracting_dis = Decimal(ftotal_dis) - applying_dis

            final_total.configure(text=f'${subtracting_dis:.2f}')
            show_notification(frame2, f'{selected_value} has been applied', duration=5000, bg_color="pale green", x=230,
                              y=105, height=30, width=150)
        return  subtracting_dis
    except (ValueError, InvalidOperation) as e:
        print(f"Error converting discount value: {e}")


def payment_Screen():
    disvalue = f'{dis_set():.2f}'
    accout_figures = bill_data()
    taxvalue = f'{accout_figures[1]}'
    netvalue = f'{accout_figures[0]}'
    subTvalue = f'{accout_figures[2]}'

    print(disvalue)
    subprocess.Popen(["python3", "payment.py", ppp_id,disvalue,bill_idd,patient_name,taxvalue,netvalue,subTvalue])
    return

def bill_data():
    global view_more_btn, apply_dis_btn,general_charge,cal_cost
    check = 1
    if check:
        bb_id.configure(text=billid)
        pp_id.configure(text=patient_idd)
        pp_name.configure(text=patient_name)
        pp_address.configure(text=paddress)
        pp_phone.configure(text=phone_number)
        pp_date.configure(text=visitdate)
        pp_service_total.configure(text=cost_value)
        general_charge = 60.00
        pp_diag_total.configure(text=general_charge)
        medication = 'See your \nPharmacist'
        pp_med_total.configure(text=medication)

        # [25, 'P0031', datetime.date(2024, 11, 6), 'Sick', 'Pscan, QQscan', 'Sick', 'shehu1i', 'wasila', 'shehu',
        #  '12 man man', datetime.date(2024, 11, 4), '22222', 'East End Health Services', '321 Pine St, Cityville', 14,
        #  Decimal('890.00'), datetime.date(2024, 11, 6), None]

        # Convert values to Decimal
        subTotal = Decimal(cost_value) + Decimal(general_charge)
        sub_total.configure(text=f'${subTotal}')

        get_tax = subTotal * Decimal('2.75') / Decimal('100')
        taxes.configure(text=f'${get_tax:.2f}')

        ftotal = get_tax + subTotal
        final_total.configure(text=f'${ftotal:.2f}')
        p_tcost.configure(text=f'Total Charges: {ftotal:.2f}')
        cal_cost = f'Total Charges Due: {ftotal:.2f}'
        return ftotal,get_tax,subTotal
    else:
        messagebox.showerror("Database Error", "No patient found")
    bill_data()

def view_more():
    show_frame(mainframe)

show_frame(mainframe)
root.mainloop()