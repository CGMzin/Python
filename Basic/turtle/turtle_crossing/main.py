import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
cars = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.move, "Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    cars.move(scoreboard.level)
    cars.refresh()
    scoreboard.refresh()

    if player.ycor() > 280:
        scoreboard.level += 1
        cars.level_up()
        player.restart()

    for car in cars.car_list:
        if player.distance(car) < 20:
            scoreboard.game_over()
            game_is_on = False

screen.exitonclick()
