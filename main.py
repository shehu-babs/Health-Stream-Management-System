import tkinter as tk
from tkinter import ttk
from operation import Style,resize_image
import subprocess
import sys
import customtkinter as ctk
from tkinter import messagebox



home_window = tk.Tk()
home_window.title("Health Stream Management System")
home_window.focus_force()
# home_window.resizable(False,False)
home_window.iconphoto(True, resize_image((90, 90), 'images/HSMS.png'))



# Center the entire window on the screen
window_width = 700
window_height = 500
screen_width = home_window.winfo_screenwidth()
screen_height = home_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
home_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

tk_image = resize_image((700, 500), 'images/hsms_bg.jpg')
logo_image = resize_image((90, 90), 'images/HSMS.png')

# Create a Label widget with the resized image

bg_image = tk.Label(home_window, image=tk_image)
bg_image.place(x=0, y=0, relwidth=1, relheight=1)



lets_begin_login_section = tk.Frame(home_window)
lets_begin_login_section.pack( pady = 100)



def lets_begin():
    subprocess.Popen(["python3", "signin.py"])
    home_window.withdraw()

def on_label_right_click():
    messagebox.showinfo('Copy Right Notice',"®©2024 Shehu. \n All rights reserved.\n This content is protected by copyright law.\n No part of this may be reproduced or distributed \n without prior written permission from the owner.")
    return



ctk.CTkLabel(home_window,text = "Health Stream Management System",font = ("San Francisco",25,"bold"),text_color = '#6A0032',fg_color="#ffc107").place(x=160, y=100)
lg_image = ctk.CTkLabel(home_window, text='', image=logo_image, fg_color="#ffc107")
lg_image.place(x=320, y=140)

subtitle_text = """Health Visit\n Clinic Information System """
ctk.CTkLabel(home_window, text=subtitle_text, font=("Geneva", 20,'bold'), wraplength=600,fg_color = "#ffc107").place(x=240 , y=240)

#ffc107
lets_begin_login_button = ctk.CTkButton(home_window,fg_color="gray92",bg_color="gray92", width=100, height=50,text="Get Started",hover_color="Green",
                                        font =Style.page_heading, text_color=Style.page_heading_color, command=lets_begin)
lets_begin_login_button.place(y=450, x=285)


right= ctk.CTkLabel(home_window,text = "®©2024 shehu. \nAll rights reserved.",font =("Geneva",9,"bold"),text_color = '#6A0032',fg_color="#ffc107")
right.place(y=465, x=550)

right.bind("<Button-1>", lambda event: on_label_right_click())

home_window.mainloop()


