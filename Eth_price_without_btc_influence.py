import requests

# Ввести за какой период времени провести анализ влияния btcusdt на ethusdt
days = 1000

# Получаем исторические данные о BTCUSDT и ETHUSDT за указанное время
response_btc = requests.get(f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit={days}")
response_eth = requests.get(f"https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1d&limit={days}")

# Помещаем ответ в json файл
btc_data = response_btc.json()
eth_data = response_eth.json()

# Вытаскиваем среднюю цену за день (открытие торгов + закрытие торгов + минимальная цена + максимальная цена)/4
eth, btc = [], []
for data in btc_data:
    btc.append((float(data[1]) + float(data[2]) + float(data[3]) + float(data[4])) / 4)
for data in eth_data:
    eth.append((float(data[1]) + float(data[2]) + float(data[3]) + float(data[4])) / 4)

# Считаем процент изменения в средней стоимости криптовалюты за день
btc_change, eth_change = [], []
for index in range(1, len(btc)):
    btc_change.append((btc[index] / btc[index - 1]) * 100 - 100)
for index in range(1, len(eth)):
    eth_change.append((eth[index] / eth[index - 1]) * 100 - 100)

# Считаем зависимости btc и eth
diff = []
for i in range(len(btc_change)):
    diff.append(abs(btc_change[i] - eth_change[i]))

corr = sum(diff) / len(diff)

# Заполняем таблицу дынными о цене ethusdt без учета влияния btcusdt
real_eth = {}
for index, num in enumerate(eth):
    real_eth[index] = (num / 100) * (100 - corr)

# Вывод цены ethusdt без влияния btcusdt
print("day -- price")
for day, price in real_eth.items():
    print(f"{day + 1} -- {price}")