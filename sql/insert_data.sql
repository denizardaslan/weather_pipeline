INSERT INTO weather_data (
    latitude, 
    longitude, 
    station_name, 
    climate_id, 
    datetime, 
    temp, 
    year, 
    month, 
    feature_id, 
    map,
    temperature_celsius_avg, 
    temperature_celsius_min, 
    temperature_celsius_max, 
    temperature_celsius_yoy_avg
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);