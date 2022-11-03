import re
import discord
import os
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import requests, uuid, json
from utils.table import table

def tr_request(text, cible = 'en', origine = ''):
    url = "https://api.cognitive.microsofttranslator.com/translate"
    headers = {
        'Ocp-Apim-Subscription-Key': os.environ['microsoft'],
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    params = {
        'api-version': '3.0',
        'from': origine,
        'to': [cible]
    }

    body = [{
        'text': text
    }]

    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()

    return response

liste = [(Choice(name = k, value = v)) for k,v in table()]

class Translator(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_language(self, flag):
        with open("utils/languages.json", "r") as datafile:
            jsondata = json.loads(datafile.read())
            return jsondata.get(flag)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.count > 1:
            return
        language = self.get_language(reaction.emoji)
        if language:
            text = re.sub(
                "<@[0-9]{18}>",
                "@@@@",
                re.sub("<@![0-9]{18}>", "@@@@", reaction.message.content),)
            translated_json = tr_request(text, language)[0]
            translated_text = translated_json['translations'][0]['text']
          
            embed = discord.Embed(title=f"Translation to {language} {reaction.emoji}",description=translated_text,            colour=discord.Colour(0xA6A67A))
            embed.set_footer(text=f"Requested by @{user.name}#{user.discriminator}",icon_url=user.avatar)
            await reaction.message.channel.send(embed=embed)

    
    @app_commands.command(name = 'translate', description = 'Translates given text')
    @app_commands.describe(origin = "Original language", destination = "Destination Language", text = "Text to translate")
    @app_commands.choices(origin = liste, destination = liste)
                                
    async def translate(self, interaction: discord.Interaction, origin:str, destination:str, text:str):
        translated_json = tr_request(text, destination, origin)[0]
        translated_text = translated_json['translations'][0]['text']
        embed = discord.Embed(title=f"Translation to {destination}",description=translated_text,            colour=discord.Colour(0xA6A67A))
        embed.set_footer(text=f"Requested by @{interaction.user.name}#{interaction.user.discriminator}",icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)


async def setup(client):
    await client.add_cog(Translator(client))