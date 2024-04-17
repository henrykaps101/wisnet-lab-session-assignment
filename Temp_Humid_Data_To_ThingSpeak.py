import RPi.GPIO as GPIO
import dht11
import time
import datetime
import requests

# initializing GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# Reading data using pin 14
instance = dht11.DHT11(pin=14)

# ThingSpeak parameters
THINGSPEAK_API_KEY = 'J8T2DAT4OC8L808T'
THINGSPEAK_URL = f'https://api.thingspeak.com/update?api_key=J8T2DAT4OC8L808T&field1=0'

try:
    while True:
        result = instance.read()
        if result.is_valid():
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
           
            # Sending data to ThingSpeak platforms
            payload = {'field1': result.temperature, 'field2': result.humidity}
            try:
                response = requests.get(THINGSPEAK_URL, params=payload)
                if response.status_code == 200:
                    print("Data sent to ThingSpeak successfully")
                else:
                    print(f"Failed to send data to ThingSpeak: {response.status_code}")
            except Exception as e:
                print(f"Failed to send data to ThingSpeak: {e}")
           
        time.sleep(2)  # Delay
except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()