from turtle import Turtle
import random
DIRECTIONS = {"UL": 135, "DL": 225, "UR": 45, "DR": 315}
DIRECTIONS_NAMES = ["UL", "DL", "UR", "DR"]

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(1, 1)
        self.setheading(DIRECTIONS[random.choice(DIRECTIONS_NAMES)])
        self.color("white")
        self.pu()

    def move(self):
        self.fd(13)

    def restart(self):
        self.home()
        self.setheading(DIRECTIONS[random.choice(DIRECTIONS_NAMES)])

    def refresh(self):
        #if ball touches top--------------------------------------------
        if self.ycor() >= 290 and self.heading() == DIRECTIONS["UL"]:
            self.setheading(DIRECTIONS["DL"])
        elif self.ycor() >= 290 and self.heading() == DIRECTIONS["UR"]:
            self.setheading(DIRECTIONS["DR"])
        #if ball touches bottom-----------------------------------------
        elif self.ycor() <= -290 and self.heading() == DIRECTIONS["DL"]:
            self.setheading(DIRECTIONS["UL"])
        elif self.ycor() <= -290 and self.heading() == DIRECTIONS["DR"]:
            self.setheading(DIRECTIONS["UR"])

    def collide(self):
        if self.heading() == DIRECTIONS["DL"]:
            self.setheading(DIRECTIONS["DR"])
        elif self.heading() == DIRECTIONS["UL"]:
            self.setheading(DIRECTIONS["UR"])
        elif self.heading() == DIRECTIONS["DR"]:
            self.setheading(DIRECTIONS["DL"])
        elif self.heading() == DIRECTIONS["UR"]:
            self.setheading(DIRECTIONS["UL"])
