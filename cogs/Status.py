import discord
from discord.ext import commands
import requests
from discord import app_commands
from discord.app_commands import Choice


def get_infos(interaction, ip, motd, pl):
  url = 'https://api.mcsrvstat.us/2/' + ip
  response = requests.get(url)
  result = response.json()

  if result['online'] == False:
    return discord.Embed(title='Server is offline :name_badge:', description="IP: " + ip, color=0x14aaeb)

  player_amount = result['players']['online']
  player_max = result['players']['max']
  version = result['version']

  embed = discord.Embed(title='Server is online :white_check_mark:', description="IP: " + ip, color=0x14aaeb)
  embed.set_thumbnail(url="https://api.mcsrvstat.us/icon/"+ip)
  embed.add_field(name="Version:", value=f"{version}", inline=True)
  
  if motd == 1:
    embed.set_image(url="https://api.loohpjames.com/serverbanner.png?ip=" + ip + "&width=1000")

  if pl == 1:
    try:
      liste = result['players']['list']
      player_list = ' * '.join(liste)
      if player_amount <= 12:
        embed.add_field(name='Player List:', value = f'{player_list}')
      else:
        embed.add_field(name='Player List:', value = f'{player_list} * ...')
    except:
      embed.add_field(name='Player List:', value = 'Unable to get the player list.')

  embed.add_field(name="Online Players", value=f"{player_amount} / {player_max}", inline=True)
  embed.set_footer(text='You can also show motd / playerlist !', icon_url = interaction.user.avatar)
  return embed



class MCServ(commands.Cog) :
    def __init__(self, client) :
        self.client = client

    @app_commands.command(name = 'serverstatus', description = 'Fetch server\'s status/informations')
    @app_commands.describe(ip = "Default: jumpcraft.org", motd = "Default: False", playerlist = "Default: False")
    @app_commands.choices(motd = [Choice(name = 'True', value = 1), Choice(name = 'False', value = 0)], playerlist = [Choice(name = 'True', value = 1), Choice(name = 'False', value = 0)])
    async def mcserv(self, interaction: discord.Interaction, ip:str = 'jumpcraft.org', motd:int = 0, playerlist:int = 0):
            result = get_infos(interaction, ip, motd, playerlist)
            await interaction.response.send_message(embed=result)


async def setup(bot) :
    await bot.add_cog(MCServ(bot))