#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# Contributor: CyberOrg - jigish.gohil@gmail.com - https://paraguide.in

import time
import board
from adafruit_bme280 import basic as adafruit_bme280
import math
import subprocess

# PWSWeather ID and PASSWORD
pwsid = ""
pwspassword = ""

# Weather Underground ID and PASSWORD
wunderid = ""
wunderpass = ""

# Windy API key
windykey = ""

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
#bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280.sea_level_pressure = 866

# Read temperature and pressure
temperature_celsius = bme280.temperature
pressure_hpa = bme280.pressure

# Convert temperature to Fahrenheit
temperature_fahrenheit = (temperature_celsius * 9/5) + 32

# Convert pressure to inches of mercury (inHg)
pressure_inhg = pressure_hpa * 0.02953

# Calculate dew point in Celsius
b = 17.62
c = 243.12
gamma = (b * temperature_celsius /(c + temperature_celsius)) + math.log(bme280.humidity / 100.0)
dewpoint_celsius = (c * gamma) / (b - gamma)

# Convert dew point to Fahrenheit
dewpoint_fahrenheit = (dewpoint_celsius * 9/5) + 32

# Execute curl command for PWSWeather
curl_pws_command = 'curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "ID=%s&PASSWORD=%s&dateutc=now&tempf=%0.1f&humidity=%0.1f&baromin=%0.2f&dewptf=%0.1f&action=updateraw" "https://www.pwsweather.com/pwsupdate/pwsupdate.php"' % (pwsid, pwspassword, temperature_fahrenheit, bme280.relative_humidity, pressure_inhg, dewpoint_fahrenheit)
subprocess.run(curl_pws_command, shell=True)

# Execute curl command for Weather Underground
curl_wunder_command = 'curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "ID=%s&PASSWORD=%s&dateutc=now&tempf=%0.1f&humidity=%0.1f&baromin=%0.2f&dewptf=%0.1f&action=updateraw" "https://rtupdate.wunderground.com/weatherstation/updateweatherstation.php"' % (wunderid, wunderpass, temperature_fahrenheit, bme280.relative_humidity, pressure_inhg, dewpoint_fahrenheit)
subprocess.run(curl_wunder_command, shell=True)

# Execute curl command for Windy PWS update
curl_windy_command = 'curl -X GET "https://stations.windy.com/pws/update/%s?tempf=%0.1f&humidity=%0.1f&baromin=%0.2f&dewptf=%0.1f"' % (windykey, temperature_fahrenheit, bme280.relative_humidity, pressure_inhg, dewpoint_fahrenheit)
subprocess.run(curl_windy_command, shell=True)

