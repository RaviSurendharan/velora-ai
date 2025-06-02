from twilio.rest import Client
import os

# Get Twilio credentials from environment variables
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_PHONE_NUMBER")

# Initialize Twilio client
client = Client(account_sid, auth_token)

def send_sms(to_number, message):
    """Send SMS message using Twilio"""
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=to_number
        )
        return {"success": True, "sid": message.sid}
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return {"success": False, "error": str(e)}
