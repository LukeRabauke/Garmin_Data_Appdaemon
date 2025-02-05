#just to play around with the garmin data csv file

import os
import pandas as pd
from datetime import datetime, timezone, timedelta


csv_file = "activities.csv"

    
# Read the CSV file using pandas
df = pd.read_csv(csv_file)

# Ensure the 'distance' column exists and sum its values
if "Distance (km)" in df.columns:
    #sum all values in columg "Distance (km)" and with "Activity Type" == "Running"
    total_distance_running = df.loc[df["Activity Type"] == "Running", "Distance (km)"].astype(float).sum()
    total_distance_all_activities = df["Distance (km)"].astype(float).sum()
    print("Total distance of Running Activies: {:.2f} km".format(total_distance_running))
    print("Total distance of all activities: {:.2f} km".format(total_distance_all_activities))
    # Drop rows where either "Start Time" or "End Time" is missing
    df = df.dropna(subset=["Start Time", "End Time"]) 
    df["Start Time"] = df["Start Time"].str.split('T').str[0]
    df["End Time"] = df["End Time"].str.split('T').str[0]  
    #sum all values in columg "Distance (km)" and with "Activity Type" == "Running" and Year is 2025 in "Start Time" with format 2023-12-03T16:00:29+01:00
    total_distance_running_2025 = df.loc[(df["Activity Type"] == "Running") & (df["Start Time"].str.contains("2025")), "Distance (km)"].astype(float).sum()
    print("Total distance of Running Activies in 2025: {:.2f} km".format(total_distance_running_2025))
    #sum all values in columg "Distance (km)" and with "Activity Type" == "Running" and Year is 2024 in "Start Time" with format 2023-12-03T16:00:29+01:00
    total_distance_running_2024 = df.loc[(df["Activity Type"] == "Running") & (df["Start Time"].str.contains("2024")), "Distance (km)"].astype(float).sum()
    print("Total distance of Running Activies in 2024: {:.2f} km".format(total_distance_running_2024))

    # Beispiel für das aktuelle Datum und die Uhrzeit im gewünschten Format
    today = pd.Timestamp.today().strftime('%Y-%m-%d')
    print(today)  # Beispiel-Ausgabe: 2025-02-02
    #sum all values in columg "Distance (km)" and with "Activity Type" == "Running" and "Start Time" is today
    total_distance_running_today = df.loc[(df["Activity Type"] == "Running") & (df["Start Time"].str.contains(today)), "Distance (km)"].astype(float).sum()
    print("Total distance of Running Activies today: {:.2f} km".format(total_distance_running_today))
    #sum all values in columg "Distance (km)" and with "Activity Type" == "Running" and for the last 7 days using "Start Time" and formated_time
    last_7_days = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    total_distance_running_last_7_days = df.loc[(df["Activity Type"] == "Running") & (df["Start Time"] > last_7_days), "Distance (km)"].astype(float).sum()
    print("Total distance of Running Activies in the last 7 days: {:.2f} km".format(total_distance_running_last_7_days))
    # Find the most recent run based on today's date
    most_recent_run = df.loc[df["Activity Type"] == "Running"].sort_values(by="Start Time", ascending=False).iloc[0]
    most_recent_run_distance = most_recent_run["Distance (km)"]
    print("Most recent run distance: {:.2f} km".format(most_recent_run_distance))
    most_recent_run_duration = most_recent_run["Duration (h:m:s)"]
    print("Most recent run duration: {}".format(most_recent_run_duration))
    most_recent_run_average_heart_rate = most_recent_run["Average Heart Rate (bpm)"]
    print("Most recent run average heart rate: {}".format(most_recent_run_average_heart_rate))
    most_recent_run_elevation_gain = most_recent_run["Elevation Gain (m)"]  
    print("Most recent run elevation gain: {}".format(most_recent_run_elevation_gain))
    total_distance_Brooks_Glycerin_20 = df.loc[(df["Activity Type"] == "Running") & (df["Gear"].str.contains("Brooks Glycerin 20")), "Distance (km)"].astype(float).sum()
    print("Total distance of Running Activies with Brooks Glycerin 20: {:.2f} km".format(total_distance_Brooks_Glycerin_20))
    # do the same for new balane 1080 
    total_distance_New_Balance_1080 = df.loc[(df["Activity Type"] == "Running") & (df["Gear"].str.contains("New Balance 1080")), "Distance (km)"].astype(float).sum()
    print("Total distance of Running Activies with New Balance 1080: {:.2f} km".format(total_distance_New_Balance_1080))
    # do the same for Kinvara 15
    total_distance_Kinvara_15 = df.loc[(df["Activity Type"] == "Running") & (df["Gear"].str.contains("Kinvara v15")), "Distance (km)"].astype(float).sum()
    print("Total distance of Running Activies with Kinvara 15: {:.2f} km".format(total_distance_Kinvara_15))
else:
    print("CSV file does not contain a 'Distance (km)' column.")