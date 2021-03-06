import os, wget, shutil, time
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from discord.utils import get



#Env Variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = os.getenv('ARCHSTONE_GUILD')


#Custom Defined
blacklist_file = "blockedusers.txt"
Server_Admin_Role = "Adjudicator"
Server_Host_Role = "Server Host"
Current_RR_Message_ID = 0
Role_NA_Emoji_Name = "na"
Role_EU_Emoji_Name = "eu"
Role_AS_Emoji_Name = "as"
Role_RPCS3_Emoji_Name = "rpcs3"
Role_NA_PVP_Emoji_Name = "napvp"
Role_EU_PVP_Emoji_Name = "eupvp"
Role_AS_PVP_Emoji_Name = "aspvp"
Role_RPCS3_PVP_Emoji_Name = "rpcs3pvp"
Role_RPCS3_Emoji_Name = "pfrpcs3"
Role_PS3_Emoji_Name = "pfps3"
Role_PS5_Emoji_Name = "pfps5"
Role_Phantom_Emoji_Name = "phantom"

Roles_NA = "PS3 North America"
Roles_EU = "PS3 Europe"
Roles_AS = "PS3 Asia"
Roles_RPCS3 = "RPCS3"
Roles_NA_PVP = "PS3 NA - PvP"
Roles_EU_PVP = "PS3 EU - PvP"
Roles_AS_PVP = "PS3 AS - PvP"
Roles_RPCS3_PVP = "RPCS3 - PvP"
Roles_RPCS3 = "RPCS3"
Roles_PS3 = "PS3"
Roles_PS5 = "PS5"
Roles_Phantom = "Phantom"

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'----- ARCHSTONES BOT START -----\n'
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    #channel = bot.get_channel(493504461583417354)
    #await channel.send('-------- Bot Started, Please run "!setrr" to have role reactions work. --------', delete_after=120 )


#---- Events
@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = payload.member

    if member is None:
        print("Error Getting Member ID")
        return

    if guild.name != GUILD:
        return

    if payload.message_id != Current_RR_Message_ID:
        return
    
    if payload.message_id == Current_RR_Message_ID and payload.emoji.name == Role_PS5_Emoji_Name:
        role = discord.utils.get(guild.roles, name=Roles_PS5)
        print("Added %s to %s Role" % (member, role))
        await member.add_roles(role)
    elif payload.message_id == Current_RR_Message_ID and payload.emoji.name == Role_PS3_Emoji_Name:
        role = discord.utils.get(guild.roles, name=Roles_PS3)
        print("Added %s to %s Role" % (member, role))
        await member.add_roles(role)
    elif payload.message_id == Current_RR_Message_ID and payload.emoji.name == Role_RPCS3_Emoji_Name:
        role = discord.utils.get(guild.roles, name=Roles_RPCS3)
        print("Added %s to %s Role" % (member, role))
        await member.add_roles(role)
    elif payload.message_id == Current_RR_Message_ID and payload.emoji.name == Role_Phantom_Emoji_Name:
        role = discord.utils.get(guild.roles, name=Roles_Phantom)
        print("Added %s to %s Role" % (member, role))
        await member.add_roles(role)
    else:
        print("Failed to find reaction match for emoji %s" % (payload.emoji.name))

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = get(guild.members, id=payload.user_id)

    if member is None:
        print("Error Getting Member ID")
        return

    if guild.name != GUILD:
        return

    if payload.message_id != Current_RR_Message_ID:
        return
    
    if payload.message_id == Current_RR_Message_ID and payload.emoji.name == Role_PS5_Emoji_Name:
        role = discord.utils.get(guild.roles, name=Roles_PS5)
        print("Removed %s from %s Role" % (member, role))
        await member.remove_roles(role)
    elif payload.message_id == Current_RR_Message_ID and payload.emoji.name == Role_PS3_Emoji_Name:
        role = discord.utils.get(guild.roles, name=Roles_PS3)
        print("Removed %s from %s Role" % (member, role))
        await member.remove_roles(role)
    elif payload.message_id == Current_RR_Message_ID and payload.emoji.name == Role_RPCS3_Emoji_Name:
        role = discord.utils.get(guild.roles, name=Roles_RPCS3)
        print("Removed %s from %s Role" % (member, role))
        await member.remove_roles(role)
    elif payload.message_id == Current_RR_Message_ID and payload.emoji.name == Role_Phantom_Emoji_Name:
        role = discord.utils.get(guild.roles, name=Roles_Phantom)
        print("Removed %s from %s Role" % (member, role))
        await member.remove_roles(role)
    else:
        print("Failed to find reaction match for emoji %s" % (payload.emoji.name))



