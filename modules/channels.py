import discord

async def delete_channel(interaction: discord.Interaction, channel_name: str):
    guild = interaction.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)

    if existing_channel is not None:
        await existing_channel.delete()
        await interaction.response.send_message(f"🗑️ Kanal **{channel_name}** wurde gelöscht!")
    else:
        await interaction.response.send_message(f"⚠️ Kanal **{channel_name}** existiert nicht.", ephemeral=True)


async def create_channel(interaction: discord.Interaction, name: str):
    guild = interaction.guild
    await guild.create_text_channel(name)
    await interaction.response.send_message(f"📂 Kanal **{name}** wurde erstellt!")
