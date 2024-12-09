import sys
import json
from tkinter import messagebox

from add_staff import Add_Staff
import tkinter as tk
from tkinter import ttk
from operation import Style, resize_image, show_frame, days_count, fetch_employee_data_all, message_user, \
    show_notification, get_user_msg, confirm_read
import subprocess
# from manage_employee import call_employee_screen
import customtkinter as ctk

username = sys.argv[1]
fname = sys.argv[2]
lname = sys.argv[3]
# userrole=sys.argv[4]
# useraddress = sys.argv[5]
# userage=sys.argv[6]
# userphone=sys.argv[7]
# usergender =sys.argv[8]
# user_name=sys.argv[9]
# day_worked=sys.argv[10]
# userid=sys.argv[11]

# print(userid)
def on_logout_label_click(event):
    result = messagebox.askyesno("Question", "Are you sure you want to sign out?")
    if result:
        subprocess.Popen(["python3", "main.py"])
        dashboard_window.destroy()


def on_view_report_click(event):
    subprocess.Popen(["python3", 'report_dashboard.py',username,fname,lname])
    return


def call_add_service_page(event):
    subprocess.Popen(["python3", 'add_service.py', username])
    return


def call_add_staff_page(event):
    Add_Staff(event)
    return


def lets_begin():
    subprocess.Popen(["python3", "signin.py"])
    dashboard_window.withdraw()
    return


def manage_emp(event):
    # call_employee_screen(event)
    subprocess.Popen(["python3", 'search_employee.py', username])
    # dashboard_window.withdraw()
    return

global msg_frame_msg,msg_frame_top1,userid_gotten,value,value_name,itemlisting,itemlisting2

