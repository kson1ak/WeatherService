import pytest
from unittest.mock import patch
from weather_client import get_weather

# ТЕСТ 1: Проверка успешного получения и парсинга данных (Positive Scenario)
@patch('weather_client.requests.get')
def test_get_weather_success(mock_get):
    # Имитируем полный и корректный ответ от OpenWeather API
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Москва",
        "main": {
            "temp": 15.5,
            "humidity": 72
        },
        "weather": [{"description": "ясно"}],
        "wind": {"speed": 4.2}
    }
    result = get_weather("Moscow")
    # Проверяем, что клиент корректно извлек все 5 нужных нам параметров
    assert result == {
        "city": "Москва",
        "temp": 15.5,
        "description": "ясно",
        "wind_speed": 4.2,
        "humidity": 72
    }

# ТЕСТ 2: Проверка обработки ошибки 404 (Если город не найден)
@patch('weather_client.requests.get')
def test_get_weather_not_found(mock_get):
    # Имитируем ситуацию, когда API возвращает ошибку 404
    mock_response = mock_get.return_value
    mock_response.status_code = 404
    # Проверяем, что в этом случае клиент возвращает None, а не падает с ошибкой
    assert get_weather("UnknownCity") is None

# ТЕСТ 3: Проверка правильности формирования запроса (URL и параметры)
@patch('weather_client.requests.get')
def test_get_weather_params(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Лондон", "main": {"temp": 10, "humidity": 80},
        "weather": [{"description": "дождь"}], "wind": {"speed": 5}
    }
    get_weather("London")
    # Убеждаемся, что мы отправляем правильный город, метрическую систему и наш API-ключ
    args, kwargs = mock_get.call_args
    assert kwargs['params']['q'] == "London"
    assert kwargs['params']['units'] == "metric"
    assert kwargs['params']['appid'] == "7cf22bb257edeefb648f06363b4848b9"

# ТЕСТ 4: Проверка устойчивости к некорректному формату JSON (Missing Keys)
@patch('weather_client.requests.get')
def test_get_weather_invalid_json(mock_get):
    # Имитируем ответ со статусом 200, но с "битым" телом (отсутствуют ожидаемые ключи)
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"error": "some unexpected format"}
    # Проверяем, что блок try-except в клиенте поймает KeyError и вернет None
    result = get_weather("Berlin")
    assert result is None