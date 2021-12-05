import time
import sys
import RPi.GPIO as GPIO

SERVO_PIN = 17
servo = None

# run this at startup
def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(SERVO_PIN, GPIO.OUT)

  servo = GPIO.PWM(SERVO_PIN, 50)  # GPIO 17 for PWM with 50Hz
  servo.start(2.5)  # Initialization

def stop():
  servo.stop()

# sets the servo to rotate to direction
def setServo(direction):
  if servo == None:
    raise Exception("Must run setup() before calling setServo()")
  else:
    servo.ChangeDutyCycle(direction)


# use this to test just the read functionality
if __name__ == "__main__":
  if len(sys.argv) != 1:
    print("Usage: servo.py <servoDirection>")
  else:
    print("Setting servo to " + sys.argv[0])
    setup()
    setServo(int(sys.argv[0]))
    stop()