from dotenv import load_dotenv
import asyncio
import os
import discord
import lisp
from discord.ext import commands

# Define bot stuff
# Intents are important here
intents = discord.Intents.default();
intents.message_content = True;
bot = commands.Bot(command_prefix=";", intents=intents, status="DM me to open a ticket!");

# Load credentials.
load_dotenv()
token = os.getenv("TOKEN")

# Generate global env. This persists for the entire runtime of the program.
env = lisp.std_env(lisp.OutputBuffer())

# Main function. Very async.
async def main():
    await bot.start(token);

# onready method. Runs when the bot is fully initialized.
@bot.event
async def on_ready():
    print("Bot logged in!");
    await bot.change_presence(activity=discord.CustomActivity(name='Evaluating code...'))

# onmessage method. 
# Runs every time a message is sent.
# Serves as our command handler.
@bot.event
async def on_message(message):
    if message.author.bot: # We dont want to evaluate stuff sent by bots
        return

    # We Don't evaluate stuff we dont care about
    if not content.startswith(bot.command_prefix):
        return

    # We remove leading and trailing whitespace
    content = message.content.strip()

    # Args is everything except the command prefix
    args = content[command_prefix.len:].split()
    if not args:
        return

    command_name = args[0].lower()

    # Eval itself, the star of the show.
    if command_name == "eval":
        try:
            code = "".join(args[1:])
            # output = lisp.OutputBuffer()

            result = lisp.eval(lisp.parse(code), env)

            printed = output.get_output()
            response = ""

            if printed:
                response += printed + "\n"
            if result is not None:
                response += str(result)

            output = str(result)

            # Cap the output length to 1900.
            # Discord allows for 2000 characters but whatever, 
            # 1900 is more than enough
            if len(output) > 1900:
                output = output[:1900] + "..."

            await message.channel.send(f"```lisp\n{output}\n```")

        except Exception as e:
            await message.channel.send(f"Error: `{e}`")

    else:
        await message.channel.send(f"Unknown command: `{command_name}`")

    await bot.process_commands(message)

# Run the main function. We run it async because it needs to be ran asynnc or something...
if __name__ == "__main__":
    asyncio.run(main())
