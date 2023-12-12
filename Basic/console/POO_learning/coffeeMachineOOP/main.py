from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

menu = Menu()
coffeeMaker = CoffeeMaker()
moneyMachine = MoneyMachine()

end = False

while not end:
    answer = input("What would you like? (espresso/latte/cappuccino/): ")
    if answer == "off":
        end = True
        break
    elif answer == "report":
        coffeeMaker.report()
        moneyMachine.report()
    else:
        item = menu.find_drink(answer)
        if coffeeMaker.is_resource_sufficient(item):
            if moneyMachine.make_payment(item.cost):
                coffeeMaker.make_coffee(item)