def message_area():
    def close():
        msg_frame.destroy()
        msg_frame_top.destroy()
        msg_frame_msg.destroy()
        msg_frame_top1.destroy()

    def send():
        global userid_gotten,itemlisting

        sending_to = to_entry.get().lower()
        text_msg = msg_text_area.get('1.0', ctk.END).strip()
        if not all([sending_to,text_msg]):
            show_notification(msg_frame_top, message="Can't Send Empty Message!", x=200, y=5, duration=5000, bg_color="azure",
                              width=190, height=30)
        else:
            try:
                to = itemlisting[sending_to].upper()
                print(f'message sent to {to}')

                if not all([username,to,text_msg]):
                    messagebox.showinfo('Sorry! \n You cant send empty Message! ❌')
                else:
                    userid_gotten = message_user(username, to,text_msg)
                    show_notification(msg_frame_top,message='✅ Message Sent!',x=250,y=5,duration=5000, bg_color="azure",
                               width=120,height=30)
                    # to_entry.delete(0,ctk.END)
                    to_entry.set('')
                    msg_text_area.delete(1.0,ctk.END)
                    # messagebox.showinfo('Sent','Message Sent!')
            except :
                show_notification(msg_frame_top, message="You Entered a wrong User Name!", x=150, y=5, duration=10000,
                                  bg_color="azure",
                                  width=230, height=30)

    def view_msg():
        # to_entry.delete(0,ctk.END)
        to_entry.set('')
        msg_text_area.delete(1.0,ctk.END)
        global msg_frame_msg,msg_frame_top1,userid_gotten,value,value_name
        msg_frame_msg = ctk.CTkFrame(mid_section, fg_color='azure', width=500, height=500, corner_radius=50, border_width=2)
        msg_frame_msg.grid(row=0, column=0, rowspan=4, columnspan=3)
        msg_frame_top1 = ctk.CTkFrame(mid_section, fg_color='black', width=500, height=40, corner_radius=1, )
        msg_frame_top1.place(x=0, y=1)
        ctk.CTkButton(msg_frame_top1, text='X',text_color='red' ,font=('Arial',30,'bold'), width=30, fg_color='black', hover_color='black', cursor='hand2', command=close).place(x=400, y=2)

        dataa = fetch_employee_data_all()
        global itemlisting, itemlisting2
        itemlisting = {row[7]: row[9] for row in dataa}
        itemlisting2 = {row[9]: row[7] for row in dataa}

        id_value = itemlisting[username]
        # print(f"The ID for {username} is {id_value}")

        name_value = itemlisting2[id_value]
        # print(f"The name for {id_value} is {name_value}")

        y_index = 50
        checker_for_empty_msg = False
        for val in get_user_msg(id_value):
            if val[-1] == 0:
                checker_for_empty_msg = True
                frame_for_msg = ctk.CTkFrame(msg_frame_msg, width=500, height=30, fg_color='PeachPuff2')
                frame_for_msg.place(x=25, y=y_index)

                # Display the sender's name
                sender_name = itemlisting2[val[1]].upper()
                sendname = ctk.CTkLabel(frame_for_msg, text=f'👤 {sender_name}', text_color='black', width=40,
                             font=('Geneva', 10, 'normal'))
                sendname.grid(row=0, column=0, sticky='w')
                # Display the message content
                idds_lb = ctk.CTkLabel(frame_for_msg, text=f'{val[3]}', text_color='black', width=350)
                idds_lb.grid(row=0, column=1, sticky='e')
                # Correctly bind the click event with a specific value
                idds_lb.bind('<Button-1>', lambda event, msg_id=val[0]: confirm_read(msg_id))
                sendname.bind('<Button-1>', lambda event, msg_id=val[0],: confirm_read(msg_id))
                idds_lb.bind('<Button-1>', lambda event, receiver=itemlisting2[val[1]],message_item=val[3]: reply_msg_on_click(receiver,message_item))
                sendname.bind('<Button-1>', lambda event, receiver=itemlisting2[val[1]],message_item=val[3]: reply_msg_on_click(receiver,message_item))

                y_index += 38
        if not checker_for_empty_msg:
                show_notification(msg_frame_top1, message='📭 No Message to View !', x=200, y=5, duration=5000, bg_color="azure",
                                  width=200, height=30)
                ctk.CTkLabel(msg_frame_msg,text='📭 No Message to View !', font=('Geneva',35,'normal'), text_color='red').place(x=30, y=200,)

    notification_count()


    msg_frame = ctk.CTkFrame(mid_section, fg_color='azure', width=500 ,height=500, corner_radius=50, border_width=2)
    msg_frame.grid(row=0, column=0, rowspan=4 , columnspan=3)
    msg_frame_top = ctk.CTkFrame(mid_section, fg_color='black', width=500 ,height=40, corner_radius=1,  )
    msg_frame_top.place(x=0,y=1)
    ctk.CTkButton(msg_frame_top, text='💬',text_color='red' ,font=('Arial',30,'bold'), width=30, fg_color='black', hover_color='black', cursor='hand2', command=view_msg).place(x=440, y=2)
    ctk.CTkButton(msg_frame_top, text='X',text_color='red' ,font=('Arial',30,'bold'), width=30, fg_color='black', hover_color='black', cursor='hand2', command=close).place(x=400, y=2)
    ctk.CTkLabel(msg_frame_top,text='Send Message To Staff ',text_color='white', font=('Geneva',16,'bold')).place(x= 50, y=4)
    to_label = ctk.CTkLabel(msg_frame,text='To:',font=('Geneva',20,'bold'))
    to_label.place(x= 50, y=60)
    msg_label = ctk.CTkLabel(msg_frame,text='Message:', font=('Geneva',20,'bold'))
    msg_label.place(x= 50, y=120)

    list_val = [row[7] for row in fetch_employee_data_all() if row[7] is not None]
    print(list_val)
    to_entry = ctk.CTkComboBox(msg_frame, values=list_val, border_width=1, width=300)
    to_entry.place(x= 180, y=60)
    msg_text_area = ctk.CTkTextbox(msg_frame, border_width=1, width=300, height=200)
    msg_text_area.place(x= 180, y=120)

    send_btn = ctk.CTkButton(msg_frame, text='Send',text_color='azure', fg_color='black', command=send)
    send_btn.place(x= 300, y=420)

    def enable_reply():
        global itemlisting, itemlisting2
        receiver_name = to_entry.get()
        to_entry.configure(state='normal')
        msg_text_area.configure(state='normal')
        # to_entry.delete(0,ctk.END)
        to_entry.set('')
        msg_text_area.delete(1.0,ctk.END)
        to_label.configure(text='To:')
        # to_entry.insert(0,itemlisting[receiver_name])
        fill_to_field = itemlisting2[itemlisting[receiver_name]]
        to_entry.set(itemlisting[receiver_name])
        to_entry.set(fill_to_field)

        print(f'this is new receiver id {itemlisting[receiver_name]}')

        reply_btn.destroy()

    reply_btn = ctk.CTkButton(msg_frame, text='Reply', text_color='azure', fg_color='Green', command=lambda: enable_reply())


    def reply_msg_on_click(receiver,message_item):
        # to_entry.insert(0,receiver)
        # sending = itemlisting2[receiver]
        # print(sending)
        to_entry.set(receiver)
        msg_text_area.insert(1.0,message_item)
        msg_frame_top1.destroy()
        msg_frame_msg.destroy()
        notification_count()
        to_label.configure(text='From:')
        to_entry.configure(state='readonly')
        msg_text_area.configure(state='disabled')
        reply_btn.place(x=300, y=420)



