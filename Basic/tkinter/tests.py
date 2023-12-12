import tkinter

window = tkinter.Tk()
window.title("Test")
window.minsize(width=500, height=300)

#Label

label = tkinter.Label(text="Text", font=("Arial", 24, "bold"))
label.pack()

#Button

def button_clicked():
    label["text"] = input.get()

button = tkinter.Button(text="Click Me", command=button_clicked)
button.pack()

#Entry

input = tkinter.Entry(width=15)
input.pack()

window.mainloop()