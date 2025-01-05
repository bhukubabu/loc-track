import folium
import geocoder
import json
import requests
import time
import os
import pyttsx3
import threading
from get_ip import get_public_ip
from gtts import gTTS
import streamlit as st
from streamlit_lottie import st_lottie_spinner
import streamlit.components.v1 as components


public_ip = get_public_ip()


def plot_map(loca):
     map_center=[22.5626,88.363]
     current_loc=[loca.lat,loca.lng]
     map=folium.Map(location=map_center, zoom_start=8,control_scale=True,width=700)
     html_map=folium.Marker(
          location=current_loc,
          popup=f"{loca.city}, {loca.state}",
          icon=folium.Icon(icon='info-sign',color="purple")
     ).add_to(map)
     html_map.save("cur_map.html")

def interface(location):
    plot_map(location)
    with st.chat_message('ai'):
            st.success(f"""📍{location.city}, {location.state}""")
            st.warning(f"""📍 Latitude: {location.lat}, latitude: {location.lng}""")
        
    with open("cur_map.html",'r') as f:
        map_html=f.read()
    with st.expander("Displaying your current location 🗺",expanded=True):
            components.html(map_html,height=350)


def load_lottie(path):
      with open(path,'r') as rr:
            return json.load(rr)


def play_audio():
    #engine=pyttsx3.init()
    #engine.say(content)
    #engine.runAndWait()
    playsound("audio_op.mp3")

lottie=load_lottie("Animation - 1735974601572.json")  
st.title("Where are you ?? 🗺")

location = geocoder.ip(public_ip)
if location and location.ok:
      city,state,lat,lng=location.city,location.state,location.lat,location.lng
else:
    city,state,lat,lng=None,None,None,None

user_loc=f""" Hello user do you know exact latitude and longitude of your current location ?? Your are currently in{city}, {state}. Your Latitude is {lat}, your longitude is {lng}"""

audio=gTTS(text=user_loc,lang="en")
path="audio_op.mp3"
if os.path.exists(path):
    os.remove(path)
try:
     audio.save(path)
     st.success("AUDIO SAVED")
except:
     st.error("XXXX")
audio_thread=threading.Thread(target=play_audio,args=())
audio_thread.start()

if "key" not in st.session_state:
      st.session_state.key=True

if st.session_state.key:
    with st_lottie_spinner(lottie,width=600,height=400):
            time.sleep(4)
    st.session_state.key=False


if not st.session_state.key:
    try:
        if location and location.ok:
            interface(location)
            st.session_state.key=False
    except:
            st.error("Unable to retrieve location. Check your internet connection or try again.")