def notification_count():
    global itemlisting
    dataa = fetch_employee_data_all()
    itemlisting = {row[7]: row[9] for row in dataa}
    itemlisting2 = {row[9]: row[7] for row in dataa}

    id_value = itemlisting[username]
    print(f"The ID for {username} is {id_value}")

    name_value = itemlisting2[id_value]
    print(f"The name for {id_value} is {name_value}")

    counter = 0
    for val in get_user_msg(id_value):
        print(val[-1])
        if val[-1] == 0:
            counter+=1
    print(counter)
    # global notification_label
    notification_label.configure(text=f'Notifications {counter}')





dashboard_window = tk.Tk()
dashboard_window.title("Admin Dashboard")
dashboard_window.resizable(False, False)
dashboard_window.focus_force()
dashboard_window.geometry("800x800")
dashboard_window.iconphoto(True, resize_image((90, 90), 'images/HSMS.png'))

window_width = 800
window_height = 800
screen_width = dashboard_window.winfo_screenwidth()
screen_height = dashboard_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
dashboard_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

wrapper = tk.Frame(dashboard_window, background="white")
wrapper.pack(fill='both', expand=True)

left_nav = tk.Frame(wrapper, bg='#00CCCC', width=100)
left_nav.pack(fill='y', side="right")

left_nav_title = tk.Frame(left_nav, bg='#00CCCC')
left_nav_title.pack(fill='y', side="top", anchor="w")

top_left_nav = tk.Frame(left_nav, bg='#00CCCC')
top_left_nav.pack(fill='y', side="top", anchor="w")

bottom_left_nav = tk.Frame(left_nav, bg='#00CCCC')
bottom_left_nav.pack(fill='y', side="bottom")

right_section = tk.Frame(wrapper, bg='white')
right_section.pack(fill='y', side="right", expand=True)

title = tk.Frame(right_section, bg="white", pady=20, padx=20)
title.pack(fill="y", expand=True, side='top')

mid_section = tk.Frame(right_section, bg="white", pady=20, padx=20)
mid_section.pack(fill="y", expand=True, side='top', anchor='center')

# profile = ctk.CTkFrame(mid_section, width=300, height=400)
# profile.place(x=50, y=50)

# LEFT NAV MENU

dashboard_image = resize_image((25, 25), 'images/dashboard.png')
tk.Label(left_nav_title, image=dashboard_image, bg='#00CCCC', cursor="hand2").grid(row=0, column=0, padx=(20, 0),
                                                                                   sticky='e')
tk.Label(left_nav_title, text="Admin Dashboard", justify="left", bg='#00CCCC', fg='#6A0032',
         font=("San Francisco", 15, "bold")).grid(row=0, column=1, pady=(20, 20), padx=(0, 20), sticky="w")

# TOP SECTION

# registered_staff
manage_staff_image = resize_image((20, 20), 'images/management_staff.png')
manage_staff_image_label = tk.Label(top_left_nav, image=manage_staff_image, bg='#00CCCC', cursor="hand2")
manage_staff_image_label.grid(row=0, column=0, padx=(20, 0), sticky='e')
manage_staff_label = tk.Label(top_left_nav, text="Manage Employee Profile", bg='#00CCCC', fg='black', justify="left")
manage_staff_label.grid(row=0, column=1, padx=(0, 20), sticky='w')
manage_staff_image_label.bind("<Button-1>", manage_emp)
manage_staff_label.bind("<Button-1>", manage_emp)

