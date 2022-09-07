import discord
import yaml
import P_get_lunch as pgl
from discord.ext import commands
from discord_components import *

config_loc = './config.yaml'

class setting(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command(name = '학교설정')
    @commands.has_permissions(administrator = True)
    async def school_setting(self,ctx,school_name = None):
        embed = discord.Embed(title = ":mag:", description = f"```ini\n[{school_name}] 을(를) 찾는 중입니다. 잠시 기다려 주세요...```", color=0x2E64FE)
        mes = await ctx.send(embed = embed)
        cs = pgl.check_school(school_name)
        if cs == False:
            embed = discord.Embed(title = ":warning: Error", color=0xFFFF00)
            embed.add_field(name = '에러내용', value =  f"```ini\n[{school_name}] 을(를) 찾을 수 없습니다.\n 학교이름을 다시 한번 확인한 뒤 입력해주세요.\n\n 해당문제가 지속된다면 아래 서버에서 문의하세요.\nhttps://discord.gg/fXKuPJp8mT```")
            await mes.edit(embed = embed)
        else:
            with open(config_loc, encoding='utf-8') as f:
                yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            yaml_data[ctx.guild.id]['school_name'] =f"{school_name}"
            with open(config_loc, 'w', encoding = 'utf-8') as outfile:
                yaml.dump(yaml_data, outfile, indent = 4, allow_unicode = True)

            embed = discord.Embed(title = ":white_check_mark:학교설정", description = f"```ini\n이 서버의 학교 기본값이 [{school_name}] 으로 설정되었습니다.```", color=0xCFC00)
            await mes.edit(embed = embed)
    @school_setting.error
    async def school_setting_error(self,ctx,error):
        if isinstance(error, MissingPermissions):
            embed=discord.Embed(title=":warning:", description = f'당신은 이 명령어를 사용할 권한이 없습니다!', color=0xFFFF00)
            await ctx.send(embed = embed)

    @commands.command(name = '채널설정')
    @commands.has_permissions(administrator = True)
    async def channel_setting(self, ctx):
        s_options = []
        for i in ctx.guild.text_channels:
            s_options.append(SelectOption(
                label=f"{i}",
                value=f"{i.id}",
                description=f"클릭시 급식 알림 채널을 {i} (으)로 설정합니다.",
                emoji="\U0001F4E3"
            ))
        #임베드
        embed=discord.Embed(title=f":mega:**급식 알림 채널 설정**",color=0x9370DB)
        embed.add_field(name=f"**채널 선택**",value=f"```아래의 선택창에서 원하는 채널을 선택하세요.```", inline=False)
        mes = await ctx.send(embed = embed,components=[
        Select(placeholder=f"원하는 채널을 선택하세요.",
            options=s_options)])

        def check(m):
            return m.channel.id == ctx.channel.id, m.author.id == ctx.author.id

        try:
            m_select = await self.client.wait_for("select_option",check = check)
        except:
            pass
        with open(config_loc, encoding='utf-8') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        yaml_data[ctx.guild.id]['auto_send_channel'] = int(m_select.values[0])
        with open(config_loc, 'w', encoding = 'utf-8') as outfile:
            yaml.dump(yaml_data, outfile, indent = 4, allow_unicode = True)

        embed=discord.Embed(title=f":mega:**급식 알림 채널 설정**", description = f'```ini\n급식 알림 채널이 [{self.client.get_channel(int(m_select.values[0])).name}] (으)로 설정되었습니다.```',color=0x9370DB)
        await mes.edit(embed = embed,components = [])

    @channel_setting.error
    async def channel_setting_error(self,ctx,error):
        if isinstance(error, MissingPermissions):
            embed=discord.Embed(title=":warning:", description = f'당신은 이 명령어를 사용할 권한이 없습니다!', color=0xFFFF00)
            await ctx.send(embed = embed)

#m_select.values[0]
def setup(client):
    client.add_cog(setting(client))
