import discord
from discord.ext import commands
from pymongo import MongoClient
from utils import myfunctions
import os

cluster = MongoClient(os.environ.get("TODDMONGOPREFIX"))
database = cluster["todd-data"]
collection = database["prefix"]

class Prefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def prefix(self, ctx, *, value=None):
        colour = discord.Colour.from_rgb(153, 255, 102)
        guild = ctx.guild

        if not value:
            currentPrefix = myfunctions.getprefix(guild.id)

            response = discord.Embed(title="Current Prefix", colour=colour)
            response.description = (f"The current prefix for this server is `{currentPrefix}`")
            await ctx.send(embed=response)

        else:
            newPrefix = str(value)
            results = collection.find({"guild": guild.id})

            if not list(results):
                all = collection.find({})
                total = len(list(all))
                collection.insert_one({"_id": total, "guild": guild.id, "name": guild.name, "prefix": newPrefix})
            else:
                collection.update_one({"guild": guild.id}, {"$set": {"prefix": newPrefix}})

            response = discord.Embed(title="Prefix Updated", colour=colour)
            response.description = (f"The current prefix has been updated to `{newPrefix}`")
            await ctx.send(embed=response)





def setup(client):
    client.add_cog(Prefix(client))