# add staff
add_staff_image = resize_image((20, 20), 'images/add-staff.png')
add_staff_image_label = tk.Label(top_left_nav, image=add_staff_image, bg='#00CCCC', cursor="hand2")
add_staff_image_label.grid(row=1, column=0, padx=(20, 0), sticky='w')
add_staff_label = tk.Label(top_left_nav, text="Register Staff", bg='#00CCCC', fg='black', justify="left")
add_staff_label.grid(row=1, column=1, padx=(0, 20), sticky='w')
add_staff_image_label.bind("<Button-1>", call_add_staff_page)
add_staff_label.bind("<Button-1>", call_add_staff_page)

# settings
manage_service_image = resize_image((20, 20), 'images/manage_service.png')
mng_service_image_label = tk.Label(top_left_nav, image=manage_service_image, bg='#00CCCC', cursor="hand2")
mng_service_image_label.grid(row=2, column=0, padx=(20, 0), sticky='w')
mng_service = tk.Label(top_left_nav, text="Manage Service", bg='#00CCCC', fg='black', justify="left")
mng_service.grid(row=2, column=1, padx=(0, 20), sticky='w')
mng_service_image_label.bind("<Button-1>", call_add_service_page)
mng_service.bind("<Button-1>", call_add_service_page)

# report
report_image = resize_image((20, 20), 'images/report.png')
report_image_label = tk.Label(top_left_nav, image=report_image, bg='#00CCCC', cursor="hand2")
report_image_label.grid(row=3, column=0, padx=(20, 0), sticky='w')
report_label = tk.Label(top_left_nav, text="View Reports", bg='#00CCCC', fg='black', justify="left")
report_label.grid(row=3, column=1, padx=(0, 20), sticky='w')
report_image_label.bind("<Button-1>", on_view_report_click)
report_label.bind("<Button-1>", on_view_report_click)

# messages
feedback_image = resize_image((20, 20), 'images/feedback.png')
messages1 = tk.Label(top_left_nav, image=feedback_image, bg='#00CCCC', cursor="hand2")
messages1.grid(row=4, column=0, padx=(20, 0),sticky='w')
messages2 = tk.Label(top_left_nav, text="Messages", bg='#00CCCC', fg='black', justify="left", cursor="hand2")
messages2.grid(row=4, column=1,padx=(0, 20), sticky='w')
messages2.bind('<Button-1>', lambda event: message_area())
messages1.bind('<Button-1>', lambda event: message_area())

# notification
notification_image = resize_image((20, 20), 'images/notification.png')
notification_img_label = tk.Label(top_left_nav, image=notification_image, bg='#00CCCC', cursor="hand2")
notification_img_label.grid(row=5, column=0, padx=(20, 0), sticky='w')
notification_label = tk.Label(top_left_nav, text="Notifications", bg='#00CCCC', fg='black', justify="left", cursor="hand2")
notification_label.grid(row=5, column=1,padx=(0, 20), sticky='w')
# notification_label.bind('<Button-1>', lambda event: 'message_area()')
# notification_img_label.bind('<Button-1>', lambda event: 'message_area()')
notification_count()


# BUTTOM SECTION
account_image = resize_image((20, 20), 'images/person.png')
account_image_label = tk.Label(bottom_left_nav, image=account_image, bg='#00CCCC', cursor="hand2")
account_image_label.grid(row=0, column=0, padx=(20, 0), sticky='w')
account_label = tk.Label(bottom_left_nav, text=username, bg='#00CCCC', fg='black', justify="left")
account_label.grid(row=0, column=1, padx=(0, 20), sticky='w')
account_image_label.bind('<Button-1>',)
account_label.bind('<Button-1>', )

lg_image = resize_image((20, 20), 'images/logout.png')
logout_image = tk.Label(bottom_left_nav, image=lg_image, bg='#00CCCC', cursor="hand2")
logout_image.grid(row=1, column=0, pady=(10, 30), padx=(20, 0), sticky='w')
logout_image.bind("<Button-1>", on_logout_label_click)
signout = tk.Label(bottom_left_nav, text="Sign Out", bg='#00CCCC', fg='black', cursor="hand2")
signout.grid(row=1, column=1, pady=(10, 30), padx=(0, 20), sticky='w')
signout.bind("<Button-1>", on_logout_label_click)

