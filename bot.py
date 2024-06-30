import discord
import requests

# Function to fetch a random meme URL from an API
def get_meme():
    response = requests.get('https://meme-api.com/gimme')
    json_data = response.json()
    return json_data['url']

# Function to fetch a joke from an API, optionally specifying a joke type
def get_joke(joke_type='Any'):
    response = requests.get(f'https://v2.jokeapi.dev/joke/{joke_type}')
    joke_data = response.json()
    if joke_data['type'] == 'single':
        return joke_data['joke']
    else:
        return f"{joke_data['setup']} - {joke_data['delivery']}"

# Discord client class
class MyClient(discord.Client):
    # Event: Called when the bot is ready and connected
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    # Event: Called when a message is received
    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        if message.content.startswith('$meme'):
            await message.channel.send(get_meme())
        
        if message.content.startswith('$joke'):
            parts = message.content.split()
            joke_type = parts[1] if len(parts) > 1 else 'Any' 
            await message.channel.send(get_joke(joke_type))
        
        if message.content.startswith('$help'):
            help_message = (
                "**Commands:**\n"
                "$meme - Get a random meme from the internet.\n"
                "$joke [type] - Get a joke. You can specify a type (e.g., Programming, Misc, Dark, Pun) or leave it blank for a random joke.\n"
            )
            await message.channel.send(help_message)

# Set up Discord client with intents to receive message events
intents = discord.Intents.default()
intents.message_content = True

# Initialize and run the client with the bot token
client = MyClient(intents=intents)
client.run('YOUR_BOT_TOKEN_HERE')
