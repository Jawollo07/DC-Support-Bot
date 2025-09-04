from modules.channels import create_channel, delete_channel

async def create_ticket(interaction: "discord.Interaction", topic: str):
    """Erstellt ein Ticket (eigenen Channel) für den User"""
    username = interaction.user.name
    channel_name = f"ticket-{username}-{topic.lower().replace(' ', '-')}"
    await create_channel(interaction, channel_name)
    await interaction.response.send_message(f"🎫 Ticket **{channel_name}** wurde erstellt!", ephemeral=True)

async def close_ticket(interaction: "discord.Interaction", channel_name: str):
    """Schließt ein Ticket (löscht den Kanal)"""
    await delete_channel(interaction, channel_name)