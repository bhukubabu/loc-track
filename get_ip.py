import socket

def get_public_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except requests.RequestException as e:
        return f"Error fetching public IP: {e}"
