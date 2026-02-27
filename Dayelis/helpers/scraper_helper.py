import discord
import aiohttp
from bs4 import BeautifulSoup, NavigableString, Tag
import urllib.parse

class ScraperHelper:
    def __init__(self):
        self.base_url = "https://2e.aonprd.com/"

    # Function takes query, combines it with the base url, and encodes it for spaces. Then it makes a request to the search url and parses the HTML using BeautifulSoup. 
    # It looks for links that match the category and query, and returns the full URL if found. If not found, it returns an error message.
    async def search_pathfinder(self, query: str, category: str):
        encoded_query = urllib.parse.quote(query) # encodes spaces
        search_url = f"{self.base_url}search?q={encoded_query}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch search results. Status code: {response.status}")
                html = await response.text()
        
        soup = BeautifulSoup(html, 'html.parser')
        
        links = soup.find_all("a", href=True, text=True)
        
        for link in links:
            href = link['href']
            text = link.get_text()
            if f"{category}.aspx" in href and text.lower() == query.lower():
                return f"{self.base_url}{href}"
            else:
                return None
    
    # NOTE: FOLLOWING FUNCTIONS ARE PLACEHOLDER AND NOT FINAL. THESE ARE BASIC SHAPES AND WILL ALL BE ADJUSTED. 
    # Character Related ie Class, Ancestry, Feats, Archetypes        
    async def build_ancestry_embed(self, url: str):
        
        html = await self.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        #Extract data from site, organize data and assign to different values
        ancestryName = soup.find("div", id="main-wrapper").find("div", id="main").find("h1", class_="title").find("a").get_text(strip=True)
        
        main_div = soup.select_one("div#main.main")
        spans = main_div.find_all("span")
        target_span = spans[2]
        full_text = ""
        for child in target_span.children:
            if isinstance(child, NavigableString):
                text = child.strip()
                if text:
                    full_text += text + " "
            elif isinstance(child, Tag):
                if child.name == "i":
                    full_text += child.get_text(strip=True) + " "
                elif child.name == "br":
                    continue
                else:
                    full_text += child.get_text(strip=True) + " "
        ancestryDescription = full_text
        
        
        
        ancestry_embed = discord.Embed(
            title = ancestryName,
            description = ancestryDescription,
            color = discord.Color.Red(),
        )
        
        ancestry_embed.add_field(name="Hit Points", value = hpValue, inline= True)
        ancestry_embed.add_field(name="Size", value = sizeValue, inline= True)
        ancestry_embed.add_field(name="Speed", value = speedValue, inline= True)
        ancestry_embed.add_field(name="Ability Boosts", value = abilityBoostsValue, inline= False)
        ancestry_embed.add_field(name="Ability Flaw(s)", value = abilityFlawsValue, inline= True)
        ancestry_embed.add_field(name="Languages", value = languagesKnown, inline= False)
        
        return ancestry_embed
     
    async def build_class_embed(self, url: str):
        
        html = await self.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        #Extract data from site, organize data and assign to different values
        
        class_embed = discord.Embed(
            title = className,
            description = classDescription,
            color = discord.Color.Red(),
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
