from discord.ext import commands
import discord
from discord.utils import get
import os
from scraper import update_database
from bisect_seek import find_subject
from replit import db # allows access to replit database

# client = discord.Client()

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="~", intents=intents)

def add_class_to_db(class_code, section):
    code_sec_str = f'{class_code} {section}'
    if code_sec_str in db.keys():
        return
    subj_info = find_subject('subjects.csv', class_code, section)
    if subj_info == False:
        return subj_info
    db[code_sec_str] = subj_info
    return True

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
async def join(ctx, class_code = None, section = None, excess_arg = None):
    if excess_arg:
        await ctx.send('You entered too many arguments. Make sure to format your message correctly.')
        return

    if not section:
        await ctx.channel.send('You either did not enter the class code or the section.\nPlease try again.')
        return

    # checks if class role exists
    if f'{class_code} {section}' not in db.keys():
        if add_class_to_db(class_code, section):
            role = await ctx.guild.create_role(name=f'{class_code} {section}', mentionable=True)
        else:
            await ctx.send(f'Class __{class_code} {section}__ was not found in our database.')
            return
    
    role = discord.utils.get(ctx.guild.roles, name = f'{class_code} {section}')

    # checks if user is already in the class
    if role in ctx.author.roles:
        await ctx.send(':red_circle: You\'re already in that class.')
    else:
        await ctx.author.add_roles(role)
        await ctx.send(f":white_check_mark: Added you to the class: __{class_code} {section}__")

@bot.command()
async def leave(ctx, class_code = None, section = None, excess_arg = None):
    if excess_arg:
        await ctx.send('You entered too many arguments. Make sure to format your message correctly.')
        return

    role = discord.utils.get(ctx.guild.roles, name = f'{class_code} {section}')

    if role not in ctx.author.roles:
        await ctx.send(f':red_circle: You\'re not in the class: {class_code} {section}')
    else:
        await ctx.send(f'Removing you from __{class_code} {section}__')
        await ctx.author.remove_roles(role)

    await cleardb(ctx)
             
@bot.command()
async def clear(ctx):
    for role in ctx.author.roles:
        if role.name in db.keys():
            # role = discord.utils.get(ctx.guild.roles, name = r.name)
            await ctx.send(f'Removing you from: __{role.name}__')
            await ctx.author.remove_roles(role)

    await cleardb(ctx)

@bot.command()
async def cleardb(ctx):
    for key in db.keys():
        role = discord.utils.get(ctx.guild.roles, name = key)
        if len(role.members) == 0:
            del db[key]
            await role.delete()

@bot.command()
async def classes(ctx):
    has_class = False
    for role in ctx.author.roles:
        if role.name in db.keys():
            try:
                await ctx.send(f'''**Subject code**: {db[role.name][0]}, **Section**: {db[role.name][1]}
**Course Title**: {db[role.name][2]}
**Units**: {db[role.name][3]}
**Schedule**: {db[role.name][4]}
**Professor**: {db[role.name][6]}
**Zoom link**: {db[role.name][14]} (added by <@{db[role.name][15]}>)\n-----
'''.replace('|', ','))
            except:
                await ctx.send(f'''**Subject code**: {db[role.name][0]}, **Section**: {db[role.name][1]}
**Course Title**: {db[role.name][2]}
**Units**: {db[role.name][3]}
**Schedule**: {db[role.name][4]}
**Professor**: {db[role.name][6]}
No zoom link in our database.\n-----
'''.replace('|', ','))
            has_class = True
    if not has_class:
        ctx.send('You have not joined any classes.')

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

# --------------------
            
bot.run(os.getenv('TOKEN'))