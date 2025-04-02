import discord
import requests
import subprocess
import os
from dotenv import load_dotenv

TOKEN = os.getenv("TOKEN")
intents=discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
#client = discord.Client()
apikey = os.getenv("apikey")

@client.event
async def on_ready():
    pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "ip":
        ip = str(subprocess.run(["curl", "ifconfig.co"], capture_output=True).stdout).strip()
        ip = ip[2:-3]
        mullvad = str(subprocess.run(["curl", "https://am.i.mullvad.net/ip"], capture_output=True).stdout.strip())
        mullvad = mullvad[2:-1]
        await message.channel.send(f"ip: {ip}\nmullvad ip{str(mullvad)}\njellyfin link: http://{ip}:8096\njellyfin local: http://192.168.8.121:8096")
    if message.content[0:3] == "new" or message.content[0:3] == "New" :
        try:
            name = message.content.split(" ")[1]
            passw = message.content.split(" ")[2]
            headers = {
                "X-Emby-Token": apikey}
            payload = {
                "Name" : name,
                "Password" :passw
            }
            response = requests.post("http://localhost:8096/Users/New", headers=headers, json=payload)
            print(response.status_code)
            print(response.json())
            await message.channel.send(f"created new account {name} {passw}")
        except:
            await message.channel.send("error")
client.run(TOKEN)
