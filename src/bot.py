from sys import argv
from time import sleep
from requests import get
import discord

old_hashes = None
channel_list = []

client = discord.Client()

def notify(message):
    for channel in channel_list:
        channel.send(message)

def package_updates():
    # test request
    # curl https://api.github.com/repos/void-linux/void-packages/commits | jq '.[] | .sha'
    r = get("https://api.github.com/repos/void-linux/void-packages/commits")

    new_hashes = []
    for entry in r.json():
        new_hashes.insert(0, entry['sha'])

    # if the current hashes arent listed in the old hashes, post a message
    if 'old_hashes' in vars() or 'old_hashes' in globals():
        if old_hashes != new_hashes:
            for new_entry in new_hashes:
                if new_entry not in old_hashes:
                    notify(str(new_entry['sha']))
            old_hashes = new_hashes

def update_channel_list():
    for server in client.guilds:
        for channel in server.channels:
            if channel.name == 'void-packages':
                channel_list.append(channel)

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

    while True:
        update_channel_list()
        package_updates()
        sleep(60)

# check if commandline argument was passed and exit if not
if len(argv) < 2:
    print("No auth token passed as a commandline option.")
    print("Syntax: python bot.py <token>")
    exit()
else:
    client.run(argv[1])
