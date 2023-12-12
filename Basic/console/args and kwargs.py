def add(*args):
    result = 0
    for num in args:
        result += num
    return result

print(add(1, 5, 5, 10, 50))

class Car:
    def __init__(self, **kw):
        self.make = kw.get("make")
        self.model = kw.get("model")
        self.color = kw.get("color")
        self.seats = kw.get("seats")

my_car = Car(make="Toyota", model="Corolla")
print(my_car.make, my_car.model, my_car.color, my_car.seats)