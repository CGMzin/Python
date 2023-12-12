from flask import Flask
import random

app = Flask(__name__)
num = random.randint(0, 9)

@app.route('/')
def hello_world():
    return '<h1>Guess a number between 0 and 9</h1><img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">'

@app.route('/<int:number>')
def check_num(number):
    if number > num:
        return '<h1 style="color: purple;">Too high, try again!</h1><img src="https://media.giphy.com/media/l4pTky87QVuvbzwnS/giphy.gif">'
    elif number < num:
        return '<h1 style="color: red;">Too low, try again!</h1><img src="https://media.giphy.com/media/bMycGOQLESDCEnLNUz/giphy.gif">'
    else:
        return '<h1 style="color: green;">You found me!</h1><img src="https://media.giphy.com/media/pslmyy93fH2JboH8qB/giphy.gif">'
if __name__ == "__main__":
    app.run()
