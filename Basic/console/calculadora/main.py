import art

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def div(a, b):
    return a / b

operations = {
    "+": add,
    "-": sub,
    "*": mult,
    "/": div
}

def calculator():
    print(art.logo)

    num1 = float(input("What's the first number?: "))
    for sym in operations:
        print(sym)
    cont = True

    while cont:
        op = input("Pick an operation: ")
        num2 = float(input("What's the next number?: "))
        func = operations[op]
        answer = func(num1, num2)

        print(f"{num1} {op} {num2} = {answer}")

        if input(f"Type 'y' to continue calculating with {answer}, or type 'n' to start a new calculation: ")  == "y":
            num1 = answer
        else:
            cont = False
            calculator()

calculator()