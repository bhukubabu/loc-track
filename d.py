import folium
import geocoder
import json
import time
import os
import tempfile
import threading
from gtts import gTTS
import streamlit as st
from streamlit_lottie import st_lottie_spinner
import streamlit.components.v1 as components


def plot_map(location):
    map_center = [22.5626, 88.363]  # Default center
    current_loc = [location.lat, location.lng]
    map_obj = folium.Map(location=map_center, zoom_start=8, control_scale=True, width=700)
    folium.Marker(
        location=current_loc,
        popup=f"{location.city}, {location.state}",
        icon=folium.Icon(icon='info-sign', color="purple")
    ).add_to(map_obj)
    return map_obj._repr_html_()


def interface(location):
    map_html = plot_map(location)
    with st.chat_message('ai'):
        st.success(f"📍 {location.city}, {location.state}")
        st.warning(f"📍 Latitude: {location.lat}, Longitude: {location.lng}")
    
    with st.expander("Displaying your current location 🗺", expanded=True):
        components.html(map_html, height=350)


def load_lottie(path):
    with open(path, 'r') as file:
        return json.load(file)


import os
import platform

def play_audio(file_path):
    system_name = platform.system()
    if system_name == "Darwin":  # macOS
        os.system(f"afplay {file_path}")
    #elif system_name == "Linux":  # Linux
        #os.system(f"mpg123 {file_path}")  # aplay is a common Linux audio player
    elif system_name == "Windows":  # Windows
        os.system(f'start "{file_path}"')  # Double quotes handle spaces in the path
    else:
        print("Unsupported OS for audio playback.")


# Main app
lottie = load_lottie("Animation - 1735974601572.json")
st.title("Where are you ?? 🗺")

location = geocoder.ip('me')
if location and location.ok:
    city, state, lat, lng = location.city, location.state, location.lat, location.lng
else:
    city, state, lat, lng = None, None, None, None

user_loc = f"Hello user, do you know the exact latitude and longitude of your current location? " \
           f"You are currently in {city}, {state}. Your Latitude is {lat}, your Longitude is {lng}."


audio=gTTS(text=user_loc,lang="en")
audio_file_path="audio_op.mp3"
if os.path.exists(audio_file_path):
    os.remove(audio_file_path)
audio.save(audio_file_path)
# Play audio in a separate thread
audio_thread = threading.Thread(target=play_audio, args=(audio_file_path,))
audio_thread.start()

# Lottie animation spinner
if "key" not in st.session_state:
    st.session_state.key = True

if st.session_state.key:
    with st_lottie_spinner(lottie, width=600, height=400):
        time.sleep(4)
    st.session_state.key = False

if not st.session_state.key:
    try:
        if location and location.ok:
            interface(location)
    except Exception as e:
        st.error(f"Unable to retrieve location: {e}")
