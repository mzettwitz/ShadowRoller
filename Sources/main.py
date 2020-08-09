from discord.ext import commands
from util import *

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('{0.user} dice bot is ready to roll.'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    send, msg = validate(message)
    if send:
        await message.channel.send(msg)

#read credentials and run server
f = open("../Ressources/credentials.txt", "r")
cred = f.read()
client.run(cred)