dashboard_label = tk.Label(title, text=f"Hey {username} Welcome to Health Stream \n Management System !",
                           wraplength=500,
                           font=("San Francisco", 25), fg='#660000', bg="white")
dashboard_label.grid(row=0, column=0, padx=20, pady=20)

# MANAGE EMPLOYEE
dashboard_create_image = resize_image((80, 80), 'images/management_staff.png')
# Create a Label widget with the resized image
dashboard_manage_staff = tk.Label(mid_section, image=dashboard_create_image, cursor="hand2", bg="white")
dashboard_manage_staff.grid(row=0, column=0)
dashboard_create_label = tk.Label(mid_section, text="Manage Employee Profile", font=Style.subheading, cursor="hand2",
                                  bg="white")
dashboard_create_label.grid(row=1, column=0, pady=(0, 50))
dashboard_create_label.bind("<Button-1>", manage_emp)
dashboard_manage_staff.bind("<Button-1>", manage_emp)

# REGISTER STAFF
dash_reg_image = resize_image((80, 80), 'images/register.png')
# Create a Label widget with the resized image
dashboard_reg_image = tk.Label(mid_section, image=dash_reg_image, bg="white")
dashboard_reg_image.grid(row=0, column=1)
dashboard_reg_label = tk.Label(mid_section, text="Register Staff", font=Style.subheading, cursor="hand2", bg="white")
dashboard_reg_label.grid(row=1, column=1, pady=(0, 50))
dashboard_reg_label.bind("<Button-1>", Add_Staff)
dashboard_reg_image.bind("<Button-1>", Add_Staff)

# MANAGE SERVICE CATALOG
dash_service_image = resize_image((80, 80), 'images/manage_service.png')
# Create a Label widget with the resized image
dashboard_service_image = tk.Label(mid_section, image=dash_service_image, bg="white")
dashboard_service_image.grid(row=2, column=0)
dashboard_service_label = tk.Label(mid_section, text="Manage Service", font=Style.subheading, cursor="hand2",
                                   bg="white")
dashboard_service_label.grid(row=3, column=0, pady=(0, 50))
dashboard_service_label.bind("<Button-1>", call_add_service_page)
dashboard_service_image.bind("<Button-1>", call_add_service_page)

# VIEW REPORT AREA
dash_report_image = resize_image((80, 80), 'images/report.png')
# Create a Label widget with the resized image
dashboard_report_image = tk.Label(mid_section, image=dash_report_image, bg="white")
dashboard_report_image.grid(row=2, column=1)
dashboard_report_label = tk.Label(mid_section, text="View Reports", font=Style.subheading, cursor="hand2", bg="white")
dashboard_report_label.grid(row=3, column=1, pady=(0, 50))
dashboard_report_label.bind("<Button-1>", on_view_report_click)
dashboard_report_image.bind("<Button-1>", on_view_report_click)

for column in range(3):  # Assuming you have 8 columns in the grid
    mid_section.grid_columnconfigure(column, weight=1)

for child in mid_section.winfo_children():
    child.grid_configure(padx=30)

for child in top_left_nav.winfo_children():
    child.grid_configure(pady=(0, 10))


# ctk.CTkLabel(profile, text=f'Name: {userdata[1]}'f'{userdata[2]}').grid(row=0, column=0, padx=20)
# ctk.CTkLabel(profile, text=f'Current Role: {userdata[3]}').grid(row=1, column=0, padx=20)
# ctk.CTkLabel(profile, text=f'Address: {userdata[4]}').grid(row=1, column=0, padx=20)
# ctk.CTkLabel(profile, text=f'Age: {userdata[4]}').grid(row=1, column=0, padx=20)
# ctk.CTkLabel(profile, text=f'PhoneNumber: {userdata[4]}').grid(row=1, column=0, padx=20)
# ctk.CTkLabel(profile, text=f'Gender: {userdata[4]}').grid(row=1, column=0, padx=20)
# ctk.CTkLabel(profile, text=f'User_Name: {userdata[4]}').grid(row=1, column=0, padx=20)
# ctk.CTkLabel(profile, text=f'Created_At: {userdata[4]}').grid(row=1, column=0, padx=20)
# ctk.CTkLabel(profile, text=f'USERID: {userdata[4]}').grid(row=1, column=0, padx=20)
#


dashboard_window.mainloop()
