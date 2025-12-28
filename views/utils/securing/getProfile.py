import requests

def getProfile(ssid: str):
    
    response = requests.get(
        url = "https://api.minecraftservices.com/minecraft/profile",
        headers = {
            "Authorization": f"Bearer {ssid}"
        }
    )

    if "name" in response.json():
        return response.json()["name"]
    
    return None