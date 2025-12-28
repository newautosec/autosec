import requests

def getSSID(xbl: str):
    
    response = requests.post(
        url = "https://api.minecraftservices.com/authentication/login_with_xbox",
        json = {
            "identityToken": xbl,
            "ensureLegacyEnabled": True
        }
    )

    if "access_token" in response.json():
        return response.json()["access_token"]
    
    return None
    