import pandas

data = pandas.read_csv("./nato_phonetic_alphabet.csv")
nato_dict = {row.letter:row.code for (index, row) in data.iterrows()}

sucess = False
while not sucess:
    word = input('Enter a word: ')
    try:
        print([nato_dict[letter.upper()] for letter in word])
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
    else:
        sucess = True