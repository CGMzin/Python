from turtle import Turtle, Screen, colormode
import colorgram,random

colors = colorgram.extract('./image.jpg', 15)

xi, yi = -250, -240
t = Turtle()
colormode(255)
t.speed(20)
t.hideturtle()
t.pu()
t.goto(xi, yi)

for i in range(10):
    for j in range(10):
        t.dot(25, random.choice(colors).rgb)
        t.fd(55)
    t.goto(xi, yi + (i + 1) * 55)
    
screen = Screen()
screen.exitonclick()