import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import sys
from add_staff import Add_Staff
from operation import resize_image, Style, show_frame, fetch_employee_data_one, fetch_employee_data_all, sort_column, \
    connect_to_database, load_treeview_shades, export_tree_to_excel
import subprocess

logger_name = sys.argv[1]

global frame_right2,frame_right3,item_frame,item_frame_update, p_data2,new_value,search_entry,export_title,print_btn

export_title = 'title'

#all emp record
all_emp_data_list = []
#single emp record
p_data = []
# single data for update
p_data2 = []
p_data2_labels = ["First_Name", "Last_Name", "Role", "Staff_Address", "DateOfBirth", "PhoneNumber", "Gender",
           "User_Name", "Created_At", "USERID", "Name", "Clinic_Address", "Supervisor"]
entry_list = []  # List to keep track of the CTkEntry widgets



def clear():

    for item in tree.get_children():
        tree.delete(item)


def pop_data():
    userid = search_entry.get()
    p_data.clear()
    p_data2.clear()
    try:
        # userid = search_entry.get()
        data_set = fetch_employee_data_one(userid)[0]
        print(data_set)
        s_name.configure(text=f'Name: {data_set[0]+' '+data_set[1]}')
        s_role.configure(text=f'🧑🏻‍⚕️ Role: {data_set[2].upper()}')
        s_address.configure(text=f'🏚️ Address: {data_set[3]}')
        s_dob.configure(text=f'📅 Date of Birth: {data_set[4]}')
        s_phone.configure(text=f'📞 Phone: {data_set[5]}')
        s_gender.configure(text=f'🧍🏻‍♂️🧍🏻‍♀️Gender: {data_set[6].upper()}')
        s_username.configure(text=f'👨🏼‍💻 Username: {data_set[7]}')
        s_hire.configure(text=f'📅 Hire Date: {data_set[8]}')
        s_id.configure(text=f'Staff ID#{data_set[9]}')
        s_clinic.configure(text=f'🏥 Clinic: {data_set[10]}')
        s_clinic_address.configure(text=f'🏥 Clinic: {data_set[11]}')
        s_clinic_supervisor.configure(text=f'🏥 Supervisor: {data_set[12]}')
        if data_set[13] == 1:
            is_status.configure(text='✅ Active User',text_color='Green')
            show_frame(delete_emp_btn)
        else:
            is_status.configure(text='❌ Non Active User',text_color='Red')
            show_frame(re_activate)
        warning_label.configure(text="Loaded!")
        warning_label.configure(text_color='Green')
        warning_label.place(x=940, y=65)
        for item in data_set:
            p_data.append(item)
            p_data2.append(item)


        job_info()
        first_view()


    except Exception as e:
        if isinstance(e, IndexError) and 'list index out of range' in str(e):
            print("Invalid userID")
            warning_label.configure(text="Invalid userID!")
            warning_label.configure(text_color='red')
            warning_label.place(x=900, y=65)
        else:
            print(f"An unexpected error occurred: {e}")

def job_info():
    global item_frame, p_data

    job_label.configure(text='Job Information')
    welcome_label.configure(text='')
    initial_y = 50
    # item_frame = ctk.CTkFrame(frame_right, width=600, height=30, fg_color='gray80')
    # else:
    for item in p_data:
        item_frame = ctk.CTkFrame(frame_right, width=600, height=30, fg_color='gainsboro')
        item_frame.place(x=55,y=initial_y)
        ctk.CTkLabel(item_frame, text=f'{item}', font=('Geneva', 18, 'normal')).place(x=240, y=0)
        initial_y += 40




def all_emp_data_view():
    global export_title, print_btn
    export_title = 'All Employee Data'
    clear()
    # frame_right2.configure(width=850)
    # frame_right2.place(x=0,y=100)
    counter_holder=0
    for result in fetch_employee_data_all():
        tag = load_treeview_shades(tree)
        tree.insert("", tk.END, values=result,tags=tag)
        counter_holder+=1
    emp_count_label.configure(text=f"All Staff Count: {counter_holder}")
    # Bind the click event to the Treeview
    # tree.bind("<ButtonRelease-1>", on_tree_item_click)
    tree.bind("<Double-1>", on_tree_item_click)
    print_btn.place(x=1000, y=15)

