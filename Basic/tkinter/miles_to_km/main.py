from tkinter import *

font = ("Arial", 12)

window = Tk()
window.title('Miles to Km Converter')
window.minsize(width=250, height=150)
window.configure(padx=30, pady=30)

def convert():
    label_value.configure(text=str(round(float(entry.get()) * 1.609, 1))) 

inv_label = Label()
inv_label.grid(row=0, column=0)
inv_label.configure(padx=30)

entry = Entry(width=13)
entry.grid(row=0, column=1)

label_miles = Label(text="Miles", font=font)
label_miles.configure(padx=10)
label_miles.grid(row=0, column=2)

label_equal = Label(text="is equal to", font=font)
label_equal.grid(row=1, column=0)

label_value = Label(text="0", justify="center", font=font)
label_value.grid(row=1, column=1)

label_km = Label(text="Km", font=font)
label_km.grid(row=1, column=2)

button = Button(text="Calculate", font=font, width=7, command=convert)
button.grid(row=2, column=1)

window.mainloop()