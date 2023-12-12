from turtle import Turtle, Screen
import random

is_race_on = False
screen = Screen()
screen.setup(width=500, height=400)
bet = screen.textinput(title="Make your bet", prompt="Wich turtle will win the race? Enter a color: ")
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
turtles = []

if bet:
    is_race_on = True

for i in range(0, 6):
    turtles.append(Turtle("turtle"))
    turtles[i].pu()
    turtles[i].color(colors[i])
    turtles[i].goto(-230, -70 + (30*i))

while is_race_on:
    for turtle in turtles:
        turtle.fd(random.randint(0,10))
        if turtle.xcor() > 230:
            is_race_on = False
            if bet == turtle.pencolor():
                print(f"You've won! The winner is {turtle.pencolor()} turtle")
            else:
                print(f"You've lost! The winner is {turtle.pencolor()} turtle")
            break

screen.exitonclick()