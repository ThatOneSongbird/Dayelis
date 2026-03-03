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
        
        # extracts ancestry name and description from the site and puts them into their values
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
        
        # fields ot be able to properly extract data while skipping the sections we don't want
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
        
        # attempts to find thumbnail image, if it exists, and adds it to the embed. If not, it continues without adding an image.    
        image_tag = soup.select_one("div#main.main img.thumbnail")
        image_url = None
        if image_tag:
            image_url = image_tag.get("src")
            if image_url and not image_url.startswith("/"):
                image_url = self.base_url + image_url
        if image_url:
            ancestry_embed.set_thumbnail(url=image_url)
            
        
        # builds the embed using the extracted data, and adds fields for each section that is in the VALID_FIELDS set. The inline property of each field is determined by the INLINE_MAP dictionary. Finally, it returns the completed embed.
        ancestry_embed = discord.Embed(
            title = ancestryName,
            description = ancestryDescription,
            color = discord.Color.Red(),
        )
        
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
