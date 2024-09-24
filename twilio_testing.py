from twilio.rest import Client

# Replace these with your Twilio credentials and numbers
my_twilio_number='+18667027304'
account_sid='ACa3073c6ff0b9fff02ecbd262eff90e59'
auth_token='2e0ba1fb593d1855e0006c6b7b2dbae7'
my_phone_number='+19513346999'

client = Client(account_sid, auth_token)

try:
    message = client.messages.create(
        body="Hello from Twilio!",
        from_=my_twilio_number,
        to=my_phone_number
    )
    print(f"Message SID: {message.sid}")
except Exception as e:
    print(f"An error occurred: {e}")
