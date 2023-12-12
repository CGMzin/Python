from tkinter import *
from tkinter import messagebox
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pd.read_csv("./data/unknown_words.csv").to_dict(orient='records')
except FileNotFoundError:
    data = pd.read_csv("./data/french_words.csv").to_dict(orient='records')

current_card = {}

def remove_word():
    data.remove(current_card)
    new_csv = pd.DataFrame(data)
    new_csv.to_csv("./data/unknown_words.csv", sep=",", index=False)
    new_word()

def new_word():
    global current_card, flip_timer
    print(len(data))
    window.after_cancel(flip_timer)
    current_card = random.choice(data)
    canvas.itemconfig(canvas_country, text="French", fill="black")
    canvas.itemconfig(canvas_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_bg, image=card_front)
    flip_timer = window.after(3000, flip)

def flip():
    canvas.itemconfig(canvas_bg, image=card_back)
    canvas.itemconfig(canvas_country, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=current_card["English"], fill="white")

window = Tk()
window.title("Flash Card")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

flip_timer = window.after(3000, flip)

#Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas_bg = canvas.create_image(400, 266, image=card_front)
canvas_country = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

#Button
img_yes = PhotoImage(file="./images/right.png")
btn_yes = Button(image=img_yes, highlightthickness=0, border=0, command=remove_word)
btn_yes.grid(row=1, column=0)

img_no = PhotoImage(file="./images/wrong.png")
btn_no = Button(image=img_no, highlightthickness=0, border=0, command=new_word)
btn_no.grid(row=1, column=1)

new_word()

window.mainloop()