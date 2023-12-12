#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".

names_list = []
initial_text = ''
final_text = ''

with open('./Input/Names/invited_names.txt') as names:
    names_list = names.read().splitlines()

with open('./Input/Letters/starting_letter.txt') as initial:
    initial_text = initial.read()

for name in names_list:
    final_text = initial_text.replace("[name]", f"{name}")
    with open(f"./Output/ReadyToSend/letter_for_{name}.txt", mode="w") as new_file:
        new_file.write(final_text)