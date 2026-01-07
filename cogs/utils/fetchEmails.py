from datetime import datetime
from discord import Embed
import httpx
import re

from database.database import DBConnection

# Email/Password is not needed its just as an info for the embed
async def fetchEmails(token: str, email: str, password: str) -> Embed:

    async with httpx.AsyncClient() as session:
            
        embed = Embed(
            title = "📧 Email Inbox",
            description = f"**Email:** {email}\n**Password:** {password}",
            color = 0x5865F2 
        )
        
        getEmails = await session.get(
            url = f"https://api.mail.tm/messages",
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "authorization": f"Bearer {token}"
            }
        )
        
        emails = getEmails.json()
        if emails:


            for index, email in enumerate(getEmails.json(), 1):

                response = await session.get(
                    url = f"https://api.mail.tm/messages/{email["id"]}",
                    headers = {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "authorization": f"Bearer {token}"
                    }
                )

                emailData = response.json()
                time = datetime.fromisoformat(emailData["createdAt"].replace('+00:00', '+0000')).strftime("%d/%m/%Y %H:%M")
                if emailData["from"]["address"] == "account-security-noreply@accountprotection.microsoft.com":

                    codeMatch = re.search(r"(?:single-use code is:|Security code:)\s*(\d{6})", emailData["text"])
                    if codeMatch:

                        code = codeMatch.group(1)
                        embed.add_field(
                            name = f"📨 Email #{index} ({time})",
                            value = f"**From:** {email["from"]["address"]}\n**Found OTP Code:** {code}",
                            inline = False
                        )
                        continue

                embed.add_field(
                    name = f"📨 Email #{index} ({time})",
                    value = f"**From:** {email["from"]["address"]}\n**Intro:** {email["intro"]}",
                    inline = False
                )
                continue

        else:
            
            embed.description = "This inbox hasn't received any emails yet!"
            embed.color = 0xFFFF7A

        embed.set_footer(text = "Each email is automaticly deleted by mail.tm after 7 days")

        return embed


                




            


    