from dateutil import parser
import datetime
import httpx

async def getUsernameInfo(ssid: str):

    async with httpx.AsyncClient() as session:

        response = await session.get(
            url = "https://api.minecraftservices.com/minecraft/profile/namechange",
            headers = {
                "Authorization": f"Bearer {ssid}"
            }
        )
        
        if response.json()["nameChangeAllowed"]:
            return True

        todayDate = datetime.datetime.now()
        finalDate = (parser.parse(response.json()["changedAt"]) + datetime.timedelta(days=31)).replace(tzinfo=None)

        # Amount of days to change username
        return (finalDate - todayDate).days