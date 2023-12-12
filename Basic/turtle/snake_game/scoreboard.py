from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.pu()
        self.goto(0, 260)
        self.color("white")
        self.speed("fastest")
        self.score = 0
        with open('./data.txt') as data:
            self.high_score = int(data.read())
        self.refresh()

    def refresh(self):
        self.clear()
        self.write(f"Score: {self.score}  High Score: {self.high_score}", align= "center", font=("Courier", 24, "bold"))

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open('./data.txt', mode="w") as data:
                data.write(str(self.high_score))
        self.score = 0 
        self.refresh()

    """ def game_over(self):
        self.home()
        self.write(f"GAME OVER", align= "center", font=("Courier", 24, "bold")) """