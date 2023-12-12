from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color("white")
        self.speed("fastest")
        self.player_score = 0
        self.enemy_score = 0
        self.refresh()

    def refresh(self):
        self.clear()
        self.made_line()
        self.goto(0, 200)
        self.write(f"{self.player_score}      {self.enemy_score}", align= "center", font=("OCR", 60, "bold"))

    def made_line(self):
        self.goto(0, -300)
        self.setheading(90)
        self.pensize(5)
        while self.ycor() < 300:
            self.fd(10)
            self.pu()
            self.fd(10)
            self.pd()
        self.pu()

    def player_point(self):
        self.player_score += 1

    def enemy_point(self):
        self.enemy_score += 1