import discord
from discord.ext import commands
import requests, uuid, json
from discord import app_commands
import utils.speedrunAPI as sr
from math import floor

class Speedrun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name = 'leaderboard', description = ('Leaderboard !'))
    async def test_slash(self, interaction: discord.Interaction, level:str):
        lb = sr.leaderboard(level)
        x = lb['data'][0]['runs']
        try:
            if len(x) == 0:
                rows = 'Empty...'
            else:
                rows = ''
                for i in range(len(x)):
                    time = x[i]['run']['times']['primary_t']
                    if time >= 60:
                        time = f'{floor(time//60)}\'{floor(time - time//60)}\"{round(1000*(time-floor(time)))}'
                    else:
                        time = f"{floor(time)}\"{round(1000*(time-floor(time)))}"
                    rows += f"{i+1}: **{sr.username(x[i]['run']['players'][0]['id'])}** with a **{time}** ([video]({x[i]['run']['videos']['links'][0]['uri']}))\n"
            embed = discord.Embed(title=f"Leaderboard of {level} ({sr.difficulty(level)})", description=f'Speedrun.com page: [Here]({sr.link(level)})',colour=discord.Colour(0xA6A67A))
            embed.set_footer(text=f"Requested by @{interaction.user.name}#{interaction.user.discriminator}",icon_url=interaction.user.avatar)
            embed.add_field(name="Leaderboard:", value=rows, inline=True)
            await interaction.response.send_message(embed = embed)
        except:
            await interaction.response.send_message("Error...")
async def setup(client):
    await client.add_cog(Speedrun(client))
