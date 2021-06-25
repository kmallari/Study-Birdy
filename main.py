from discord.ext import commands
import os
from scraper import update_database

# client = discord.Client()

bot = commands.Bot(command_prefix="~")

@bot.event
async def on_ready():
    print(f"Bot is ready")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="example"))

# ---------- TEMPLATE FOR COMMANDS ---------- #
# @bot.command()
# async def test(ctx, arg):
#     await ctx.send(arg)

@bot.command()
async def update(arg):
    await arg.channel.send('Updating the database. This will take around three (3) minutes to finish. You will be pinged after the database is updated. In the meantime, the bot will be unusable.')
    await update_database()
    await arg.channel.send(f'Database is updated. <@{arg.author.id}>')

@bot.command()
async def add(ctx, class_code, section):
    await ctx.channel.send(f'The class code you entered is: {class_code}')
    await ctx.channel.send(f'The section you entered is: {section}')
            
bot.run(os.getenv('TOKEN'))