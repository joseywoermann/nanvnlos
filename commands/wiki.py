import discord
from discord.ext import commands
import logging

class Wiki(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def wiki(self, ctx, *, search_term):

        while ' ' in search_term:
            search_term = search_term.replace(' ', '+')

        await ctx.send("https://wikipedia.org/w/index.php?search=" + search_term)

def setup(client):
    client.add_cog(Wiki(client))
