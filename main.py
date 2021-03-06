import discord
from discord.ext import commands, tasks
import logging
from itertools import cycle
import os
import os.path
import json
from discord_slash import SlashCommand
import random
from dotenv import dotenv_values
import sentry_sdk

# TOKEN stuff
config = dotenv_values(".env")

if "DISCORD_TOKEN" not in config:
    DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
else:
    DISCORD_TOKEN = config["DISCORD_TOKEN"]

if "GITHUB_TOKEN" not in config:
    GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
else:
    GITHUB_TOKEN = config["GITHUB_TOKEN"]

if "SHORTIO_TOKEN" not in config:
    SHORTIO_TOKEN = os.environ["SHORTIO_TOKEN"]
else:
    SHORTIO_TOKEN = config["SHORTIO_TOKEN"]

if "SENTRY_URL" not in config:
    SENTRY_URL = os.environ["SENTRY_URL"]
else:
    SENTRY_URL = config["SENTRY_URL"]

if "STATCORD_TOKEN" not in config:
    STATCORD_TOKEN = os.environ["STATCORD_TOKEN"]
else:
    STATCORD_TOKEN = config["STATCORD_TOKEN"]

# Sentry-stuff  
sentry_sdk.init(SENTRY_URL, traces_sample_rate=1.0)

# CONFIGURATION
logging.basicConfig(
    format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d; %H:%M:%S',
    level=logging.INFO
)

intents = discord.Intents.all()


test_guilds = [707243781946343425]

client = commands.Bot(command_prefix="-", intents = intents)
client.remove_command('help')
slash = SlashCommand(client, sync_commands = True)

statusmessages = ["Slash Commands", 'navnlos.ml', 'nvnls.ml/support']
statusmsg = cycle(statusmessages)

# a universal embed used in all try...except blocks
error_msgs = [
    "Something really bad happened!",
    "That shouldn't have happened",
    "So you've caused an error...",
    "That didn't go so well..."
]

async def make_error_embed(exception):
    logging.warn(f"An error occured!\nERROR: {exception}")
    embed = discord.Embed(
        title = str(random.choice(error_msgs)),
        description = f"```\n{exception}```",
        color = discord.Color.red()
    )
    embed.set_footer(text = "If you need help, join our support server! discord.gg/52TbNHPBU9")
    return embed

# END OF CONFIGURATION STUFF




@client.event
async def on_ready():
    change_status.start()
    logging.info("Bot is online.")
    owner = client.get_user(586206645592391711)
    await owner.send("Online!")

@tasks.loop(seconds=20)
async def change_status():
    newstatus = next(statusmsg)
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name= newstatus
        )
    )
    #logging.info(f"Changed activity to \"{newstatus}\"")



@client.command()
@commands.is_owner()
async def load(ctx, extension):

    try:
        client.load_extension(extension)
        await ctx.reply(f"Extension `{str(extension)}` loaded")
        logging.info(f"Extension \"{str(extension)}\" loaded.")

    except Exception as e:
        embed = await make_error_embed(e)
        await ctx.reply(embed = embed)

@client.command()
@commands.is_owner()
async def unload(ctx, extension):

    try:
        client.unload_extension(extension)
        await ctx.reply(f"Extension `{str(extension)}` unloaded")
        logging.info(f"Extension \"{str(extension)}\" unloaded.")

    except Exception as e:
        embed = await make_error_embed(e)
        await ctx.reply(embed = embed)

@client.command()
@commands.is_owner()
async def reload(ctx, extension):

    try:
        client.unload_extension(extension)
        client.load_extension(extension)
        await ctx.reply(f"Extension `{str(extension)}` reloaded")
        logging.info(f"Extension \"{str(extension)}\" reloaded.")

    except Exception as e:
        embed = await make_error_embed(e)
        await ctx.reply(embed = embed)


# load all cogs
for filename in os.listdir("./auto_publisher"):
    if filename.endswith(".py"):
        client.load_extension(f"auto_publisher.{filename[:-3]}")

for filename in os.listdir("./fun"):
    if filename.endswith(".py"):
        client.load_extension(f"fun.{filename[:-3]}")

for filename in os.listdir("./member_actions"):
    if filename.endswith(".py"):
        client.load_extension(f"member_actions.{filename[:-3]}")

for filename in os.listdir("./moderation"):
    if filename.endswith(".py"):
        client.load_extension(f"moderation.{filename[:-3]}")

for filename in os.listdir("./role_menu"):
    if filename.endswith(".py"):
        client.load_extension(f"role_menu.{filename[:-3]}")

for filename in os.listdir("./system"):
    if filename.endswith(".py"):
        client.load_extension(f"system.{filename[:-3]}")

for filename in os.listdir("./tools"):
    if filename.endswith(".py"):
        client.load_extension(f"tools.{filename[:-3]}")

for filename in os.listdir("./vc_role"):
    if filename.endswith(".py"):
        client.load_extension(f"vc_role.{filename[:-3]}")

for filename in os.listdir("./log_system"):
    if filename.endswith(".py"):
        client.load_extension(f"log_system.{filename[:-3]}")


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
