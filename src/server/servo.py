import time
import Adafruit_PCA9685

# Initialize PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# Servo position limits
pwm0_init, pwm0_max, pwm0_min = 300, 450, 150
pwm0_pos = pwm0_init

def ctrl_range(value, max_val, min_val):
    """Ensure the value stays within the specified range."""
    return max(min(value, max_val), min_val)

def move_servo(channel, position):
    """Move servo to a specific position."""
    pwm.set_pwm(channel, 0, ctrl_range(position, pwm0_max, pwm0_min))

def turn_right():
    global pwm0_pos
    pwm0_pos = ctrl_range(pwm0_pos + 50, pwm0_max, pwm0_min)
    move_servo(0, pwm0_pos)
    time.sleep(1)

def turn_left():
    global pwm0_pos
    pwm0_pos = ctrl_range(pwm0_pos - 50, pwm0_max, pwm0_min)
    move_servo(0, pwm0_pos)
    time.sleep(1)
