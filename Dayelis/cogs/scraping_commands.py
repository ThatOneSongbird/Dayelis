import discord
import random
from discord.ext import commands
import asyncio

class Scraping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scraper = ScraperHelper()

    # Character Related ie Class, Ancestry, Feats, Archetypes
    @commands.command()
    async def ancestry(self, ctx, *, ancestry_name: str):
        try:
            ancestry_embed = await self.scraper.build_ancestry_embed(ancestry_name)
        except Exception:
            await ctx.send("I couldn't find that ancestry. Please check the spelling and try again.")
            return

        await ctx.send(embed=ancestry_embed)
        
    @commands.command()
    async def cclass(self, ctx, *, class_name: str): # needed to be cclass becuase class is a reserved word in python lol
        try:
            class_embed = await self.scraper.build_class_embed(class_name)
        except Exception:
            await ctx.send("I couldn't find that class. Please check the spelling and try again.")
            return

        await ctx.send(embed=class_embed)

    @commands.command()
    async def archetype(self, ctx, *, archetype_name: str):
        try:
            archetype_embed = await self.scraper.build_archetype_embed(archetype_name)
        except Exception:
            await ctx.send("I couldn't find that archetype. Please check the spelling and try again.")
            return

        await ctx.send(embed=archetype_embed)
        
    @commands.command()
    async def feats(self, ctx, *, feat_name: str):
        try:
            feat_embed = await self.scraper.build_feat_embed(feat_name)
        except Exception:
            await ctx.send("I couldn't find that feat. Please check the spelling and try again.")
            return

        await ctx.send(embed=feat_embed)
        
    # Creature, Spell, Items 
    @commands.command()
    async def creature(self, ctx, *, creature_name: str):
        try:
            creature_embed = await self.scraper.build_creature_embed(creature_name)
        except Exception:
            await ctx.send("I couldn't find that creature. Please check the spelling and try again.")
            return

        await ctx.send(embed=creature_embed)
        
    @commands.command()
    async def spell(self, ctx, *, spell_name: str):
        try:
            spell_embed = await self.scraper.build_spell_embed(spell_name)
        except Exception:
            await ctx.send("I couldn't find that spell. Please check the spelling and try again.")
            return

        await ctx.send(embed=spell_embed)
    
    @commands.command()
    async def item(self, ctx, *, item_name: str):
        try:
            item_embed = await self.scraper.build_item_embed(item_name)
        except Exception:
            await ctx.send("I couldn't find that item. Please check the spelling and try again.")
            return

        await ctx.send(embed=item_embed)
        
# Adds cog to bot
async def setup(bot):
    await bot.add_cog(Scraping(bot))
