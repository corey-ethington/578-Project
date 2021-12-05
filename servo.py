import time
import sys
import RPi.GPIO as GPIO

SERVO_PIN = 17
DUTY_CYCLE_MIN = 1
DUTY_CYCLE_MAX = 12
servo = None

# run this at startup
def setup():
  global servo
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(SERVO_PIN, GPIO.OUT)

  servo = GPIO.PWM(SERVO_PIN, 50)  # GPIO 17 for PWM with 50Hz

def secondarySetup():
  global servo
  servo.start(2.5)  # Initialization

def stop():
  global servo
  servo.stop()
  #GPIO.cleanup()

# sets the servo to rotate to direction (direction should be a float between 0 and 1)
def setServo(direction):
  global servo
  secondarySetup()
  if servo == None:
    raise Exception("Must run setup() before calling setServo()")
  elif direction < 0 or direction > 1:
    raise Exception("Direction must be between 0 and 1")
  else:
    dutyCycle = ((DUTY_CYCLE_MAX - DUTY_CYCLE_MIN) * direction) + DUTY_CYCLE_MIN
    servo.ChangeDutyCycle(dutyCycle)
    time.sleep(5)
    stop()


# use this to test just the read functionality
if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: servo.py <servoDirection>")
  else:
    print("Setting servo to " + sys.argv[1])
    setup()
    setServo(float(sys.argv[1]))
    GPIO.cleanup()