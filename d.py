import folium
import json
import time
import streamlit as st
import streamlit.components.v1 as components


def plot_map(lat, lng):
    """Plot a map centered on the given latitude and longitude."""
    map_center = [lat, lng]
    map_obj = folium.Map(location=map_center, zoom_start=15, control_scale=True)
    folium.Marker(
        location=[lat, lng],
        popup=f"📍 Latitude: {lat}, Longitude: {lng}",
        icon=folium.Icon(icon="info-sign", color="purple"),
    ).add_to(map_obj)
    return map_obj._repr_html_()


def display_map(lat, lng):
    """Display the user's location on a map."""
    map_html = plot_map(lat, lng)
    st.success(f"📍 Detected Location: Latitude {lat}, Longitude {lng}")
    with st.expander("Map of your current location 🗺", expanded=True):
        components.html(map_html, height=400)


# JavaScript to fetch geolocation
geolocation_script = """
<script>
    // Fetch the user's location using the browser's Geolocation API
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const locationData = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            // Send the location data back to Streamlit
            const data = JSON.stringify(locationData);
            window.parent.postMessage(data, "*");
        },
        function(error) {
            const errorData = { error: error.message };
            window.parent.postMessage(JSON.stringify(errorData), "*");
        }
    );
</script>
"""

# Streamlit app starts here
st.title("Browser-based Location Detection 🌍")

# Inject JavaScript into the Streamlit app
components.html(geolocation_script, height=0, width=0)

# Placeholder for detected location
location_placeholder = st.empty()

# Wait for geolocation data to be sent back
location_data = st.experimental_get_query_params().get("location", [None])[0]

# Retrieve location data from the session or the browser's message
if "location" not in st.session_state:
    st.session_state["location"] = None

if location_data:
    st.session_state["location"] = location_data

# Check if location data is available
if st.session_state["location"]:
    try:
        location_json = json.loads(st.session_state["location"])
        if "error" in location_json:
            st.error(f"Error fetching location: {location_json['error']}")
        else:
            lat, lng = location_json.get("lat"), location_json.get("lng")
            display_map(lat, lng)
    except Exception as e:
        st.error(f"Error parsing location data: {e}")
else:
    st.info("Waiting for location data... Please allow location access in your browser.")
