from turtle import Turtle, Screen, colormode
import random

turtle = Turtle()
colormode(255)
turtle.speed(20)

def gen_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

for i in range(0, 361, 5):
    turtle.color(gen_color())
    turtle.setheading(i)
    turtle.circle(100)

screen = Screen()
screen.exitonclick()