from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from random import randint, choice
import pyperclip
import json

# ---------------------------- FIND PASSWORD ------------------------------------ #

def find_password():
    try:
        user_entry = website_entry.get()

        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data Found")
    else:
        for data_item in data:
            if data_item == user_entry:
                password = data[data_item]["password"]
                email = data[data_item]["email"]
                messagebox.showinfo(title=data_item, message=f"Email: {email} \nPassword: {password}")
            else:
                messagebox.showinfo(title="Error", message=f"No details for {user_entry} exists")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    numbers_list = [choice(numbers) for _ in  range(randint(2, 4))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]


    password_list = letters_list + numbers_list + symbols_list

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Ooops", message="Please make sure you have not left any fields empty")
    else:
        is_ok = messagebox.askokcancel(title="Website", message=f"These are the details entered: "
                                                                f"\nWebsite: {website} "
                                                                f"\nEmail:{email}\nPassword:{password}"
                                                                f"\nIs it okay to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_files:
                    data = json.load(data_files)
            except FileNotFoundError:
                with open("data.json", "w") as data_files:
                    json.dump(new_data, data_files, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_files:
                    json.dump(data, data_files, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

            messagebox.showinfo(title="Success", message="You have successfully entered your details!")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.config(padx=150, pady=50, bg="yellow")
window.title("Password Manager")
input_image_path = "pngegg.png"
original_image = Image.open(input_image_path)
target_width = 200
width_percent = (target_width / float(original_image.size[0]))
target_height = int((float(original_image.size[1]) * float(width_percent)))
resized_image = original_image.resize((target_width, target_height))
img = ImageTk.PhotoImage(resized_image)
canvas = Canvas(window, width=200, height=200, highlightthickness=0, bg="yellow")
canvas.create_image(0, 0, anchor='nw', image=img)
canvas.grid(row=0, column=1, pady=20)

#Label
website_label = Label(text="Website:", font=("Arial", 10), bg="yellow")
website_label.grid(row=1, column=0)

email_label = Label(text="Email:", font=("Arial", 10), bg="yellow")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:", font=("Arial", 10), bg="yellow")
password_label.grid(row=3, column=0)

#Entries

website_entry = Entry(width=30)
website_entry.grid(row=1, column=1, columnspan=1)

email_entry = Entry(width=50)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "vladimir@gmail .com")
password_entry = Entry(width=30)
password_entry.grid(row=3, column=1)

#Button

generate_password_button = Button(text="Generate Password", font=("Arial", 10), command=generate_password)
generate_password_button.grid(row=3, column=2)

add_password_button = Button(text="Add Password", width=30, font=("Arial", 10), command=save)
add_password_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", font=("Arial", 10), width=15, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()