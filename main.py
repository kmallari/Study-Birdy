from discord.ext import commands
import discord
import os
from scraper import update_database
from bisect_seek import find_subject
from replit import db # allows access to replit database

# client = discord.Client()

bot = commands.Bot(command_prefix="~")

def add_subj_to_db(class_code, section):
    code_sec_str = f'{class_code} {section}'
    if code_sec_str in db.keys():
        return
    subj_info = find_subject('subjects.csv', class_code, section)
    db[code_sec_str] = subj_info
    print(db[code_sec_str])

def add_to_role(id, class_code, section):
    add_subj_to_db(class_code, section)
    # ---- pseudocode -----
    # check if subject role exists. if not, then call add_subj_to_db
        # now, make the role
    # add user to the role
    # ---- end of pseudocode ----

@bot.event
async def on_ready():
    print(f"Bot is ready")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="example"))

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
async def add(ctx, class_code, section):
    await ctx.channel.send(f'The class code you entered is: {class_code}')
    await ctx.channel.send(f'The section you entered is: {section}')
    add_to_role(ctx.message.author.id, class_code, section)

# @bot.command()
# async def test(ctx,):
#     add_to_role(ctx.message.author.id, 'PHILO132.2i', 'A')
            
bot.run(os.getenv('TOKEN'))