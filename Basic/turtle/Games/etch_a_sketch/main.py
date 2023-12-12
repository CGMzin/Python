from turtle import Turtle, Screen

t = Turtle()
screen = Screen()

def fd():
    t.fd(10)

def bk():
    t.bk(10)

def rt():
    t.rt(10)

def lt():
    t.lt(10)

def clear():
    t.home()
    t.clear()


screen.onkey(fd, "w")
screen.onkey(bk, "s")
screen.onkey(lt, "a")
screen.onkey(rt, "d")
screen.onkey(clear, "c")
screen.listen()


screen.exitonclick()