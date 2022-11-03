import discord
from discord.ext import commands
import requests, uuid, json
from discord import app_commands

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name = 'test', description = ('random command'))    
    async def test_slash(self, interaction: discord.Interaction): 
      await interaction.response.send_message('ca marche !')

    @commands.command()
    async def test(self, ctx):
      await ctx.send('salut')
      
async def setup(client):
    await client.add_cog(Test(client))