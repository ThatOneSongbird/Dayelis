import discord
from discord.ext import commands, tasks
import logging 
import re
from datetime import datetime, timedelta
from itertools import cycle
from discord.ext.commands import MissingPermissions
from dotenv import load_dotenv
import random
import asyncio
import os
import sys

load_dotenv()  # Load environment variables from .env file

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True
allowed_mentions = discord.AllowedMentions(everyone=True, users=True, roles=True)

bot = commands.Bot(command_prefix="!", intents=intents)

# Assign environment variables to bot attributes for easy access in cogs
bot.FOUNDRY_LINK = os.getenv("FOUNDRY_URL")
bot.ANNOUNCEMENT_CHANNEL_ID = int(os.getenv("ANNOUNCEMENT_CHANNEL_ID"))
bot.SCHEDULE_CHANNEL_ID = int(os.getenv("SCHEDULE_CHANNEL_ID"))
bot.PLAYER_ROLE_ID = int(os.getenv("PLAYER_ROLE_ID"))

# LOGGING FOR MISSING ENVIRONMENT VARIABLES
required_env = [
    "DISCORD_TOKEN",
    "FOUNDRY_URL",
    "ANNOUNCEMENT_CHANNEL_ID",
    "SCHEDULE_CHANNEL_ID",
    "PLAYER_ROLE_ID"
]

# Loops through required_env, checks if any are missing/empty, and prints an error message if so. If all are present, it prints a success message.
missing = [x for x in required_env if not os.getenv(x)]
if missing:
    print(f"[ERROR] Missing environment variables: {', '.join(missing)}. Please check your .env file.")
    sys.exit(1) # Stops bot from starting
else: 
    print("[INFO] All required environment variables found. Starting bot...")
    
# FILE HANDLING SECTION
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.DEBUG, handlers=[handler])

# BOT PRESSENCE SECTION
bot_statuses = cycle([
    discord.Activity(type=discord.ActivityType.listening, name="the prayers of Exandria."),
    discord.Activity(type=discord.ActivityType.watching, name="the flowers of Verðandi bloom."),
    discord.Activity(type=discord.ActivityType.playing, name="over the realm of Exandria.")
])



@tasks.loop(minutes=1)
async def change_bot_status():
    await bot.change_presence(activity=next(bot_statuses))

#BOT ON_READY SECTION
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    change_bot_status.start()
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"Silly friend, I'm afraid you can't use that command {ctx.author.mention}. Terribly sorry.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f"You're not allowed to run this command silly. Sorry.")
    else:
        await ctx.send("Hm...uncharted waters. Strange.")
        
#LOAD COGS
async def main():
    async with bot:
        await bot.load_extension("cogs.general_commands")
        
        # Loads token/url from environment variable.
        TOKEN = os.getenv("DISCORD_TOKEN")
        await bot.start(TOKEN)

asyncio.run(main())
