# INVITE LINK https://discord.com/oauth2/authorize?client_id=857219790220689468&permissions=268953712&scope=bot

"""
To Do:
    - Additional error checking for commands
    - ~help command to display commands and samples
    - Mention @subject+section 10 minutes before sync meeting
    - Ability to change the time for sync meeting
Done
    - Make text sent by bot prettier
"""

'''
list of commands so far:
    ~help
    ~join <class_code> <section>
    ~leave
    ~clear
    ~classes
    ~zoom
'''

from discord.ext import commands
import discord
from discord import Embed
from json import loads
# from discord.utils import get
import os
from scraper import update_database
from bisect_seek import find_subject
from replit import db # allows access to replit database

# bot and client startup
client = discord.Client()
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="~", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot is ready")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Your friendly study buddy."))

# ----------------------

# # does not work
# @client.event
# async def on_guild_join(guild):
#     for channel in guild.text_channels:
#         if channel.permissions_for(guild.me).send_messages:
#             temp_ban_embeds = aboutme_msg()
#             await channel.send('test1')
#             for embed in temp_ban_embeds:
#                 await channel.send(embed=embed)
#                 await channel.send('test2')
#             await channel.send('test3')
#         break

# returns about me embedded message from json file
def aboutme_msg():
    with open("jsons/aboutme.json", "r") as file:
        temp_ban_embeds = parse_embed_json(file.read())
    return temp_ban_embeds

def help_msg():
    with open("jsons/help.json", "r") as file:
        temp_ban_embeds = parse_embed_json(file.read())
    return temp_ban_embeds

# parses json file
def parse_embed_json(json_file):
    embeds_json = loads(json_file)['embeds']
    
    for embed_json in embeds_json:
        embed = Embed().from_dict(embed_json)
        yield embed

# adds class to replit database
def add_class_to_db(class_code, section):
    code_sec_str = f'{class_code} {section}'
    if code_sec_str in db.keys():
        return
    subj_info = find_subject('classes.csv', class_code, section)
    if subj_info == False:
        return subj_info
    db[code_sec_str] = subj_info
    return True

# ---------- TEMPLATE FOR COMMANDS ---------- #
# @bot.command()
# async def test(ctx, arg):
#     await ctx.send(arg)

# update the database
# to do: update such that only an admin can use this command
@bot.command()
async def update(ctx):
    await ctx.channel.send('Updating the database. This will take around three (3) minutes to finish. You will be pinged after the database is updated. In the meantime, the bot will be unusable.')
    await update_database()
    await ctx.channel.send(f'Database is updated. <@{ctx.author.id}>')

# join a class
@bot.command()
async def join(ctx, class_code = None, section = None, excess_arg = None):
    # error checking
    if excess_arg or not section:
        embed=discord.Embed(title="<a:x_:859805339511685121> An error has occured.", description="Make sure you you use the command in this format:\n`~join <class_code> <section>`.\nNote that there should be no space in the class code.", color=0x57afdb)
        embed.add_field(name="Example", value="`~join ArtAp10 A`", inline=False)
        await ctx.send(embed=embed)
        return

    # checks if class role exists
    if f'{class_code} {section}' not in db.keys():
        if add_class_to_db(class_code, section):
            role = await ctx.guild.create_role(name=f'{class_code} {section}', mentionable=True)
        else:
            embed=discord.Embed(title=f"<a:x_:859805339511685121> {class_code} {section} was not found in our database.", description="Make sure you you use the command in this format: `~join <class_code> <section>`. Note that there should be no space in the class code.", color=0x57afdb)
            embed.add_field(name="Example", value="`~join ArtAp10 A`", inline=False)
            await ctx.send(embed=embed)

            return
    
    role = discord.utils.get(ctx.guild.roles, name = f'{class_code} {section}')

    # checks if user is already in the class
    if role in ctx.author.roles:
        embed=discord.Embed(title=f"<a:x_:859805339511685121> You're already in the class: {class_code} {section}.", color=0x57afdb)
        await ctx.send(embed=embed)
    else:
        await ctx.author.add_roles(role)
        embed=discord.Embed(title="<a:check:859805173051293696> Successfully added you to the class!", description=f"You are now in the class: {class_code} {section}",color=0x57afdb)
        await ctx.send(embed=embed)

# leave a class
@bot.command()
async def leave(ctx, class_code = None, section = None, excess_arg = None):
    if excess_arg or not section:
        embed=discord.Embed(title="<a:x_:859805339511685121> An error has occured.", description="Make sure you you use the command in this format:\n`~leave <class_code> <section>`.\nNote that there should be no space in the class code.", color=0x57afdb)
        embed.add_field(name="Example", value="`~leave ArtAp10 A`", inline=False)
        await ctx.send(embed=embed)
        return

    role = discord.utils.get(ctx.guild.roles, name = f'{class_code} {section}')

    # If the class is not in the database or if the user is not in the class
    if role not in ctx.author.roles:
        embed = discord.Embed(title=f'<a:x_:859805339511685121> You\'re currently not in the class: {class_code} {section}.', description = 'Or the class is currently not in our database', color=0x57afdb)
        await ctx.send(embed=embed)
    else:
        await ctx.author.remove_roles(role)
        embed=discord.Embed(title = '<a:check:859805173051293696> Successfully removed you from the class!', description = f'You are no longer in the class: {class_code} {section}', color = 0x57afdb)
        await ctx.send(embed = embed)
    await cleardb(ctx)
             
