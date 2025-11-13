import appdaemon.plugins.hass.hassapi as hass
import os
import pandas as pd
from datetime import datetime, timedelta

class garmin_data(hass.Hass):
    def initialize(self):
        # Schedule the function to run every hour
        self.run_every(self.process_csv, "now", 60)

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
                total_elevation_gain_last_7_days = self.calculate_elevation_gain_days(df, 7, activity_type="Running")
                total_elevation_gain_last_4_weeks = self.calculate_elevation_gain_weeks(df, 4, activity_type="Running")
                # Find the most recent run
                most_recent_run = df.loc[df["Activity Type"] == "Running"].sort_values(by="Start Time", ascending=False).iloc[0]
                most_recent_run_distance = round(most_recent_run["Distance (km)"], 2)
                most_recent_run_duration = most_recent_run["Duration (h:m:s)"]
                most_recent_run_average_heart_rate = most_recent_run["Average Heart Rate (bpm)"]
                most_recent_run_elevation_gain = most_recent_run["Elevation Gain (m)"]

                # Calculate distances for specific gear
                total_distance_New_Balance_1080 = self.calculate_total_distance(df, "Running", gear="New Balance 1080")
                total_distance_Kinvara_15 = self.calculate_total_distance(df, "Running", gear="Kinvara v15")
                total_distance_Glyc_Max = self.calculate_total_distance(df, "Running", gear="Brooks Glycerin Max")
                total_distance_Cascadia_18 = self.calculate_total_distance(df, "Running", gear="Brooks Cascadia v18")
                total_distance_Endorphin_Pro_4 = self.calculate_total_distance(df, "Running", gear="Saucony Endorphin Pro 4")
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
                self.update_sensor("sensor.garmin_most_recent_run_distance", most_recent_run_distance, "Distance")
                self.update_sensor("sensor.garmin_most_recent_run_duration", most_recent_run_duration, "Time", "h:m:s")
                self.update_sensor("sensor.garmin_most_recent_run_average_heart_rate", most_recent_run_average_heart_rate,"av. HR", "bpm")
                self.update_sensor("sensor.garmin_most_recent_run_elevation_gain", most_recent_run_elevation_gain, "HM Gain", "m")
                self.update_sensor("sensor.garmin_distance_New_Balance_1080", total_distance_New_Balance_1080, "New Balance 1080 Gelaufene Kilometer")
                self.update_sensor("sensor.garmin_distance_Kinvara_15", total_distance_Kinvara_15, "Kinvara 15 Gelaufene Kilometer")
                self.update_sensor("sensor.garmin_elevation_gain_last_7_days", total_elevation_gain_last_7_days, "7days HM", "m")
                self.update_sensor("sensor.garmin_elevation_gain_last_4_weeks", total_elevation_gain_last_4_weeks, "4weeks HM", "m")
                self.update_sensor("sensor.garmin_distance_Glyc_Max", total_distance_Glyc_Max, "Brooks Glycerin Max Gelaufene Kilometer")
                self.update_sensor("sensor.garmin_distance_Cascadia_18", total_distance_Cascadia_18, "Brooks Cascadia v18 Gelaufene Kilometer")
                self.update_sensor("sensor.garmin_distance_Endorphin_Pro_4", total_distance_Endorphin_Pro_4, "Saucony Endorphin Pro 4 Gelaufene Kilometer")
                self.log("Sensor updates completed successfully.")
            else:
                self.log("CSV file does not contain a 'Distance (km)' column.")

        except Exception as e:
            # Use repr() to avoid issues if exception types implement non-standard __str__/__format__
            try:
                self.log(f"Error processing the CSV file: {e!r}")
            except Exception:
                self.log("Error processing the CSV file: <unrepresentable exception>")

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
    def calculate_elevation_gain_days(self, df, days, activity_type=None):
        last_days = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        query = df["Start Time"] > last_days
        if activity_type:
            query &= df["Activity Type"] == activity_type
        return round(df.loc[query, "Elevation Gain (m)"].astype(float).sum(), 2)
    def calculate_elevation_gain_weeks(self, df, weeks, activity_type=None):
        last_weeks = (datetime.now() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
        query = df["Start Time"] > last_weeks
        if activity_type:
            query &= df["Activity Type"] == activity_type
        return round(df.loc[query, "Elevation Gain (m)"].astype(float).sum(), 2)
    def update_sensor(self, sensor, state, friendly_name, unit="km"):
        # Sensor immer setzen, aber bei Wert 0 als String "0"
        try:
            val = None
            try:
                val = float(state)
            except Exception:
                val = None
            if val is not None and val == 0.0:
                state = "0"
            self.set_state(sensor, state=str(state), attributes={
                "unit_of_measurement": unit,
                "friendly_name": friendly_name
            })
        except Exception as e:
            try:
                self.log(f"Failed to set state for {sensor}. state type={type(state)}, state={state!r}, attrs={{'unit_of_measurement': unit, 'friendly_name': friendly_name}}, error={e!r}")
            except Exception:
                self.log(f"Failed to set state for {sensor}. error={e!r}")
