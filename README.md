# Garmin Stats for Home Assistant using AppDaemon

## Introduction

This guide will help you set up Garmin Stats integration with Home Assistant using AppDaemon.

## Prerequisites

- Home Assistant installed and running
- AppDaemon installed and configured
- Garmin account

## Installation

1. go to AddOn Store and Install AppDaemon

## Configuration

1. Take the appdaemon.yaml coming with this repo and bring it to your installation path of AppDaemon on your server device
    
2. Important is to mount the app location to the homeassistant filesystem (app_dir)
3. Copy apps.yaml, garmin_data.py and garmin_download.py to /homeassistant/appdaemon/apps

## Usage

garmin_download.py is called every 10 minutes to fetch the last 5 activities (this will make sure you dont miss one if you didnt sync your watch for some time). Parameter available to modify.
Now the garmin_data.py file should be reading the activities.csv and publish the defined sensor signals to your hass. 
Gear Names need to be modified accordingly.


Todos:
- features to include
    - average heart rate last 5 runs
    - average heart rate last 4 weeks
    - 

    ## Screenshots

    ![Garmin Data in Home Assistant](/screenshots/1.jpeg)
    ![Garmin Data in Home Assistant2](/screenshots/2.jpeg)