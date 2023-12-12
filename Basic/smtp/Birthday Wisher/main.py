import smtplib, random
import datetime as dt
import pandas as pd

my_email = "email"
password = "password"

data = pd.read_csv("./birthdays.csv").to_dict(orient='records')

now = dt.datetime.now()

for item in data:
    if item['month'] == now.month and item['day'] == now.day:
        with open(f'./letter_templates/letter_{random.randint(1, 3)}.txt') as txt:
            text = txt.read()
            text = text.replace('[NAME]', item['name'])

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=item['email'], msg=f"Subject:Happy Birthday\n\n{text}")
            

