from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip, json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(6,10))]
    password_list += [choice(symbols) for _ in range(randint(4, 10))]
    password_list += [choice(numbers) for _ in range(randint(4, 10))]

    shuffle(password_list)

    passwd = "".join(password_list)

    entry_password.delete(0, END)
    entry_password.insert(0, passwd)
    pyperclip.copy(passwd)
# ---------------------------- SAVE / SEARCH PASSWORD ------------------------------- #
def save():

    new_data = {
        website.get().upper(): {
            "email": email_username.get(),
            "password": password.get()
        }
    }

    if len(website.get()) != 0 and len(password.get()) != 0 and len(email_username.get()) != 0:
        data = {}
        try:    
            with open(file="./Passwords.json", mode="r") as file:
                data = json.load(file)
                data.update(new_data)
        except FileNotFoundError:
            data = new_data
        finally:
            with open(file="./Passwords.json", mode="w") as file:
                json.dump(data, file, indent=4)
                entry_website.delete(0, END)
                entry_password.delete(0, END)
    else:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")

def find_password():
    data = {}
    try:    
        with open(file="./Passwords.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="ERROR", message="No Data File Found")
    finally:
        if entry_website.get().upper() in data.keys():
            messagebox.showinfo(entry_website.get().upper(), f"Email: {data[entry_website.get().upper()]['email']} \nPassword: {data[entry_website.get().upper()]['password']}")
        else:
            messagebox.showerror("Fail", "No details for the website exists")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

img = PhotoImage(file="./logo.png")

canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

#Labels
lbl_website = Label(text="Website:")
lbl_website.grid(row=1, column=0)

lbl_email_username = Label(text="Email/Username:")
lbl_email_username.grid(row=2, column=0)

lbl_password = Label(text="Password:")
lbl_password.grid(row=3, column=0)

#Entrys
website = StringVar()
entry_website = Entry(width=32, textvariable=website)
entry_website.grid(row=1, column=1)
entry_website.focus()

email_username = StringVar()
entry_email_username = Entry(width=50, textvariable=email_username)
entry_email_username.grid(row=2, column=1, columnspan=2)

password = StringVar()
entry_password = Entry(width=32, textvariable=password)
entry_password.grid(row=3, column=1)

#Buttons
btn_generate_password = Button(text="Generate Password", width=14, command=generate_password)
btn_generate_password.grid(row=3, column=2)

btn_add = Button(text="Add", width=42, command=save)
btn_add.grid(row=4, column=1, columnspan=2)

btn_search = Button(text="Search", width=14, command=find_password)
btn_search.grid(row=1, column=2)

window.mainloop()