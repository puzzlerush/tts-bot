import discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
import youtube_dl
import os

TOKEN = 'token'
BOT_PREFIX = 'chad '

bot = commands.Bot(command_prefix = BOT_PREFIX)
status = cycle(['Super Seducer', 'with your feelings', 'guitar'])

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_ready():
    change_status.start()
    print("Chad is ready.")
    return True

'''
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You\'re not giving me enough information.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('I don\'t know how to do that.')
'''

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded cogs.{extension}')
    print(f'Loaded cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded cogs.{extension}')
    print(f'Unloaded cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')
	bot.load_extension(f'cogs.{extension}')
	await ctx.send(f'Reloaded cogs.{extension}')
	print(f'Reloaded cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
