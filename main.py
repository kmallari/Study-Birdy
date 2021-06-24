import discord
import os
from replit import db
from scraper import create_database

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('~'):
        await message.channel.send("Hello!")

client.run(os.getenv('TOKEN'))