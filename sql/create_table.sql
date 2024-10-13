CREATE TABLE IF NOT EXISTS weather_data (
    latitude DECIMAL,
    longitude DECIMAL,
    station_name TEXT,
    climate_id TEXT,
    datetime TEXT,
    temp DECIMAL,
    year INT,
    month INT,
    feature_id TEXT,
    map TEXT,
    temperature_celsius_avg DECIMAL(5, 2),
    temperature_celsius_min DECIMAL(5, 2),
    temperature_celsius_max DECIMAL(5, 2),
    temperature_celsius_yoy_avg DECIMAL(5, 2)
);