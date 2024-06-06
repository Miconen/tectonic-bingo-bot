from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

cogs = (
    "bot.commands.tiles",
    "bot.commands.debug",
    "bot.commands.tile",
    "bot.commands.submit",
    "bot.commands.teams",
    "bot.commands.board",
    "bot.commands.help",
    "bot.commands.submissions",
)


@bot.event
async def setup_hook() -> None:
    for cog in cogs:
        await bot.load_extension(cog)
    await bot.tree.sync()


@bot.event
async def on_ready():
    """Called when the bot is ready."""
    print("Logged on as", bot.user)
