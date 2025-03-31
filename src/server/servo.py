import Adafruit_PCA9685

try:
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(50)
    print("PCA9685 detected and initialized successfully.")
except Exception as e:
    print("Error detecting PCA9685:", e)
