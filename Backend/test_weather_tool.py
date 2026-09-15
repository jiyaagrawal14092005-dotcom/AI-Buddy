from app.tools.weather import WeatherTool


weather_tool = WeatherTool()


print("=== WEATHER: JAIPUR ===")

print(
    weather_tool.get_weather(
        "Jaipur"
    )
)


print("\n=== WEATHER: DELHI ===")

print(
    weather_tool.get_weather(
        "Delhi"
    )
)


print("\n=== EMPTY CITY ===")

print(
    weather_tool.get_weather(
        ""
    )
)


print("\n=== INVALID CITY TYPE ===")

print(
    weather_tool.get_weather(
        12345
    )
)


print("\n=== UNKNOWN CITY ===")

print(
    weather_tool.get_weather(
        "XYZUnknownCity12345"
    )
)