#---- Normal User Commands
@bot.command(name='privateserver', help='Answer Question Relating to Private Server')
async def Archstones_privateserver(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        embedVar = discord.Embed(title="The Archstones Private Server", description="The Archstones was established back in Feb 2018. Currently the most active server for Demon's Souls on PS3 & RPCS3. Please visit https://thearchstones.com for more information.", color=0x6928D4)
        embedVar.add_field(name="Getting Started", value="Visit #northern-outskirts and set your role thats applicable to your version of Demon's Souls.", inline=False)
        embedVar.add_field(name="How to Connect", value="Please visit the #private-server channel for information on how to connect.", inline=False)
        await ctx.send(embed=embedVar, delete_after=35)
        await ctx.message.delete()
        

@bot.command(name='ps3', help='Answer Question Relating to PS3')
async def Archstones_ps3(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        embedVar = discord.Embed(title="PS3 Setup", description="", color=0x6928D4)
        embedVar.add_field(name="Getting Started", value="Visit #northern-outskirts and set your role thats applicable to your version of Demon's Souls.", inline=False)
        embedVar.add_field(name="How to Connect", value="1.   Go to Network PS3 Settings > Internet Connection Settings. \n 2.    Here, press 'Custom' and 'Enter Manually'. \n 3.    Change your Primary DNS to 142.93.245.186", inline=False)
        await ctx.send(embed=embedVar, delete_after=35)
        await ctx.message.delete()

@bot.command(name='patreon', help='')
async def Archstones_Patreon(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        embed=discord.Embed(title="The Archstones Patreon", url="https://www.patreon.com/TheArchstones", color=0xa600ff)
        await ctx.send(embed=embed, delete_after=35)
        await ctx.message.delete()

@bot.command(name='online-na', help='Shows North America Online Users')
async def Archstones_OnlineUsersNA(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        save_path_na = "MapNA_Count.txt"
        file = wget.download('https://thearchstones.com/MapNA_Count.txt', save_path_na)
        if os.path.exists(save_path_na):
            shutil.move(file,save_path_na)
        

        embedVar = discord.Embed(title="The Archstones - Online Users", description="", color=0x6928D4)
        embedVar.add_field(name="PS3", value="North America", inline=False)
        with open(save_path_na, 'r') as lines:
            for line in lines:
                a,b,c,online,area = line.split(' ', 4)
                embedVar.add_field(name=area, value=online, inline=True)

        embedVar.set_footer(text="Visit https://thearchstones.com/onlineusers for more information", icon_url = ctx.author.avatar_url)

        await ctx.send(embed=embedVar, delete_after=35)
        await ctx.message.delete()

@bot.command(name='online-eu', help='Shows Europe Online Users')
async def Archstones_OnlineUsersEU(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        save_path_eu = "MapEU_Count.txt"
        file = wget.download('https://thearchstones.com/MapEU_Count.txt', save_path_eu)
        if os.path.exists(save_path_eu):
            shutil.move(file,save_path_eu)

        embedVar = discord.Embed(title="The Archstones - Online Users", description="", color=0x6928D4)
        embedVar.add_field(name = chr(173), value = chr(173), inline=False)
        embedVar.add_field(name="PS3", value="Europe", inline=False)
        with open(save_path_eu, 'r') as lines:
            for line in lines:
                a,b,c,online,area = line.split(' ', 4)
                embedVar.add_field(name=area, value=online, inline=True)

        embedVar.set_footer(text="Visit https://thearchstones.com/onlineusers for more information", icon_url = ctx.author.avatar_url)

        await ctx.send(embed=embedVar, delete_after=35)
        await ctx.message.delete()

@bot.command(name='online-as', help='Shows Asia Online Users')
async def Archstones_OnlineUsersAS(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        save_path_jp = "MapJP_Count.txt"
        file = wget.download('https://thearchstones.com/MapJP_Count.txt', save_path_jp)
        if os.path.exists(save_path_jp):
            shutil.move(file,save_path_jp)
        

        embedVar = discord.Embed(title="The Archstones - Online Users", description="", color=0x6928D4)
        embedVar.add_field(name="PS3", value="Asia", inline=False)
        with open(save_path_jp, 'r') as lines:
            for line in lines:
                a,b,c,online,area = line.split(' ', 4)
                embedVar.add_field(name=area, value=online, inline=True)

        embedVar.set_footer(text="Visit https://thearchstones.com/onlineusers for more information", icon_url = ctx.author.avatar_url)

        await ctx.send(embed=embedVar, delete_after=35)
        await ctx.message.delete()

@bot.command(name='online-rpcs3', help='Shows rpcs3 Online Users')
async def Archstones_OnlineUsersCR(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        save_path_cr = "MapCR_Count.txt"
        file = wget.download('https://rpcs3.thearchstones.com/MapCR_Count.txt', save_path_cr)
        if os.path.exists(save_path_cr):
            shutil.move(file,save_path_cr)
        

        embedVar = discord.Embed(title="The Archstones - Online Users", description="", color=0x6928D4)
        embedVar.add_field(name="RPCS3", value="Cross Region", inline=False)
        with open(save_path_cr, 'r') as lines:
            for line in lines:
                a,b,c,online,area = line.split(' ', 4)
                embedVar.add_field(name=area, value=online, inline=True)

        embedVar.set_footer(text="Visit https://thearchstones.com/onlineusers for more information", icon_url = ctx.author.avatar_url)

        await ctx.send(embed=embedVar, delete_after=35)
        await ctx.message.delete()

@bot.command(name='worldtendency', help='Shows World Tendency')
async def Archstones_worldtendency(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        save_path_ps3 = "ps3GTValue.txt"
        save_path_rpcs3 = "rpcs3GTValue.txt"
        file = wget.download('https://thearchstones.com/GTValue.txt', save_path_ps3)
        if os.path.exists(save_path_ps3):
            shutil.move(file,save_path_ps3)

        file2 = wget.download('https://rpcs3.thearchstones.com/GTValue.txt', save_path_rpcs3)
        if os.path.exists(save_path_rpcs3):
            shutil.move(file2,save_path_rpcs3)
        
        embedVar = discord.Embed(title="The Archstones - Current Global World Tendency", description="", color=0x6928D4)

        with open(save_path_ps3) as f:
            lines = f.readlines()
            embedVar.add_field(name="PS3", value=lines[0], inline=False)
        with open(save_path_rpcs3) as f:
            lines = f.readlines()
            embedVar.add_field(name="RPCS3", value=lines[0], inline=False)

        await ctx.send(embed=embedVar, delete_after=35)
        await ctx.message.delete()

@bot.command(name='sl1', help='Answer Question Relating to SL1 run')
async def Archstones_slq(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        embedVar = discord.Embed(title="SL1 Guidelines", url="https://bigsoundlogan.github.io/Demon-s-Souls-SL1-Repository/", description="A comprehensive and community-supported repository on how the Demon's Souls Discord server manages SL1 runs and their numerous challenge variations. Maintained by Sen#1775 \n \n https://bigsoundlogan.github.io/Demon-s-Souls-SL1-Repository/")
        await ctx.send(embed=embedVar, delete_after=35)
        await ctx.message.delete()

@bot.command(name='troubleshoot', help='Answer Question for troubleshooting')
async def Archstones_slq(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        embedVar=discord.Embed(title="Troubleshoot Connection", url="https://discord.com/channels/245489122892840961/564301616283385856", description="Will help give you an idea about why you might not be able to connect to The Archstones. Use the message you get when attempting to connect to find a potential solution below.", color=0x29c758)
        embedVar.set_author(name="The Archstones", url="https://Thearchstones.com")
        embedVar.add_field(name="Cannot connect to the Demon's Souls server", value="**PS3** \n 1. Please verify you have the set your **Primary DNS to 142.93.245.186** \n 2. Try creating a hotspot with your phone and connect your PS3 to that, ensure you still set the Primary DNS as stated above. Sometimes the issues can be your ISP that is blocking custom DNS servers. \n **RPCS3** \n 1. Ensure you have set your IP/Host Switch, Created your RPCN account, and Set your token in the configuration. \n If you still continue to have issue, feel free to reach out, we will try to assist where possible. ", inline=False)
        embedVar.add_field(name="The Demon's Souls Online Service has been terminated", value="Normally this represents two things, Either you have not set your DNS properly for PS3, IP/Host Switch for RPCS3, or somewhere between your connection and the internet your network is not receiving the right domain name to connect. Please ensure you have set your DNS / IP/Host Switch, If you have issues still please contact the mod team we have a solution for you.", inline=True)
        embedVar.add_field(name="Archstones Patcher", value="If you continue to experience issues, you might want to try the patcher which will help resolve DNS related issues. You can find this at  https://github.com/Yuvi-App/Archstones-Patcher/releases", inline=True)
        embedVar.set_footer(text="visit #private-server for more detailed information", icon_url = ctx.author.avatar_url)
        await ctx.send(embed=embedVar, delete_after=35)
        await ctx.message.delete()

#---- Admin User Commands
@bot.command(name='editrr', help='Edit Current Role Reaction Message | Example Use !editrr channelID messageID "INSERT TITLE HERE" "INTERE CONTENT HERE" HexColorValue')
@commands.has_any_role(Server_Admin_Role, Server_Host_Role)
async def Archstones_RR(ctx, channelID, messageID, title, content, color):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        channel_ID = int(channelID)
        message_ID = int(messageID)
        message_title = str(title)
        message_content = str(content)
        message_color = discord.Colour(int(f'0x{color}', 16))
        embedVar = discord.Embed(title=message_title, description=message_content, color=message_color)
        channel = bot.get_channel(channel_ID)
        message = await channel.fetch_message(message_ID)

        await message.edit(embed=embedVar)
        print("RR Message Update")
        await ctx.message.delete()

@bot.command(name='newrr', help='Add New Message | Example Use !editrr channelID "INSERT TITLE HERE" "INTERE CONTENT HERE" HexColorValue')
@commands.has_any_role(Server_Admin_Role, Server_Host_Role)
async def Archstones_NEW_RR(ctx, channelID, title, content, color):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        channel_ID = int(channelID)
        message_title = str(title)
        message_content = str(content)
        message_color = discord.Colour(int(f'0x{color}', 16))
        embedVar = discord.Embed(title=message_title, description=message_content, color=message_color)
        channel = bot.get_channel(channel_ID)

        await channel.send(embed=embedVar)
        print("Added new RR Message")
        await ctx.message.delete()

@bot.command(name='setrr', help="Sets messageID to the RoleReaction Message to Monitor | !setrr channelID messageID")
@commands.has_any_role(Server_Admin_Role, Server_Host_Role)
async def Archstones_SET_RR(ctx, channelID, messageID):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        channel_ID = int(channelID)
        message_ID = int(messageID)
        global Current_RR_Message_ID
        Current_RR_Message_ID = message_ID
        print("Set RR Message to ID %r" % Current_RR_Message_ID)
        await ctx.send('Set Role Reaction Monitor Message to %r' % Current_RR_Message_ID, delete_after=35)
        await ctx.message.delete()

@bot.command(name='isrrset', help="check if messageID to the RoleReaction Message to Monitor")
@commands.has_any_role(Server_Admin_Role, Server_Host_Role)
async def Archstones_IS_RR(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        global Current_RR_Message_ID
        if Current_RR_Message_ID == 0:
            print("RR Message is not set")
            await ctx.send('RR Message is not set', delete_after=35)
            await ctx.message.delete()
        else:
            print("RR Message is set to ID %r" % Current_RR_Message_ID)
            await ctx.send('RR Message is set to ID %r' % Current_RR_Message_ID, delete_after=35)
            await ctx.message.delete()

@bot.command(name='deleterr', help='Deletes Message | Example Use !deleterr channelID messageID')
@commands.has_any_role(Server_Admin_Role, Server_Host_Role)
async def Archstones_DELETE_RR(ctx, channelID, messageID):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        channel_ID = int(channelID)
        message_ID = int(messageID)
    
        channel = bot.get_channel(channel_ID)
        message = await channel.fetch_message(message_ID)

        await message.delete()
        await ctx.message.delete()
        print("Deleted RR Message")

@bot.command(name='blockuser', help="Blocks users from using bots commands")
@commands.has_any_role(Server_Admin_Role, Server_Host_Role)
async def Archstones_Block_User(ctx, user):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        fobj = open("blockedusers.txt")
        blacklist = fobj.read()

        if user.lower() in blacklist:
            print("User %s already in blacklist" % (user))
            await ctx.send('User %s already in blacklist' % (user), delete_after=35)
            await ctx.message.delete()
        else:
            with open("blockedusers.txt", "a+") as file_object:
                file_object.seek(0)
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                file_object.write(user.lower())

            print("User %s added to blacklist" % (user))
            await ctx.send('User %s added to blacklist' % (user), delete_after=35)
            await ctx.message.delete()

        fobj.close()

@bot.command(name='unblockuser', help="unblocks users from using bots commands")
@commands.has_any_role(Server_Admin_Role, Server_Host_Role)
async def Archstones_Unblock_User(ctx, user):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        fobj = open("blockedusers.txt")
        blacklist = fobj.read()

        if user.lower() in blacklist:
            with open('blockedusers.txt','r+') as f:
                data = ''.join([i for i in f if not i.lower().startswith(user.lower())])
                f.seek(0)
                f.write(data)
                f.truncate()

            print("Removed User %s from blacklist" % (user))
            await ctx.send('Removed User %s from blacklist' % (user), delete_after=35)
            await ctx.message.delete()


        else:
            print("Unable to find User %s in blacklist" % (user))
            await ctx.send('Unable to find User %s in blacklist' % (user), delete_after=35)
            await ctx.message.delete()

        fobj.close()

 

#---- Logging
@bot.event
async def on_error(event, *args, **kwargs):
    with open('error.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise






bot.run(TOKEN)