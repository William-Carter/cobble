import bot
import command
import permissions
import os
import discord
dirPath = os.path.dirname(os.path.realpath(__file__))


testBot = bot.Bot(dirPath+"/config.json", "TestBot", ".")


testBot.addCommand(command.HelpCommand(testBot))


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content[0] == testBot.prefix:
        if message.author.id in testBot.admins:
            permissionLevel = permissions.ADMIN
        elif "Trusted" in [role.name for role in message.author.roles]:
            permissionLevel = permissions.TRUSTED
        else:
            permissionLevel = permissions.EVERYONE

        await message.channel.send(testBot.processCommand(message.content[1:], permissionLevel))



client.run(testBot.token)