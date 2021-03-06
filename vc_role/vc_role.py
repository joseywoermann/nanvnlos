import discord
from discord.ext import commands
import logging
from main import make_error_embed


class VC_role(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        vc_role = discord.utils.get(member.guild.roles, name="in voicechat")

        if before.channel is None:
            try:
                await member.add_roles(vc_role)
            except Exception as e:
                make_error_embed(e)

        if after.channel is None:
            try:
                await member.remove_roles(vc_role)
            except Exception as e:
                make_error_embed(e)

def setup(client):
    client.add_cog(VC_role(client))
