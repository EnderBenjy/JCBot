import discord
from discord.ext import commands
import requests, uuid, json
from discord import app_commands
from math import sqrt, floor
  
class Leveling(commands.Cog):
    def __init__(self, client):
        self.client = client
      
    @app_commands.command(name = 'level', description = ('Calculate in-game level cost')) 
    async def level(self, interaction: discord.Interaction, level1:int, level2:int):
        cost = 500*(level2*(level2+1) - level1*(level1+1))
        await interaction.response.send_message(f'Level {level1} to {level2}: \nYou need **${cost:,}.** \nThat\'s worth {cost/200} speed potions!')

    @app_commands.command(name = 'maxlevel', description = ('Calculate in-game reachable level')) 
    async def maxlevel(self, interaction: discord.Interaction, level1:int, money:int):
        level2 = floor((1/2)*(sqrt(1+4*(money/500 + level1 * (level1 + 1))) -1))
        await interaction.response.send_message(f'Level {level1} with ${money:,}: \nYou can get to level **{level2}.** \nYou would have: **${money - (500*(level2*(level2+1) - level1*(level1+1))):,}** left!')
      
async def setup(client):
    await client.add_cog(Leveling(client))