import requests
import inquirer
from inquirer.themes import BlueComposure

units = dict(metric="°C", imperial="°F")


def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    unit = inquirer.list_input("Metric or imperial?", choices=["metric", "imperial"])
    # inquirer.prompt([unit], theme=BlueComposure())
    params = {
        "q": city_name,
        "appid": api_key,
        "units": unit,
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        main = data["main"]
        wind = data["wind"]
        weather = data["weather"][0]

        # Extracting specific information
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        weather_description = weather["description"]
        wind_speed = wind["speed"]

        # Printing the weather details
        print(f"Weather in {city_name}:")
        print(f"Temperature: {temperature}{"°F" if unit == "imperial" else "°C"}")
        print(f"Pressure: {pressure} hPa")
        print(f"Humidity: {humidity}%")
        print(f"Description: {weather_description}")
        print(f"Wind Speed: {wind_speed} m/s")

    else:
        print("City not found or error fetching data.")


if __name__ == "__main__":
    api_key = "d1cce3a7f8feaf27450e3b475acef7b3"
    city_name = input("Enter city name: ")
    get_weather(city_name, api_key)
