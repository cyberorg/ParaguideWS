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

# Read temperature
temperature_celsius = bme280.temperature

# Convert temperature to Fahrenheit
temperature_fahrenheit = (temperature_celsius * 9/5) + 32

#Station altitude in meters
salti = 1375

# Pressure adjusted to sea level
pressure_hpa = bme280.pressure * (1 - (0.0065 * salti / (bme280.temperature + 0.0065 * salti + 273.15))) ** -5.257

# Convert pressure to inches of mercury (inHg)
pressure_inhg = pressure_hpa * 0.02953

# Calculate dew point in Celsius
a = 17.27
b = 237.7
alpha = ((a * temperature_celsius) / (b + temperature_celsius)) + math.log(bme280.humidity / 100.0)
dewpoint_celsius = (b * alpha) / (a - alpha)

# corrected to measured pressure
dew_point_corrected = dewpoint_celsius - ((0.66077 * (1.0 + (0.00115 * temperature_celsius))) * (1.0 + (0.48488 * math.log(bme280.pressure / 10))))

# Convert dew point to Fahrenheit
dewpoint_fahrenheit = (dew_point_corrected * 9/5) + 32

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

