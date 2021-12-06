import os
import RPi.GPIO as GPIO
import idHashStorage
import rfid

FILEPATH = "knownHashes.csv"

# appends the list of valid id's to the file 'knownHashes.csv'
def writeToFile(idsList):
    if len(idsList) > 0:
        fileEmpty = (not os.path.exists(FILEPATH)) or os.stat(FILEPATH).st_size == 0
        file = open(FILEPATH, "a")
        stringToAppend = ""
        if not fileEmpty: stringToAppend += ","
        for i in range(0, len(idsList)):
            stringToAppend += idsList[i]
            if i < len(idsList) - 1: stringToAppend += ","
        file.write(stringToAppend)
        file.close()

if __name__ == "__main__":
    print("Scan a card to authorize it to unlock the container...")
    try:
        rfid.setup()
        rfidData = str(rfid.read())
        idHashStorage.setStringKnown(rfidData)
        writeToFile(idHashStorage.validHashes)
        print(f"Successfully added {rfidData} to known RFIDs")
    except KeyboardInterrupt:
        print("Exiting: Keyboard Interrupt")
    finally:
        GPIO.cleanup()