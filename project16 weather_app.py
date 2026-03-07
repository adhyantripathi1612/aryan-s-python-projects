import requests
import os
import time
from datetime import datetime

api_key = os.getenv("OWM_API_KEY", "2e2c753d00f317e759670c19a13d62be")
base_url = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    print("\nFetching weather data... Please wait.")
    time.sleep(1)
    url = f"{base_url}?appid={api_key}&q={city}&units=metric"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print("Error fetching data. Check your internet connection.")
        return {"cod": 404, "message": "Network error"}

def display_temperature(data):
    if data.get("cod") == 200:
        main = data["main"]
        temp = round(main["temp"], 2)
        feels_like = round(main["feels_like"], 2)
        temp_min = round(main["temp_min"], 2)
        temp_max = round(main["temp_max"], 2)
        
        print("Temperature: {}C (Feels like {}C)".format(temp, feels_like))
        print("Min/Max: {}C / {}C".format(temp_min, temp_max))
    else:
        print("City not found or error occurred!")

def display_humidity(data):
    if data.get("cod") == 200:
        humidity = data["main"]["humidity"]
        print("Humidity: {}%".format(humidity))
    else:
        print("City not found or error occurred!")

def display_sunrise_sunset(data):
    if data.get("cod") == 200:
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")
        print("Sunrise: {} | Sunset: {}".format(sunrise, sunset))
    else:
        print("City not found or error occurred!")

def display_wind_speed(data):
    if data.get("cod") == 200:
        wind_speed = round(data["wind"]["speed"], 2)
        print("Wind Speed: {} m/s".format(wind_speed))
    else:
        print("City not found or error occurred!")

def display_sky_condition(data):
    if data.get("cod") == 200:
        sky = data["weather"][0]["description"].title()
        print("Sky Condition: {}".format(sky))
    else:
        print("City not found or error occurred!")

def display_location_info(data):
    if data.get("cod") == 200:
        lat = round(data["coord"]["lat"], 4)
        lon = round(data["coord"]["lon"], 4)
        print("Location: {}, {}".format(data['name'], data['sys']['country']))
        print("Latitude: {} | Longitude: {}".format(lat, lon))
    else:
        print("City not found or error occurred!")

def display_all_info(data):
    if data.get("cod") == 200:
        main = data["main"]
        weather = data["weather"][0]
        
        temp = round(main["temp"], 2)
        feels_like = round(main["feels_like"], 2)
        temp_min = round(main["temp_min"], 2)
        temp_max = round(main["temp_max"], 2)
        humidity = main["humidity"]
        wind_speed = round(data["wind"]["speed"], 2)
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")
        sky = weather["description"].title()
        lat = round(data["coord"]["lat"], 4)
        lon = round(data["coord"]["lon"], 4)
        
        print("\n" + "="*50)
        print("Weather Info for {}, {}".format(data['name'], data['sys']['country']))
        print("Temperature: {}C (Feels like {}C)".format(temp, feels_like))
        print("Min/Max: {}C / {}C".format(temp_min, temp_max))
        print("Humidity: {}%".format(humidity))
        print("Sunrise: {} | Sunset: {}".format(sunrise, sunset))
        print("Wind Speed: {} m/s".format(wind_speed))
        print("Sky Condition: {}".format(sky))
        print("Latitude: {} | Longitude: {}".format(lat, lon))
        print("="*50 + "\n")
    else:
        print("City not found! Please check the city name.")

def show_menu():
    print("WEATHER APP")
    print("=" * 30)
    print("1. Temperature")
    print("2. Humidity")
    print("3. Sunrise and Sunset")
    print("4. Wind Speed")
    print("5. Sky Condition")
    print("6. Location Info")
    print("7. All Weather Info")
    print("8. Exit")
    print("=" * 30)

def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == "8":
            print("Goodbye!")
            break
        elif choice in ["1", "2", "3", "4", "5", "6", "7"]:
            city = input("Enter city name: ").strip()
            if not city:
                print("City name cannot be empty!")
                input("Press Enter to continue...")
                continue
            
            data = get_weather_data(city)
            
            if choice == "1":
                display_temperature(data)
            elif choice == "2":
                display_humidity(data)
            elif choice == "3":
                display_sunrise_sunset(data)
            elif choice == "4":
                display_wind_speed(data)
            elif choice == "5":
                display_sky_condition(data)
            elif choice == "6":
                display_location_info(data)
            elif choice == "7":
                display_all_info(data)
        else:
            print("Invalid choice! Please select 1-8.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
