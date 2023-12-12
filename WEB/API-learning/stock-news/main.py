import requests, datetime, os
from twilio.rest import Client

today = datetime.datetime.now()
day_1 = today - datetime.timedelta(days=1)
day_2 = today - datetime.timedelta(days=2)
last_month = today - datetime.timedelta(days=30)
ALPHAVANTAGEAPI_KEY = "YY3HL8UY93NCYY67"
NEWSAPI_KEY = "2a4effb9b1c346faae9b22512b38954c"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
parameters_alpha = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGEAPI_KEY,
}

response_alpha = requests.get("https://www.alphavantage.co/query", params=parameters_alpha)
data_alpha = response_alpha.json()
time_series = data_alpha["Time Series (Daily)"]
day_1_close = float(time_series[f"{day_1.date()}"]["4. close"]) 
day_2_close = float(time_series[f"{day_2.date()}"]["4. close"])

per_change = 0
value_up = "🔻"
if day_1_close > day_2_close:
    per_change = (day_1_close - day_2_close)/day_2_close * 100
    value_up = "🔺"
else:
    per_change = (day_2_close - day_1_close)/day_1_close * 100


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
parameters_news = {
    "q": COMPANY_NAME,
    "from": last_month,
    "sortBy": "publishedAt",
    "apiKey": NEWSAPI_KEY,
}

response_news = requests.get("https://newsapi.org/v2/everything", params=parameters_news)
data_news = response_news.json()
last_articles = data_news["articles"][:3]
formatted_articles = [f"Headline: {article['title']}, \n\nBrief: {article['description']}" for article in last_articles]

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
print(os.environ['TWILIO_ACCOUNT_SID'])
account_sid = os.environ['TWILIO_ACCOUNT_SID'] #AC3d1b269d4b312fe2607069331d7307bf
auth_token = os.environ['TWILIO_AUTH_TOKEN'] #10a149645426d567aa200190d0b4599b
client = Client(account_sid, auth_token)

if day_1_close < day_2_close - (day_2_close * 0.05) or day_1_close > day_2_close + (day_2_close * 0.05):
    message = client.messages.create(
                                body=f'{STOCK}: {value_up}{round(per_change, 2)}% \n{formatted_articles[0]} \n\n{formatted_articles[1]} \n\n{formatted_articles[2]}',
                                from_='+15855586152',
                                to='+5511976725978'
                            ) 

    print(message.status)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

