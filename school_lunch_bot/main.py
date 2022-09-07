import discord
import os
import time as t
import yaml
from discord.ext import commands
from discord_components import *


#============  초기변수 설정  =================
version = "1.3.2"
bot_manager = [339017884703653888,797179819690950686]
config_loc = './config.yaml'

#============  intents  ================
intents = discord.Intents.all()
intents.members = True
intents.guilds = True


#============  봇 트리거  ================
bot = commands.Bot(command_prefix='-', intents=intents, help_command = None)

def status():
    print('\n\n\n')
    print("====================================")
    print(f'Running on {len(bot.guilds)} servers...')
    print(f"Bot version: {version}")
    print(f'Bot Manager ID: {bot_manager}')
    print(f"starting time: {t.strftime('%Y-%m-%d %H:%M', t.localtime(t.time()))}")
    print('bot prefix: -')
    print('bot made by Lanturn#9899')
    print("====================================\n")
    DiscordComponents(bot)

#============  봇이 실행됬을때  ===========
@bot.event
async def on_ready():
    print(f'{bot.user} Login!')
    await bot.change_presence(status = discord.Status.online, activity = discord.Game('-도움말'))
    status()
'''
@bot.event
async def on_command_error(ctx,error):
    embed = discord.Embed(title = ":warning: Error", color=0xFFFF00)
    embed.add_field(name = '에러내용', value =  f"```{error}```")
    await ctx.send(embed = embed)
'''
@bot.event
async def on_guild_join(guild):
    status()
    print(f'bot join {guild.name}   id: {guild.id}')
    with open(config_loc, encoding='utf-8') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
    yaml_data[guild.id] = {'school_name': '','auto_send_channel': 0,'server_name': guild.name}
    with open(config_loc, 'w', encoding = 'utf-8') as outfile:
        yaml.dump(yaml_data, outfile, allow_unicode = True)

@bot.event
async def on_guild_remove(guild):
    status()
    print(f'bot remove {guild.name}   id: {guild.id}')
    with open(config_loc, encoding='utf-8') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
    del yaml_data[guild.id]
    with open(config_loc, 'w', encoding = 'utf-8') as outfile:
        yaml.dump(yaml_data, outfile, allow_unicode = True)
#=============  cogs  ===================
@bot.command()
async def load(ctx, extension = None):
    if ctx.author.id in bot_manager:
        if extension == None:
            embed=discord.Embed(title="Cogs", color=0x90EE90)
            embed.add_field(name=f"**에러**", value=f"load 할 파일의 이름을 입력해주세요.", inline=False)
            await ctx.send(embed = embed)
        else:
            try:
                bot.load_extension(f'Cogs.{extension}')
                embed=discord.Embed(title="Cogs", color=0x90EE90)
                embed.add_field(name=f"**load**", value=f"{extension}이(가) load 되었습니다.", inline=False)
                await ctx.send(embed = embed)
            except Exception as e:
                embed=discord.Embed(title=":warning:Error", color=0xFFFF00)
                embed.add_field(name=f"**에러내용**", value=f"```{e}```", inline=False)
                await ctx.send(embed = embed)
@bot.command()
async def unload(ctx, extension = None):
    if ctx.author.id in bot_manager:
        if extension == None:
            embed=discord.Embed(title="Cogs", color=0x90EE90)
            embed.add_field(name=f"**에러**", value=f"unload 할 파일의 이름을 입력해주세요.", inline=False)
            await ctx.send(embed = embed)
        else:
            try:
                bot.unload_extension(f'Cogs.{extension}')
                embed=discord.Embed(title="Cogs", color=0x90EE90)
                embed.add_field(name=f"**unload**", value=f"{extension}이(가) unload 되었습니다.", inline=False)
                await ctx.send(embed = embed)
            except Exception as e:
                embed=discord.Embed(title=":warning:Error", color=0xFFFF00)
                embed.add_field(name=f"**에러내용**", value=f"```{e}```", inline=False)
                await ctx.send(embed = embed)
@bot.command()
async def reload(ctx, extension = None):
    if ctx.author.id in bot_manager:
        if extension == None:
            embed=discord.Embed(title="Cogs", color=0x90EE90)
            embed.add_field(name=f"**에러**", value=f"reload 할 파일의 이름을 입력해주세요.", inline=False)
            await ctx.send(embed = embed)
        else:
            try:
                bot.unload_extension(f'Cogs.{extension}')
                bot.load_extension(f'Cogs.{extension}')
                embed=discord.Embed(title="Cogs", color=0x90EE90)
                embed.add_field(name=f"**reload**", value=f"{extension}이(가) reload 되었습니다.", inline=False)
                await ctx.send(embed = embed)
            except Exception as e:
                embed=discord.Embed(title=":warning:Error", color=0xFFFF00)
                embed.add_field(name=f"**에러내용**", value=f"```{e}```", inline=False)
                await ctx.send(embed = embed)

#=================  봇이 처음 켜질때 모든 Cogs 로드  =====================
a = 0
for filename in os.listdir('./Cogs'):
    if filename.startswith('E_'):
        if filename.endswith('.py'):
            print(f'Cog {filename[:-3]}이(가) Load 되었습니다.')
            a+=1
            bot.load_extension(f'Cogs.{filename[:-3]}')
print(f'총 {a}개의 Cog가 로드되었습니다.')



bot.run('YOUR_BOT_ROKEN')
