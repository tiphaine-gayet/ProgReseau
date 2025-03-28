import time
from rpi_ws281x import *
import argparse
from src.server import move, infra, detectLine

# LED strip configuration:
LED_COUNT      = 12      # Number of LED pixels.
LED_PIN        = 18       # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class LED:
    def __init__(self):
        self.LED_COUNT      = 12      # Number of LED pixels.
        self.LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 5      # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    # Define functions which animate LEDs in various ways.
    # def colorWipe(self, R, G, B):
    # def colorWipe(self, color, wait_ms=0):
    #     """Wipe color across display a pixel at a time."""
    #     for i in range(self.strip.numPixels()):
    #         self.strip.setPixelColor(i, color)
    #         self.strip.show()
    #         time.sleep(wait_ms / 1000.0)

    def colorWipe(self, R, G, B):
        color = Color(R,G,B)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def blink(self, r=0, g=0, b=0, time_sec=1):
        print(f"Blinking {self.strip.numPixels()} LEDs with color ({r}, {g}, {b})")
        self.colorWipe(r, g, b)  # Turn ON all LEDs
        time.sleep(time_sec)
        print("Turning off LEDs")
        self.colorWipe(0, 0, 0)  # Turn OFF all LEDs

    def blink_shot(self):
        for _ in range(2):
            self.blink(r=255, g=0, b=0, time_sec=0.5)
            time.sleep(0.5)

if __name__ == '__main__':
    led = LED()
    try:  
        while True:  
            led.colorWipe(255, 0, 0)  # red
            time.sleep(1)  
            led.colorWipe(0, 255, 0)  # green
            time.sleep(1)  
            led.colorWipe(0, 0, 255)  # blue
            time.sleep(1) 
            infra.shoot()
    except:  
        led.colorWipe(0,0,0)  # Lights out
