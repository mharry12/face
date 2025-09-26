# utils.py
import requests
from ipware import get_client_ip

def get_location_from_ip(request):
    ip, is_routable = get_client_ip(request)
    if ip is None:
        return None
    
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        data = response.json()
        return {
            "ip": ip,
            "country": data.get("country_name"),
            "region": data.get("region"),
            "city": data.get("city"),
            "country_code": data.get("country_code")
        }
    except:
        return None