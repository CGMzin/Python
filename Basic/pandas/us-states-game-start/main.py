import turtle, pandas

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "./blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

data = pandas.read_csv("./50_states.csv")
correct_answers = []
missed_states = []
score = 0

t = turtle.Turtle()
t.pu()
t.hideturtle()
font = ("Courier", 7, "bold")

while len(correct_answers) < 50:
    answer_state = screen.textinput(title=f"{score}/50 States Correct", prompt="What's another state name?").title()

    if answer_state == "Exit":
        break
    for row in data.state:
        if row == answer_state and (answer_state not in correct_answers):
            t.goto(int(data[data["state"] == answer_state]["x"]), int(data[data["state"] == answer_state]["y"]))
            t.write(answer_state, False, "center", font)
            correct_answers.append(answer_state)
            score += 1

missed_states = [state for state in data.state if state not in correct_answers]
missed_states_data = pandas.DataFrame(missed_states)
missed_states_data.to_csv("./missed_states.csv")