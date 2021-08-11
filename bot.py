import uuid
import os
import discord
from storage import *
from bot_util import *
from datetime import datetime

now = datetime.now()
client = discord.Client()

@client.event
async def on_ready():
    print('\nWe are logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!qr"))

@client.event
# Listen for an incomming message
async def on_message(message):
    # If the author is the robot itself, then do nothing!
    if message.author == client.user:
        return
    if message.content == "!qr":
        current_time = now.strftime("%H:%M:%S")
        print('\n')
        # This for loop check for all the user's DiscordID in the Database
        if str(message.author.id) in scholar_dict:
            # value with discordID
            scholar = scholar_dict[str(message.author.id)]
            # discordID's privateKey from the database
            account_private_key = scholar[2]
            # discordID's EthWalletAddress from the database
            account_address = scholar[1]
            # Get a message from AxieInfinty
            raw_message = get_raw_message()
            # Sign that message with accountPrivateKey
            signed_message = get_sign_message(raw_message, account_private_key)
            # Get an accessToken by submitting the signature to AxieInfinty
            access_token = submit_signature(signed_message, raw_message, account_address)
            #try sending message to reqested user
            try:
                qr_code_path = f"QRCode_{message.author.id}_{str(uuid.uuid4())[0:8]}.png"
                qrcode.make(access_token).save(qr_code_path)
                message_embed = discord.Embed(title="QR Code for " + message.author.name, description="**Note: ** Dont share with anyone")
                message_embed.set_image(url="attachment://" + qr_code_path)
                message_embed.set_footer(text="Powered by Alpha Bots")
                await message.author.send(file=discord.File(qr_code_path), embed=message_embed)
                os.remove(qr_code_path)
            except:
                await message.reply("Seems you have turned off private messages. Please activate them in the discord privacy settings!")
            return
        else:
            await message.reply("Seems you are not a team-member yet. Please contact the Discord Owners or ask in `scholarship` channel for help. ")
            return

#Run the client (This runs first)
client.run(discord_bot_token)
