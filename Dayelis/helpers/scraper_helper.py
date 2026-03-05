import discord
import asyncio
import aiohttp
from bs4 import BeautifulSoup, NavigableString, Tag
import urllib.parse
from urllib.parse import urljoin

class ScraperHelper:
    def __init__(self):
        self.CATEGORY_URLS = {
        "ancestries": "https://2e.aonprd.com/Ancestries.aspx",
        "archetypes": "https://2e.aonprd.com/Archetypes.aspx",
        "classes": "https://2e.aonprd.com/Classes.aspx",
        "equipment": "https://2e.aonprd.com/Equipment.aspx",
        "creatures": "https://2e.aonprd.com/Creatures.aspx",
        "feats": "https://2e.aonprd.com/Feats.aspx",
        "spells": "https://2e.aonprd.com/Feats.aspx"
        }
        
    async def fetch_page(self, url: str) -> str:
        #fetch html content of a url asynchronously
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch page. Status code: {response.status}")
                return await response.text()

    # Function takes query, combines it with the base url, and encodes it for spaces. Then it makes a request to the search url and parses the HTML using BeautifulSoup. 
    # It looks for links that match the category and query, and returns the full URL if found. If not found, it returns an error message.
    async def search_pathfinder(self, query: str, category: str):
        category_url = self.CATEGORY_URLS.get(category.lower())
        if not category_url:
            raise ValueError(f"Unknown category: {category}")
        print(f"{category_url}")
        
        await asyncio.sleep(2)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(category_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch search results. Status code: {response.status}")
                html = await response.text()
        
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select("a[href]")
        
        for link in links:
            href = link['href']
            text = link.get_text(strip=True)
            
            print(f"Debug Link: {href} | {text}")
            
            if query.lower() in text.lower():
                final_url = urljoin(category_url, href)
                print(f"DEBUG MATCH: {final_url}")
                return final_url
        return None
    
    # NOTE: FOLLOWING FUNCTIONS ARE PLACEHOLDER AND NOT FINAL. THESE ARE BASIC SHAPES AND WILL ALL BE ADJUSTED. 
    # Character Related ie Class, Ancestry, Feats, Archetypes        
    async def build_ancestry_embed(self, url: str, name: str):
        
        html = await self.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        main_div = soup.select_one("div#main.main")
        
        # ancestry name
        ancestryName = name
        
        # missing ancestry description
        
        # fields to be able to properly extract data while skipping the sections we don't want
        STOP_SECTIONS = {
            "You Might...",
            "Physical Description",
            "Society",
            "Beliefs",
            "Others Probably...",
            "Society",
            "Names",
            "Adventurers",
            "Other Information",
        }
        
        VALID_FIELDS = {
            "Hit Points",
            "Size",
            "Speed",
            "Attribute Boosts",
            "Attribute Flaw",
            "Languages",
        }
        
        INLINE_MAP = {
            "Hit Points": True,
            "Size": True,
            "Speed": True,
            "Attribute Boosts": False,
            "Attribute Flaw": True,
            "Languages": False,
        }
        parsed_sections = {}
        
        # section for extracting class mechanical data since they are all h2, and skips over lore sections
        for header in main_div.find_all("h2", class_="title"):
            title = header.get_text(strip=True)
            if title in STOP_SECTIONS:
                continue
            # extract value until next h2
            value = ""
            node = header.next_sibling
            while node and not (isinstance(node, Tag) and node.name == "h2"):
                if isinstance(node, NavigableString):
                    text = node.strip()
                    if text:
                        value += text + " "
                elif isinstance(node, Tag) and node.name != "br":
                    value += node.get_text(strip=True) + " "
                node = node.next_sibling
            
            parsed_sections[title] = value.strip()
        
        # builds the embed using the extracted data, and adds fields for each section that is in the VALID_FIELDS set. The inline property of each field is determined by the INLINE_MAP dictionary. Finally, it returns the completed embed.
        ancestry_embed = discord.Embed(
            title = ancestryName,
            description = ancestryDescription,
            color = discord.Color.red(),
        )        
        
        # attempts to find thumbnail image, if it exists, and adds it to the embed. If not, it continues without adding an image.    
        image_tag = soup.select_one("div#main.main img.thumbnail")
        image_url = None
        if image_tag:
            src = image_tag.get("src")
            if src:
                image_url = urljoin("https://2e.aonprd.com/", src)
        if image_url:
            ancestry_embed.set_thumbnail(url=image_url)
        
        for name, value in parsed_sections.items():
            if name in VALID_FIELDS:
                ancestry_embed.add_field(
                    name=name, 
                    value=value,
                    inline=INLINE_MAP.get(name, False)
                )
        
        return ancestry_embed
     
    async def build_class_embed(self, url: str):
        
        html = await self.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        #Extract data from site, organize data and assign to different values
        
        class_embed = discord.Embed(
            title = className,
            description = classDescription,
            color = discord.Color.red(),
        )
        
        return class_embed
    
    async def build_archetype_embed(self, url: str):
        
        html = await self.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        #Extract data from site, organize data and assign to different values
        
        archetype_embed = discord.Embed(
            title = archetypeName,
            description = archetypeDescription,
            color = discord.Color.Red(),
        )
        
        return archetype_embed
    
    async def build_feat_embed(self, url: str):
        
        html = await self.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        #Extract data from site, organize data and assign to different values
        
        feat_embed = discord.Embed(
            title = featName,
            description = featDescription,
            color = discord.Color.Red(),
        )
        
        return feat_embed
    
    # Creature, Spell, Items
    async def build_creature_embed(self, url: str):
        
        html = await self.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        #Extract data from site, organize data and assign to different values
        
        creature_embed = discord.Embed(
            title = creatureName,
            description = creatureDescription,
            color = discord.Color.Red(),
        )
        
        return creature_embed
    
    async def build_spell_embed(self, url: str):
        
        html = await self.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        #Extract data from site, organize data and assign to different values
        
        spell_embed = discord.Embed(
            title = spellName,
            description = spellDescription,
            color = discord.Color.Red(),
        )
        
        return spell_embed
    
    async def build_item_embed(self, url: str):
        
        html = await self.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        #Extract data from site, organize data and assign to different values
        
        item_embed = discord.Embed(
            title = itemName,
            description = itemDescription,
            color = discord.Color.Red(),
        )
        
        return item_embed
