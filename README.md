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
3. Copy apps.yaml and garmin_data.py to /homeassistant/appdaemon/apps

## Usage

Now the python file should be reading the activities.csv and publish the defined sensor signals to your hass.


Todos:
- include download also in own appdaemon + copy csv to correct path
- features to include
    - average heart rate last 5 runs
    - average heart rate last 4 weeks
    - 