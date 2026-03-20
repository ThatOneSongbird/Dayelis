import discord
from discord.ext import commands, tasks
import logging 
import re
from datetime import datetime, timedelta, time
from itertools import cycle
from discord.ext.commands import MissingPermissions
from dotenv import load_dotenv
import random
import asyncio
import os
import sys
import pytz

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
    discord.Activity(type=discord.ActivityType.watching, name="over the realm of Exandria.")
])


# Task loop set to change the bot's status every minute
@tasks.loop(minutes=1)
async def change_bot_status():
    await bot.change_presence(activity=next(bot_statuses))

# Task to send a gif every Saturday, and a poll every Monday to check player availability for the next session. Both are set to Central Time (CT).
CT = pytz.timezone("America/Chicago")
    
@tasks.loop(time=time(hour = 10, minute = 0, tzinfo = CT))
async def today_is_the_day():
    if datetime.now(CT).weekday() == 5:  # 5 = Saturday
        channel = bot.get_channel(bot.ANNOUNCEMENT_CHANNEL_ID)
        await channel.send("https://tenor.com/view/today-yay-gif-25615367")
        
@tasks.loop(time=time(hour = 12, minute = 0, tzinfo = CT))
async def schedule(self, ctx):
    target_channel = self.bot.get_channel(self.bot.SCHEDULE_CHANNEL_ID)
    if target_channel:
        message = await target_channel.send(
            f"<@&{self.bot.PLAYER_ROLE_ID}> Are you guys available for the next session?\n👍 Yes\n or \n👎 No"
        )
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await ctx.send("Poll created in the schedule channel!")
    else:
        await ctx.send("Error: Schedule channel not found.")

#BOT ON_READY SECTION
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    change_bot_status.start()
    today_is_the_day.start()
    schedule.start()
    
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
        await bot.load_extension("cogs.scraping_commands")
        
        # Loads token/url from environment variable.
        TOKEN = os.getenv("DISCORD_TOKEN")
        await bot.start(TOKEN)

asyncio.run(main())
