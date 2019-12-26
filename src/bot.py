from sys import argv
from requests import get
import discord

recent_hashes = []
channel_list = []

client = discord.Client()

def package_updates():
    r = get("https://api.github.com/repos/void-linux/void-packages/commits")
    if r:
        print(r.json())

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    for server in client.guilds:
        for channel in server.channels:
            if channel.name == 'void-packages':
                channel_list.append(channel)

    updates = package_updates()
    if updates:
        for update in updates:
            await channel.send("Package {} was updated!")

# check if commandline argument was passed and exit if not
if len(argv) < 2:
    print("No auth token passed as a commandline option.")
    print("Syntax: python bot.py <token>")
    exit()
else:
    client.run(argv[1])
