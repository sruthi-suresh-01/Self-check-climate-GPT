from pyowm import OWM
from twilio.rest import Client

# Assuming credentials are properly defined in a credentials module
# from credentials import my_twilio_number, account_sid, auth_token, my_phone_number
my_twilio_number='+18667027304'
account_sid='ACa3073c6ff0b9fff02ecbd262eff90e59'
auth_token='2e0ba1fb593d1855e0006c6b7b2dbae7'
my_phone_number='+19513346999'



# Instantiate OWM object
owm = OWM('09af04fd9ecb516601ec2ba54c149666')
mgr = owm.weather_manager()

# Check for rain and clear status
def umbrellaNotRequired(weather):
    rain = weather.rain
    status = weather.status.lower().strip()
    return len(rain) == 0 or status == "clear"

# Function to send weather SMS
def send_weather_sms():
    client = Client(account_sid, auth_token)

    try:
        observation = mgr.weather_at_place("Riverside,US")
        weather = observation.weather
        if umbrellaNotRequired(weather):
            temperature = weather.temperature("fahrenheit")["temp"]
            humidity = weather.humidity
            client.messages.create(
                from_=my_twilio_number,
                to=my_phone_number,
                body=f'''
                    Hey, sky is clear and you don't need an umbrella. Weather details:
                    1. Humidity: {humidity}%
                    2. Temperature: {temperature}° Fahrenheit
                '''
            )
    except Exception as e:
        # This will handle any exception, which you might assume as API being offline or similar
        print(f"Error occurred: {e}")
        client.messages.create(
            from_=my_twilio_number,
            to=my_phone_number,
            body="Hey, weather service is not available, please check it out by yourself."
        )

# Main execution point
if __name__ == '__main__':
    send_weather_sms()
