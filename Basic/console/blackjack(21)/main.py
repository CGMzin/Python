from art import logo, cheap, cards
import random

############### Our Blackjack House Rules #####################

## The deck is unlimited in size. 
## There are no jokers. 
## The Jack/Queen/King all count as 10.
## The the Ace can count as 11 or 1.
## Use the following list as the deck of cards:
## cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
## The cards in the list have equal probability of being drawn.
## Cards are not removed from the deck as they are drawn.
## The computer is the dealer.

def generateCard():
    card = random.choice(cards)
    cards.remove(card)
    return card

def increaseValue(card, points):
    value = 0
    if card[:-1] == "j" or card[:-1] == "q" or card[:-1] == "k":
        value = 10
    elif card[:-1] == "1":
        if points < 11:
            value = 11
        else:
            value = 1
    else:
        value = int(card[:-1])
    
    return value

end = False
while not end:
    again = True
    print(logo)
    card = ""
    pValues = []
    dValues = []
    pFirstCard = generateCard()
    dFirstCard = generateCard()
    pValues.append(increaseValue(pFirstCard, 0))
    dValues.append(increaseValue(dFirstCard, 0))
    pCards = [cheap[pFirstCard]]
    dCards = [cheap[dFirstCard]]
    pTotal = 0
    dTotal = 0
    while again:
        pTotal = sum(pValues)
        dTotal = sum(dValues)
        print("Your cards:")
        print(*pCards)
        print(f"Your points: {pTotal}\n")
        print("Dealer cards:")
        print(*dCards)

        if pTotal < 21 and dTotal < 21:
            answer = input("\nWant a new card (y or n)? ")
            if answer.lower() == "y":
                card = generateCard()
                pCards.append(cheap[card])
                pValues.append(increaseValue(card, pTotal))
            if dTotal < 18:
                card = generateCard()
                dCards.append(cheap["secret"])
                dValues.append(increaseValue(card, dTotal))
            if answer.lower() != "y" and dTotal >= 18:
                if pTotal > dTotal:
                    print(f"\n\nYour points: {pTotal}")
                    print(f"Dealer points: {dTotal}")
                    print("You win!!!") 
                else:
                    print(f"\n\nYour points: {pTotal}")
                    print(f"Dealer points: {dTotal}")
                    print("You lose the game!")
                again = False
        elif pTotal > 21 or dTotal > 21:
            if pTotal > 21 and dTotal < 22:
                print(f"\n\nYour points: {pTotal}")
                print(f"Dealer points: {dTotal}")
                print("You lose the game!")
            elif pTotal < 21 and dTotal > 21:
                print(f"\n\nYour points: {pTotal}")
                print(f"Dealer points: {dTotal}")
                print("You win!!!")
            else:
                print("Draw!!")
            again = False
        elif pTotal == 21 or dTotal == 21:
            if pTotal == 21:
                print(f"\n\nYour points: {pTotal}")
                print(f"Dealer points: {dTotal}")
                print("You win!!!")
            else:
                print(f"\n\nYour points: {pTotal}")
                print(f"Dealer points: {dTotal}")
                print("You lose the game!")
            again = False
    answer = input("\nWant to play again (y or n)? ")
    if answer.lower() != "y":
        end = True