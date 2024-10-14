# Weather Data ETL Pipeline

## Overview

This is a sample ETL pipeline for weather data. It retrieves data from spesified stations in spesific year and months. The data is transformed, cleaned, processed to generate some stats such as average, minimum, maximum, and year-over-year (YoY) temperature differences. The final processed data is stored in a SQLite database and can be optionally uploaded to AWS S3 for further use or analysis.

## Project Structure

The project is organized into several modules following the ETL structure:
```graphql
.
├── data/                # Folder to store downloaded weather and station data
│   ├── weather/         # Contains weather data CSVs
│   └── station.csv      # Contains station data CSV
│   └── temp_stats.csv   # Final processed data CSV
├── src/
│   ├── extract.py       # Handles data extraction from API
│   ├── transform.py     # Handles data transformation and cleaning
│   ├── load.py          # Handles loading data into SQLite database
│   └── boto_upload.py   # Uploads final data to AWS S3
├── config.py            # Contains project-specific configurations
├── sql/
│   ├── create_table.sql # SQL query for creating the database table
│   └── insert_data.sql  # SQL query for inserting data into the database
└── main.py              # Main script to run the entire ETL process
```

## Configuration (config.py)

The configuration file config.py has project settings:

```python
# config.py
weather_station_url = "http://geogratis.gc.ca/services/geoname/en/geonames.csv"
weather_url = "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={}&Year={}&Month=9&Day=3&time=LST&timeframe=1&submit=Download+Data"
station_ids = [2953, 31688]
years = [2022, 2023, 2024]
```

## ETL Process

### 1. Extract

The `extract.py` module fetches data from the weather station.
- Downloads station metadata and saves it as `station.csv`.
- Fetches weather data for all defined stations and years, saving each station year combination as a CSV file.

### 2. Transform

The `transform.py` module processes the downloaded CSV files:
- Loads the weather and station data.
- Rounds latitude and longitude values to match weather data and station data.
- Cleans the data by dropping rows with missing temperature values.
- Calculates the average, minimum, and maximum temperatures by station, year, and month.
- Calculates the year-over-year (YoY) average temperature difference.
- Saves the processed data into a CSV file for review `temp_stats.csv`.

### 3. Load

The `load.py` module is responsible for loading the processed data into a SQLite database:
- It reads SQL queries from external files to create the table and insert the data.
- Connects to the SQLite database `weather_data.db`.
- Creates a table with the required schema.
- Inserts the transformed data into the table.

#### SQL Structure:
- **Create Table (`create_table.sql`)**:
    ```sql
    CREATE TABLE IF NOT EXISTS weather_data (
        latitude DECIMAL,
        longitude DECIMAL,
        station_name TEXT,
        climate_id TEXT,
        datetime TEXT,
        temp DECIMAL,
        year INT,
        month INT,
        temperature_celsius_avg DECIMAL(5, 2),
        temperature_celsius_min DECIMAL(5, 2),
        temperature_celsius_max DECIMAL(5, 2),
        temperature_celsius_yoy_avg DECIMAL(5, 2),
        feature_id TEXT,
        map TEXT
    );
    ```

- **Insert Data (`insert_data.sql`)**:
    ```sql
    INSERT INTO weather_data (latitude, longitude, station_name, climate_id, datetime, temp, year, month, temperature_celsius_avg, temperature_celsius_min, temperature_celsius_max, temperature_celsius_yoy_avg, feature_id, map)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ```

### 4. Upload to S3

The `s3_upload.py` module allows uploading the processed CSV to an S3 bucket for backup or further analysis. It:
- Connects to AWS S3 using credentials.
- Uploads the file in `temp_stats.csv` to the specified bucket and key.

---

## Running the Project

To run the entire ETL process, you can use the `main.py` script. It orchestrates the execution of the extraction, transformation, loading, and optional S3 upload steps.

```python
from src.extract import extract
from src.transform import transform
from src.load import load
from src.boto_upload import upload_to_s3

if __name__ == "__main__":
    # Step 1: Extract
    extract()

    # Step 2: Transform
    df = transform()

    # Step 3: Load
    load(df)

    # Step 4: Upload to S3
    save_to_s3(df, bucket_name, file_name)
```

---

## Future Enhancements

1. More logging
2. Improving data validation
3. Using orchestration and cloud integration
