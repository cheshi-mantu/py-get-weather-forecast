import os
import requests

def get_coordinates(api_key, city, country_code):
    try:
        geo_api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country_code}&limit=1&appid={api_key}"
        response = requests.get(geo_api_url)

        if response.status_code == 200:
            geo_data = response.json()
            if geo_data:
                coordinates = geo_data[0]['lat'], geo_data[0]['lon']
                return coordinates
            else:
                print("No coordinates found for the provided city and country.")
                return None
        else:
            print(f"Geo API call failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error making Geo API call: {e}")
        return None

def get_weather(api_key, coordinates):
    try:
        weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?lat={coordinates[0]}&lon={coordinates[1]}&units=metric&lang=en&appid={api_key}"
        response = requests.get(weather_api_url)

        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            print(f"Weather API call failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error making Weather API call: {e}")
        return None

if __name__ == "__main__":
    # Get API key, country code, and city from environment variables
    api_key = os.getenv("WEATHER_API_KEY")
    country_code = os.getenv("WEATHER_COUNTRY_CODE")
    city = os.getenv("WEATHER_CITY")

    if not all([api_key, country_code, city]):
        print("Please set WEATHER_API_KEY, WEATHER_COUNTRY_CODE, and WEATHER_CITY environment variables.")
    else:
        # Get coordinates from Geo API
        coordinates = get_coordinates(api_key, city, country_code)

        if coordinates:
            # Get weather data using coordinates
            weather_data = get_weather(api_key, coordinates)

            if weather_data:
                # Extract and print specific fields from the weather data
                print("Weather Information:")
                print(f"Weather: {weather_data['weather'][0]['main']}")
                print(f"Description: {weather_data['weather'][0]['description']}")
                print(f"Temperature: {weather_data['main']['temp']} °C")
                print(f"Pressure: {weather_data['main']['pressure']} hPa")
                print(f"Visibility: {weather_data.get('visibility', 'N/A')} meters")
                print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
                print(f"Wind Direction: {weather_data['wind']['deg']} degrees")
                print(f"City ID: {weather_data['id']}")
                print(f"City Name: {weather_data['name']}")
            else:
                print("Error getting weather information.")
