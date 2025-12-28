import requests

# Spamming this endpoint gets you ratelimited for 1~2 minutes
def getMethod(ssid: str):

    licenses = requests.get(
        url = "https://api.minecraftservices.com/entitlements/license?requestId=c24114ab-1814-4d5c-9b1f-e8825edaec1f",
        headers = {
            "Authorization": f"Bearer {ssid}"
        }
    ).json()

    if "items" in licenses:
        for item in licenses["items"]:
            if (item["name"] == "product_minecraft" or item["name"] == "game_minecraft"):
                if item["source"] == "GAMEPASS":
                    return "Gamepass"
                elif (item["source"] == "PURCHASE" or item["source"] == "MC_PURCHASE"):
                    return "Purchased"
                
    return None