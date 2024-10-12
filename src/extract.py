import requests as r
from config import weather_station_url, weather_url, station_ids, years


def extract():
    try:
        # Fetch and save station data
        station = r.get(weather_station_url)
        with open("data/station.csv", "w") as file:
            file.write(station.text)
            print("Station CSV saved successfully.")

        # Fetch and save weather data for each station and year
        for station in station_ids:
            for year in years:
                weather = r.get(weather_url.format(station, year))
                if weather.status_code == 200:
                    with open(f"data/weather/{station}-{year}.csv", "w") as file:
                        file.write(weather.text)
                        print(f"CSV saved for station {station} in {year}")
                else:
                    print(
                        f"Failed to retrieve data for station {station} in {year}. Status code: {weather.status_code}"
                    )

    except r.RequestException as e:
        print(f"Error fetching data from URL: {e}")
    except OSError as e:
        print(f"Error writing to CSV files: {e}")
