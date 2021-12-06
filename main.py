import time
import hashlib
import multiprocessing
import RPi.GPIO as GPIO
import rfid
import servo
import sms

STAY_CLOSED_TIME = 15 # number of seconds that must elapse since the device was unlocked for it to unlock again
TIME_UNLOCKED = 10 # amount of time the container will stay unlocked before automatically re-locking

# positioning info for servo
SERVO_LOCK_DIR = 0.25
SERVO_UNLOCK_DIR = 0.75

timeSinceUnlock = time.time()
timeSinceUnlockThreadInt = multiprocessing.Value('i', int(time.time()))
didSendMessageThread = multiprocessing.Value('b', False)
knownHashes = []


# sets the time last unlocked
def setLastUnlockTime():
    global  timeSinceUnlock
    global timeSinceUnlockThreadInt
    global didSendMessageThread
    timeSinceUnlock = time.time()
    timeSinceUnlockThreadInt.value = int(timeSinceUnlock)
    didSendMessageThread.value = False

# checks the time elapsed, and sends an SMS message if necessary (this is meant to run in a separate thread)
def checkTimeElapsed(lastTime, didSendMessage):
    SMS_REMINDER_TIME = 20 # will send SMS reminder if this many seconds elapse since the container was last unlocked
    try:
        while True:
            timeElapsed = int(time.time()) - lastTime.value
            #print(f"T: {timeElapsed}")
            if timeElapsed >= SMS_REMINDER_TIME and not didSendMessage.value:
                sms.sendMessage("Did you forget to take your medicine?")
                didSendMessage.value = True
            time.sleep(1)
    except KeyboardInterrupt:
        pass

# returns RFID code if read is successful, otherwise returns None
def tryReadRfid():
    return rfid.read()

# generates a hash from rfid data
def generateHash(rfidDataString):
    # return hashlib.sha256(bytes(rfidDataString)).hexdigest()
    return rfidDataString


# unlocks the container, waits for a set amount of time, and re-locks the container
def unlockLock():
    global timeSinceUnlock

    setLastUnlockTime() # do this now so user doesn't get a reminder message while they're in the unlock process

    # unlock
    print("Unlocking...")
    servo.setServo(SERVO_UNLOCK_DIR)
    print("Unlocked")
    time.sleep(TIME_UNLOCKED)

    # re-lock
    print("Locking...")
    servo.setServo(SERVO_LOCK_DIR)
    print("Locked")

    setLastUnlockTime() # do this again so that the last unlock time is in sync with the time when we know the box was fully back in the locked position



def setup():
    servo.setup()
    rfid.setup()
    servo.secondarySetup()

    checkTimeProcess = multiprocessing.Process(target = checkTimeElapsed, args = (timeSinceUnlockThreadInt, didSendMessageThread))
    checkTimeProcess.start()

def mainLoop():
    rfidData = tryReadRfid()
    timeElapsed = time.time() - timeSinceUnlock
    rfidHash = generateHash(rfidData)
    print(f"Read {rfidHash}")
    if len(knownHashes) == 0: #add the first card read into known cards (this is for debug purposes)
        knownHashes.append(rfidHash)
        print(f"Added {rfidHash} to known card ids")
    if rfidHash in knownHashes:
        if timeElapsed > STAY_CLOSED_TIME: unlockLock()
        else: print(f"Time elapsed: {int(timeElapsed)} / {STAY_CLOSED_TIME} seconds")

if __name__ == "__main__":
    setup()
    try:
        while True: mainLoop()
    except KeyboardInterrupt:
        print("Exiting: Keyboard Interrupt")
    finally:
        servo.stop()
        GPIO.cleanup()