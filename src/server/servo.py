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
    pwm.set_pwm(channel, 0, position)

def turn_camera_right():
    """Turn the camera 50 units to the right."""
    global pwm0_pos
    pwm0_pos = ctrl_range(pwm0_pos + 50, pwm0_max, pwm0_min)
    move_servo(0, pwm0_pos)
    time.sleep(1)

def turn_camera_left():
    """Turn the camera 50 units to the left."""
    global pwm0_pos
    pwm0_pos = ctrl_range(pwm0_pos - 50, pwm0_max, pwm0_min)
    move_servo(0, pwm0_pos)
    time.sleep(1)

if __name__ == "__main__":
    move_servo(0, pwm0_init)  # Ensure the servo starts at the initial position
    pwm.set_pwm(pwm, 0, 150)
