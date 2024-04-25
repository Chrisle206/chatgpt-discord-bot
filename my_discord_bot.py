import discord
import discord.ext
from discord.ext import commands
import openai
import secret

# Set up your OpenAI key
openai.api_key = secret.openai_key

print(openai.__version__)

# Declare intents for bot's usage
intents = discord.Intents.default()
intents.messages = True # Enable the messages intent
intents.message_content = True # Enable the message content intent

# Set up your Discord bot
bot = commands.Bot(command_prefix='!ask', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')

# Event: Bot recieves a message
@bot.event
async def on_message(message):

  if message.author == bot.user:
    return # Ignore messages sent by the bot itself
  
  # Send the user's message to OpenAI for a response
  try:
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt = message.content,
    temperature = 0.7,
    max_tokens=150
  )
  except Exception as e:
    print(f"An error occured: {e}")
    await message.channel.send("Sorry, I couldn't process your request at the moment.")
    return

  # Send the response back to the Discord server
  await message.channel.send(response.choices[0].text.strip())

# Run the bot with the token
bot.run(secret.discord_key)
