import requests
import time

prices = []
time_index = 0
# Задаем интервал между проверками цены на eth
time_interval = 5
# Запускаем бесконечный цикл, который будет проверять цену на eth с указанным интервалом
# и сравнивать ее с ценой, которая была час назад и если разница больше 1% выдавать сообщение
while True:
    current_price = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT").json()["price"]
    try:
        if (float(current_price) / prices[time_index]) * 100 - 100 > 1:
            print("Разница больше процента")
        prices[time_index] = float(current_price)
    except IndexError:
        prices.append(float(current_price))
    time.sleep(time_interval)
    if time_index < (60 // time_interval) * 60:
        time_index += 1
    else:
        time_index = 0