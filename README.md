# junior-back-end

Скачайте все файлы и запустите файл main.py

В файле clinet.py ответ на задание 1. Его можно запустить поменяв параметры криптовалют, чтобы парсить другие криптовалюты

В файле main.py находится API. Запустите код через 
```
python main.py
```
и тестируйте сервер. 

#№ примеры тестов
```
import requests

# Получение всех цен для тикера "btc"
response = requests.get("http://127.0.0.1:8000/prices/all?ticker=btc")
print(response.json())  # Печатает ответ сервера в формате JSON

# Получение последней цены для тикера "eth"
response = requests.get("http://127.0.0.1:8000/prices/latest?ticker=eth")
print(response.json())

# Получение цен по дате для тикера "btc"
response = requests.get("http://127.0.0.1:8000/prices/by_date?ticker=btc&date=1672531200")
print(response.json())
```
