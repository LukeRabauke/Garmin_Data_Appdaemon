import subprocess
import appdaemon.plugins.hass.hassapi as hass
import os

class GarminDownload(hass.Hass):

    def initialize(self):
        self.log("GarminDownload App Initialized")
        #self.run_daily(self.download_garmin_data, "20:00:00")
        self.run_every(self.download_garmin_data, "now", 60)



    def download_garmin_data(self, kwargs):
        self.log("Starting Garmin data download")
        # please self.log the time of the download
        self.log(f"Download started at {self.datetime()}")
        command = [
            "python3", "/homeassistant/appdaemon/apps/garmin-connect-export/gcexport.py",
            "-d", "/homeassistant/appdaemon/apps/MyActivities_Json",
            "-c", "5",
            "--desc", "20",
            "-f", "json",
            "-u",
        ]
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            self.log(f"Garmin data download completed: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.log(f"Error downloading Garmin data: {e.stderr}", level="ERROR")