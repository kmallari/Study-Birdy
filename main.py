import discord
import os
from scraper import update_database

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    msg = message.content

    if message.author == client.user:
        return
    
    if msg.startswith('~'):
        # updates the .csv database
        if msg.split('~', 1)[1].lower() == 'update':
            await message.channel.send('Updating the database. This will take around a minute to finish. You will be pinged after the database is updated.')
            update_database()
            await message.channel.send(f'Database is updated. <@{message.author.id}>')
        await message.channel.send('Message started with "~"')

        if msg.split('~', 1)[1].lower() == 'test':
            

client.run(os.getenv('TOKEN'))