import json
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class WeatherTool:

    GEOCODING_URL = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    WEATHER_URL = (
        "https://api.open-meteo.com/v1/forecast"
    )

    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    def _request_json(self, url: str) -> dict:

        request = Request(
            url,
            headers={
                "User-Agent": "AI-Buddy/1.0"
            }
        )

        with urlopen(request, timeout=10) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    def _get_location(self, city: str) -> dict:

        url = (
            f"{self.GEOCODING_URL}"
            f"?name={quote(city)}"
            f"&count=1"
            f"&language=en"
            f"&format=json"
        )

        data = self._request_json(url)

        results = data.get("results")

        if not results:
            return {
                "success": False,
                "message": f"Could not find the city '{city}'."
            }

        location = results[0]

        return {
            "success": True,
            "name": location.get("name"),
            "country": location.get("country"),
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude")
        }

    def get_weather(self, city: str) -> dict:

        if not city:
            return {
                "success": False,
                "message": "City name is required."
            }

        if not isinstance(city, str):
            return {
                "success": False,
                "message": "City name must be text."
            }

        city = city.strip()

        if not city:
            return {
                "success": False,
                "message": "City name cannot be empty."
            }

        try:

            location = self._get_location(city)

            if not location["success"]:
                return location

            latitude = location["latitude"]
            longitude = location["longitude"]

            weather_url = (
                f"{self.WEATHER_URL}"
                f"?latitude={latitude}"
                f"&longitude={longitude}"
                f"&current="
                f"temperature_2m,"
                f"relative_humidity_2m,"
                f"apparent_temperature,"
                f"weather_code,"
                f"wind_speed_10m"
                f"&timezone=auto"
            )

            weather_data = self._request_json(
                weather_url
            )

            current = weather_data.get(
                "current",
                {}
            )

            temperature = current.get(
                "temperature_2m"
            )

            feels_like = current.get(
                "apparent_temperature"
            )

            humidity = current.get(
                "relative_humidity_2m"
            )

            wind_speed = current.get(
                "wind_speed_10m"
            )

            weather_code = current.get(
                "weather_code"
            )

            condition = self.WEATHER_CODES.get(
                weather_code,
                "Unknown"
            )

            return {
                "success": True,
                "city": location["name"],
                "country": location["country"],
                "temperature": (
                    f"{temperature}°C"
                    if temperature is not None
                    else None
                ),
                "feels_like": (
                    f"{feels_like}°C"
                    if feels_like is not None
                    else None
                ),
                "humidity": (
                    f"{humidity}%"
                    if humidity is not None
                    else None
                ),
                "wind_speed": (
                    f"{wind_speed} km/h"
                    if wind_speed is not None
                    else None
                ),
                "condition": condition,
                "weather_code": weather_code,
                "timezone": weather_data.get(
                    "timezone"
                ),
                "message": (
                    f"The current weather in "
                    f"{location['name']} is "
                    f"{condition} with a temperature "
                    f"of {temperature}°C."
                )
            }

        except HTTPError as error:

            return {
                "success": False,
                "message": (
                    f"Weather service returned "
                    f"HTTP error {error.code}."
                )
            }

        except URLError:

            return {
                "success": False,
                "message": (
                    "Unable to connect to the "
                    "weather service."
                )
            }

        except TimeoutError:

            return {
                "success": False,
                "message": (
                    "Weather service request timed out."
                )
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Unable to fetch weather data."
                ),
                "error": str(error)
            }