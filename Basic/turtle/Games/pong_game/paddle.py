from turtle import Turtle
import random
MOVE_DISTANCE = 10
UP = 90
DOWN = 270

class Paddle(Turtle):
    def __init__(self, pos):
        super().__init__()
        self.shape("square")
        self.shapesize(1, 5)
        self.setheading(UP)
        self.color("white")
        self.pu()
        self.init_pos = pos
        self.ball_y = 0
        self.ball_dir = 0
        self.goto(self.init_pos)

    def move(self):
        if (self.ycor() < 260 and self.ycor() > -260) or (self.ycor() >= 260 and self.heading() == DOWN) or (self.ycor() <= -260 and self.heading() == UP):
            self.fd(MOVE_DISTANCE)

    def easy(self):
        if self.ycor() > 240:
            self.setheading(DOWN)
        elif self.ycor() < -240:
            self.setheading(UP)

    def medium(self):
        if self.ball_dir == 45:
            if (self.ycor() + random.randint(15, 40)) < self.ball_y:
                self.setheading(UP)
        elif self.ball_dir == 315:
            if (self.ycor() - random.randint(15, 40)) > self.ball_y:
                self.setheading(DOWN)

    def hard(self):
        if self.ball_dir == 45:
            if (self.ycor() + random.randint(10, 30)) < self.ball_y:
                self.setheading(UP)
        elif self.ball_dir == 315:
            if (self.ycor() - random.randint(10, 30)) > self.ball_y:
                self.setheading(DOWN)

    def restart(self):
        self.goto(self.init_pos)
        self.setheading(UP)

    def up(self):
        if self.heading() != UP:
            self.setheading(UP)

    def down(self):
        if self.heading() != DOWN:
            self.setheading(DOWN)