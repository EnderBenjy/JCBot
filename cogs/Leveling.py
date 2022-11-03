import discord
from discord.ext import commands
import requests, uuid, json
from discord import app_commands
from math import sqrt
  
class Leveling(commands.Cog):
    def __init__(self, client):
        self.client = client
      
    @app_commands.command(name = 'level', description = ('Calculate level cost')) 
    async def level(self, interaction: discord.Interaction, level1:int, level2:int):
        await interaction.response.send_message(f'Cost: ${500*(level2*(level2+1) - level1*(level1+1)):,}')

    @app_commands.command(name = 'maxlevel', description = ('Calculate level cost')) 
    async def maxlevel(self, interaction: discord.Interaction, level1:int, money:int):
        level2 = round((1/2)*(sqrt(1+4*(money/500 + level1 * (level1 + 1))) -1))
        await interaction.response.send_message(f'You can get to level {level2}. \n Cost: ${500*(level2*(level2+1) - level1*(level1+1)):,}')
      
async def setup(client):
    await client.add_cog(Leveling(client))