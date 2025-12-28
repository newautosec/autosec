import requests

def getCapes(ssid: str) :

    response = requests.get(
        url = "https://api.minecraftservices.com/minecraft/profile",
        headers = {
            "Authorization": f"Bearer {ssid}"
        }
    )
    
    if "capes" in response.json():
        return response.json()["capes"]
    
    return None