import discord
import yaml
from discord.ext import commands

yaml_loc = 'C:/python/Discord_Bot/school_lunch_bot/help.yaml'

class help(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command(name = '도움말',aliases=['help', '도움'])
    async def help(self,ctx):
        with open(yaml_loc, encoding='utf-8') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        embed=discord.Embed(title="**help**",description=f"학교 급식 알림 봇의 도움말입니다.",color=0xE0FFFF)
        for i in yaml_data['commands_help']:
            embed.add_field(name = f"{yaml_data['commands_help'][i]['COMMAND']}", value = f"```ini\n[필요권한]: {yaml_data['commands_help'][i]['PERMISSION']}\n[설명]: {yaml_data['commands_help'][i]['DESCRIPTION']}```",inline = False)
        embed.add_field(name = f"더 많은 도움", value = f'[여기](https://discord.gg/fXKuPJp8mT) 에서 물어보세요.\n\n 이 봇은 {self.client.get_user(339017884703653888).mention}에 의해 제작되었습니다.')
        mes = await ctx.send(embed = embed)


def setup(client):
    client.add_cog(help(client))
