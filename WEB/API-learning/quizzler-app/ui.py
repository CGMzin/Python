from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR, padx=20, pady=20)
        
        self.txt_score = Label(text="Score: 0", font=("Arial", 25, "bold"), bg=THEME_COLOR, fg="white")
        self.txt_score.grid(row=0, column=1)
        
        self.canvas = Canvas(width=300, height=250)
        self.canvas_text = self.canvas.create_text(150, 125, text="", font=("Arial", 20, "italic"), width=280)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)
        
        img_no = PhotoImage(file="./images/false.png")
        img_yes = PhotoImage(file="./images/true.png")
        self.btn_yes = Button(image=img_yes, highlightthickness=0, command=self.answer_true)
        self.btn_yes.grid(row=2, column=0)
        self.btn_no = Button(image=img_no, highlightthickness=0, command=self.answer_false)
        self.btn_no.grid(row=2, column=1)
        
        self.get_next_question()
        
        self.window.mainloop()
        
    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.txt_score.configure(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.canvas_text, text=q_text)
        else:
            self.canvas.itemconfig(self.canvas_text, text="You've reached the end of the quiz")
            self.btn_no.config(state="disabled")
            self.btn_yes.config(state="disabled")

    def answer_true(self):
        self.give_feedback(self.quiz.check_answer("true"))

    def answer_false(self):
        self.give_feedback(self.quiz.check_answer("false"))

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.configure(bg="green")
            self.window.after(1000, self.get_next_question)
        else:
            self.canvas.configure(bg="red")
            self.window.after(1000, self.get_next_question)