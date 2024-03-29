import discord
from discord.ext import commands
import os
import sys
import time
import dotenv
from helper import create_embed, is_guild_owner, format_time, wait_for_reaction
from constants import CHECK_EMOJI

dotenv.load_dotenv('.env')
CLIENT_ID = os.getenv('CLIENT_ID')

class bot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.uptime = time.time()

    @commands.command()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def run(self, context, *, code):
        response = await context.send(embed=create_embed({
            'title': 'Running code...',
            'color': discord.Color.gold(),
        }, {
            'Code': code,
        }))

        try:
            exec(code)
            await response.edit(embed=create_embed({
                'title': 'Ran code',
                'color': discord.Color.green(),
            }, {
                'Code': code,
            }))
        except Exception as error_message:
            await response.edit(embed=create_embed({
                'title': 'Could not run code',
                'color': discord.Color.red(),
            }, {
                'Error Message': error_message,
                'Code': code,
            }))

            print(f'ERROR: Could not run code {code}')
            print(error_message)

    @commands.command()
    @commands.check_any(commands.is_owner())
    async def cls(self, context):
        response = await context.send(embed=create_embed({
            'title': 'Clearing terminal',
            'color': discord.Color.gold(),
        }))

        try:
            os.system('cls')
            await response.edit(embed=create_embed({
                'title': 'Terminal cleared',
                'color': discord.Color.green(),
            }))
        except Exception as error_message:
            await response.edit(embed=create_embed({
                'title': 'Could not clear terminal',
                'color': discord.Color.red(),
            }, {
                'Error Message': error_message,
            }))

            print(f'Could not clear terminal')
            print(error_message)
    
    @commands.command()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def restart(self, context):
        response = await context.send(embed=create_embed({
            'title': f'Are you sure you want to restart the bot?',
            'color': discord.Color.gold()
        }))
        
        await response.add_reaction(CHECK_EMOJI)
        reaction, user = await wait_for_reaction(self.client, context, CHECK_EMOJI, 30)
        if reaction:
            await response.edit(embed=create_embed({
                'title': 'Restarting bot...',
                'color': discord.Color.green()
            }))

            sys.exit()
        else:
            await response.edit(embed=create_embed({
                'title': f'You did not respond in time',
                'color': discord.Color.red()
            }))
            
    @commands.command()
    async def info(self, context):
        response = await context.send(embed=create_embed({
            'title': 'Loading bot info...',
            'color': discord.Color.gold()
        }))

        try:
            uptime = round(time.time() - self.uptime)
            uptime_text = format_time(uptime)
            ping = round(self.client.latency * 1000)
            invite_url = discord.utils.oauth_url(client_id=CLIENT_ID, permissions=discord.Permissions(8))

            connected_servers = 0
            members_watching = 0
            user_ids = []

            for guild in self.client.guilds:
                connected_servers += 1
                for member in guild.members:
                    members_watching += 1
                    if not member.id in user_ids:
                        user_ids.append(member.id)

            users_watching = len(user_ids)
            await response.edit(embed=create_embed({
                'title': 'Invite',
                'url': invite_url,
                'inline': True,
            }, {
                'Ping': f'{ping} ms',
                'Uptime': uptime_text,
                'Connected Servers': connected_servers,
                'Users Watching': members_watching,
                'Unique Users Watching': users_watching
            }))
        except Exception as error_message:
            await response.edit(embed=create_embed({
                'title': 'Could not load bot info',
                'color': discord.Color.red()
            }, {
                'Error Message': error_message
            }))

            print(f'Cannot load bot info')
            print(error_message)

def setup(client):
    client.add_cog(bot(client))