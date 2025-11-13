import appdaemon.plugins.hass.hassapi as hass
import os
import pandas as pd
from datetime import datetime, timedelta

class Marathon_Training_2025(hass.Hass):
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

                # Calculate Distance of Week 1 of Marathon Training in 2025, and date range is 2025-01-13 to 2025-01-19
                # week1

                total_distance_Marathon_Training_2025_W1 = self.filter_by_date_range(df, "Running", "2025-01-13", "2025-01-19")
                # week2
                total_distance_Marathon_Training_2025_W2 = self.filter_by_date_range(df, "Running", "2025-01-20", "2025-01-26")
                # week3
                total_distance_Marathon_Training_2025_W3 = self.filter_by_date_range(df, "Running", "2025-01-27", "2025-02-02")
                # week4
                total_distance_Marathon_Training_2025_W4 = self.filter_by_date_range(df, "Running", "2025-02-03", "2025-02-09")
                # week5
                total_distance_Marathon_Training_2025_W5 = self.filter_by_date_range(df, "Running", "2025-02-10", "2025-02-16")
                # week6
                total_distance_Marathon_Training_2025_W6 = self.filter_by_date_range(df, "Running", "2025-02-17", "2025-02-23")
                # week7
                total_distance_Marathon_Training_2025_W7 = self.filter_by_date_range(df, "Running", "2025-02-24", "2025-03-02")
                # week8
                total_distance_Marathon_Training_2025_W8 = self.filter_by_date_range(df, "Running", "2025-03-03", "2025-03-09")
                # week9
                total_distance_Marathon_Training_2025_W9 = self.filter_by_date_range(df, "Running", "2025-03-10", "2025-03-16")
                # week10
                total_distance_Marathon_Training_2025_W10 = self.filter_by_date_range(df, "Running", "2025-03-17", "2025-03-23")
                # week11
                total_distance_Marathon_Training_2025_W11 = self.filter_by_date_range(df, "Running", "2025-03-24", "2025-03-30")
                # week12
                total_distance_Marathon_Training_2025_W12 = self.filter_by_date_range(df, "Running", "2025-03-31", "2025-04-06")
                # total distance W1 till W12
                total_distance_Marathon_Training_2025 = self.filter_by_date_range(df, "Running", "2025-01-13", "2025-04-06")

                # Update sensors
                # sensor.garmin_distance_Marathon_Training_2025_W1
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W1", total_distance_Marathon_Training_2025_W1, "Week 1 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W2
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W2", total_distance_Marathon_Training_2025_W2, "Week 2 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W3
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W3", total_distance_Marathon_Training_2025_W3, "Week 3 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W4
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W4", total_distance_Marathon_Training_2025_W4, "Week 4 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W5
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W5", total_distance_Marathon_Training_2025_W5, "Week 5 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W6
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W6", total_distance_Marathon_Training_2025_W6, "Week 6 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W7
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W7", total_distance_Marathon_Training_2025_W7, "Week 7 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W8
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W8", total_distance_Marathon_Training_2025_W8, "Week 8 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W9
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W9", total_distance_Marathon_Training_2025_W9, "Week 9 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W10
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W10", total_distance_Marathon_Training_2025_W10, "Week 10 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W11
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W11", total_distance_Marathon_Training_2025_W11, "Week 11 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025_W12
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025_W12", total_distance_Marathon_Training_2025_W12, "Week 12 Freiburg")
                # sensor.garmin_distance_Marathon_Training_2025
                self.update_sensor("sensor.garmin_distance_Marathon_Training_2025", total_distance_Marathon_Training_2025, "Total Distance Freiburg")
                
            else:
                self.log("CSV file does not contain a 'Distance (km)' column.")

        except Exception as e:
            try:
                self.log(f"Error processing the CSV file: {e!r}")
            except Exception:
                self.log("Error processing the CSV file: <unrepresentable exception>")

    def calculate_total_distance(self, df, activity_type, year=None, month=None, days=None, weeks=None, gear=None, description=None):
        query = (df["Activity Type"] == activity_type)
        # i need to be able to filter for a specific date range in "Start Time" column and hand over start and end date as "2025-mm-dd"

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
        if description:
            query &= df["Description"].str.contains(description)
        return round(df.loc[query, "Distance (km)"].astype(float).sum(), 2)
    def filter_by_date_range(self, df, activity_type, start_date, end_date):
        mask = (df["Start Time"] >= start_date) & (df["Start Time"] <= end_date)
        #add activity type
        mask &= df["Activity Type"] == activity_type
        filtered_df = df.loc[mask]
        return round(filtered_df["Distance (km)"].astype(float).sum(), 2)
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

