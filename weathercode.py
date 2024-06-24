import streamlit as st
import requests
import json
import datetime
from PIL import Image
from io import BytesIO
import base64

# Function to encode an image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_hack(main_bg):
    bin_str = get_base64_of_bin_file(main_bg)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Specify the path to your background image
bg_image_path = "beach.png"
set_bg_hack(bg_image_path)

# Dates and Time
dt = datetime.datetime.now()
st.markdown(f"<h2 style='text-align: center; color: black;'>{dt.strftime('%Y-%m-%d')}</h2>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align: center; color: black;'>{dt.strftime('%I:%M %p')}</h2>", unsafe_allow_html=True)

# City Search
city_name = st.text_input("Enter city name:", "", max_chars=30)

# Function to fetch weather data
def fetch_weather_data(city):
    api_key = "dd1441b2810f9f56693732488d04cac6"
    api_request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}")
    return json.loads(api_request.content)

# Search Button
if st.button("Search"):
    if city_name:
        api = fetch_weather_data(city_name)
        
        # Extract weather details
        y = api['main']
        current_temperature = y['temp']
        humidity = y['humidity']
        temp_min = y['temp_min']
        temp_max = y['temp_max']
        
        x = api['coord']
        longitude = x['lon']
        latitude = x['lat']
        
        z = api['sys']
        country = z['country']
        state = z.get('state', '')  # State information might not be available
        city_name = api['name']
        
        weather = api['weather'][0]
        weather_icon = weather['icon']
        
        # Fetch weather icon
        icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(BytesIO(icon_response.content))
        
        # Display data
        st.image(icon_image, width=100)
        st.markdown(f"<h3 style='text-align: center; color: black;'>City: {city_name}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: black;'>Country: {country}</h3>", unsafe_allow_html=True)
        if state:
            st.markdown(f"<h3 style='text-align: center; color: black;'>State: {state}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: black;'>Longitude: {longitude}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: black;'>Latitude: {latitude}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; color: black;'>Temperature: {current_temperature} °C</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: black;'>Humidity: {humidity}%</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: black;'>Max Temp: {temp_max} °C</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: black;'>Min Temp: {temp_min} °C</h3>", unsafe_allow_html=True)

# Static note
st.markdown("<p style='text-align: center; color: black;'>All temperatures in degree Celsius</p>", unsafe_allow_html=True)
