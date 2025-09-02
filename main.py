import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from modules import channels   # channel Modul laden

# .env laden
load_dotenv()
token = os.getenv("DC_BOT_TOKEN")

# Intents einstellen
intents = discord.Intents.default()
intents.message_content = True

# Bot erstellen
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # Slash-Command-Tree

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot ist online als {bot.user} und Slash-Commands wurden synchronisiert.")

# /ping
@tree.command(name="ping", description="Antwortet mit Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# /delete_channel
@tree.command(name="delete_channel", description="Löscht einen Textkanal.")
async def delete_channel(interaction: discord.Interaction, channel_name: str):
    await channels.delete_channel(interaction, channel_name)

# /create_channel
@tree.command(name="create_channel", description="Erstellt einen neuen Textkanal.")
async def create_channel(interaction: discord.Interaction, name: str):
    await channels.create_channel(interaction, name)

# Bot starten
bot.run(token)