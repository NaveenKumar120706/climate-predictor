import requests
import pandas as pd
import os
from datetime import datetime, timedelta
API_KEY = '4b5e665056ca440b85e103828250208'
BASE_URL = 'http://api.weatherapi.com/v1'
def fetch_historical_weather(city, date):
    url = f"{BASE_URL}/history.json?key={API_KEY}&q={city}&dt={date}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed for {date}: {response.status_code}")
        return None
def generate_historical_dataset(city, years=50, output_path='weather/ml_model/historical_weather.csv'):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * years)
    current_date = start_date
    all_data = []

    print(f"Fetching data from {start_date.date()} to {end_date.date()} for {city}")

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        data = fetch_historical_weather(city, date_str)

        if data:
            try:
                hourly_data = data['forecast']['forecastday'][0]['hour']
                df = pd.json_normalize(hourly_data)
                all_data.append(df)
            except Exception as e:
                print(f"Error parsing {date_str}: {e}")

        current_date += timedelta(days=1)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final_df.to_csv(output_path, index=False)
        print(f"Saved full historical dataset to {output_path}")
    else:
        print("No data collected.")
if __name__ == '__main__':
    generate_historical_dataset("Chennai", years=1)
