#####################################################################################
#                                                                                   #
#    Copyright (C) 2025 lattiahirvio                                                #
#                                                                                   #
#    This file is part of evalbot.                                                  #
#                                                                                   #
#    evalbot is free software: you can redistribute it and/or modify                #
#    it under the terms of the GNU Affero General Public License as published by    #
#    the Free Software Foundation, either version 3 of the License, or              #
#    any later version.                                                             #
#                                                                                   #
#    Evalbot is distributed in the hope that it will be useful,                     #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of                 #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                  #
#    GNU Affero General Public License for more details.                            #
#                                                                                   #
#    You should have received a copy of the GNU Affero General Public License       #
#    along with evalbot.  If not, see <https://www.gnu.org/licenses/>.              #
#                                                                                   #
#####################################################################################

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
output = lisp.OutputBuffer()
env = lisp.std_env(output)

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

    # We remove leading and trailing whitespace
    content = message.content.strip()

    # We Don't evaluate stuff we dont care about
    if not content.startswith(bot.command_prefix):
        return

    # Args is everything except the command prefix
    args = content[len(bot.command_prefix):].split()
    if not args:
        return

    command_name = args[0].lower()
    global output
    global env

    # Eval itself, the star of the show.
    if command_name == "eval":
        try:
            code = " ".join(args[1:])

            result = lisp.eval(lisp.parse(code), env)

            printed = output.get_output()
            response = ""

            if printed:
                response += printed + "\n"
            if result is not None:
                response += str(result)

            output.write(result)

            # Cap the output length to 1900.
            # Discord allows for 2000 characters but whatever, 
            # 1900 is more than enough
            printed = output.get_output()
            output.clear()
            
            if len(printed) > 1900:
                printed = printed[:1900] + "..."

            await message.channel.send(f"```lisp\n{printed}\n```")

        except Exception as e:
            await message.channel.send(f"Error: `{e}`")

    else:
        await message.channel.send(f"Unknown command: `{command_name}`")

    await bot.process_commands(message)

# Run the main function. We run it async because it needs to be ran asynnc or something...
if __name__ == "__main__":
    asyncio.run(main())
