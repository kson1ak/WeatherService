import requests

# Передайте свой API_KEY для работы программы
# API_KEY = "Ваш_API_KEY"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = { "q": city, "appid": API_KEY, "units": "metric", "lang": "ru" }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get("name"),
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "humidity": data["main"]["humidity"]
            }
        return None
    except Exception:
        return None

if __name__ == "__main__":
    city_input = input("Введите название города: ").strip()
    result = get_weather(city_input)
    if result:
        print(f"\nТекущая погода:")
        print(f"Город: {result['city']}")
        print(f"Температура: {result['temp']}°C")
        print(f"Описание: {result['description']}")
        print(f"Скорость ветра: {result['wind_speed']}м/с")
        print(f"Влажность: {result['humidity']}%")
    else:
        print("Ошибка: город не найден или сервис недоступен.")