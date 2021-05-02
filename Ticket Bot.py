import discord
import asyncio
import os
import sys
import traceback
import datetime

INTENTS = discord.Intents.all()
client = discord.Client(intents=INTENTS)

################################메인################################
@client.event
async def on_message(message):
    if message.author.bot:
        return None

    elif message.author.system:
        return None

    elif message.channel.type == discord.ChannelType.group:
        return None

    elif message.channel.type == discord.ChannelType.private:
        return None

    elif message.content.startswith("!티켓"):
        content = ""
        channel_name = (f'{message.author}님_채널').replace("#", "")
        for channel in message.guild.text_channels:
            if str(channel.name) == str(channel_name):
                content = f"이미 {message.author.mention}님이 요청하신 채널({channel.mention})이 있습니다."
        if content != "":
            await message.channel.send(content)
        else:
            overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True)
            }

            channel = await message.guild.create_text_channel(channel_name, overwrites=overwrites)
            embed = discord.Embed(title="채널생성",description="채널 생성을 완료 하였습니다.", color=0xFAF8CD, timestamp=datetime.datetime.utcnow())
            await channel.send(content="@here", embed=embed)

    elif message.content.startswith("!채널삭제"):
        if message.author.guild_permissions.manage_channels:
            if message.channel.name.endswith("님_채널") == False:
                await message.channel.send("티켓 채널이 아니라면, 삭제할 수 없습니다.")
            else:
                embed = discord.Embed(title="채널삭제",description="채널을 삭제하시겠습니까?", color=0xFAF8CD, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                checkembed = await message.channel.send(embed=embed)
                for emoji in ['⭕', '❌']:
                    await checkembed.add_reaction(emoji)
                def auditcheck(reaction, user):
                    return user == message.author and (str(reaction.emoji) == '⭕' or str(reaction.emoji) == '❌')
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=auditcheck)
                except asyncio.TimeoutError:
                    embed=discord.Embed(title=f'⛔ 시간이 초과되었습니다.', color=0xFAF8CD)
                    await message.channel.send(embed=embed)
                else:
                    if reaction.emoji == '⭕':
                        embed=discord.Embed(title=f'✅ 3초후 채널이 삭제됩니다', color=0xFAF8CD)
                        await checkembed.edit(embed=embed)
                        await asyncio.sleep(3)
                        await message.channel.delete()

                    elif reaction.emoji == '❌':
                        embed=discord.Embed(title=f'✅ 취소되었습니다.', color=0xFAF8CD)
                        await checkembed.edit(embed=embed)
        else:
            await message.channel.send(f"{message.author.mention}님은 채널삭제 권한이 없습니다")
            
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 837897610680991795 and payload.emoji.name == '☎️':
        content = ""
        channel_name = (f'{payload.member.name}{payload.member.discriminator}님_채널').replace("#", "")
        for channel in payload.member.guild.text_channels:
            if str(channel.name) == str(channel_name):
                content = f"이미 {client.get_user(int(payload.member.id)).mention}님이 요청하신 채널이 있습니다."
        if content != "":
            channel = await client.get_user(int(payload.member.id)).create_dm()
            await channel.send(content)
        else:
            overwrites = {
            payload.member.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            payload.member.guild.get_member(int(payload.user_id)): discord.PermissionOverwrite(read_messages=True)
            }

            channel = await payload.member.guild.create_text_channel(channel_name, overwrites=overwrites)
            embed = discord.Embed(title="채널생성",description="채널 생성을 완료 하였습니다.", color=0xFAF8CD, timestamp=datetime.datetime.utcnow())
            await channel.send(content="@here", embed=embed)


################################오류################################
@client.event
async def on_error(event, *args, **kwargs):
    excinfo = sys.exc_info()

    if event == "on_message":
        embed = discord.Embed(title='⛔ 오류발생!', description=f'흠..오류가 발생한것 같으니, 체크를 해봐야겠어요..', color=0xFAF8CD)
        await args[0].channel.send(embed = embed)
    
    errstr = f'{"".join(traceback.format_tb(excinfo[2]))}{excinfo[0].__name__}: {excinfo[1]}'
    await client.get_channel(837884032192610394).send(f"\n**[오류발생]** \n타입 : {event}\n내용 : {errstr}")
    

client.run("your bot token")