def all_active_emp_view():
    global export_title,print_btn
    export_title = 'Active Employee'
    clear()
    # frame_right2.configure(width=850)
    # frame_right2.place(x=0,y=100)
    counter_holder = 0
    for result in fetch_employee_data_all():
        if result[13] == 1:
            tag = load_treeview_shades(tree)
            tree.insert("", tk.END, values=result,tags=tag)
            counter_holder +=1

    emp_count_label.configure(text=f"Active Staff : {counter_holder}")
    # Bind the click event to the Treeview
    # tree.bind("<ButtonRelease-1>", on_tree_item_click)
    tree.bind("<Double-1>", on_tree_item_click)
    print_btn.place(x=1000,y=15)

def all_deleted_emp_view():
    global export_title,print_btn
    export_title='Non Active Employee'
    clear()
    # frame_right2.configure(width=850)
    # frame_right2.place(x=0,y=100)
    counter_holder = 0
    for result in fetch_employee_data_all():
        if result[13]==0:
            tag = load_treeview_shades(tree)
            tree.insert("", tk.END, values=result,tags=tag)
            counter_holder +=1

    emp_count_label.configure(text=f"Non Active Staff : {counter_holder}")
    # Bind the click event to the Treeview
    # tree.bind("<ButtonRelease-1>", on_tree_item_click)
    tree.bind("<Double-1>", on_tree_item_click)
    print_btn.place(x=1000,y=15)

    # ctk.CTkButton(frame_left, text='Activate Employee', font=('Geneva', 14, 'bold'), text_color='black', fg_color='azure'
    #               , cursor='hand2', width=40, hover_color='firebrick1', command=lambda: pop_up_frame()).place(x=280,y=600)




def on_tree_item_click(event):
    # Get the selected item
    selected_item = tree.focus()
    if selected_item:
        item_data = tree.item(selected_item)
        item_values = item_data['values']
        if len(item_values) > 9:  # Check if index 9 is available

            print(f"Selected Item Values: {item_values}")
            pop_entry_field = item_values[9]
            search_entry.delete(0,tk.END)
            search_entry.insert(0,pop_entry_field)
            pop_data()


