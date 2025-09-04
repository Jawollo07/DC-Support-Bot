import discord

async def create_channel(interaction: discord.Interaction, name: str):
    """Erstellt einen Textkanal im aktuellen Server"""
    guild = interaction.guild
    await guild.create_text_channel(name)
    # Optional: nur Ephemeral oder Serverweite Nachricht
    await interaction.response.send_message(f"📂 Kanal **{name}** wurde erstellt!", ephemeral=True)

async def delete_channel(interaction: discord.Interaction, name: str):
    """Löscht einen Textkanal im aktuellen Server"""
    guild = interaction.guild
    existing_channel = discord.utils.get(guild.channels, name=name)
    
    if existing_channel:
        await existing_channel.delete()
        await interaction.response.send_message(f"🗑️ Kanal **{name}** wurde gelöscht!", ephemeral=True)
    else:
        await interaction.response.send_message(f"⚠️ Kanal **{name}** existiert nicht.", ephemeral=True)
