# AutoSecure

**Contact:** `maka677` / [`discord server`](https://discord.gg/6mzg5uXJPM)

**Big thanks to these contributors**:
- `Enrique (22robin)`
- `Chickens`
  
---

## Overview

**It is fully request based.** No browser simulation aka playwright/selenium is used.

AutoSecure is a **Discord bot for ethical cybersecurity training**. It simulates account verification scams to teach users how attackers trick people into sharing information. It’s **for educational use only** — never use it on real users or accounts.

It was made with the purpose of giving everyone acess to an autosecure without the need of having to pay for one or having to use dhooked free ones, it is fully open-source so you can check the code yourself. It will have most features that paid autosecures have.

---
### Status

- Adding Features
  
## Features

* [ ] - Get Owners Info (Name, Country...)
* [ ] - Grabs all purchases
* [ ] - Grabs Xbox gamertag
* [ ] - Grabs subscriptions
* [X] - Change primary alias
* [X] - Removes all security proofs (emails)
* [X] - Signs out of all devices
* [X] - Bypasses email 2FA verification
* [X] - Checks if an account is locked
* [X] - Disables 2FA
* [X] - Improved embeds 
* [X] - Gets recovery code
* [X] - Changes security email
* [X] - Changes password
* [X] - Removes Windows Hello keys (Zyger exploit)
* [X] - Checks Minecraft (Owns MC, username/no name set, purchase method, capes, SSID)

---

## Disclaimer

**This tool is for learning, testing, and awareness training only.** Using it without consent or on real systems is illegal. The author is not responsible for misuse.

---

## How to Set Up

1. **Install Python 3.12:**
   [Download Here](https://www.python.org/downloads/release/python-3110/)

2. **Create a Bot:**
   Get a Discord bot token and enable all intents [here](https://discord.com/developers/applications).

3. **Get API Keys:**

   * [Donarev419](https://donarev419.com) for aliases replacement.* (Required)
   * [Hypixel](https://developer.hypixel.net/) for Hypixel stats. (Optional)

    **You can get your donarev token by:**

    - Login in donarev
    - Open your developer tab with F12
    - Click the Application/Storage Tab and select Local Storage
    - Click the donarev link and copy the user value
    - Copy and paste that into the config
    
4. **Configure the Bot:**
   Edit `config.json` and add:

   ```python
   bot_token = "YOUR_DISCORD_BOT_TOKEN"
   donarev_token = "YOUR_DONAREV_TOKEN"
   hypixel_key = "YOUR_HYPIXEL_KEY"
   owners = [YOUR_DISCORD_ID]
   ```

5. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Bot:**

   ```bash
   python bot.py
   ```

7. **Set Logs Channel:**
   Use `/set` to select where logs go.

   ⚠️ Do NOT modify the channel ID in the config if you don't know what you are doing.
   If you remove the ID after setting it up and the bot stops working it is you fault hence why I did not add any checking if it is there.

8. **Set your Verification Embed:**
   Use `send_embed` to send the verification embed in the same channel you are in.
   
---
