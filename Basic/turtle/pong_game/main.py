from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(width=1200, height=600)
screen.bgcolor("black")
screen.tracer(0)

difficulty = screen.textinput(title="Choose a difficulty", prompt="CHOOSE THE DIFFICULTY:\nHARD\nMEDIUM\nEASY")

player_paddle = Paddle((-585, 0))
enemy_paddle = Paddle((580, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player_paddle.up, "Up")
screen.onkey(player_paddle.down, "Down")
game_is_on = False

if difficulty:
    game_is_on = True

while game_is_on:
    time.sleep(0.05)
    scoreboard.refresh()
    screen.update()
    player_paddle.move()
    enemy_paddle.move()
    ball.move()
    ball.refresh()
    enemy_paddle.ball_y = ball.ycor()
    enemy_paddle.ball_dir = ball.heading()

    if ball.distance(player_paddle) < 60 and ball.xcor() < -570 or ball.distance(enemy_paddle) < 60 and ball.xcor() > 570:
        ball.collide()

    if difficulty.lower() == "easy":
        enemy_paddle.easy()
    elif difficulty.lower() == "medium":
        enemy_paddle.medium()
    elif difficulty.lower() == "hard":
        enemy_paddle.hard()

    if ball.xcor() > 600 or ball.xcor() < -610:
        if ball.xcor() < 1:
            scoreboard.enemy_point()
        else: 
            scoreboard.player_point()
        ball.restart()
        player_paddle.restart()
        enemy_paddle.restart()
        time.sleep(1)

screen.exitonclick()