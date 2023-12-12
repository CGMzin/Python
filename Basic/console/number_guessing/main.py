import random
from art import logo

print(logo)

NUMBER = random.randint(1, 100)
attempts = 0
end = False

def verify():
    global attempts, end
    if attempts == 0:
        end = True
    else:
        print(f"\nYou have {attempts} attempts remaining to guess the number.")
        guess = int(input("Make a guess: "))
        if guess == NUMBER:
            print(f"You got it! The answer was {NUMBER}.")
            end = True
        else:
            if guess < NUMBER:
                print("Too low.")
            else:
                print("Too high.")
            print("Guess again.")
            attempts -= 1
    

print("I'm thinking of a number between 1 and 100.")
difficulty = input("Choose a dificulty. Type 'easy' or 'hard': ")
if difficulty == "easy":
    attempts = 10
else:
    attempts = 5
while not end:
    verify()