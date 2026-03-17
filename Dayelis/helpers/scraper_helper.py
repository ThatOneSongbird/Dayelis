import discord
import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup, NavigableString, Tag
import urllib.parse
from urllib.parse import urljoin, urlparse, parse_qs

class ScraperHelper:
    def __init__(self):
        self.CATEGORY_URLS = {
        "ancestries": "https://2e.aonprd.com/Ancestries.aspx",
        "archetypes": "https://2e.aonprd.com/Archetypes.aspx",
        "classes": "https://2e.aonprd.com/Classes.aspx",
        "equipment": "https://2e.aonprd.com/Equipment.aspx",
        "creatures": "https://2e.aonprd.com/Creatures.aspx",
        "feats": "https://2e.aonprd.com/Feats.aspx",
        "spells": "https://2e.aonprd.com/Spells.aspx"
        }
        
        #functions to load jsons on initalization
        with open("helpers/data/ancestry-table.json", encoding = "utf-8") as f:
            content = f.read()
            content = content.replace("\\u00e2\\u20ac\\u00a6",  "...")
            self.ancestries = json.loads(content)
        with open("helpers/data/archetype-table.json", encoding = "utf-8") as f:
            self.archetypes = json.load(f)
        with open("helpers/data/background-table.json", encoding = "utf-8") as f:
            self.backgrounds = json.load(f)
        with open("helpers/data/class-table.json", encoding = "utf-8") as f:
            self.classes = json.load(f)
        with open("helpers/data/feat-table.json", encoding="utf-8") as f:
            content = f.read()
            content = content.replace("\\u2019", "'")
            self.feats = json.loads(content)
        with open("helpers/data/creature-table.json", encoding="utf-8") as f:
            self.creatures = json.load(f)
        with open("helpers/data/spell-table.json", encoding = "utf-8") as f:
            self.spells = json.load(f)
        
    async def fetch_page(self, url: str) -> str:
        #fetch html content of a url asynchronously
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch page. Status code: {response.status}")
                return await response.text()
            
    # NOTE: ID matching for creatures may conflict where same-named creatures
    # exist across multiple sources. To be handled in future update.        
    async def fetch_id(self, name:str, category:str):
        # function to match category to CATEGORY_URLS, and then find the url/id
        html = await self.fetch_page(self.CATEGORY_URLS.get(category.lower()))
        soup = BeautifulSoup(html, 'html.parser')
        
        links = soup.select("a[href]")
        
        for link in links:
            href = link.get("href", "")
            text = link.get_text(strip=True)
            
            if name.lower() in text.lower() and "ID=" in href:
                parsed = parse_qs(urlparse(href).query)
                id = parsed["ID"][0]
                url = urljoin("https://2e.aonprd.com/", href)
                
                #fetch for image
                html2 = await self.fetch_page(url)
                soup2 = BeautifulSoup(html2, 'html.parser')
                
                image_tag = soup2.select_one("div#main.main a img.thumbnail")
                if image_tag:
                        src = image_tag.get("src").replace("\\", "/")
                        image_url = urljoin("https://2e.aonprd.com/", src)
                else:
                    image_url = ""

                return id, url, image_url
                
        return None, None, ""
        
    # NOTE: FOLLOWING FUNCTIONS ARE PLACEHOLDER AND NOT FINAL. THESE ARE BASIC SHAPES AND WILL ALL BE ADJUSTED. 
    # Character Related ie Class, Ancestry, Feats, Archetypes        
    async def build_ancestry_embed(self, name: str):
        entry = next((e for e in self.ancestries if e["name"].lower() == name.lower()), None)

        if not entry:
            raise ValueError(f"Could not find {name} in ancestries data.")

        if "id" in entry and entry["id"] and "image_url" in entry:
            # construct both urls directly
            url = f"https://2e.aonprd.com/Ancestries.aspx?ID={entry['id']}"
            image_url = entry["image_url"]
        else:
            # call the fetch_id
            id, url, image_url = await self.fetch_id(name, "ancestries")
            entry["id"] = id
            entry["url"] = url
            entry["image_url"] = image_url
            with open("helpers/data/ancestry-table.json", "w", encoding = "utf-8") as f:
                json.dump(self.ancestries, f, indent=4)
        
        ancestryName = entry["name"]
        ancestryDescription = entry["summary"]
        
    
        # builds the embed using the extracted data from the json, matching key names to key values
        ancestry_embed = discord.Embed(
            title = ancestryName,
            url = url,
            description = ancestryDescription,
            color = discord.Color.red(),
        )
        
        if image_url:
            ancestry_embed.set_thumbnail(url=image_url)        
        
        ancestry_embed.add_field(name="Hit Points", value=entry["hp"], inline=True)
        ancestry_embed.add_field(name="Size", value=entry["size"], inline=True)
        ancestry_embed.add_field(name="Speed", value=entry["speed"], inline=True)
        ancestry_embed.add_field(name="Attribute Boosts", value=entry["ability_boost"], inline=False)
        ancestry_embed.add_field(name="Attribute Flaw", value=entry["ability_flaw"] or "None", inline=True)
        ancestry_embed.add_field(name="Languages", value=entry["language"], inline=False)
        ancestry_embed.add_field(name="Vision", value=entry["vision"] or "Normal", inline=True)
        
        return ancestry_embed
     
    async def build_class_embed(self, name: str):
        entry = next((e for e in self.classes if e["name"].lower() == name.lower()), None)
        
        if not entry:
            raise ValueError(f"Could not find {name} in classes data.")

        if "id" in entry and entry["id"] and "image_url" in entry:
            # construct both urls directly
            url = f"https://2e.aonprd.com/Classes.aspx?ID={entry['id']}"
            image_url = entry["image_url"]
        else:
            # call the fetch_id
            id, url, image_url = await self.fetch_id(name, "classes")
            entry["id"] = id
            entry["url"] = url
            entry["image_url"] = image_url
            with open("helpers/data/class-table.json", "w", encoding = "utf-8") as f:
                json.dump(self.classes, f, indent=4)
        
        className = entry["name"]
        classDescription = entry["summary"]
        
    
        # builds the embed using the extracted data from the json, matching key names to key values
        class_embed = discord.Embed(
            title = className,
            url = url,
            description = classDescription,
            color = discord.Color.red(),
        )
        
        if image_url:
            class_embed.set_thumbnail(url=image_url)        
        
        class_embed.add_field(name="Main Stat", value=entry["ability"], inline=True)
        class_embed.add_field(name="Starting Hit Points", value=entry["hp"], inline=True)
        class_embed.add_field(name="Spellcasting Tradition", value=entry["tradition"] or "Not Caster", inline=False)
        class_embed.add_field(name="Attack Proficiencies", value=entry["attack_proficiency"], inline=True)
        class_embed.add_field(name="Defense Proficiencies", value=entry["defense_proficiency"] or "None", inline=True)
        class_embed.add_field(name="Fortitude Proficiency", value=entry["fortitude_proficiency"], inline=False)
        class_embed.add_field(name="Reflex Proficiency", value=entry["reflex_proficiency"] , inline=False)
        class_embed.add_field(name="Will Proficiency", value=entry["will_proficiency"], inline=False)
        class_embed.add_field(name="Skill Proficiencies", value=entry["skill_proficiency"], inline=False)

        return class_embed
    
    async def build_archetype_embed(self, name: str):
        entry = next((e for e in self.archetypes if e["name"].lower() == name.lower()), None)

        if not entry:
            raise ValueError(f"Could not find {name} in archetype data.")

        if "id" in entry and entry["id"] and "image_url" in entry:
            # construct both urls directly
            url = f"https://2e.aonprd.com/Archetypes.aspx?ID={entry['id']}"
            image_url = entry["image_url"]
        else:
            # call the fetch_id
            id, url, image_url = await self.fetch_id(name, "archetypes")
            entry["id"] = id
            entry["url"] = url
            entry["image_url"] = image_url
            with open("helpers/data/archetype-table.json", "w", encoding = "utf-8") as f:
                json.dump(self.archetypes, f, indent=4)
        
        archetypeName = entry["name"]
        archetypeDescription = entry["summary"]
        
        # builds the embed using the extracted data from the json, matching key names to key values
        archetype_embed = discord.Embed(
            title = archetypeName,
            url = url,
            description = archetypeDescription,
            color = discord.Color.red(),
        )
        
        archetype_embed.add_field(name="Prerequisite", value=entry["prerequisite"] or "None", inline=False)
        
        if image_url:
            archetype_embed.set_thumbnail(url=image_url)        
        
        return archetype_embed
    
    async def build_feat_embed(self, name: str):
        entry = next((e for e in self.feats if e["name"].lower() == name.lower()), None)
        
        #same call without image since no images across, and search is slightly different
        if "id" in entry and entry["id"]:
            url = f"https://2e.aonprd.com/Feats.aspx?ID={entry['id']}"
        elif "url" in entry and entry["url"]:
            url = urljoin("https://2e.aonprd.com/", entry["url"])
        else:
            raise ValueError(f"No URL found for {name}")

        feat_embed = discord.Embed(
            title=entry["name"],
            url=url,
            description=entry["summary"],
            color=discord.Color.red(),
        )

        feat_embed.add_field(name="Level", value=entry["level"], inline=True)
        feat_embed.add_field(name="Traits", value=entry["trait"] or "None", inline=False)
        feat_embed.add_field(name="Prerequisite", value=entry["prerequisite"] or "None", inline=False)

        return feat_embed
    
    async def build_creature_embed(self, name: str):
        entry = next((e for e in self.creatures if e["name"].lower() == name.lower()), None)

        if not entry:
            raise ValueError(f"Could not find {name} in creatures data.")

        #since url is already known, we do one search to find the image url, and then cache that **if** it has an image, otherwise empty
        if "image_url" in entry and entry["image_url"]:
            url = urljoin("https://2e.aonprd.com/", entry["url"])
            image_url = entry["image_url"]
        elif "url" in entry and entry["url"]:
            url = urljoin("https://2e.aonprd.com/", entry["url"])
            html = await self.fetch_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            image_tag = soup.select_one("div#main.main a img.thumbnail")
            if image_tag:
                src = image_tag.get("src").replace("\\", "/")
                image_url = urljoin("https://2e.aonprd.com/", src)
            else:
                image_url = ""
            entry["image_url"] = image_url
            with open("helpers/data/creature-table.json", "w", encoding="utf-8") as f:
                json.dump(self.creatures, f, indent=4)
        else:
            url = None
            image_url = ""

        creature_embed = discord.Embed(
            title=entry["name"],
            url=url,
            description=entry.get("summary", ""),
            color=discord.Color.red(),
        )

        if image_url:
            creature_embed.set_thumbnail(url=image_url)
        
        creature_embed.add_field(name="Level", value=entry["level"], inline=False)
        creature_embed.add_field(name="Size", value=entry["size"], inline=False)
        creature_embed.add_field(name="Traits", value=entry["trait"] or "None", inline=False)
        if entry["creature_family"]:
            creature_embed.add_field(name="Creature Family", value=entry["creature_family"], inline=False)
        creature_embed.add_field(name="HP", value=entry["hp"], inline=True)
        creature_embed.add_field(name="AC", value=entry["ac"], inline=True)
        creature_embed.add_field(name="Perception", value=entry["perception"], inline=False)
        creature_embed.add_field(name="Senses", value=entry["sense"] or "Normal", inline=False)
        creature_embed.add_field(name="Speed", value=entry["speed"], inline=False)
        creature_embed.add_field(name="Fortitude", value=entry["fortitude"], inline=True)
        creature_embed.add_field(name="Reflex", value=entry["reflex"], inline=True)
        creature_embed.add_field(name="Will", value=entry["will"], inline=True)

        return creature_embed
    
    async def build_spell_embed(self, name: str):
        entry = next((e for e in self.spells if e["name"].lower() == name.lower()), None)

        if not entry:
            raise ValueError(f"Could not find {name} in spells data.")

        if "url" in entry and entry["url"]:
            url = urljoin("https://2e.aonprd.com/", entry["url"])
        else:
            url = None

        spell_embed = discord.Embed(
            title=entry["name"],
            url=url,
            description=entry["summary"],
            color=discord.Color.red(),
        )
        
        spell_embed.add_field(name="Spell Type", value=entry["spell_type"], inline=False)
        spell_embed.add_field(name="Rank", value=entry["rank"], inline=False)
        if entry["heighten"]:
            spell_embed.add_field(name="Heighten", value=entry["heighten"], inline=False)
        if entry["tradition"]:
            spell_embed.add_field(name="Tradition", value=entry["tradition"], inline=False)
        if entry["school"]:
            spell_embed.add_field(name="School", value=entry["school"], inline=False)   
        if entry["trait"]:
            spell_embed.add_field(name="Traits", value=entry["trait"], inline=False)
        spell_embed.add_field(name="Actions", value=entry["actions"], inline=False)
        if entry["component"]:
            spell_embed.add_field(name="Components", value=entry["component"], inline=False)
        if entry["trigger"]:
            spell_embed.add_field(name="Trigger", value=entry["trigger"], inline=False)
        if entry["target"]:
            spell_embed.add_field(name="Target", value=entry["target"], inline=True)
        if entry["range"]:
            spell_embed.add_field(name="Range", value=entry["range"], inline=True)
        if entry["area"]:
            spell_embed.add_field(name="Area", value=entry["area"], inline=True)
        if entry["duration"]:
            spell_embed.add_field(name="Duration", value=entry["duration"], inline=False)
        if entry["defense"]:
            spell_embed.add_field(name="Defense", value=entry["defense"], inline=False)

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
