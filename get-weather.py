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

def send_weather_to_telegram(api_key, chat_id, city, weather_data):
    try:
        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        bot_api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        
        message = f"Weather in {city} (id={weather_data['id']})\n" \
                  f"Weather: {weather_data['weather'][0]['main']}\n" \
                  f"Description: {weather_data['weather'][0]['description']}\n" \
                  f"Temperature: {weather_data['main']['temp']} °C\n" \
                  f"Pressure: {weather_data['main']['pressure']} hPa\n" \
                  f"Wind Speed: {weather_data['wind']['speed']} m/s\n" \
                  f"Wind Direction: {weather_data['wind']['deg']} degrees\n" \
                  f"Visibility: {weather_data['visibility']} meters"
        
        params = {
            'chat_id': chat_id,
            'text': message,
        }

        response = requests.post(bot_api_url, params=params)

        if response.status_code == 200:
            print("Weather data sent to Telegram.")
        else:
            print(f"Error sending message to Telegram. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

if __name__ == "__main__":
    api_key = os.getenv("WEATHER_API_KEY")
    country_code = os.getenv("WEATHER_COUNTRY_CODE")
    city = os.getenv("WEATHER_CITY")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not all([api_key, country_code, city, telegram_chat_id]):
        print("Please set WEATHER_API_KEY, WEATHER_COUNTRY_CODE, WEATHER_CITY, and TELEGRAM_CHAT_ID environment variables.")
    else:
        coordinates = get_coordinates(api_key, city, country_code)

        if coordinates:
            weather_data = get_weather(api_key, coordinates)

            if weather_data:
                send_weather_to_telegram(api_key, telegram_chat_id, city, weather_data)
            else:
                print("Error getting weather information.")
        else:
            print("Error getting coordinates.")
