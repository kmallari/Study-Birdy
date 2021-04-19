import discord
# since our code in replit is public, we need to find a way to make our token private.
# the .env file hides the information inside it from the public.
# we need to use the "os" module to access that .env file.
import os
import json

# from replit import db # allows access to replit database
from keep_alive import keep_alive
from read_text import ocr_space_url

client = discord.Client()


# on_ready() function is in the discord library.
# the program finds the function in the library and executes the lines
# inside our function.
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}.")
    json_data = json.loads(ocr_space_url('https://i.imgur.com/RPRkYjk.png'))
    # print(json_data)
    text_from_img = json_data['ParsedResults'][0]['ParsedText']
    print(text_from_img)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # variable for the message sent by a user.
    msg = message.content

    if msg == '.sb':
        # print all commands with instructions
        # .sb new <subject_code> <section> <course_name> <prof>     -> adds new subject
        # .sb new https://imgur.com/xxxxxx                          -> automatically adds objects
        # .sb list                                                  -> lists all subjects with their
        #                                                              respective indices
        # .sb <index> <subject_code / section ...>                  -> modify current info of a subj
        # .sb <index>
        print('''
.sb new <subject_code> <section> <course_name> <prof>
.sb new https://imgur.com/xxxxxx
.sb list
.sb <index> <subject_code / section ...>
        ''')
    if msg.startswith('.sb'):
        msg = msg.split(".sb ", 1)[1]
        if msg.startswith('new '):
            pass
        elif msg.startswith('list'):
            pass
        elif msg.startswith('1'): # modify: starts with a number
            pass
        else:
            message.channel.send('Sorry, you entered an unknown command. Please try again.')

keep_alive()
client.run(os.getenv("TOKEN"))
