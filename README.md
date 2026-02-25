# Dayelis
This is the bot maintained by me for personal use in my TTRPG group with my close friends. This bots purpose was to learn about Discord bot programming, and implement functionality I think would be useful. 

## Libraries / Dependencies
Dayelis using the following libraries for basic functionality:

- **discord.py** for the Discord bot api and commands
- **python-dotenv** for loading environment variables from a .env file
- **asyncio** for asynchronous operations, which is what the commands are built off of
- **beautifulsoup4** for web scraping, specifically getting information from Archives of Nethys and creating it into an embeded image

## Current Functions:  
!pf2e to pull up Archives of Nethys link for Pathfinder 2E  

!sf2e to pull up Archievs of Netyhs link for Starfinder 2E  

!foundry to pull up a Foundry link, set by environment variable
 
!hello to get a random greeting
 
!announcement to send an embedded announcement. Dayelis will prompt the user for the information, and reiterate a loop for every new field (up to 25)

!reloadcog <cog name> to reload a cog for new functionality

## Future Implementation
Webscraping using beautifulsoup4 to be able to embed different aspects of Pathfinder/Starfinder, like creatures, features, spells, and items. 
