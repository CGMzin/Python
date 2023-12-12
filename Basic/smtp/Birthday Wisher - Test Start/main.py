import smtplib, random
import datetime as dt

my_email = "email"
password = "password"
    
now = dt.datetime.now()

if now.weekday() == 1:
    text = ""
    with open("./quotes.txt") as text_file:
        complete_txt = text_file.readlines()
        text = random.choice(complete_txt)
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f"Subject:Monday Motivation\n\n{text}")
        