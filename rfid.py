import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# waits until an RFID card can be read by the sensor, and returns the id of the card once it is read
def read():
	id, text = reader.read()
	return id


# use this to test just the read functionality
if __name__ == "__main__":
	reader = SimpleMFRC522()
	try:
		while True:
			try:
				id, text = reader.read()
				print(f"{id}, {text}")
			except Exception as e:
				print(e)
			finally:
				GPIO.cleanup()
	except KeyboardInterrupt:
		print("Terminated")