import sys
from twilio.rest import Client
import credentials

HOST_PHONE_NUMBER = "+18449252895"
DEST_PHONE_NUMBER = "+19165915940"



# run this at startup
def setup():
    pass


# sends the message over SMS to the user
def sendMessage(messageText):
    client = Client(credentials.TWILIO_ACCOUNT_SID, credentials.TWILIO_AUTH_TOKEN)
    message = client.messages \
        .create(
        body = messageText,
        from_ = HOST_PHONE_NUMBER,
        to = DEST_PHONE_NUMBER
    )
    print(message.sid)
    print(f"Send message: {messageText} to {DEST_PHONE_NUMBER}")


# use this to test just the sms functionality
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sms.py <message>")
    else:
        message = sys.argv[1]
        print(f"Message: {message}")
        print(f"Sending to: {DEST_PHONE_NUMBER}")
        setup()
        sendMessage(message)