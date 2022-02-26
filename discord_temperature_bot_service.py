import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re

intents = discord.Intents.default()
intents.members=True
client = discord.Client()

# temperature converting function
def convert_temp(number, scale):
  # make sure the number is not a string
  number = float(number)
  # if the temperature is in F
  if scale.lower() == "f":
    converted_temp_number = (number - 32) * 5/9
    converted_temp_scale = "c"
  # if the temperature is in C
  elif scale.lower() == "c":
    converted_temp_number = (number * 9/5) + 32
    converted_temp_scale = "f"
  # if it isn't c or f, return none
  else:
    return None
  # after calculation, return tuple of temp num and scale
  return (converted_temp_number, converted_temp_scale)
  



# PROOF OF RUNNING SCRIPT
@client.event
# Print when the program is ready for input
async def on_ready():
  print("We have logged in as {0.user}".format(client))

# Temperature regex
temp_pattern = re.compile(r"\s(-?\d{1,}?(\.\d{1,}?)?)[\s°]?([C,c,F,f])[^\w\d]")

# Watch each message that is sent in the server
@client.event
async def on_message(message):
  # if the author of the message is a bot, do not respond
  if message.author.bot:
        return

  # response list started
  response = []
  #check if message has temperature pattern in it, add a space to help the regex incase it ends with a temp 
  temp_matches = re.findall(temp_pattern, " " + message.content + " ")
  # if there are temperature pattern matches
  if temp_matches != []:
    # convert the temperatures
    # send the temperature number (m[0]) and the temperature scale (m[1]) into the temperature converter for each match (m) in temp_matches
    temp_matches_converted = [convert_temp(m[0], m[2]) for m in temp_matches]
  
    # construct temperature portion of the response
    temp_response = ["I found " + ("temperatures" if len(temp_matches) > 1 else "a temperature") + " in that message!"]
    for i in range(len(temp_matches)):
      # AA°B = CC°D
      x = f"{float(temp_matches[i][0]): .1f}°{temp_matches[i][2].upper()}"
      y = f"{temp_matches_converted[i][0]: .1f}°{temp_matches_converted[i][1].upper()}"
      temp_response.append(f"{x: >10} = {y: <10}")
    #join the occurences of temp with new line and append to response
    response.append("\n".join(temp_response))

  # Send response message if there is information in the response
  if response != []:
    await message.channel.send("\n".join(response))
    



load_dotenv()
client.run(os.environ['DISCORD_TOKEN'])
