import sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageGrab
import customtkinter as ctk
import os

from operation import today

# Read arguments passed to the script
name = sys.argv[1]
formatted_id = sys.argv[2]
dob = sys.argv[3]
gender = sys.argv[4]
clinic_id = sys.argv[5]
address = sys.argv[6]
card_date =sys.argv[7]



# Function to create the ID Card window
def create_id_card_window():
    # Create the main window using customtkinter
    window = ctk.CTk()  # Use CTk for customtkinter windows
    window.title("ID Card")
    window.geometry("400x600")
    window.focus_force()
    window.configure(bg="#f0f0f0")
    window.resizable(False,False)

    frameM = ctk.CTkFrame(window,width=400,height=500,fg_color='azure')
    frameM.place(x=0,y=0)
    # Load an image using PIL and CTkImage
    image_path = "images/id_card.png"  # Provide the correct path to your image
    img = ctk.CTkImage(Image.open(image_path), size=(150, 150))  # Resize the image

    # Photo using CTkLabel instead of standard Label
    label_photo = ctk.CTkLabel(frameM, image=img, text="")
    label_photo.grid(row=0, column=0, pady=10, padx=130)

    # ID Card Info (Name, ID Number, etc.)
    label_name = ctk.CTkLabel(frameM, text="Name: " f"{name}", font=("Geneva", 20, "bold"))
    label_name.grid(row=1, column=0, pady=10, padx=100)

    label_id = ctk.CTkLabel(frameM, text="PatientID: " f"{formatted_id}", font=("Geneva", 16))
    label_id.grid(row=2, column=0, pady=10, padx=100)

    label_dob = ctk.CTkLabel(frameM, text="Date of Birth: " f"{dob}", font=("Geneva", 16))
    label_dob.grid(row=3, column=0, pady=10, padx=100)

    label_gender = ctk.CTkLabel(frameM, text="Gender: " f"{gender}", font=("Geneva", 16))
    label_gender.grid(row=4, column=0, pady=10, padx=100)

    label_adress = ctk.CTkLabel(frameM, text="Address: " f"{address}", font=("Geneva", 16))
    label_adress.grid(row=5, column=0, pady=10, padx=100)

    label_clinic = ctk.CTkLabel(frameM, text="Clinic ID: " f"{clinic_id}", font=("Geneva", 16))
    label_clinic.grid(row=6, column=0, pady=10, padx=100)

    # Footer section
    label_footer = ctk.CTkLabel(frameM, text="Issued:" f"{card_date}", font=("Geneva", 14), fg_color="gray", bg_color="#f0f0f0")
    label_footer.grid(row=7, column=0, pady=10, padx=100)

    # Add a "Print" button
    print_button = ctk.CTkButton(window, text="Print ID Card", command=lambda: print_id_card(frameM))
    print_button.place(x=130,y=520)

    # Start the Tkinter loop
    window.mainloop()
    return

# Function to print the ID Card
def print_id_card(frameM):
    # Get the ID card window geometry
    x = frameM.winfo_rootx()
    y = frameM.winfo_rooty()
    width = frameM.winfo_width() + x
    height = frameM.winfo_height() + y

    # Capture the window content as an image
    image = ImageGrab.grab(bbox=(x, y, width, height))

    save_directory = "/Users/shehuibrahim/Downloads/BIS698/HSMS_BIS698/IDcard"
    filename = f"{today}_{formatted_id}.png"
    save_path = os.path.join(save_directory, filename)


    # save_path = filedialog.asksaveasfilename(defaultextension=".png",
    #                                            filetypes=[("PNG files", "*.png")])
    if save_path:
        image.save(save_path)
        try:
            os.system(f'open "{save_path}"')
            os.startfile(save_path, "print")  # Trigger the print dialog to print the saved image
        except Exception as e:
            print(e)

# Run the function to create the ID card window
create_id_card_window()