# clears all the classes/roles of the student. to be used after a sem/quarter
@bot.command()
async def clear(ctx):
    i = 0
    for role in ctx.author.roles:
        if role.name in db.keys():
            await ctx.author.remove_roles(role)
            if i == 0:
                classes_removed = role.name
                i += 1
                continue
            classes_removed += ', ' + role.name
    
    embed=discord.Embed(title = '<a:check:859805173051293696> Successfully cleared your classes!', description=f"You were removed from these classes: {classes_removed}", color=0x57afdb)
    await ctx.send(embed=embed)

    await cleardb(ctx)

# ideally not to be used by user, but only by a function
# to do: change permissions such that only the bot can use this command
@bot.command()
async def cleardb(ctx):
    for key in db.keys():
        role = discord.utils.get(ctx.guild.roles, name = key)
        if len(role.members) == 0:
            del db[key]
            await role.delete()

# sends all the classes and the info of the classes to the user
@bot.command()
async def classes(ctx):
    has_class = False # to check if the user has joined any classes
    for role in ctx.author.roles:
        if role.name in db.keys():
            try:
                embed=discord.Embed(title = f'{db[role.name][0]} {db[role.name][1]}', description = db[role.name][2].replace('|', ','), color=0x57afdb)
                embed.add_field(name = 'Units', value = db[role.name][3], inline=True)
                embed.add_field(name = 'Schedule', value = db[role.name][4], inline=True)
                embed.add_field(name = 'Professor', value = db[role.name][6].replace('|', ','), inline=True)
                embed.add_field(name = 'Zoom Link', value = db[role.name][14], inline=True)
                await ctx.send(embed=embed)
                await ctx.send(f'Zoom link for the class {role.name} added by: <@{db[role.name][15]}>')
            except:
                embed=discord.Embed(title = f'{db[role.name][0]} {db[role.name][1]}', description = db[role.name][2].replace('|', ','), color=0x57afdb)
                embed.add_field(name = 'Units', value = db[role.name][3], inline=True)
                embed.add_field(name = 'Schedule', value = db[role.name][4], inline=True)
                embed.add_field(name = 'Professor', value = db[role.name][6].replace('|', ','), inline=True)
                embed.add_field(name = 'Zoom Link', value = 'The zoom link is not found in our database.', inline = True)
                await ctx.send(embed=embed)
            has_class = True
    if not has_class:
        ctx.send('You have not joined any classes.')

# add zoom link to the class
@bot.command()
async def zoom(ctx, class_code = None, section = None, link = None, excess_arg = None):
    if not class_code or not section or not link or excess_arg:
        await ctx.send('Invalid input. Please try again.')
        return

    if f'{class_code} {section}' in db.keys():
        if 'zoom.us' not in link:
            await ctx.send('Invalid link! Please try again.')
        else:
            try:
                db[f'{class_code} {section}'][14] = link
                db[f'{class_code} {section}'][15] = ctx.author.id
                await ctx.send(f'Updated the zoom link of __{class_code} {section}__ to ``{link}``')
            except:
                db[f'{class_code} {section}'].append(link)
                db[f'{class_code} {section}'].append(ctx.author.id)
                await ctx.send(f'Succesfully added ``{link}`` as the zoom link for __{class_code} {section}__')

# mentions the role 10 minutes before synchrnous class + zoom
# @bot.command()
# async def mention(ctx, role: bot.Role):
#     pass
    
# the bot should do this upon entering a server (WIP)
@bot.command()
async def aboutme(ctx):
    temp_ban_embeds = aboutme_msg()
    
    for embed in temp_ban_embeds:
        await ctx.send(embed=embed)

# lists all the commands available
@bot.command()
async def help(ctx):
    temp_ban_embeds = help_msg()

    for embed in temp_ban_embeds:
        await ctx.send(embed=embed)




# for debugging ------
@bot.command()
async def delete(ctx, class_code = None, section = None):
    if f'{class_code} {section}' in db.keys():
        await ctx.send(f'Deleting {class_code} {section}...')
        del db[f'{class_code} {section}']
        role = discord.utils.get(ctx.guild.roles, name = f'{class_code} {section}')
        await role.delete()
    else:
        await ctx.send('Class not found. Nothing is deleted.')

@bot.command()
async def listkeys(ctx):
    await ctx.send(db.keys())

@bot.command()
async def keyinfo(ctx, key):
    await ctx.send(db[key])

@bot.command()
async def roles(ctx):
    await ctx.send(ctx.author.roles)

@bot.command()
async def roleinfo(ctx, role_name):
    role = discord.utils.get(ctx.guild.roles, name = f'{role_name}')
    await ctx.send(f'Role: {role.name}')
    await ctx.send(f'Num of users: {len(role.members)}')
    await ctx.send(f'Members: {role.members}')

@bot.command()
async def default(ctx):
    await join(ctx, 'BIO399.12', 'A')
    await join(ctx, 'ATMOS299.1', 'A')
    await join(ctx, 'ENE13.05i', 'A')
    await join(ctx, 'ArtAp10', 'A')

@bot.command()
async def botsay(ctx):
    await ctx.send("something")

# --------------------
            
bot.run(os.getenv('TOKEN'))