import requests
import json

def fetch_json_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None

def write_to_json(data, filename):
    if data:
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)
        print(f"JSON file '{filename}' created successfully")
    else:
        print("No data fetched from the API")

api_url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

json_data = fetch_json_data(api_url)

json_filename = 'data.json'

write_to_json(json_data, json_filename)