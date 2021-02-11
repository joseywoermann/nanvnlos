import discord
from discord.ext import commands
import logging

class Developer(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def developer(self, ctx):
        dev_embed = discord.Embed(description="[Twitter](https://twitter.com/joseywoermann/) - [Website](https://joseywoermann.ml/) - [GitHub](https://github.com/joseywoermann/)\n\n[Discord](https://discord.gg/SchJckc) - [Reddit](https://reddit.com/u/joseywoermann/) - [Github](https://github.com/joseywoermann/)", colour=discord.Colour.dark_grey())

        dev_embed.set_author(name=ctx.message.author,icon_url=ctx.author.avatar_url)
        await ctx.reply(embed = dev_embed)


def setup(client):
    client.add_cog(Developer(client))
