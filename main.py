import pip
import discord
import os
import asyncio
from discord.ext import commands
from discord import utils
bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
@bot.command()
async def ping(ctx):
  await ctx.send("pong")

@bot.command()
async def test(ctx):
    await ctx.send("1")
    await asyncio.sleep(10)
    await ctx.send("2")

for filename in os.listdir('C:/Users/morar/Documents/Python Scripts/bot RP/cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'[{filename[:-3]}] successfully loaded')
        except Exception as e:
            print(f'[{filename[:-3]}] failed to load : {e}')

bot.run("Nzg1NTQ0MTAxNTAzMTcyNjE5.X85Y9A.IgHZQVUULm4VUlSUv8BrUalJIHM")