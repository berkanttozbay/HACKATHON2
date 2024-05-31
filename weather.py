import requests

class Weather:
    def __init__(self, api_key, city):
        self.api_key = api_key
        self.city = city

    def get_visibility(self):
        url = f"http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={self.city}&aqi=no"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching data from API: {response.status_code}")
            return None
        data = response.json()
        print(f"API Response: {data}")  # Debugging

        if 'current' in data and 'vis_km' in data['current']:
            visibility = data['current']['vis_km']
            print(f"Visibility from API: {visibility} kilometers")
            return visibility
        else:
            condition = data.get('current', {}).get('condition', {}).get('text', 'Clear')
            return self.estimate_visibility(condition)

    def estimate_visibility(self, condition):
        condition_visibility_map = {
            'Clear': 20,
            'Partly cloudy': 15,
            'Clouds': 10,
            'Mist': 5,
            'Fog': 1,
            'Rain': 8,
            'Snow': 3,
            'Haze': 5,
        }
        visibility = condition_visibility_map.get(condition, 10)
        print(f"Estimated visibility based on condition ({condition}): {visibility} kilometers")
        return visibility

    def get_weather_conditions(self):
        url = f"http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={self.city}&aqi=no"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching data from API: {response.status_code}")
            return None
        data = response.json()
        print(f"Weather Conditions Data: {data}")  # Debugging
        return data.get('current', {}).get('condition', {}).get('text', 'Clear')
