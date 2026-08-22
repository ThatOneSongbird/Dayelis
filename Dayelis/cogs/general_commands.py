import discord
import random
from discord.ext import commands
from datetime import datetime, timedelta, time
import asyncio
import pytz

CT = pytz.timezone("America/Chicago")

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()  # Only the bot owner can run this
    async def reloadcog(self, ctx, cog_name: str):
        """Reload a cog by name (e.g., general_commands)"""
        try:
            await self.bot.reload_extension(f"cogs.{cog_name}")
            await ctx.send(f"The Cog `{cog_name}` has been refreshed. Never felt better.")
        except Exception as e:
            await ctx.send(f"Unfortunately,`{cog_name}` has failed to load: {e}")
            
    @commands.command()
    async def hello(self, ctx):
        bot_hellos = [
            "Hello dear friend.",
            "Greetings, traveler.",
            "How was your day, weary soul?",
            f"Oh hello {ctx.author.mention}, how are you friend?",
            "It's a pleasure to make your aquaintance.",
            "Oh...it's you.",
        ]
        selected_greeting = random.choice(bot_hellos)
        await ctx.send(selected_greeting)

    @commands.command()
    @commands.has_permissions(administrator=True)
    # Session Warning
    async def warning(self, ctx, hours: int, minutes: int = 0):
        target_channel = self.bot.get_channel(self.bot.ANNOUNCEMENT_CHANNEL_ID)
        if target_channel:
            if hours > 0 and minutes > 0:
                await target_channel.send(
                    f"<@&{self.bot.PLAYER_ROLE_ID}> Warning: Session starts in {hours} hours and {minutes} minutes!")
            elif hours == 0 and minutes > 0:
                await target_channel.send(f"<@&{self.bot.PLAYER_ROLE_ID}> Time is approaching!Session starts in {minutes} minutes!")
            else:               
                await target_channel.send(f"<@&{self.bot.PLAYER_ROLE_ID}> Warning: Session starts in {hours} hours!")
                
            await ctx.send("Warning sent to the announcements channel!")
        else:
            await ctx.send("Error: Announcements channel not found.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    # Test command for days_since task
    async def time_since_reset(self, ctx):
        target_channel = self.bot.get_channel(self.bot.DAYS_ALIVE_CHANNEL_ID)
        days_alive = (datetime.now(CT) - self.bot.bot_start_time).days
        if target_channel:
            if days_alive == 1:
                message = await target_channel.send(
                    f"I have arisen."
                )
            elif days_alive % 7 == 0 and days_alive != 0:
                message = await target_channel.send(
                    f"What a week..."
                )
            else:
                message = await target_channel.send(
                    f"I've been alive for {days_alive} days!"
                )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def schedule():
        target_channel = self.bot.get_channel(self.bot.SCHEDULE_CHANNEL_ID)
        if target_channel:
            message = await target_channel.send(
                f"<@&{self.bot.PLAYER_ROLE_ID}> Are you guys available for the next session?\n\n👍 Yes\n👎 No\n❓ Maybe"
            )
            await message.add_reaction("👍")
            await message.add_reaction("👎")
            await message.add_reaction("❓")

    # Old Schedule command, may use in future but currently not in use.
    """@commands.command()
    @commands.has_permissions(administrator=True)
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
            await ctx.send("Error: Schedule channel not found.")"""

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        await ctx.send("Resting amongst the flowers...")
        await self.bot.close()

    @commands.command()
    async def foundry(self, ctx):
        await ctx.send(f"Foundry link: {self.bot.FOUNDRY_LINK}\nHave fun~")

    @commands.command()
    async def sf2e(self, ctx):
        await ctx.send("Archives of Nethys link for Starfinder 2e: https://2e.aonsrd.com/")

    @commands.command()
    async def pf2e(self, ctx):
        await ctx.send("Archives of Nethys link for Pathfinder 2e: https://2e.aonprd.com/")
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announcement(self, ctx):
        
        target_channel = self.bot.get_channel(self.bot.ANNOUNCEMENT_CHANNEL_ID)
        
        if target_channel is None:
            await ctx.send("Announcement channel is unfortunately not found.")
            return
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        # Ask for title
        await ctx.send("What is the title of the announcement?")
        try:
            msg = await self.bot.wait_for("message", timeout=180.0, check=check)
            title = msg.content 
        except asyncio.TimeoutError:
            await ctx.send("I'm sorry, but you took too long. Please try again.")
            return

        # Ask for description
        await ctx.send("What is the description of the announcement?")
        try: 
            msg = await self.bot.wait_for("message", timeout=180.0, check=check)
            description = msg.content
        except asyncio.TimeoutError:
            await ctx.send("I'm sorry, but you took too long. Please try again.")
            return

        # Create embed once
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.dark_green()
        )
        
        # Ask for thumbnail, must be sent in the form of an image URL, otherwise set default thumbnail.
        await ctx.send("Would you like to add a thumbnail, friend? If no, default is used. Format needs to be an image URL. (yes/no)")
        try:
            response = await self.bot.wait_for("message", timeout=180.0, check=check)
            if response.content.lower() in ["yes", "y"]:
                await ctx.send("Please provide the URL for the thumbnail:")
                url_msg = await self.bot.wait_for("message", timeout=180.0, check=check)
                embed.set_thumbnail(url=url_msg.content)
            else:
                embed.set_thumbnail(url="https://img.goodfon.com/wallpaper/big/6/63/merlin-fate-grand-order-fate-grand-order-zettai-majuu-sensen.webp")
        except asyncio.TimeoutError:
            await ctx.send("Timed out, using default thumbnail.")
            embed.set_thumbnail(url="https://img.goodfon.com/wallpaper/big/6/63/merlin-fate-grand-order-fate-grand-order-zettai-majuu-sensen.webp")
        
        # Add optional fields
        while True:
            await ctx.send("Would you like to add a field? (yes/no)")
            try: 
                response = await self.bot.wait_for("message", timeout=180.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Timed out, sorry.")
                break  # exit loop but still send embed

            if response.content.lower() not in ["yes", "y"]:
                break
            
            # Ask field info
            await ctx.send("What is the field title?")
            name_msg = await self.bot.wait_for("message", timeout=180.0, check=check)
            await ctx.send("What is the field value?")
            value_msg = await self.bot.wait_for("message", timeout=180.0, check=check)
            await ctx.send("Should this be inline? (yes/no)")
            inline_msg = await self.bot.wait_for("message", timeout=180.0, check=check)
            inline = inline_msg.content.lower() in ["yes", "y"]

            # Add field directly to embed
            embed.add_field(
                name=name_msg.content,
                value=value_msg.content,
                inline=inline
            )

        # Send final embed to announcement channel
        await target_channel.send(embed=embed)

    

# Adds cog to bot
async def setup(bot):
    await bot.add_cog(General(bot))
