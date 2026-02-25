import discord
import aiohttp
from bs4 import BeautifulSoup
import urllib.parse

class ScraperHelper:
    def __init__(self):
        self.base_url = "https://2e.aonprd.com/"

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
            text = link.get_text
            if f"{category}.aspx" in href and text.lower() == query.lower():
                return f"{self.base_url}{href}"
        return (f"Sorry, I couldn't find a {category} named '{query}'. Please check the spelling and try again.")        
    
    