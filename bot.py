import discord
import responses

async def send_message(message, user_message, is_private):
    try:
        #Get response from responses.py, then check if should be a private message or not
        response = responses.handle_response(user_message)

        print(response)
        print(type(response))
        
        if isinstance(response, discord.File):
            await message.author.send(file=response) if is_private else await message.channel.send(file=response)
        elif isinstance(response, discord.Embed):
            embed = discord.Embed()
            embed.description = response
            await message.author.send(embed=embed) if is_private else await message.channel.send(embed=embed)
        elif isinstance(response, str):
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTE4MzEyNTg1NTQwOTU0NTMxNg.G40f0S.kZjgd-aUBvILZA7tQeB1NinzLTYP99JH2MCz8c'
    intents = discord.Intents.default()
    # intents.members = True
    # intents.presences = True
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is running!')

    @client.event
    async def on_message(message):
        #Error check message
        if not message:
            return

        #Make sure message doesn't come from bot
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said '{user_message}' in ({channel})")

        #Checks for private message
        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, True)
        else:
            await send_message(message, user_message, False)

    client.run(TOKEN)