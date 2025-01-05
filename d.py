import folium
import json
import time
import os
import threading
import platform
import streamlit as st
import streamlit.components.v1 as components


def plot_map(lat, lng):
    map_center = [lat, lng]  # Centered on the user's location
    map_obj = folium.Map(location=map_center, zoom_start=15, control_scale=True, width=700)
    folium.Marker(
        location=[lat, lng],
        popup=f"📍 Latitude: {lat}, Longitude: {lng}",
        icon=folium.Icon(icon='info-sign', color="purple")
    ).add_to(map_obj)
    return map_obj._repr_html_()


def interface(lat, lng):
    map_html = plot_map(lat, lng)
    with st.chat_message('ai'):
        st.success(f"📍 Latitude: {lat}, Longitude: {lng}")
    
    with st.expander("Displaying your current location 🗺", expanded=True):
        components.html(map_html, height=350)


def load_lottie(path):
    with open(path, 'r') as file:
        return json.load(file)


def main_interface(lat, lng):
    system_name = platform.system()
    st.markdown(f"System Detected: {system_name}")
    
    # Lottie animation spinner (if animation file is available)
    if "key" not in st.session_state:
        st.session_state.key = True

    if st.session_state.key:
        with st.spinner("Loading..."):
            time.sleep(4)
        st.session_state.key = False

    if not st.session_state.key:
        try:
            interface(lat, lng)
        except Exception as e:
            st.error(f"Unable to retrieve location: {e}")


# Main app
st.title("Where are you?? 🗺")

# JavaScript Geolocation API
components.html("""
<script>
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const coords = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            const data = JSON.stringify(coords);
            window.parent.postMessage(data, "*");
        },
        function(error) {
            const err = { error: error.message };
            window.parent.postMessage(JSON.stringify(err), "*");
        }
    );
</script>
""", height=0, width=0)

# Placeholder to receive coordinates
location_placeholder = st.empty()

# Receive message from JavaScript
message = st.session_state.get("location_message", None)
if message is None:
    message = st.text_input("Paste location details here (if auto-detection fails):")

# Wait for location data
try:
    location_data = st.session_state.get("location_message", None)
    if location_data:
        location_json = json.loads(location_data)
        lat, lng = location_json.get("lat"), location_json.get("lng")
        st.session_state["location_message"] = location_data
    elif message:
        location_json = json.loads(message)
        lat, lng = location_json.get("lat"), location_json.get("lng")
        st.session_state["location_message"] = message
    else:
        st.warning("Waiting for location data...")
        st.stop()
except Exception as e:
    st.error("Unable to parse location data. Please try again.")
    st.stop()

# Render the interface
main_interface(lat, lng)
