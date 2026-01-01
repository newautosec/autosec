from dateutil import parser
import datetime
import requests

def getUsernameInfo(ssid: str):

    response = requests.get(
        url = "https://api.minecraftservices.com/minecraft/profile/namechange",
        headers = {
            "Authorization": f"Bearer {ssid}"
        }
    ).json()

    if response["nameChangeAllowed"]:
        return True
    
    todayDate = datetime.datetime.now()
    finalDate = (parser.parse(response["changedAt"]) + datetime.timedelta(days=31)).replace(tzinfo=None)

    # Amount of days to change username
    return (finalDate - todayDate)