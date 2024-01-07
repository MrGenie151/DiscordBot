import discord
from discord.ext import commands
import requests
import json
import os
import dotenv
dotenv.load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='gb!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

def split_string(input_string):
    max_length = 2000
    return [input_string[i:i+max_length] for i in range(0, len(input_string), max_length)]

@bot.command(name="rbxoutfits")
async def hello(ctx, username):
    print(username)
    data = {
        "usernames": [
            username
        ],
        "excludeBannedUsers": True
    }
    useridRequest = requests.post("https://users.roblox.com/v1/usernames/users",json=data)
    print(useridRequest.content)
    userid = json.loads(useridRequest.content)
    print(userid["data"][0]["id"])
    r = requests.get("https://avatar.roblox.com/v1/users/" + str(userid["data"][0]["id"]) + "/outfits?page=1&itemsPerPage=999&isEditable=true")
    #print(r.content)
    outfits = json.loads(r.content)
    outfitString = "Outfits"
    for outfit in outfits["data"]:
        outfitString += "\nOutfit Name: " + outfit["name"] + "\nOutfit ID: " + str(outfit["id"])+"\n"
    
    checkers = split_string(outfitString)
    for thing in checkers:
        await ctx.send(thing)
    await ctx.send('Finished sending outfits for ' + userid["data"][0]["displayName"])

# Add more commands here!

bot.run(os.getenv("TOKEN"))
