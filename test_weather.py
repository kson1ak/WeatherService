import pytest
from unittest.mock import patch
from weather_client import get_weather

@patch('weather_client.requests.get')
def test_get_weather_success(mock_get):
    # Имитируем полный ответ API
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

    # Проверяем все 5 параметров
    assert result == {
        "city": "Москва",
        "temp": 15.5,
        "description": "ясно",
        "wind_speed": 4.2,
        "humidity": 72
    }

@patch('weather_client.requests.get')
def test_get_weather_not_found(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 404
    assert get_weather("UnknownCity") is None