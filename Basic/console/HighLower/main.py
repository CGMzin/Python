import random
from art import logo, vs
from gamedata import data

print(logo)

def formatdata(account):
    name = account["name"]
    descr = account["description"]
    country = account["country"]
    return f"{name}, {descr}, from {country}"

def compare(a, b):
    print(f"Compare A: {formatdata(a)}.")
    print(vs)
    print(f"\nAgainst B: {formatdata(b)}.")
    answer = input("Who has more followers? Type 'A' or 'B': ")
    return answer

lose = False
points = 0
a = random.choice(data)
b = random.choice(data)
if b == a:
    b = random.choice(data)

while not lose:
    answer = compare(a, b)

    if a["follower_count"] > b["follower_count"] and answer == "A":
        points += 1
        print(f"\nYou're right! Current score: {points}\n")
    elif a["follower_count"] < b["follower_count"] and answer == "B":
        points += 1
        print(f"\nYou're right! Current score: {points}\n")
    else:
        print(f"\nSorry, that's wrong. Final score: {points}\n")
        lose = True

    a, b = b, random.choice(data)
    if b == a:
        b = random.choice(data)