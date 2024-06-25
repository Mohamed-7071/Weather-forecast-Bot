import requests

def get_location_info(country_name):
    url = f'https://restcountries.com/v3.1/name/{country_name}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        
        if data:
            country_info = data[0]  # Get the first result
            name = country_info.get('name', {}).get('common', 'N/A')
            population = country_info.get('population', 'N/A')
            latlng = country_info.get('latlng', ['N/A', 'N/A'])
            lat = latlng[0]
            lng = latlng[1]
            
            return {
                'name': name,
                'population': population,
                'latitude': lat,
                'longitude': lng
            }
        else:
            return {'error': 'No location data available'}
    
    except requests.RequestException as e:
        return {'error': f'Error fetching location data: {str(e)}'}

def get_weather(latitude, longitude):
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': True
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        current_weather = data.get('current_weather')
        
        if current_weather:
            temperature = current_weather.get('temperature')
            windspeed = current_weather.get('windspeed')
            weathercode = current_weather.get('weathercode')
            
            return {
                'temperature': temperature,
                'windspeed': windspeed,
                'weathercode': weathercode
            }
        else:
            return {'error': 'No current weather data available'}
    
    except requests.RequestException as e:
        return {'error': f'Error fetching weather data: {str(e)}'}

# Get the country name from user input
country_name = input("Enter the name of the country: ")
location_info = get_location_info(country_name)

if 'error' in location_info:
    print(location_info['error'])
else:
    print(f"Name: {location_info['name']}")
    print(f"Population: {location_info['population']}")
    print(f"Latitude: {location_info['latitude']}")
    print(f"Longitude: {location_info['longitude']}")
    
    # Fetch and print weather information
    weather_info = get_weather(location_info['latitude'], location_info['longitude'])
    
    if 'error' in weather_info:
        print(weather_info['error'])
    else:
        print(f"Temperature: {weather_info['temperature']}°C")
        print(f"Windspeed: {weather_info['windspeed']} km/h")
        print(f"Weather Code: {weather_info['weathercode']}")
