import requests

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        public_ip = response.json().get("ip")
        return public_ip
    except requests.RequestException as e:
        return f"Error fetching public IP: {e}"