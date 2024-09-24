from pyowm import OWM
from pyowm.utils.config import get_default_config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Assuming credentials are defined here (Use environment variables or a secure method in production)
gmail_user = 'sruthisuresh1402@gmail.com'  # Your Gmail address
gmail_password = 'judm drom xstt mpxm'  # Your Gmail password or app password

# Receiver's email
to_email = 'ssure040@ucr.edu'

# Configuration for OWM
config = get_default_config()
config['language'] = 'en'  # Optionally set language

# Instantiate OWM object
owm = OWM('09af04fd9ecb516601ec2ba54c149666', config)
mgr = owm.weather_manager()
air_mgr = owm.airpollution_manager()  # Directly use OWM's airpollution_manager

# Check for rain and clear status
def umbrellaNotRequired(weather):
    rain = weather.rain
    status = weather.status.lower().strip()
    return len(rain) == 0 or status == "clear"

# Function to get AQI
def get_air_quality_index(latitude, longitude):
    air_quality = air_mgr.air_quality_at_coords(latitude, longitude)
    if air_quality is not None:
        aqi = air_quality.aqi  # AQI value
    else:
        aqi = None
    return aqi

# Function to send weather email
def send_weather_email():
    try:
        observation = mgr.weather_at_place("Los Angeles,US")
        weather = observation.weather
        if umbrellaNotRequired(weather):
            temperature = weather.temperature("fahrenheit")["temp"]
            humidity = weather.humidity

            # Fetch AQI
            location = observation.location
            latitude = location.lat
            longitude = location.lon
            aqi = get_air_quality_index(latitude, longitude)

            if aqi is not None:
                aqi_message = f"3. Air Quality Index (AQI): {aqi}"
            else:
                aqi_message = "3. Air Quality Index (AQI): Data not available"

            # Email setup
            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = to_email
            msg['Subject'] = "Weather and Air Quality Update"
            body = f'''
                Hey, sky is clear and you don't need an umbrella. Weather and Air Quality details:
                1. Humidity: {humidity}%
                2. Temperature: {temperature}° Fahrenheit
                {aqi_message}
            '''
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(gmail_user, gmail_password)
            text = msg.as_string()
            server.sendmail(gmail_user, to_email, text)
            server.quit()
            print("Email sent successfully!")

    except Exception as e:
        # Handle any exceptions, possibly due to weather API or email issues
        print(f"Error occurred: {e}")

# Main execution point
if __name__ == '__main__':
    send_weather_email()
