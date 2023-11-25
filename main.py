import requests
from datetime import date
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_price_api_key = my_stock_price_api_key
news_api_key = my_news_api_key
date = date.today()
TWILTO_SID = my_id
TWILTO_AUTH_TOKEN = MY_TOKEN
my_number = your_phone

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_price_api_key
}


# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
response_stock = requests.get(STOCK_ENDPOINT, params=parameters)
data = response_stock.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

# day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

dif = abs(yesterday_closing_price) - abs(day_before_yesterday_closing_price)
dif_percentage = (dif/yesterday_closing_price)*100

if dif_percentage > 5:
    parameters_news = {
        "qInTitle": COMPANY_NAME,
        "from": date,
        "sortBy": "popularity",
        "apiKey": news_api_key,
    }

    response_news = requests.get(NEWS_ENDPOINT, params=parameters_news)
    data_news = response_news.json()["articles"]
    #get the first 3 new pieces using python slice operator
    first_3_articles = data_news[:3]

    # to send a separate message with each article's title and description to your phone number.
    formatted_articles = [f"Headline: {article['title']}. \nBrief:{article['description']}" for article in first_3_articles]
    client = Client(TWILTO_SID,TWILTO_AUTH_TOKEN)
    # send each article separately
    for article in formatted_articles:
        message = client.messages.create(
                             body=article,
                             from_='+15017122661', #from virtual Twilio number
                             to=my_number
                         )

