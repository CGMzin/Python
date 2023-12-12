file = open(".\my_file.txt")
contents = file.read()
print(contents)
file.close() 

with open(".\my_file.txt", mode="a") as file:
    file.write("New text.")