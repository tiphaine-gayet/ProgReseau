import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# Essayer une position centrale
pwm.set_pwm(0, 0, 300)
time.sleep(2)

# Essayer une position extrême
pwm.set_pwm(0, 0, 150)
time.sleep(2)

# Retour à la position centrale
pwm.set_pwm(0, 0, 300)
