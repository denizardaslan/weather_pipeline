import pandas as pd
import glob
import os
import numpy as np


def transform():
    # Load station data
    station_df = pd.read_csv("./data/station.csv")

    # Load all weather data files
    weather_files = glob.glob(os.path.join("./data/weather", "*.csv"))
    weather_df = pd.concat((pd.read_csv(f) for f in weather_files), ignore_index=True)

    # Handle missing temperature values
    missing_temp = weather_df["Temp (°C)"].isnull().sum()
    if missing_temp > 0:
        print("Dropping rows with missing temperature data")
    weather_df = weather_df.dropna(subset=["Temp (°C)"])

    # Round coordinates for both dataframes
    weather_df["Longitude (x)"] = np.floor(weather_df["Longitude (x)"])
    weather_df["Latitude (y)"] = np.floor(weather_df["Latitude (y)"])
    station_df["latitude"] = np.floor(station_df["latitude"])
    station_df["longitude"] = np.floor(station_df["longitude"])

    # Rename columns for merging
    weather_df = weather_df.rename(
        columns={"Longitude (x)": "longitude", "Latitude (y)": "latitude"}
    )

    # Merge weather and station data
    df = pd.merge(weather_df, station_df, how="left", on=["longitude", "latitude"])

    # Keep only relevant columns
    df = df[
        [
            "latitude",
            "longitude",
            "Station Name",
            "Climate ID",
            "Date/Time (LST)",
            "Temp (°C)",
            "Year",
            "Month",
            "feature.id",
            "map",
        ]
    ]

    # Rename columns for consistency
    df.columns = [
        "latitude",
        "longitude",
        "station_name",
        "climate_id",
        "datetime",
        "temp",
        "year",
        "month",
        "feature_id",
        "map",
    ]

    # Calculate temp avg, min, max
    monthly_avg_temp = (
        df.groupby(["station_name", "year", "month"])
        .agg(
            temperature_celsius_avg=("temp", "mean"),
            temperature_celsius_min=("temp", "min"),
            temperature_celsius_max=("temp", "max"),
        )
        .reset_index()
    )

    # Calculate YoY average temperature difference
    monthly_avg_temp["temperature_celsius_yoy_avg"] = monthly_avg_temp.groupby("month")[
        "temperature_celsius_avg"
    ].diff()

    # Merge back to original dataframe to maintain all columns
    df = pd.merge(
        df,
        monthly_avg_temp[
            [
                "station_name",
                "year",
                "month",
                "temperature_celsius_avg",
                "temperature_celsius_min",
                "temperature_celsius_max",
                "temperature_celsius_yoy_avg",
            ]
        ],
        on=["station_name", "year", "month"],
        how="left",
    )

    df.to_csv("mydata.csv")

    return df
