from turtle import Turtle
import random
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 3
car_list = []

class CarManager:
    def __init__(self):
        for _ in range(5):
            car = Turtle("square")
            car.color(random.choice(COLORS))
            car.pu()
            car.shapesize(1, 2)
            car.setheading(180)
            car.goto(random.randint(300, 1000), random.randint(-240, 240))
            car_list.append(car)
        self.car_list = car_list

    def move(self, level):
        for car in car_list:
            car.fd(STARTING_MOVE_DISTANCE + (MOVE_INCREMENT * (level - 1)))

    def refresh(self):
        for car in car_list:
            if car.xcor() < (random.randint(320, 360) * -1):
                car.goto(random.randint(300, 350), random.randint(-240, 240))

    def level_up(self):
        self.__init__()
        for car in car_list:
            car.goto(random.randint(300, 1000), random.randint(-240, 260))


