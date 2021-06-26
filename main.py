from discord.ext import commands
import discord
import os
from scraper import update_database
from bisect_seek import find_subject
from replit import db # allows access to replit database

# client = discord.Client()

db['roles'] = []

bot = commands.Bot(command_prefix="~")

def add_subj_to_db(class_code, section):
    code_sec_str = f'{class_code} {section}'
    if code_sec_str in db.keys():
        return
    subj_info = find_subject('subjects.csv', class_code, section)
    db[code_sec_str] = subj_info
    print(db[code_sec_str])

@bot.event
async def on_ready():
    print(f"Bot is ready")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Your friendly study buddy."))

# ---------- TEMPLATE FOR COMMANDS ---------- #
# @bot.command()
# async def test(ctx, arg):
#     await ctx.send(arg)

@bot.command()
async def update(ctx):
    await ctx.channel.send('Updating the database. This will take around three (3) minutes to finish. You will be pinged after the database is updated. In the meantime, the bot will be unusable.')
    await update_database()
    await ctx.channel.send(f'Database is updated. <@{ctx.author.id}>')

@bot.command()
async def join(ctx, class_code = None, section = None):
    if not section:
        await ctx.channel.send('You either did not enter the class code or the section.\nPlease try again.')
        return
    await ctx.channel.send(f'The class code you entered is: {class_code}')
    await ctx.channel.send(f'The section you entered is: {section}')

    if class_code not in db['roles']:
        add_subj_to_db(class_code, section)
        role = await ctx.guild.create_role(name=f'{class_code} {section}', mentionable=True)
    
    print(db.keys()) # for debugging

    await ctx.author.add_roles(role)
    await ctx.send(f"Successfully created and assigned {role.mention}!")


# @bot.command()
# async def test(ctx,):
#     add_to_role(ctx.message.author.id, 'PHILO132.2i', 'A')
            
bot.run(os.getenv('TOKEN'))