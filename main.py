import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from modules.Token import get_token
from modules.channels import create_channel, delete_channel
from modules.tickets import create_ticket, close_ticket

# -------------------------------
# Token laden
# -------------------------------
token = get_token()

# -------------------------------
# Bot Setup
# -------------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# -------------------------------
# Events
# -------------------------------
@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot ist online als {bot.user}")

# -------------------------------
# Slash-Commands
# -------------------------------

# Ping
@tree.command(name="ping", description="Antwortet mit Pong!")
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# Channel erstellen
@tree.command(name="create_channel", description="Erstellt einen Textkanal")
@discord.app_commands.describe(name="Name des Kanals")
async def create_channel_command(interaction: discord.Interaction, name: str):
    await create_channel(interaction, name)

# Channel löschen
@tree.command(name="delete_channel", description="Löscht einen Textkanal")
@discord.app_commands.describe(name="Name des Kanals")
async def delete_channel_command(interaction: discord.Interaction, name: str):
    await delete_channel(interaction, name)

# Ticket erstellen
@tree.command(name="create_ticket", description="Erstellt ein Support-Ticket")
@discord.app_commands.describe(topic="Kurzes Thema/Problem für das Ticket")
async def create_ticket_command(interaction: discord.Interaction, topic: str):
    await create_ticket(interaction, topic)

# Ticket schließen
@tree.command(name="close_ticket", description="Schließt ein Support-Ticket")
@discord.app_commands.describe(channel_name="Name des Ticket-Channels")
async def close_ticket_command(interaction: discord.Interaction, channel_name: str):
    await close_ticket(interaction, channel_name)

# -------------------------------
# Bot starten
# -------------------------------
bot.run(token)