def updating_emp():
    global item_frame_update, p_data2,new_value
    # p_data2.clear()
    # if isinstance(new_value.get()):
    #     for item in
    entry_list.clear()
    initial_y = 50
    # item_frame = ctk.CTkFrame(frame_right, width=600, height=30, fg_color='gray80')
    # else:
    for item,item_lb in zip(p_data2,p_data2_labels):
        item_frame_update = ctk.CTkFrame(frame_right3, width=600, height=28, fg_color='gainsboro')
        item_frame_update.place(x=75, y=initial_y)
        new_value = ctk.CTkEntry(item_frame_update, placeholder_text=f'{item}', font=('Geneva', 14, 'normal'), width=250)
        new_value.place(x=240, y=0)
        new_value.insert(0,item)
        ctk.CTkLabel(item_frame_update, text=f'{item_lb}', font=('Geneva', 18, 'normal')).place(x=80, y=0)

        entry_list.append(new_value)
        initial_y += 40



        
    def get_post_value():
        values_to_post_db = [entry.get() for entry in entry_list]
        print(values_to_post_db)
        return values_to_post_db

    def post_to_db():
        global conn
        data = get_post_value()
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Ensure that data has the expected format
            if len(data) >= 10 and isinstance(data[0], str) and isinstance(data[9], str):
                # Update query example
                sql = (""" UPDATE STAFF 
                           SET First_Name = %s, Last_Name = %s, Role = %s, Staff_Address = %s,
                           PhoneNumber = %s
                           WHERE USERID = %s """)

                # Execute the query with collected data
                cursor.execute(sql, (
                    data[0],  # First Name
                    data[1],  # Last Name
                    data[2],  # Role
                    data[3],  # Address
                    data[5],  # Phone
                    data[9],  # UserID
                ))

                conn.commit()
                print("Database update successful!")
            else:
                print("Invalid data format.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    ctk.CTkButton(frame_right3, text='↑ Update Emp',fg_color='black',hover_color='firebrick1', command=post_to_db).place(x=600, y=600)




def first_view():
    show_frame(frame_left)
    show_frame(frame_right)
    # search_entry.delete(0, tk.END)

def second_view():
    show_frame(frame_right2)
    all_emp_data_view()
    search_entry.delete(0, tk.END)

def third_view():
    show_frame(frame_left)
    show_frame(frame_right3)
    updating_emp()
    # search_entry.delete(0, tk.END)

def forth_view():
    show_frame(frame_right2)
    all_active_emp_view()
    search_entry.delete(0, tk.END)

def fifth_view():
    show_frame(frame_right2)
    all_deleted_emp_view()
    search_entry.delete(0,tk.END)

# def add_emp():
#     subprocess.Popen(['python3', ''])

def pop_up_frame():
    pop_frame = ctk.CTkFrame(manage_emp_window, width=300, height=300, corner_radius=40,fg_color='#ffc107', )
    pop_frame.place(x=490, y=150)
    pop_frame.focus_force()

    ctk.CTkLabel(pop_frame,text='Confirm Action', text_color='black', font=('Geneva',20,'bold')).place(x=80,y=20)

    name_name = ctk.CTkEntry(pop_frame)
    name_name.place(x=80,y=60)

    pwd = ctk.CTkEntry(pop_frame, placeholder_text='🔐Enter Password',placeholder_text_color='black')
    pwd.place(x=80,y=90)

    user_to_delete = search_entry.get()

    name_name.insert(0,logger_name)

    def validate():
        statu_ck = is_status.cget('text')
        name_get = name_name.get()
        pwd_get = pwd.get()
        if not all([name_get, pwd_get]):
            messagebox.showwarning("Fields Empty", " 😅\nEnter a Valid \nUser Name and Password")
            return
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Check the username and password in the database
            sql = ("SELECT * FROM STAFF "
                   "WHERE (PhoneNumber = %s OR User_Name = %s) "
                   "AND password = %s")
            cursor.execute(sql, (name_get, name_get, pwd_get))
            result = cursor.fetchone()

            if result:
                if pwd_get == result[10]:
                    print('correct password')

                    try:
                        cursor.execute('SET SQL_SAFE_UPDATES = 0;')

                        if statu_ck == '✅ Active User':
                            print(f'{user_to_delete} Deactivated')
                            query = "UPDATE STAFF SET is_active = 0 WHERE USERID = %s ;"
                        else:
                            query = "UPDATE STAFF SET is_active = 1 WHERE USERID = %s ;"
                            print(f'{user_to_delete} Activated')

                        cursor.execute(query, (user_to_delete,))

                        cursor.execute('SET SQL_SAFE_UPDATES = 1;')

                        # Commit the changes
                        conn.commit()
                        pop_data()
                        pop_frame.destroy()
                    except Exception as e:
                        print(e)
            else:
               print('invalid password!')

        except Exception as e:
            print(e)

            conn.close()


    ctk.CTkButton(pop_frame,text='Enter',fg_color='black',hover_color='green', command=validate).place(x=80, y=130)



    ctk.CTkButton(pop_frame,text='E❌it ',fg_color='black',hover_color='green', command=pop_frame.destroy).place(x=80,y=230)


    # show_frame(pop_frame)


global print_btn

manage_emp_window = tk.Tk()
manage_emp_window.title("")
manage_emp_window.resizable(False,False)
manage_emp_window.iconphoto(True, resize_image((90, 90), 'images/HSMS.png'))
manage_emp_window.focus_force()

# Center-aligning the window on the screen
window_width = 1200
window_height = 750
screen_width = manage_emp_window.winfo_screenwidth()
screen_height = manage_emp_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
manage_emp_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")


frame_top = ctk.CTkFrame(manage_emp_window, fg_color='gray97', width=1200, height=100)
frame_top.pack()
frame_left = ctk.CTkFrame(manage_emp_window, fg_color='azure', width=450, height=650, border_width=1, corner_radius=0)
frame_left.place(x=0,y=100)
frame_right = ctk.CTkFrame(manage_emp_window, fg_color='azure', width=750, height=650,border_width=1, corner_radius=0)
frame_right.place(x=450,y=100)
frame_right2 = ctk.CTkFrame(manage_emp_window, fg_color='azure', width=1200, height=650,border_width=1, corner_radius=0)
frame_right2.place(x=0,y=100)
frame_right3 = ctk.CTkFrame(manage_emp_window, fg_color='azure', width=750, height=650,border_width=1, corner_radius=0)
frame_right3.place(x=450,y=100)




#Items on top frame
prof_label = ctk.CTkLabel(frame_top,text='Employee Profile', font=('Geneva',25,'bold'))
prof_label.place(x=15,y=15)
emp_count_label = ctk.CTkLabel(frame_top,text='', font=('Geneva',12,'bold'),text_color='dark blue')
emp_count_label.place(x=220,y=20)
warning_label = ctk.CTkLabel(frame_top,text='Enter ID:',text_color='black', font=('Geneva',14,'bold'))
warning_label.place(x=940,y=65)
staff_add_btn = ctk.CTkButton(frame_top,text='+ Add Employee', width=20, fg_color='black',)
staff_add_btn.place(x=1080,y=15)

staff_add_btn.bind('<Button-1>', Add_Staff)

overview_btn = ctk.CTkButton(frame_top, text='Over View', font=('Geneva',14,'bold'),text_color='black',fg_color='gray97'
                             ,cursor='hand2',width=40,hover_color='gray92', command=lambda: first_view()).place(x=35,y=70)

view_all_btn = ctk.CTkButton(frame_top, text='View All', font=('Geneva',14,'bold'),text_color='black',fg_color='gray97'
                             ,cursor='hand2',width=40,hover_color='gray92',command=lambda:second_view()).place(x=135,y=70)

update_btn = ctk.CTkButton(frame_top, text='Update View', font=('Geneva',14,'bold'),text_color='black',fg_color='gray97'
                             ,cursor='hand2',width=40,hover_color='gray92', command=lambda: third_view()).place(x=235,y=70)

update_btn = ctk.CTkButton(frame_top, text='Active Emp.', font=('Geneva',14,'bold'),text_color='black',fg_color='gray97'
                             ,cursor='hand2',width=40,hover_color='gray92', command=lambda: forth_view()).place(x=345,y=70)

update_btn = ctk.CTkButton(frame_top, text='Non Active Emp.', font=('Geneva',14,'bold'),text_color='black',fg_color='gray97'
                             ,cursor='hand2',width=40,hover_color='gray92', command=lambda: fifth_view()).place(x=465,y=70)


search_entry =  ctk.CTkEntry(frame_top,placeholder_text='🔍 Search Employee', placeholder_text_color='black')
search_entry.place(x=1020,y=65)
search_entry.bind('<Return>', lambda event: pop_data())

delete_emp_btn = ctk.CTkButton(frame_left, text='X Delete Staff', font=('Geneva', 14, 'bold'), text_color='black', fg_color='azure'
                  , cursor='hand2', width=210, hover_color='firebrick1', command=lambda: pop_up_frame())
delete_emp_btn.place(x=180, y=600)

re_activate = ctk.CTkButton(frame_left, text='Activate Employee', font=('Geneva', 14, 'bold'), text_color='black', fg_color='azure'
                  , cursor='hand2', width=210, hover_color='firebrick1', command=lambda: pop_up_frame())
re_activate.place(x=180,y=600)


# items on left frame
img = resize_image((150,150),'images/profile_image B.png')
image_lable = ctk.CTkLabel(frame_left, text='', image=img).place(x=5,y=15)

s_name = ctk.CTkLabel(frame_left,text='', font=('Geneva',18,'bold'), text_color=Style.level_one_subheading_color)
s_name.place(x=155, y=40)
s_id = ctk.CTkLabel(frame_left,text='', font=Style.level_one_subheading, text_color=Style.level_one_subheading_color)
s_id.place(x=155, y=80)
is_status =ctk.CTkLabel(frame_left,text='', font=Style.level_one_subheading, text_color=Style.level_one_subheading_color)
is_status.place(x=155, y=110)

ctk.CTkLabel(frame_left,text='About',font=('Arial',14,'bold')).place(x=55,y=170)
s_phone = ctk.CTkLabel(frame_left,text='',font=('Geneva',14,'bold'))
s_phone.place(x=55,y=200)
s_address = ctk.CTkLabel(frame_left,text='',font=('Geneva',14,'bold'))
s_address.place(x=55,y=230)
s_dob = ctk.CTkLabel(frame_left,text='',font=('Geneva',14,'bold'))
s_dob.place(x=55,y=260)
s_gender = ctk.CTkLabel(frame_left,text='',font=('Geneva',14,'bold'))
s_gender.place(x=55,y=290)
ctk.CTkLabel(frame_left,text='_______________________________________',font=('Arial',12,'underline')).place(x=55,y=320)

ctk.CTkLabel(frame_left,text='Employee Details',font=('Arial',14,'bold')).place(x=55,y=350)
s_username = ctk.CTkLabel(frame_left,text='',font=('Geneva',14,'bold'))
s_username.place(x=55,y=380)
s_hire = ctk.CTkLabel(frame_left,text='',font=('Geneva',14,'bold'))
s_hire.place(x=55,y=410)
s_role = ctk.CTkLabel(frame_left,text='',font=('Geneva',14,'bold'))
s_role.place(x=55,y=440)
s_clinic = ctk.CTkLabel(frame_left,text='',font=('Geneva',14,'bold'))
s_clinic.place(x=55,y=470)
s_clinic_address = ctk.CTkLabel(frame_left,text='',font=('Geneva',14,'bold'))
s_clinic_address.place(x=55,y=500)
s_clinic_supervisor = ctk.CTkLabel(frame_left,text='',font=('Geneva',14,'bold'))
s_clinic_supervisor.place(x=55,y=530)
ctk.CTkLabel(frame_left,text='_______________________________________',font=('Arial',12,'underline')).place(x=55,y=560)

#items on right frame
job_label = ctk.CTkLabel(frame_right,text='',font=('Arial',16,'bold'))
job_label.place(x=55,y=20)
welcome_label = ctk.CTkLabel(frame_right,text=f'{logger_name.upper()} \n 👨🏻‍⚕️ Welcome To Staff Portal',font=('Geneva',40,'bold'))
welcome_label.place(x=115,y=260)



# Create the Treeview

columns = ("First_Name", "Last_Name", "Role", "Staff_Address", "DateOfBirth", "PhoneNumber", "Gender",
           "User_Name", "Created_At", "USERID", "Name", "Clinic_Address", "Supervisor")
tree = ttk.Treeview(frame_right2, columns=columns, show="headings", height=50)
# Define the column headings and the sorting behavior
tree.heading("First_Name", text="First Name", command=lambda: sort_column(tree, "First_Name", False), anchor='center')
tree.heading("Last_Name", text="Last Name", command=lambda: sort_column(tree, "Last_Name", False))
tree.heading("Role", text="Role", command=lambda: sort_column(tree, "Role", False))
tree.heading("Staff_Address", text="Staff Address", command=lambda: sort_column(tree, "Staff_Address", False))
tree.heading("DateOfBirth", text="Date of Birth", command=lambda: sort_column(tree, "DateOfBirth", False))
tree.heading("PhoneNumber", text="Phone Number", command=lambda: sort_column(tree, "PhoneNumber", False))
tree.heading("Gender", text="Gender", command=lambda: sort_column(tree, "Gender", False))
tree.heading("User_Name", text="User Name", command=lambda: sort_column(tree, "User_Name", False))
tree.heading("Created_At", text="Created At", command=lambda: sort_column(tree, "Created_At", False))
tree.heading("USERID", text="User ID", command=lambda: sort_column(tree, "USERID", False))
tree.heading("Name", text="Clinic Name", command=lambda: sort_column(tree, "Name", False))
tree.heading("Clinic_Address", text="Clinic Address", command=lambda: sort_column(tree, "Clinic_Address", False))
tree.heading("Supervisor", text="Supervisor", command=lambda: sort_column(tree, "Supervisor", False))

# Set the column widths
tree.column("First_Name", width=90, anchor='center')
tree.column("Last_Name", width=90, anchor='center')
tree.column("Role", width=80, anchor='center')
tree.column("Staff_Address", width=150, anchor='center')
tree.column("DateOfBirth", width=100,anchor='center')
tree.column("PhoneNumber", width=110,anchor='center')
tree.column("Gender", width=40, anchor='center')
tree.column("User_Name", width=60, anchor='center')
tree.column("Created_At", width=90,anchor='center')
tree.column("USERID", width=70, anchor='center')
tree.column("Name", width=110,anchor='center')
tree.column("Clinic_Address", width=110)
tree.column("Supervisor", width=110)

tree.bind('<Return>', lambda event: pop_data)


print_btn = ctk.CTkButton(frame_top,text='Export 📂', width=20, fg_color='black', command=lambda: export_tree_to_excel(tree,export_title))




tree.pack(fill=tk.BOTH, expand=True)
# tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")






first_view()
manage_emp_window.mainloop()