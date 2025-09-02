import discord
from discord.ext import commands
import json, base64, os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import enc_token
KEY_FILE = "key.json"
DATA_FILE = "encryption_data.json"

# -------------------------------
# Bot Setup
# -------------------------------
key = enc_token.load_key()
token = enc_token.token_encrypt(key)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot ist online als {bot.user}")

@tree.command(name="ping", description="Antwortet mit Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

bot.run(token)
