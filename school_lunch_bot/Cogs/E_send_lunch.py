import discord
import yaml
import time as t
import P_get_lunch as pgl
import datetime
from datetime import datetime
from discord.ext import tasks,commands
from discord_components import *

config_loc = './config.yaml'

class send_lunch(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.auto_send_lunch.start()

    @commands.command(name = '급식')
    async def send_lunch(self,ctx,school_name = None):
        lunch_find = False
        if school_name == None:
            with open(config_loc, encoding='utf-8') as f:
                yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            if ctx.guild.id not in yaml_data:
                embed = discord.Embed(title = ":warning: Error", color=0xFFFF00)
                embed.add_field(name = '에러내용', value =  f'```--급식 명령어를 사용하기 전에 "-학교설정" 명령어를 사용해 학교를 등록하세요.```')
                await ctx.send(embed = embed)
            else:
                school_name = yaml_data[ctx.guild.id]['school_name']
        embed=discord.Embed(title=":arrows_counterclockwise: **loading...**",description=f"```{school_name}의 급식 데이터를 가져오는중...```",color=0x9370DB)
        embed.set_footer(text = "made by Lanturn#9899")
        mes = await ctx.send(embed = embed)
        lunch = pgl.lunch().get_lunch(school_name)
        lunch_date = str(datetime.today().month) + '.' + str(datetime.today().day) + '.'
        if lunch.error == None:
            for i in range(0,len(lunch.menu),2):
                if lunch_date in lunch.menu[i]:
                    embed=discord.Embed(title=f":fork_and_knife:**{school_name} {lunch.menu[i]}**",color=0x9370DB)
                    embed.add_field(name=f"**메뉴**",value=f"**```{lunch.menu[i+1]}```**", inline=False)
                    await mes.edit(embed = embed)
                    lunch_find = True
            if lunch_find == False:
                embed=discord.Embed(title=f":warning: Error!",description = f'```{school_name}의 {lunch_date} 급식을 찾을 수 없습니다.```',color=0xFFFF00)
                await mes.edit(embed = embed)
        else:
            embed=discord.Embed(title=f":warning: Error!",description = f'```{lunch.error}```',color=0xFFFF00)
            await mes.edit(embed = embed)


    @commands.command(name = '-급식')
    async def send_lunch_date(self,ctx,school_name = None,):
        if school_name == None:
            with open(config_loc, encoding='utf-8') as f:
                yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            if ctx.guild.id not in yaml_data:
                embed = discord.Embed(title = ":warning: Error", color=0xFFFF00)
                embed.add_field(name = '에러내용', value =  f'```--급식 명령어를 사용하기 전에 "-학교설정" 명령어를 사용해 학교를 등록하세요.```')
                await ctx.send(embed = embed)
            else:
                school_name = yaml_data[ctx.guild.id]['school_name']
        embed=discord.Embed(title=":arrows_counterclockwise: **loading...**",description=f"```{school_name}의 급식 데이터를 가져오는중...```",color=0x9370DB)
        mes = await ctx.send(embed = embed)
        lunch = pgl.lunch().get_lunch(school_name)

        lunch_date = str(datetime.today().month) + '.' + str(datetime.today().day) + '.'
        if lunch.error == None:
            #메세지에 select 컴포넌트 추가
            s_options = []
            for i in range(0,int(len(lunch.menu)),2):
                s_options.append(SelectOption(
                    label=f"{lunch.menu[i]}",
                    value=f"{lunch.menu[i]}",
                    description=f"클릭시 {lunch.menu[i]} 메뉴를 보여줍니다.",
                    emoji="\U0001F4C5"
                ))
            #임베드
            embed=discord.Embed(title=f":fork_and_knife:**{school_name} 급식**",color=0x9370DB)
            embed.add_field(name=f"**날짜선택**",value=f"아래의 선택창에서 원하는 날짜를 선택하세요.", inline=False)
            await mes.edit(embed = embed,components=[
            Select(placeholder=f"원하는 날짜를 선택하세요.",
                options=s_options)])
            def check(m):
                return m.channel.id == ctx.channel.id, m.author.id == ctx.author.id

            m_select = await self.client.wait_for("select_option",check = check)
            for i in range(0,len(lunch.menu),2):
                if m_select.values[0] == lunch.menu[i]:
                    embed=discord.Embed(title=f":fork_and_knife:**{school_name} {lunch.menu[i]}**",color=0x9370DB)
                    embed.add_field(name=f"**메뉴**",value=f"**```{lunch.menu[i+1]}```**", inline=False)
                    await mes.edit(embed = embed,components = [])
                    return None
        else:
            embed = discord.Embed(title = ":warning: Error", color=0xFFFF00)
            embed.add_field(name = '에러내용', value =  f'```{lunch.error}```')
            await mes.edit(embed = embed)


    @tasks.loop(seconds = 60)
    async def auto_send_lunch(self):
        if t.strftime('%a', t.localtime(t.time())) == 'Sun' or t.strftime('%a', t.localtime(t.time())) == 'Sat':
            pass
        else:
            now = t.strftime('%H:%M', t.localtime(t.time()))
            now = now.split(':')
            if int(now[0]) == 8:
                if int(now[1]) == 00:
                    with open(config_loc, encoding='utf-8') as f:
                        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
                    lunch_find = False
                    for i in yaml_data:
                        for j in self.client.guilds:
                            if i == j.id:
                                channel = self.client.get_channel(yaml_data[i]['auto_send_channel'])
                                if channel == None or yaml_data[i]['school_name'] == '':
                                    break
                                lunch = pgl.lunch().get_lunch(yaml_data[i]["school_name"])
                                lunch_date = str(datetime.today().month) + '.' + str(datetime.today().day) + '.'
                                if lunch.error == None:
                                    for j in range(0,len(lunch.menu),2):
                                        if lunch_date in lunch.menu[j]:
                                            embed=discord.Embed(title=f":fork_and_knife:**{yaml_data[i]['school_name']} {lunch.menu[j]}**",color=0x9370DB)
                                            embed.add_field(name=f"**메뉴**",value=f"```{lunch.menu[j+1]}```", inline=False)
                                            await ctx.send(embed = embed)
                                            print(f"send lunch to {yaml_data[i]['school_name']}...OK")
                                            lunch_find = True
                                    if lunch_find == False:
                                        pass
                                else:
                                    embed=discord.Embed(title=f":warning: Error!",description = f'```{lunch.error}```',color=0xFFFF00)
                                    await mes.edit(embed = embed)
                else:
                    pass

    @auto_send_lunch.before_loop
    async def before_auto_send_lunch(self):
        print('waiting for bot on...')
        await self.client.wait_until_ready()



    @auto_send_lunch.after_loop
    async def after_auto_send_lunch(self):
        print(f'auto_send_lunch...OK')



def setup(client):
    client.add_cog(send_lunch(client))
