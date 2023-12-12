import turtle as t
import random

turtle = t.Turtle()
t.colormode(255)

def gen_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

turtle.pensize(10)
turtle.speed(10)
angles = [0, 90, 180, 270]

for i in range(500):
    turtle.color(gen_color())
    turtle.fd(30)
    turtle.setheading(random.choice(angles))