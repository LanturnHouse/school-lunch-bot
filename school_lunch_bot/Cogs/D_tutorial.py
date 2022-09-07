import discord
import P_get_lunch as pgl
from discord.ext import commands
from discord.utils import get
from discord_components import *



json_loc = 'C:/python/Discord_Bot/school_lunch_bot/data.json'

class tutorial(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command(name = '튜토리얼')
    async def tutorial(self,ctx,school_name = None):
        embed=discord.Embed(title="**안녕하세요!**",description = '```이 봇은 학생들을 위한 학교 급식 알림 봇입니다.```' ,color=0x7FFFD4)
        embed.add_field(name=f"**튜토리얼**",value=f"```이 봇을 처음 사용하는 분들을 위해 튜토리얼을 준비했습니다.\n봇을 사용하는데 필요한 기본정보, 커맨드, 사용방법 등을 알려줍니다.```", inline=False)
        embed.add_field(name=f"**건너뛰기**",value=f"```튜토리얼을 진행하지 않습니다.\n언제든지 '-튜토리얼' 커맨드를\n입력하여 튜토리얼을 진행할 수 있습니다.```", inline=True)
        embed.add_field(name=f"**진행**",value=f"```튜토리얼을 진행합니다.\n봇을 사용하는데 필요한\n기본정보, 커맨드, 사용방법 등\n에대하여 알려줍니다.```", inline=True)
        embed.set_footer(text = "made by Lanturn#9899")
        message_1 = await ctx.send(embed = embed,
        components=[
            [Button(style = ButtonStyle.green, label="건너뛰기"),
            Button(style = ButtonStyle.blue, label="진행")]
            ])

        def check(m):
            return m.channel.id == ctx.channel.id, m.author.id == ctx.author.id

        bt_click_1 = await self.client.wait_for("button_click",check = check)
        if bt_click_1.component.label == '건너뛰기':
            embed=discord.Embed(title=f"**튜토리얼 스킵!**",description = f"```튜토리얼을 스킵하셨습니다.\n언제든지 '-튜토리얼' 명령어를 사용하여 튜토리얼을 진행할 수 있습니다.```\n\n\n 봇을 초대해주셔서 감사합니다. 봇에 관련한 질문은 아래 디스코드 서버에서 해주세요." ,color=0x7FFFD4)
            embed.set_footer(text = "made by Lanturn#9899")
            await message_1.edit(embed = embed,components = [Button(style = ButtonStyle.URL, label="디스코드",url = 'https://discord.gg/4nxyKU6r3Y')])

        elif bt_click_1.component.label == "진행":
            embed=discord.Embed(title="**튜토리얼**",description = '**step.1**' ,color=0x7FFFD4)
            embed.add_field(name=f"**서버 학교 설정**",value=f"""**```우선, 이 서버에서 사용할 학교를 정하여야 합니다.\n학교가 등록이 될 경우 매일 아침 8시에 등록된 학교의 급식 식단을 지정된 채널에 보내줍니다.```**""", inline=False)
            embed.add_field(name=f"**등록**",value=f"```채팅창에 학교 이름을 입력해주세요.```", inline=True)
            embed.set_footer(text = "made by Lanturn#9899")
            await message_1.edit(embed = embed,components = [])

            while True:
                mes_wait_1 = await self.client.wait_for("message",check = check)

                embed = discord.Embed(title="**튜토리얼**",description = '**step.1**' ,color=0x7FFFD4)
                embed.add_field(name=f"**서버 학교 설정**",value=f"""**```우선, 이 서버에서 사용할 학교를 정하여야 합니다.\n학교가 등록이 될 경우 매일 아침 8시에 등록된 학교의 급식 식단을 지정된 채널에 보내줍니다.```**""", inline=False)
                embed.add_field(name=f"**등록**",value=f"```{mes_wait_1.content}을(를) 찾는중...```", inline=True)
                embed.set_footer(text = "made by Lanturn#9899")
                await message_1.edit(embed = embed)

                cs = pgl.check_school(mes_wait_1.content)

                if cs != False:
                    embed = discord.Embed(title="**튜토리얼**",description = '**step.1**' ,color=0x7FFFD4)
                    embed.add_field(name=f"**서버 학교 설정**",value=f"""**```우선, 이 서버에서 사용할 학교를 정하여야 합니다.\n학교가 등록이 될 경우 매일 아침 8시에 등록된 학교의 급식 식단을 지정된 채널에 보내줍니다.```**""", inline=False)
                    embed.add_field(name=f"**등록**",value=f"```{mes_wait_1.content}을(를) 찾았습니다!\n\n해당학교가 맞다면 다음 튜토리얼로 넘어가주세요.```", inline=True)
                    embed.set_footer(text = "made by Lanturn#9899")
                    await message_1.edit(embed = embed,
                    components=[
                    [Button(style = ButtonStyle.green, label="다시입력"),
                    Button(style = ButtonStyle.blue, label="다음")]])
                else:
                    embed = discord.Embed(title="**튜토리얼**",description = '**step.1**' ,color=0x7FFFD4)
                    embed.add_field(name=f"**서버 학교 설정**",value=f"""**```우선, 이 서버에서 사용할 학교를 정하여야 합니다.\n학교가 등록이 될 경우 매일 아침 8시에 등록된 학교의 급식 식단을 지정된 채널에 보내줍니다.```**""", inline=False)
                    embed.add_field(name=f"**등록**",value=f"```{mes_wait_1.content}을(를) 찾지 못했습니다.\n학교이름을 확인한 뒤 다시 입력해주세요.```", inline=True)
                    embed.set_footer(text = "made by Lanturn#9899")
                    await message_1.edit(embed = embed)
                    continue

                bt_click_2 = await self.client.wait_for("button_click",check = check)
                if bt_click_2.component.label == '다음':
                    break
                elif bt_click_2.component.label == '다시입력':
                    embed=discord.Embed(title="**튜토리얼**",description = '**step.1**' ,color=0x7FFFD4)
                    embed.add_field(name=f"**서버 학교 설정**",value=f"""**```우선, 이 서버에서 사용할 학교를 정하여야 합니다.\n학교가 등록이 될 경우 매일 아침 8시에 등록된 학교의 급식 식단을 지정된 채널에 보내줍니다.```**""", inline=False)
                    embed.add_field(name=f"**등록**",value=f"```채팅창에 학교 이름을 입력해주세요.```", inline=True)
                    embed.set_footer(text = "made by Lanturn#9899")
                    await message_1.edit(embed = embed,components = [])
                    continue


            while True:

                s_options = []
                for channel in ctx.guild.text_channels:
                    s_options.append(SelectOption(
                        label=f"{channel.name}",
                        value=f"{channel.name}",
                        description=f"클릭시 {channel.name} 채널로 채널을 설정합니다.",
                        emoji="\U0001F4AC"
                    ))

                embed = discord.Embed(title="**튜토리얼**",description = '**step.2**' ,color=0x7FFFD4)
                embed.add_field(name=f"**채널 설정**",value=f"""**```매일 아침 8시에 학교 급식을 보낼 채널을 선택하여 주세요.\n\n튜토리얼 진행중 채널을 새로 만들었다면 아무채널이나 선택한 뒤 '다시선택' 버튼을 누르면 새로 만든 채널도 선택이 가능해집니다.```**""", inline=False)
                embed.set_footer(text = "made by Lanturn#9899")
                await message_1.edit(embed = embed,components=[
                Select(placeholder=f"원하는 채널을 선택하세요.",
                    options=s_options)])

                select_1 = await self.client.wait_for("select_option",check = check)

                embed = discord.Embed(title="**튜토리얼**",description = '**step.2**' ,color=0x7FFFD4)
                embed.add_field(name=f"**채널 설정**",value=f"""**```{select_1.values[0]}이(가) 선택되었습니다.\n\n'다시선택' 버튼을 눌러 채널을 다시 선택합니다.\n'다음' 버튼을 눌러 다음 튜토리얼로 이동합니다.```**""", inline=False)
                embed.set_footer(text = "made by Lanturn#9899")
                await message_1.edit(embed = embed,components=[
                [Button(style = ButtonStyle.green, label="다시선택"),
                Button(style = ButtonStyle.blue, label="다음")]])

                bt_click_3 = await self.client.wait_for("button_click",check = check)
                if bt_click_3.component.label == '다시선택':
                    continue
                elif bt_click_3.component.label == '다음':
                    break
            embed = discord.Embed(title="**튜토리얼**",description = '**모든 튜토리얼이 끝났습니다.\n아래에서 봇의 커맨드들과 사용방법을 알 수 있습니다.\n봇을 초대해주셔서 감사합니다!**' ,color=0x7FFFD4)
            embed.add_field(name=f"**-급식**",value=f"""**```설정한 학교의 오늘 급식 메뉴를 보여줍니다.```**""",inline = False)
            embed.add_field(name=f"**-급식 <학교이름>**",value=f"""**```<학교이름>의 오늘 급식 메뉴를 보여줍니다.```**""",inline = False)
            embed.add_field(name=f"**--급식**",value=f"""**```커맨드를 입력한 뒤 선택한 날짜의 급식을 보여줍니다.```**""",inline = False)
            embed.add_field(name=f"**--급식 <학교이름>**",value=f"""**```커맨드를 입력한 뒤 선택한 날짜의 급식을 보여줍니다.```**""",inline = True)
            embed.add_field(name=f"**-학교설정**",value=f"""**```서버의 학교를 설정합니다```**""",inline = False)
            embed.add_field(name=f"**-설정**",value=f"""**```봇의 설정 메뉴를 엽니다.```**""",inline = False)
            embed.set_footer(text = "아래버튼을 클릭하여 개발자의 디스코드 서버에 들어오세요!\nmade by Lanturn#9899")
            await ctx.send(embed = embed,components=[
            Button(style = ButtonStyle.URL, label="디스코드",url = 'https://discord.gg/4nxyKU6r3Y')])
            return None








def setup(client):
    client.add_cog(tutorial(client))
