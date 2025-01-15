import discord
from discord.ext import commands
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Hardcoded bot token and prefix
TOKEN = "YOUR_ACTUAL_BOT_TOKEN"  # Replace with your actual bot token
PREFIX = "!"  # Replace with your desired bot prefix

if not TOKEN:
    logger.error("Bot token is missing. Please hardcode it in the script.")
    exit(1)

# Display banner
def display_banner():
    banner = """
  ____  _           _     _   _       _             
 |  _ \\| |         | |   | \\ | |     | |            
 | |_) | | __ _ ___| |_  |  \\| |_   _| | _____ _ __ 
 |  _ <| |/ _` / __| __| | . ` | | | | |/ / _ \\ '__|
 | |_) | | (_| \\__ \\ |_  | |\\  | |_| |   <  __/ |   
 |____/|_|\\__,_|___/\\__| |_| \\_|\\__,_|_|\_\\___|_|   
                                                    
    """
    logger.info(banner)

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Initialize bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    display_banner()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    else:
        logger.error(f"Unexpected error: {error}")
        await ctx.send("An error occurred.")

# Command to display the command list
@bot.command(name="commands")
async def command_list(ctx):
    command_list_text = """
    **Available Commands:**
    [1] - `ban_all` - Bans all members in the server.
    [2] - `delete_channels` - Deletes all channels.
    [3] - `delete_roles` - Deletes all roles.
    [4] - `kick_members` - Kicks members from the server.
    [5] - `prune_members` - Prune inactive members.
    [6] - `create_channels` - Creates new channels.
    [7] - `spam_channels` - Spam all channels with messages.
    [8] - `create_roles` - Creates new roles.
    [9] - `delete_roles` - Deletes specific roles.
    [10] - `rename_channels` - Renames all channels.
    [11] - `rename_guild` - Renames the server (guild).
    [12] - `rename_roles` - Renames all roles.
    [13] - `credits` - Displays credits for the bot.
    [14] - `exit` - Shuts down the bot (Owner only).
    """
    embed = discord.Embed(title="Command List", description=command_list_text, color=discord.Color.blue())
    await ctx.send(embed=embed)

# Command: Ban all members
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban_all(ctx):
    success, failures = [], []
    await ctx.send("Starting to ban all members (excluding bots and server owner).")

    for member in ctx.guild.members:
        if not member.bot and member != ctx.guild.owner:
            try:
                await member.ban(reason="Banned by bot command.")
                success.append(member.name)
            except Exception as e:
                failures.append(member.name)
                logger.error(f"Failed to ban {member.name}: {e}")

    embed = discord.Embed(
        title="Ban All Members Report",
        color=discord.Color.red(),
    )
    embed.add_field(name="Success", value="\n".join(success) if success else "None", inline=False)
    embed.add_field(name="Failures", value="\n".join(failures) if failures else "None", inline=False)
    await ctx.send(embed=embed)

# Command: Exit the bot
@bot.command()
@commands.is_owner()
async def exit(ctx):
    await ctx.send("Shutting down the bot.")
    await bot.close()

# Run the bot
bot.run(TOKEN)