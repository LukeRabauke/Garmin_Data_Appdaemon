import appdaemon.plugins.hass.hassapi as hass
import os
import pandas as pd
from datetime import datetime, timedelta

class garmin_data(hass.Hass):
    def initialize(self):
        # Schedule the function to run every hour
        self.run_every(self.process_csv, "now", 3600)

    def process_csv(self, kwargs):
        csv_file = "/homeassistant/appdaemon/apps/MyActivities_Json/activities.csv"

        try:
            # Ausgabe des aktuellen Pfads
            current_path = os.path.dirname(os.path.abspath(__file__))
            self.log(f"Aktueller Pfad: {current_path}")

            # Read the CSV file using pandas
            df = pd.read_csv(csv_file)
            # Drop rows where either "Start Time" or "End Time" is missing
            df = df.dropna(subset=["Start Time", "End Time"])
            df["Start Time"] = df["Start Time"].str.split('T').str[0]
            df["End Time"] = df["End Time"].str.split('T').str[0]

            # Ensure the 'distance' column exists and sum its values
            if "Distance (km)" in df.columns:
                self.log(f"Preparing to process data from {csv_file}")

                # Calculate total distances
                total_distance_running = self.calculate_total_distance(df, "Running")
                total_distance_all_activities = round(df["Distance (km)"].astype(float).sum(), 2)

                # Calculate yearly distances
                yearly_distances = {year: self.calculate_total_distance(df, "Running", year) for year in range(2017, 2026)}

                # Calculate distances for year 2025 for each month
                monthly_distances_2025 = {month: self.calculate_total_distance(df, "Running", year=2025, month=month) for month in range(1, 13)}
                # Calculate distances for year 2024 for each month
                monthly_distances_2024 = {month: self.calculate_total_distance(df, "Running", year=2024, month=month) for month in range(1, 13)}

                # Calculate distances for the last 7 days and 4 weeks
                total_distance_running_last_7_days = self.calculate_total_distance(df, "Running", days=7)
                total_distance_running_last_4_weeks = self.calculate_total_distance(df, "Running", weeks=4)

                # Find the most recent run
                most_recent_run = df.loc[df["Activity Type"] == "Running"].sort_values(by="Start Time", ascending=False).iloc[0]
                most_recent_run_distance = round(most_recent_run["Distance (km)"], 2)
                most_recent_run_duration = most_recent_run["Duration (h:m:s)"]
                most_recent_run_average_heart_rate = most_recent_run["Average Heart Rate (bpm)"]
                most_recent_run_elevation_gain = most_recent_run["Elevation Gain (m)"]

                # Calculate distances for specific gear
                total_distance_New_Balance_1080 = self.calculate_total_distance(df, "Running", gear="New Balance 1080")
                total_distance_Kinvara_15 = self.calculate_total_distance(df, "Running", gear="Kinvara v15")

                # Update sensors
                self.update_sensor("sensor.garmin_distance_all_running", total_distance_running, "Alle Läufe")
                self.update_sensor("sensor.garmin_distance_all_activities", total_distance_all_activities, "Gesamte Kilometer alle Aktivitäten")
                for year, distance in yearly_distances.items():
                    self.update_sensor(f"sensor.garmin_distance_running_{year}", distance, str(year))
                for month, distance in monthly_distances_2025.items():
                    self.update_sensor(f"sensor.garmin_distance_running_2025_{month:02}", distance, f"2025-{month:02}")
                for month, distance in monthly_distances_2024.items():
                    self.update_sensor(f"sensor.garmin_distance_running_2024_{month:02}", distance, f"2024-{month:02}")
                self.update_sensor("sensor.garmin_distance_running_last_7_days", total_distance_running_last_7_days, "7 Tage")
                self.update_sensor("sensor.garmin_distance_running_last_4_weeks", total_distance_running_last_4_weeks, "4 Wochen")
                self.update_sensor("sensor.garmin_most_recent_run_distance", most_recent_run_distance, "Gelaufene Kilometer letzter Lauf")
                self.update_sensor("sensor.garmin_most_recent_run_duration", most_recent_run_duration, "Dauer letzter Lauf", "h:m:s")
                self.update_sensor("sensor.garmin_most_recent_run_average_heart_rate", most_recent_run_average_heart_rate, "Durchschnittliche Herzfrequenz letzter Lauf", "bpm")
                self.update_sensor("sensor.garmin_most_recent_run_elevation_gain", most_recent_run_elevation_gain, "Höhenmeter letzter Lauf", "m")
                self.update_sensor("sensor.garmin_distance_New_Balance_1080", total_distance_New_Balance_1080, "New Balance 1080 Gelaufene Kilometer")
                self.update_sensor("sensor.garmin_distance_Kinvara_15", total_distance_Kinvara_15, "Kinvara 15 Gelaufene Kilometer")

            else:
                self.log("CSV file does not contain a 'Distance (km)' column.")

        except Exception as e:
            self.log(f"Error processing the CSV file: {e}")

    def calculate_total_distance(self, df, activity_type, year=None, month=None, days=None, weeks=None, gear=None):
        query = (df["Activity Type"] == activity_type)
        if year:
            query &= df["Start Time"].str.contains(str(year))
        if month:
            query &= df["Start Time"].str.contains(f"{year}-{month:02}")
        if days:
            last_days = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            query &= df["Start Time"] > last_days
        if weeks:
            last_weeks = (datetime.now() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
            query &= df["Start Time"] > last_weeks
        if gear:
            query &= df["Gear"].str.contains(gear)
        return round(df.loc[query, "Distance (km)"].astype(float).sum(), 2)

    def update_sensor(self, sensor, state, friendly_name, unit="km"):
        self.set_state(sensor, state=state, attributes={
            "unit_of_measurement": unit,
            "friendly_name": friendly_name
        })