from data import MENU, resources

end = False
profit = 0

def report():
    for key in resources.keys():
        if key != "coffee":
            print(f"{key.capitalize()}: {str(resources[key])}ml")
        else:
            print(f"{key.capitalize()}: {str(resources[key])}g")
    print(f"Money: ${profit}")

def insertMoney():
    print("Please insert coins.")
    total = int(input("how many quarters?: ")) * 0.25
    total += int(input("how many dimes?: ")) * 0.1
    total += int(input("how many nickles?: ")) * 0.05
    total += int(input("how many pennies?: ")) * 0.01
    return total

def checkTransaction(cost):
    value = insertMoney()
    if value < cost:
        print("Sorry that's not enough money. Money refunded.")
        return False
    else:
        change = round(value - cost, 2)
        print(f"Here is ${change} in change.")
        global profit
        profit += cost
        return True

def check(ingredients):
    for item in ingredients:
        if resources[item] < ingredients[item]:
            print(f"Sorry there is not enough {item}.")
            return False
    return True

def makeCoffee(drink, ingredients):
    global resources
    for item in ingredients:
        resources[item] -= ingredients[item]
    print(f"Here is your {drink} ☕️. Enjoy!")

def order(drink):
    orderIngredients = MENU[drink]["ingredients"]
    if check(orderIngredients):
        if checkTransaction(MENU[drink]["cost"]):
            makeCoffee(drink, orderIngredients)

while not end:
    answer = input(("What would you like? (espresso/latte/cappuccino): "))
    if answer == "report":
        report()
    elif answer == "off":
        end = True
        break
    else:
        order(answer)