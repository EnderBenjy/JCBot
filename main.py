import os
import datetime
import discord
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(command_prefix=commands.when_mentioned_or(","),
                   description='JC Multipurpose bot ^^',
                   case_insensitive=False,
                   intents=discord.Intents.all())

bot.uptime = datetime.datetime.now()
bot.messages_in = bot.messages_out = 0
bot.region = 'France'


@bot.event
async def on_ready():
    print('Connecté comme {0} ({0.id})'.format(bot.user))
  
    # Load Modules
    modules = ['Translator', 'Test', 'Leveling', 'Status', 'Speedrun']
    for module in modules:
        try:
            await bot.load_extension('cogs.' + module)
            print('Loaded: ' + module)
        except Exception as e:
            print(f'Error loading {module}: {e}')

    await bot.tree.sync()
          
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Game(name="React with flag for translation !"))
      
    print('Bot.....Activated')
      

  
# Ready to start!
keep_alive()
print('Starting Bot...')
bot.run(os.environ['TOKEN'])
