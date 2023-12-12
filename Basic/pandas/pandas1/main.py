import pandas

""" with open("./weather_data.csv") as data_file:
    data = data_file.readlines() """

""" import csv

with open("./weather_data.csv") as data_file:
    data = csv.reader(data_file)
    temperatures = []
    for row in data:
        if row[1] != "temp":
            temperatures.append(int(row[1]))
    print(temperatures) """
""" 
data = pandas.read_csv("./weather_data.csv")
print(data) """

data = pandas.read_csv("./2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
gray = len(data[data["Primary Fur Color"] == "Gray"])
cinnamon = len(data[data["Primary Fur Color"] == "Cinnamon"])
black = len(data[data["Primary Fur Color"] == "Black"])
""" for row in data['Primary Fur Color']:
    if row == "Gray":
        gray += 1
    elif row == "Cinnamon":
        cinnamon += 1
    if row == "Black":
        black += 1 """
new_data = {
    "Fur Color" : ["Gray", "Cinnamon", "Black"],
    "Count" : [gray, cinnamon, black]
}
new_dataframe = pandas.DataFrame(new_data)
new_dataframe.to_csv("./squirrel_count.csv")
