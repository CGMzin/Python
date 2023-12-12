from turtle import Turtle, Screen

turtle = Turtle()
turtle.shape("turtle")

angle = 0
sides = 3
turtle.pu()
turtle.goto(-50, 250)
turtle.speed(30)
turtle.pd()

while sides <= 20:
    angle = 360 / sides
    for _ in range(sides):
        turtle.fd(50)
        turtle.rt(angle)
    sides += 1

screen = Screen()
screen.exitonclick()