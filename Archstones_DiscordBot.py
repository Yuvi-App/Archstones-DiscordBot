import os, wget, shutil, time, sqlite3, datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from discord.utils import get
from collections.abc import Sequence
from dislash import InteractionClient, SelectMenu, SelectOption, ActionRow, Button, ButtonStyle,  Option, OptionType



#Env Variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = os.getenv('ARCHSTONE_GUILD')

#SQLite Stuff
Accountdbfilename = "AccountLink.sqlite"
RPCS3_PlayerDBfilename = "/root/Desktop/Archstones/db/players.sqlite"
PS3_PlayerDBfilename = "/mnt/PS3_ARCHSTONES/players.sqlite"
conn = sqlite3.connect(Accountdbfilename)
c = conn.cursor()
conn2 = sqlite3.connect(RPCS3_PlayerDBfilename)
c2 = conn2.cursor()
conn3 = sqlite3.connect(PS3_PlayerDBfilename)
c3 = conn2.cursor()


#Custom Defined
blacklist_file = "blockedusers.txt"
Server_Admin_Role = "Administrator"
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

guild = discord.utils.get(bot.guilds, name=GUILD)
inter_client = InteractionClient(bot, test_guilds=guild)

#channel = bot.get_channel(493504461583417354)
#await channel.send('-------- Bot Started, Please run "!setrr" to have role reactions work. --------', delete_after=30 )


#---- Events
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'----- ARCHSTONES BOT START -----\n'
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

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


#---- Normal Slash Commands
@inter_client.slash_command(description="Reports the current Global World Tendency")
async def currentglobaltendency(ctx):
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

        await ctx.send(embed=embedVar)

@inter_client.slash_command(description="Answer Question Relating to Private Server")
async def privateserver(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        embedVar = discord.Embed(title="The Archstones Private Server", description="The Archstones was established back in Feb 2018. Currently the most active server for Demon's Souls on PS3 & RPCS3. Please visit https://thearchstones.com for more information.", color=0x6928D4)
        embedVar.add_field(name="Getting Started", value="Visit #assign-role and set your role thats applicable to your version of Demon's Souls.", inline=False)
        embedVar.add_field(name="How to Connect", value="Please visit the #private-server channel for information on how to connect.", inline=False)
        await ctx.send(embed=embedVar, delete_after=20)

@inter_client.slash_command(description="Eternal Thank you")
async def patreon(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        embed=discord.Embed(title="The Archstones Patreon", url="https://www.patreon.com/TheArchstones", color=0xa600ff)
        await ctx.send(embed=embed)

@inter_client.slash_command(description="All About SL1 Runs")
async def sl1_runs(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        embedVar = discord.Embed(title="SL1 Guidelines", url="https://bigsoundlogan.github.io/Demon-s-Souls-SL1-Repository/", description="A comprehensive and community-supported repository on how the Demon's Souls Discord server manages SL1 runs and their numerous challenge variations. Maintained by Sen \n \n https://bigsoundlogan.github.io/Demon-s-Souls-SL1-Repository/")
        await ctx.send(embed=embedVar)

@inter_client.slash_command(description="Troubleshooting Steps")
async def troubleshoot_connection(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        embedVar=discord.Embed(title="Troubleshoot Connection", url="https://discord.com/channels/245489122892840961/564301616283385856", description="Will help give you an idea about why you might not be able to connect to The Archstones. Use the message you get when attempting to connect to find a potential solution below.", color=0x29c758)
        embedVar.set_author(name="The Archstones", url="https://Thearchstones.com")
        embedVar.add_field(name="Cannot connect to the Demon's Souls server", value="**PS3** \n 1. Please verify you have the set your **Primary DNS to 142.93.245.186** \n 2. Try creating a hotspot with your phone and connect your PS3 to that, ensure you still set the Primary DNS as stated above. Sometimes the issues can be your ISP that is blocking custom DNS servers. \n **RPCS3** \n 1. Ensure you have set your IP/Host Switch, Created your RPCN account, and Set your token in the configuration. \n If you still continue to have issue, feel free to reach out, we will try to assist where possible. ", inline=False)
        embedVar.add_field(name="The Demon's Souls Online Service has been terminated", value="Normally this represents two things, Either you have not set your DNS properly for PS3, IP/Host Switch for RPCS3, or somewhere between your connection and the internet your network is not receiving the right domain name to connect. Please ensure you have set your DNS / IP/Host Switch, If you have issues still please contact the mod team we have a solution for you.", inline=True)
        embedVar.add_field(name="Archstones Patcher", value="If you continue to experience issues, you might want to try the patcher which will help resolve DNS related issues. You can find this at  https://github.com/Yuvi-App/Archstones-Patcher/releases", inline=True)
        embedVar.set_footer(text="visit #private-server for more detailed information", icon_url = ctx.author.avatar_url)
        await ctx.send(embed=embedVar)

@inter_client.slash_command(description="PS3 Connection Info")
async def ps3_connection(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        embedVar = discord.Embed(title="PS3 Setup", description="", color=0x6928D4)
        embedVar.add_field(name="Getting Started", value="Visit #northern-outskirts and set your role thats applicable to your version of Demon's Souls.", inline=False)
        embedVar.add_field(name="How to Connect", value="1.   Go to Network PS3 Settings > Internet Connection Settings. \n 2.    Here, press 'Custom' and 'Enter Manually'. \n 3.    Change your Primary DNS to 142.93.245.186", inline=False)
        await ctx.send(embed=embedVar)

@inter_client.slash_command(description="Online PS3 - North American Users")
async def online_ps3_na(ctx):
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

        await ctx.send(embed=embedVar)

@inter_client.slash_command(description="Online PS3 - Europe Users")
async def online_ps3_eu(ctx):
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

        await ctx.send(embed=embedVar)

@inter_client.slash_command(description="Online PS3 - Asia Users")
async def online_ps3_as(ctx):
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

        await ctx.send(embed=embedVar)

@inter_client.slash_command(description="Online RPCS3 - Cross Region Users")
async def online_rpcs3(ctx):
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

        await ctx.send(embed=embedVar)

#---- Slash Commands for Archstone/Discord Intergration
@inter_client.slash_command(
    description="Change World Tendency",
    options=[
        Option("platform", "Enter Platform | RPCS3 or PS3", OptionType.STRING, required=True),
        Option("desired_tendency", "Enter Between -200 & 200 | -200 = Pure Black, 200 = Pure White", OptionType.INTEGER, required=True)
    ])
async def changeworldtendency(ctx, platform, desired_tendency):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        DISCORD_NAME = ctx.author
        desired_tendency = int(desired_tendency)
        VERSION = platform
        VERSION = VERSION.upper()

        #Sanitize Input for INT Value
        try:
            if -200 <= desired_tendency <= 200:
                #Check What Version
                if VERSION == "RPCS3":
                    #Check if account exist 
                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"RPCS3")).fetchone()[0]
                    PSN_NAME = row
                    if PSN_NAME is None:
                        print("WT Command - %s account not linked" % (DISCORD_NAME))
                        emb = discord.Embed(
                            title="Account Not Link!",
                            description="Please link account first",
                            color=discord.Color.red()
                        )
                        await ctx.reply(embed=emb,delete_after=10)
                        return
                    elif PSN_NAME is not None:
                        conn2.execute("update players set desired_tendency = ? where characterID = ?", (desired_tendency, str(PSN_NAME),))
                        conn2.commit()
                        print("WT Command - %s Discord Account, %s PSN Account, changed WT to %s, Version %s" % (DISCORD_NAME,PSN_NAME,str(desired_tendency), VERSION))
                        emb = discord.Embed(
                            title="SUCCESS - %s" % VERSION,
                            description='Changed World Tendency to %s!' % str(desired_tendency),
                            color=discord.Color.blue()
                        )
                        await ctx.reply(embed=emb)
                    else:
                        return
                elif VERSION == "PS3":
                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"PS3")).fetchone()[0]
                    PSN_NAME = row
                    if PSN_NAME is None:
                        print("WT Command - %s account not linked" % (DISCORD_NAME))
                        emb = discord.Embed(
                            title="Account Not Link!",
                            description="Please link account first",
                            color=discord.Color.red()
                        )
                        await ctx.reply(embed=emb,delete_after=10)
                        return
                    elif PSN_NAME is not None:
                        PSN_NAME = row
                        conn3.execute("update players set desired_tendency = ? where characterID = ?", (desired_tendency, str(PSN_NAME),))
                        conn3.commit()
                        print("WT Command - %s Discord Account, %s PSN Account, changed WT to %s, Version %s" % (DISCORD_NAME,PSN_NAME,str(desired_tendency), VERSION))
                        emb = discord.Embed(
                            title="SUCCESS - %s" % VERSION,
                            description='Changed World Tendency to %s!' % str(desired_tendency),
                            color=discord.Color.blue()
                        )
                        await ctx.reply(embed=emb)
                    else:
                        return
                else:
                    print("WT Command - %s account Invalid Version entered %s" % (DISCORD_NAME, str(VERSION)))
                    return
            else:
                print("WT Command - %s User, Wrong Input Value %s" % (DISCORD_NAME,str(desired_tendency)))
                emb = discord.Embed(
                            title="ERROR - %s" % VERSION,
                            description='Enter a Value between -200 & 200!',
                            color=discord.Color.blue()
                        )
                await ctx.reply(embed=emb, delete_after=10)
        except:
            print("WT Command - %s User, Failed to Sanitize Value %s" % (DISCORD_NAME,str(desired_tendency)))
            return        



@inter_client.slash_command(description="Link Discord Account to RPCN/PSN")
async def link(ctx):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        DISCORD_NAME = ctx.author
        timenow = datetime.datetime.now()

        emb = discord.Embed(
            title="Check DM to Continue",
            description="",
            color=discord.Color.green()
        )
        await ctx.reply(embed=emb,delete_after=10)

        #DM Users to Setup the Link process
        await ctx.author.send("Link Account for PS3 or RPCS3?")
        response = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel), timeout=120)
        VERSION = response.content.upper()
        
        #Ensure RPCS3 or PS3 is Entered
        if VERSION == "RPCS3":
            #Get RPCN Name
            await ctx.author.send("Please enter your RPCN Username")
            response2 = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel), timeout=120)
            PSN_NAME = response2.content
            PSN_NAME += "0"
            print("Verify - Discord User %s, PSN User %s, Version %s" % (DISCORD_NAME, PSN_NAME, VERSION))

            #Check if account exist for RPCS3
            row = conn.execute("select count(*) from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"RPCS3")).fetchone()
            print("Value = %s %s %s %s" % (row, DISCORD_NAME, PSN_NAME, timenow))
       
            if row[0] == 0:
                #Account not Found, Link Accounts in DB
                conn.execute("insert into linkedaccounts(DISCORD_NAME, PSN_NAME, VERSION, DATE_TIME) VALUES (?,?,?,?)", (str(DISCORD_NAME),str(PSN_NAME),str(VERSION),str(timenow)))
                conn.commit()
                print("Linked Account %s to %s for %s" % (DISCORD_NAME,PSN_NAME,VERSION))
                await ctx.author.send('Linked Account Success!')

            elif row[0] >= 1:
                #Acccount Found, Leave Function since its linked
                await ctx.author.send('RPCN Account Already Linked!')
                return
        elif VERSION == "PS3":
            #Get PSN Name
            await ctx.author.send("Please enter your PSN Username")
            response2 = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel), timeout=120)
            PSN_NAME = response2.content
            PSN_NAME += "0"
            print("Verify - Discord User %s, PSN User %s, Version %s" % (DISCORD_NAME, PSN_NAME, VERSION))

            #Check if account exist for PS3
            row = conn.execute("select count(*) from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"PS3")).fetchone()
            print("Value = %s %s %s %s" % (row, DISCORD_NAME, PSN_NAME, timenow))
       
            if row[0] == 0:
                #Account not Found, Link Accounts in DB
                conn.execute("insert into linkedaccounts(DISCORD_NAME, PSN_NAME, VERSION, DATE_TIME) VALUES (?,?,?,?)", (str(DISCORD_NAME),str(PSN_NAME),str(VERSION),str(timenow)))
                conn.commit()
                print("Linked Account %s to %s for %s" % (DISCORD_NAME,PSN_NAME,VERSION))
                await ctx.author.send('Linked Account Success!')

            elif row[0] >= 1:
                #Acccount Found, Leave Function since its linked
                await ctx.author.send('PS3 Account Already Linked!')
                return
        else:
            #Incorrect Version entered
            await ctx.author.send('Please enter RPCS3 or PS3')
            return



@inter_client.slash_command(
    description="Change from Global Tendency Control, vs Manual Tendency Control",
    options=[
        Option("platform", "Enter Platform | RPCS3 or PS3", OptionType.STRING, required=True),
        Option("global_or_manual", "global = for Server Tendency to affect you | manual = to allow you to control your own tendency", OptionType.STRING, required=True)
    ])
async def globalmanualtendency(ctx, platform, global_or_manual):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        DISCORD_NAME = ctx.author
        global_or_manual = global_or_manual.upper()
        VERSION = platform
        VERSION = VERSION.upper()

        #Check if in Role
        #roles = str(DISCORD_NAME.roles)
        #if Roles_RPCS3 not in roles or Roles_PS3 not in roles:
        #    return


        #Sanitize Version Input
        if VERSION == "RPCS3":
            #Sanitize Input
            if global_or_manual == "GLOBAL":
                GlobalTendency = 0
                try:
                    #Get PSNNAME
                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"RPCS3")).fetchone()[0]
                    PSN_NAME = row

                    #Set Global Tendency
                    conn2.execute("update players set enable_manual_tendency = ? where characterID = ?", (GlobalTendency, str(PSN_NAME),))
                    conn2.commit()

                    emb = discord.Embed(
                            title="SUCCESS - RPCS3",
                            description="Enabled Global Tendency",
                            color=discord.Color.red()
                        )
                    await ctx.reply(embed=emb)
                    print("GT_MT Command - %s User, Enabled Global Tendency %s" % (DISCORD_NAME,str(global_or_manual)))

                except:
                    print("GT_MT Command - %s account not linked" % (DISCORD_NAME))
                    emb = discord.Embed(
                            title="Account Not Link!",
                            description="Please link account first",
                            color=discord.Color.red()
                        )
                    await ctx.reply(embed=emb,delete_after=10)
                    return


            elif global_or_manual == "MANUAL":
                ManualTendency = 1
                try:
                    #Get PSNNAME
                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"RPCS3")).fetchone()[0]
                    PSN_NAME = row

                    #Set Manual Tendency
                    conn2.execute("update players set enable_manual_tendency = ? where characterID = ?", (ManualTendency, str(PSN_NAME),))
                    conn2.commit()

                    print("GT_MT Command - %s User, Enabled Manual Tendency %s" % (DISCORD_NAME,str(global_or_manual)))
                    emb = discord.Embed(
                            title="SUCCESS - RPCS3",
                            description="Enabled Manual Tendency",
                            color=discord.Color.red()
                        )
                    await ctx.reply(embed=emb)
                except:
                    print("GT_MT Command - %s account not linked" % (DISCORD_NAME))
                    emb = discord.Embed(
                            title="Account Not Link!",
                            description="Please link account first",
                            color=discord.Color.red()
                        )
                    await ctx.reply(embed=emb,delete_after=10)
                    return
            else:
                print("GT_MT Command - %s User, Failed to Sanitize Global/MT Value %s" % (DISCORD_NAME,str(global_or_manual)))
                return

        elif VERSION == "PS3":
            #Sanitize Input
            if global_or_manual == "GLOBAL":
                GlobalTendency = 0
                try:
                    #Get PSNNAME
                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"PS3")).fetchone()[0]
                    PSN_NAME = row

                    #Set Global Tendency
                    conn3.execute("update players set enable_manual_tendency = ? where characterID = ?", (GlobalTendency, str(PSN_NAME),))
                    conn3.commit()

                    print("GT_MT Command - %s User, Enabled Global Tendency %s" % (DISCORD_NAME,str(global_or_manual)))
                    emb = discord.Embed(
                            title="SUCCESS - PS3",
                            description="Enabled Global Tendency",
                            color=discord.Color.red()
                        )
                    await ctx.reply(embed=emb)

                except:
                    print("GT_MT Command - %s account not linked" % (DISCORD_NAME))
                    emb = discord.Embed(
                            title="Account Not Link!",
                            description="Please link account first",
                            color=discord.Color.red()
                        )
                    await ctx.reply(embed=emb,delete_after=10)
                    return

            elif global_or_manual == "MANUAL":
                ManualTendency = 1
                try:
                    #Get PSNNAME
                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"PS3")).fetchone()[0]
                    PSN_NAME = row

                    #Set Manual Tendency
                    conn3.execute("update players set enable_manual_tendency = ? where characterID = ?", (ManualTendency, str(PSN_NAME),))
                    conn3.commit()

                    print("GT_MT Command - %s User, Enabled Manual Tendency %s" % (DISCORD_NAME,str(global_or_manual)))
                    emb = discord.Embed(
                            title="SUCCESS - PS3",
                            description="Enabled Manual Tendency",
                            color=discord.Color.red()
                        )
                    await ctx.reply(embed=emb)
                except:
                    print("GT_MT Command - %s account not linked" % (DISCORD_NAME))
                    emb = discord.Embed(
                            title="Account Not Link!",
                            description="Please link account first",
                            color=discord.Color.red()
                        )
                    await ctx.reply(embed=emb,delete_after=10)
                    return

            else:
                print("GT_MT Command - %s User, Failed to Sanitize Global/MT Value %s" % (DISCORD_NAME,str(global_or_manual)))
                await ctx.send('ERROR: Please enter GLOBAL or CUSTOM', delete_after=30)
                await ctx.message.delete()
                return
        else:
            Print("GT_MT Command - %s User, Failed to Sanitize Version Value %s" % (DISCORD_NAME,str(global_or_manual)))
            await ctx.send('ERROR: Please enter RPCS3 or PS3', delete_after=30)
            await ctx.message.delete()
            return



@inter_client.slash_command(
    description="Unlink Discord Account to PSN Account",
    options=[
        Option("platform", "Enter Platform | RPCS3 or PS3", OptionType.STRING, required=True),
        Option("discord_name", "@ User", OptionType.USER, required=True)
    ])
async def unlink(ctx, platform, discord_name):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        if "@" in str(discord_name):
            discord_name = bot.fetch_member(discord_name).name

        user = ctx.author
        roles = str(user.roles)
        DISCORD_NAME = discord_name
        VERSION = platform
        VERSION = VERSION.upper()
        if Server_Host_Role in roles or Server_Admin_Role in roles:
            if VERSION == "RPCS3":
                conn.execute("DELETE FROM linkedaccounts WHERE VERSION = ? AND DISCORD_NAME = ?", ("RPCS3", str(DISCORD_NAME)))
                conn.commit()
                print("Unlink Command - %s Admin, Unlinked User %s" % (str(user),str(DISCORD_NAME)))
                emb = discord.Embed(
                    title="SUCCESS",
                    description="Unlinked User %s" % str(DISCORD_NAME),
                    color=discord.Color.blue()
                )
                await ctx.reply(embed=emb)
            elif VERSION == "PS3":
                conn.execute("DELETE FROM linkedaccounts WHERE VERSION = ? AND DISCORD_NAME = ?", ("PS3", str(DISCORD_NAME)))
                conn.commit()
                print("Unlink Command - %s Admin, Unlinked User %s" % (str(user),str(DISCORD_NAME)))
                emb = discord.Embed(
                    title="SUCCESS",
                    description="Unlinked User %s" % str(DISCORD_NAME),
                    color=discord.Color.blue()
                )
                await ctx.reply(embed=emb)
            else:
                Print("Unlink Command - %s Admin, Failed to Sanitize Version Value %s" % (str(user),str(global_or_manual)))
                emb = discord.Embed(
                    title="ERROR",
                    description="Please enter RPCS3 or PS3",
                    color=discord.Color.red()
                )
                await ctx.reply(embed=emb,delete_after=10)
                return
        else:
            print("Unlink - Invalid Permissions - %s" % user)
            emb = discord.Embed(
                title="ERROR",
                description="Invalid Permissions - PLease contact an admin for assistance",
                color=discord.Color.red()
            )
            await ctx.reply(embed=emb,delete_after=10)



@inter_client.slash_command(
    description="Get Personal Server Stats",
    options=[
        Option("platform", "Enter Platform | RPCS3 or PS3", OptionType.STRING, required=True),
        Option("discord_name", "@ User", OptionType.USER, required=True)
    ])
async def personalstats(ctx, platform, discord_name):
    if ctx.guild.name != GUILD:
        return
    if ctx.guild.name == GUILD:
        if "@" in str(discord_name):
            discord_name = bot.fetch_member(discord_name).name

        user = ctx.author
        roles = str(user.roles)
        DISCORD_NAME = discord_name
        VERSION = platform
        VERSION = VERSION.upper()

        #Only Author can run check
        if discord_name != ctx.author:
            print("PersonalStats - %s tried to get %s stats" % (ctx.author, discord_name))
            return

        #Get PSNNAME
        try:
            row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"RPCS3")).fetchone()[0]
            PSN_NAME = row
        except:
            print("PersonalStats Command - %s account not linked" % (DISCORD_NAME))
            emb = discord.Embed(
                title="Account Not Link!",
                description="Please link account first",
                color=discord.Color.red()
            )
            await ctx.reply(embed=emb,delete_after=10)
            return

        #Get stats
        if VERSION == "RPCS3":
            stats = conn2.execute("select * from players where characterID = ?", (str(PSN_NAME),)).fetchone()
            grade_s = stats[1]
            grade_a = stats[2]
            grade_b = stats[3]
            grade_c = stats[4]
            grade_d = stats[5]
            numsessions = stats[6]
            messageratings = stats[7]
            gameversion = stats[8]
            psndeaths = stats[9]
            enable_manual_tendency = stats[10]
            desired_tendency = stats[11]
            global_tendency = stats[12]

            if enable_manual_tendency == 1:
                enable_manual_tendency = "True"
            elif enable_manual_tendency == 0:
                enable_manual_tendency = "False"

            emb = discord.Embed(
                title="%s - %s Personal Stats" % (DISCORD_NAME,VERSION),
                description="",
                color=discord.Color.red()
            )
            emb.add_field(name="Multiplayer Sessions:", value="%s" % numsessions, inline=False)
            emb.add_field(name="Grade S", value="%s" % grade_s, inline=True)
            emb.add_field(name="Grade A", value="%s" % grade_a, inline=True)
            emb.add_field(name="Grade B", value="%s" % grade_b, inline=True)
            emb.add_field(name="Grade C", value="%s" % grade_c, inline=True)
            emb.add_field(name="Grade D", value="%s" % grade_d, inline=True)
            emb.add_field(name="Ratings Given", value="%s" % messageratings, inline=True)
            emb.add_field(name="Deaths on The Archstone's", value="%s" % psndeaths, inline=False)
            emb.add_field(name="Manual Tendency Enabled", value="%s" % enable_manual_tendency, inline=True)
            emb.add_field(name="Desired Tendency", value="%s" % desired_tendency, inline=True)
            await ctx.reply(embed=emb)
            print("PersonalStats - %s Got Stats" % (ctx.author))

        elif VERSION == "PS3":
            stats = conn3.execute("select * from players where characterID = ?", (str(PSN_NAME),)).fetchone()
            grade_s = stats[1]
            grade_a = stats[2]
            grade_b = stats[3]
            grade_c = stats[4]
            grade_d = stats[5]
            numsessions = stats[6]
            messageratings = stats[7]
            gameversion = stats[8]
            psndeaths = stats[9]
            enable_manual_tendency = stats[10]
            desired_tendency = stats[11]
            global_tendency = stats[12]

            if enable_manual_tendency == 1:
                enable_manual_tendency = "True"
            elif enable_manual_tendency == 0:
                enable_manual_tendency = "False"

            emb = discord.Embed(
                title="%s - %s Personal Stats" % (DISCORD_NAME,VERSION),
                description="",
                color=discord.Color.red()
            )
            emb.add_field(name="Multiplayer Sessions:", value="%s" % numsessions, inline=False)
            emb.add_field(name="Grade S", value="%s" % grade_s, inline=True)
            emb.add_field(name="Grade A", value="%s" % grade_a, inline=True)
            emb.add_field(name="Grade B", value="%s" % grade_b, inline=True)
            emb.add_field(name="Grade C", value="%s" % grade_c, inline=True)
            emb.add_field(name="Grade D", value="%s" % grade_d, inline=True)
            emb.add_field(name="Ratings Given", value="%s" % messageratings, inline=True)
            emb.add_field(name="Deaths on The Archstone's", value="%s" % psndeaths, inline=False)
            emb.add_field(name="Manual Tendency Enabled", value="%s" % enable_manual_tendency, inline=True)
            emb.add_field(name="Desired Tendency", value="%s" % desired_tendency, inline=True)
            await ctx.reply(embed=emb)
            print("PersonalStats - %s Got Stats" % (ctx.author))
        else:
            print("PersonalStats Command - %s User, Failed to Sanitize Version Value %s" % (DISCORD_NAME,str(global_or_manual)))
            await ctx.send('ERROR: Please enter RPCS3 or PS3', delete_after=10)
            await ctx.message.delete()
            return


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
        await ctx.send('Set Role Reaction Monitor Message to %r' % Current_RR_Message_ID, delete_after=10)
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

#---- Functions 
def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)
    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True
    return check

def old_code_just_to_keep_clean_view():
    ##---- Normal User Commands
    #@bot.command(name='privateserver', help='Answer Question Relating to Private Server')
    #async def Archstones_privateserver(ctx):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        embedVar = discord.Embed(title="The Archstones Private Server", description="The Archstones was established back in Feb 2018. Currently the most active server for Demon's Souls on PS3 & RPCS3. Please visit https://thearchstones.com for more information.", color=0x6928D4)
    #        embedVar.add_field(name="Getting Started", value="Visit #northern-outskirts and set your role thats applicable to your version of Demon's Souls.", inline=False)
    #        embedVar.add_field(name="How to Connect", value="Please visit the #private-server channel for information on how to connect.", inline=False)
    #        await ctx.send(embed=embedVar, delete_after=35)
    #        await ctx.message.delete()

    #@bot.command(name='ps3', help='Answer Question Relating to PS3')
    #async def Archstones_ps3(ctx):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        embedVar = discord.Embed(title="PS3 Setup", description="", color=0x6928D4)
    #        embedVar.add_field(name="Getting Started", value="Visit #northern-outskirts and set your role thats applicable to your version of Demon's Souls.", inline=False)
    #        embedVar.add_field(name="How to Connect", value="1.   Go to Network PS3 Settings > Internet Connection Settings. \n 2.    Here, press 'Custom' and 'Enter Manually'. \n 3.    Change your Primary DNS to 142.93.245.186", inline=False)
    #        await ctx.send(embed=embedVar, delete_after=35)
    #        await ctx.message.delete()

    #@bot.command(name='patreon', help='')
    #async def Archstones_Patreon(ctx):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        embed=discord.Embed(title="The Archstones Patreon", url="https://www.patreon.com/TheArchstones", color=0xa600ff)
    #        await ctx.send(embed=embed, delete_after=35)
    #        await ctx.message.delete()

    #@bot.command(name='online-na', help='Shows North America Online Users')
    #async def Archstones_OnlineUsersNA(ctx):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        save_path_na = "MapNA_Count.txt"
    #        file = wget.download('https://thearchstones.com/MapNA_Count.txt', save_path_na)
    #        if os.path.exists(save_path_na):
    #            shutil.move(file,save_path_na)
        

    #        embedVar = discord.Embed(title="The Archstones - Online Users", description="", color=0x6928D4)
    #        embedVar.add_field(name="PS3", value="North America", inline=False)
    #        with open(save_path_na, 'r') as lines:
    #            for line in lines:
    #                a,b,c,online,area = line.split(' ', 4)
    #                embedVar.add_field(name=area, value=online, inline=True)

    #        embedVar.set_footer(text="Visit https://thearchstones.com/onlineusers for more information", icon_url = ctx.author.avatar_url)

    #        await ctx.send(embed=embedVar, delete_after=35)
    #        await ctx.message.delete()

    #@bot.command(name='online-eu', help='Shows Europe Online Users')
    #async def Archstones_OnlineUsersEU(ctx):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        save_path_eu = "MapEU_Count.txt"
    #        file = wget.download('https://thearchstones.com/MapEU_Count.txt', save_path_eu)
    #        if os.path.exists(save_path_eu):
    #            shutil.move(file,save_path_eu)

    #        embedVar = discord.Embed(title="The Archstones - Online Users", description="", color=0x6928D4)
    #        embedVar.add_field(name = chr(173), value = chr(173), inline=False)
    #        embedVar.add_field(name="PS3", value="Europe", inline=False)
    #        with open(save_path_eu, 'r') as lines:
    #            for line in lines:
    #                a,b,c,online,area = line.split(' ', 4)
    #                embedVar.add_field(name=area, value=online, inline=True)

    #        embedVar.set_footer(text="Visit https://thearchstones.com/onlineusers for more information", icon_url = ctx.author.avatar_url)

    #        await ctx.send(embed=embedVar, delete_after=35)
    #        await ctx.message.delete()

    #@bot.command(name='online-as', help='Shows Asia Online Users')
    #async def Archstones_OnlineUsersAS(ctx):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        save_path_jp = "MapJP_Count.txt"
    #        file = wget.download('https://thearchstones.com/MapJP_Count.txt', save_path_jp)
    #        if os.path.exists(save_path_jp):
    #            shutil.move(file,save_path_jp)
        

    #        embedVar = discord.Embed(title="The Archstones - Online Users", description="", color=0x6928D4)
    #        embedVar.add_field(name="PS3", value="Asia", inline=False)
    #        with open(save_path_jp, 'r') as lines:
    #            for line in lines:
    #                a,b,c,online,area = line.split(' ', 4)
    #                embedVar.add_field(name=area, value=online, inline=True)

    #        embedVar.set_footer(text="Visit https://thearchstones.com/onlineusers for more information", icon_url = ctx.author.avatar_url)

    #        await ctx.send(embed=embedVar, delete_after=35)
    #        await ctx.message.delete()

    #@bot.command(name='online-rpcs3', help='Shows rpcs3 Online Users')
    #async def Archstones_OnlineUsersCR(ctx):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        save_path_cr = "MapCR_Count.txt"
    #        file = wget.download('https://rpcs3.thearchstones.com/MapCR_Count.txt', save_path_cr)
    #        if os.path.exists(save_path_cr):
    #            shutil.move(file,save_path_cr)
        

    #        embedVar = discord.Embed(title="The Archstones - Online Users", description="", color=0x6928D4)
    #        embedVar.add_field(name="RPCS3", value="Cross Region", inline=False)
    #        with open(save_path_cr, 'r') as lines:
    #            for line in lines:
    #                a,b,c,online,area = line.split(' ', 4)
    #                embedVar.add_field(name=area, value=online, inline=True)

    #        embedVar.set_footer(text="Visit https://thearchstones.com/onlineusers for more information", icon_url = ctx.author.avatar_url)

    #        await ctx.send(embed=embedVar, delete_after=35)
    #        await ctx.message.delete()

    #@bot.command(name='worldtendency', help='Shows World Tendency')
    #async def Archstones_worldtendency(ctx):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        save_path_ps3 = "ps3GTValue.txt"
    #        save_path_rpcs3 = "rpcs3GTValue.txt"
    #        file = wget.download('https://thearchstones.com/GTValue.txt', save_path_ps3)
    #        if os.path.exists(save_path_ps3):
    #            shutil.move(file,save_path_ps3)

    #        file2 = wget.download('https://rpcs3.thearchstones.com/GTValue.txt', save_path_rpcs3)
    #        if os.path.exists(save_path_rpcs3):
    #            shutil.move(file2,save_path_rpcs3)
        
    #        embedVar = discord.Embed(title="The Archstones - Current Global World Tendency", description="", color=0x6928D4)

    #        with open(save_path_ps3) as f:
    #            lines = f.readlines()
    #            embedVar.add_field(name="PS3", value=lines[0], inline=False)
    #        with open(save_path_rpcs3) as f:
    #            lines = f.readlines()
    #            embedVar.add_field(name="RPCS3", value=lines[0], inline=False)

    #        await ctx.send(embed=embedVar, delete_after=35)
    #        await ctx.message.delete()

    #@bot.command(name='sl1', help='Answer Question Relating to SL1 run')
    #async def Archstones_slq(ctx):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        embedVar = discord.Embed(title="SL1 Guidelines", url="https://bigsoundlogan.github.io/Demon-s-Souls-SL1-Repository/", description="A comprehensive and community-supported repository on how the Demon's Souls Discord server manages SL1 runs and their numerous challenge variations. Maintained by Sen#1775 \n \n https://bigsoundlogan.github.io/Demon-s-Souls-SL1-Repository/")
    #        await ctx.send(embed=embedVar, delete_after=35)
    #        await ctx.message.delete()

    #@bot.command(name='troubleshoot', help='Answer Question for troubleshooting')
    #async def Archstones_slq(ctx):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        embedVar=discord.Embed(title="Troubleshoot Connection", url="https://discord.com/channels/245489122892840961/564301616283385856", description="Will help give you an idea about why you might not be able to connect to The Archstones. Use the message you get when attempting to connect to find a potential solution below.", color=0x29c758)
    #        embedVar.set_author(name="The Archstones", url="https://Thearchstones.com")
    #        embedVar.add_field(name="Cannot connect to the Demon's Souls server", value="**PS3** \n 1. Please verify you have the set your **Primary DNS to 142.93.245.186** \n 2. Try creating a hotspot with your phone and connect your PS3 to that, ensure you still set the Primary DNS as stated above. Sometimes the issues can be your ISP that is blocking custom DNS servers. \n **RPCS3** \n 1. Ensure you have set your IP/Host Switch, Created your RPCN account, and Set your token in the configuration. \n If you still continue to have issue, feel free to reach out, we will try to assist where possible. ", inline=False)
    #        embedVar.add_field(name="The Demon's Souls Online Service has been terminated", value="Normally this represents two things, Either you have not set your DNS properly for PS3, IP/Host Switch for RPCS3, or somewhere between your connection and the internet your network is not receiving the right domain name to connect. Please ensure you have set your DNS / IP/Host Switch, If you have issues still please contact the mod team we have a solution for you.", inline=True)
    #        embedVar.add_field(name="Archstones Patcher", value="If you continue to experience issues, you might want to try the patcher which will help resolve DNS related issues. You can find this at  https://github.com/Yuvi-App/Archstones-Patcher/releases", inline=True)
    #        embedVar.set_footer(text="visit #private-server for more detailed information", icon_url = ctx.author.avatar_url)
    #        await ctx.send(embed=embedVar, delete_after=35)
    #        await ctx.message.delete()
                



    ##---- Archstones/Discord Intergration User Commands
    ##@bot.command(name='linkaccount', help='Links PSN/RPCS3 Account to Discord Account')
    ##async def Archstones_privateserver(ctx, VERSION, PSN_NAME):
    ##    if ctx.guild.name != GUILD:
    ##        await ctx.message.delete()
    ##        return
    ##    if ctx.guild.name == GUILD:
    ##        timenow = datetime.datetime.now()
    ##        PSN_NAME += "0"
    ##        DISCORD_NAME = ctx.message.author
    ##        VERSION = VERSION.upper()

    ##        #Ensure RPCS3 or PS3 is Entered
    ##        if VERSION == "RPCS3" or VERSION == "PS3":
    ##            #Check if account exist
    ##            row = conn.execute("select count(*) from linkedaccounts where DISCORD_NAME = ?", (str(DISCORD_NAME),)).fetchone()
    ##            print("Value = %s %s %s %s" % (row, DISCORD_NAME, PSN_NAME, timenow))
       
    ##            if row[0] == 0:
    ##                #Account not Found, Link Accounts in DB
    ##                conn.execute("insert into linkedaccounts(DISCORD_NAME, PSN_NAME, VERSION, DATE_TIME) VALUES (?,?,?,?)", (str(DISCORD_NAME),str(PSN_NAME),str(VERSION),str(timenow)))
    ##                conn.commit()
    ##                print("Linked Account %s to %s for %s" % (DISCORD_NAME,PSN_NAME,VERSION))


    ##                await ctx.send('Linked Account Success!', delete_after=30)
    ##                await ctx.message.delete()

    ##            elif row[0] >= 1:
    ##                #Acccount Found, Leave Function since its linked
    ##                await ctx.send('Account Already Linked!', delete_after=30)
    ##                await ctx.message.delete()
    ##                return
    ##        else:
    ##            #Incorrect Version entered
    ##            await ctx.send('Please enter RPCS3 or PS3!', delete_after=30)
    ##            await ctx.message.delete()
    ##            return

    #@bot.command(name='link', help='Links PSN/RPCS3 Account to Discord Account')
    #async def Archstones_privateserver(ctx):
    #    if ctx.guild.name != GUILD:
    #        await ctx.message.delete()
    #        return
    #    if ctx.guild.name == GUILD:
    #        await ctx.message.delete()
    #        DISCORD_NAME = ctx.message.author
    #        timenow = datetime.datetime.now()

    #        #DM Users to Setup the Link process
    #        await ctx.author.send("Link Account for PS3 or RPCS3?")
    #        response = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel), timeout=120)
    #        VERSION = response.content.upper()
        
    #        #Ensure RPCS3 or PS3 is Entered
    #        if VERSION == "RPCS3":
    #            #Get RPCN Name
    #            await ctx.author.send("Please enter your RPCN Username")
    #            response2 = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel), timeout=120)
    #            PSN_NAME = response2.content
    #            PSN_NAME += "0"
    #            print("Verify - Discord User %s, PSN User %s, Version %s" % (DISCORD_NAME, PSN_NAME, VERSION))

    #            #Check if account exist for RPCS3
    #            row = conn.execute("select count(*) from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"RPCS3")).fetchone()
    #            print("Value = %s %s %s %s" % (row, DISCORD_NAME, PSN_NAME, timenow))
       
    #            if row[0] == 0:
    #                #Account not Found, Link Accounts in DB
    #                conn.execute("insert into linkedaccounts(DISCORD_NAME, PSN_NAME, VERSION, DATE_TIME) VALUES (?,?,?,?)", (str(DISCORD_NAME),str(PSN_NAME),str(VERSION),str(timenow)))
    #                conn.commit()
    #                print("Linked Account %s to %s for %s" % (DISCORD_NAME,PSN_NAME,VERSION))
    #                await ctx.author.send('Linked Account Success!')

    #            elif row[0] >= 1:
    #                #Acccount Found, Leave Function since its linked
    #                await ctx.author.send('RPCN Account Already Linked!')
    #                return
    #        elif VERSION == "PS3":
    #            #Get PSN Name
    #            await ctx.author.send("Please enter your PSN Username")
    #            response2 = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel), timeout=120)
    #            PSN_NAME = response2.content
    #            PSN_NAME += "0"
    #            print("Verify - Discord User %s, PSN User %s, Version %s" % (DISCORD_NAME, PSN_NAME, VERSION))

    #            #Check if account exist for PS3
    #            row = conn.execute("select count(*) from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"PS3")).fetchone()
    #            print("Value = %s %s %s %s" % (row, DISCORD_NAME, PSN_NAME, timenow))
       
    #            if row[0] == 0:
    #                #Account not Found, Link Accounts in DB
    #                conn.execute("insert into linkedaccounts(DISCORD_NAME, PSN_NAME, VERSION, DATE_TIME) VALUES (?,?,?,?)", (str(DISCORD_NAME),str(PSN_NAME),str(VERSION),str(timenow)))
    #                conn.commit()
    #                print("Linked Account %s to %s for %s" % (DISCORD_NAME,PSN_NAME,VERSION))
    #                await ctx.author.send('Linked Account Success!')

    #            elif row[0] >= 1:
    #                #Acccount Found, Leave Function since its linked
    #                await ctx.author.send('PS3 Account Already Linked!')
    #                return
    #        else:
    #            #Incorrect Version entered
    #            await ctx.author.send('Please enter RPCS3 or PS3')
    #            return

    #@bot.command(name='changewt', help='Changes World Tendency for your PSN Account')
    #async def Archstones_privateserver(ctx, VERSION, desired_tendency):
    #    if ctx.guild.name != GUILD:
    #        await ctx.message.delete()
    #        return
    #    if ctx.guild.name == GUILD:
    #        DISCORD_NAME = ctx.message.author

    #        #Sanitize Input for INT Value
    #        try:
    #            desired_tendency = int(desired_tendency)
    #            VERSION = VERSION.upper()
    #            if -200 <= desired_tendency <= 200:
    #                #Check What Version
    #                if VERSION == "RPCS3":
    #                    #Check if account exist 
    #                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"RPCS3")).fetchone()[0]
    #                    PSN_NAME = row
    #                    if PSN_NAME is None:
    #                        print("WT Command - %s account not linked" % (DISCORD_NAME))
    #                        await ctx.send('Account Not Link!', delete_after=30)
    #                        await ctx.send('Please link using "!linkaccount PSN-NAME" before setting World Tendency', delete_after=30)
    #                        await ctx.message.delete()
    #                        return
    #                    elif PSN_NAME is not None:
    #                        conn2.execute("update players set desired_tendency = ? where characterID = ?", (desired_tendency, str(PSN_NAME),))
    #                        conn2.commit()
    #                        print("WT Command - %s Discord Account, %s PSN Account, changed WT to %s, Version %s" % (DISCORD_NAME,PSN_NAME,str(desired_tendency), VERSION))
    #                        await ctx.send('SUCCESS: Changed World Tendency to %s!' % str(desired_tendency), delete_after=30)
    #                        #await ctx.message.delete()
    #                    else:
    #                        await ctx.message.delete()
    #                        return
    #                elif VERSION == "PS3":
    #                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"PS3")).fetchone()[0]
    #                    PSN_NAME = row
    #                    if PSN_NAME is None:
    #                        print("WT Command - %s account not linked" % (DISCORD_NAME))
    #                        await ctx.send('Account Not Link!', delete_after=30)
    #                        await ctx.send('Please link using "!linkaccount PSN-NAME" before setting World Tendency', delete_after=30)
    #                        await ctx.message.delete()
    #                        return
    #                    elif PSN_NAME is not None:
    #                        PSN_NAME = row
    #                        conn3.execute("update players set desired_tendency = ? where characterID = ?", (desired_tendency, str(PSN_NAME),))
    #                        conn3.commit()
    #                        print("WT Command - %s Discord Account, %s PSN Account, changed WT to %s, Version %s" % (DISCORD_NAME,PSN_NAME,str(desired_tendency), VERSION))
    #                        await ctx.send('SUCCESS: Changed World Tendency to %s!' % str(desired_tendency), delete_after=30)
    #                        #await ctx.message.delete()
    #                    else:
    #                        await ctx.message.delete()
    #                        return
    #                else:
    #                    print("WT Command - %s account Invalid Version entered %s" % (DISCORD_NAME, str(VERSION)))
    #                    await ctx.message.delete()
    #                    return
    #            else:
    #                print("WT Command - %s User, Wrong Input Value %s" % (DISCORD_NAME,str(desired_tendency)))
    #                await ctx.send('ERROR: Enter a Value between -200 & 200!', delete_after=30)
    #                await ctx.message.delete()
    #        except:
    #            print("WT Command - %s User, Failed to Sanitize Value %s" % (DISCORD_NAME,str(desired_tendency)))
    #            await ctx.send('ERROR: Please link your Account first', delete_after=30)
    #            await ctx.message.delete()
    #            return

    #@bot.command(name='gtmt', help='Changes between Global and Manual Tendency')
    #async def Archstones_privateserver(ctx, VERSION, global_or_manual):
    #    if ctx.guild.name != GUILD:
    #        await ctx.message.delete()
    #        return
    #    if ctx.guild.name == GUILD:
    #        DISCORD_NAME = ctx.message.author
    #        global_or_manual = global_or_manual.upper()
    #        VERSION = VERSION.upper()

    #        #Sanitize Version Input
    #        if VERSION == "RPCS3":
    #            #Sanitize Input
    #            if global_or_manual == "GLOBAL":
    #                GlobalTendency = 0
    #                try:
    #                    #Get PSNNAME
    #                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"RPCS3")).fetchone()[0]
    #                    PSN_NAME = row

    #                    #Set Global Tendency
    #                    conn2.execute("update players set enable_manual_tendency = ? where characterID = ?", (GlobalTendency, str(PSN_NAME),))
    #                    conn2.commit()

    #                    print("GT_MT Command - %s User, Enabled Global Tendency %s" % (DISCORD_NAME,str(global_or_manual)))
    #                    await ctx.send('SUCCESS: Enabled Global Tendency', delete_after=30)
    #                    #await ctx.message.delete()
    #                except:
    #                    print("GT_MT Command - %s account not linked" % (DISCORD_NAME))
    #                    await ctx.send('Account Not Link!', delete_after=30)
    #                    await ctx.send('Please link using "!linkaccount PSN-NAME"', delete_after=30)
    #                    await ctx.message.delete()
    #                    return


    #            elif global_or_manual == "MANUAL":
    #                ManualTendency = 1
    #                try:
    #                    #Get PSNNAME
    #                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"RPCS3")).fetchone()[0]
    #                    PSN_NAME = row

    #                    #Set Manual Tendency
    #                    conn2.execute("update players set enable_manual_tendency = ? where characterID = ?", (ManualTendency, str(PSN_NAME),))
    #                    conn2.commit()

    #                    print("GT_MT Command - %s User, Enabled Manual Tendency %s" % (DISCORD_NAME,str(global_or_manual)))
    #                    await ctx.send('SUCCESS: Enabled Manual Tendency', delete_after=30)
    #                    #await ctx.message.delete()
    #                except:
    #                    print("GT_MT Command - %s account not linked" % (DISCORD_NAME))
    #                    await ctx.send('Account Not Link!', delete_after=30)
    #                    await ctx.send('Please link using "!linkaccount PSN-NAME"', delete_after=30)
    #                    await ctx.message.delete()
    #                    return
    #            else:
    #                print("GT_MT Command - %s User, Failed to Sanitize Global/MT Value %s" % (DISCORD_NAME,str(global_or_manual)))
    #                await ctx.send('ERROR: Please enter GLOBAL or CUSTOM', delete_after=30)
    #                await ctx.message.delete()
    #                return

    #        elif VERSION == "PS3":
    #            #Sanitize Input
    #            if global_or_manual == "GLOBAL":
    #                GlobalTendency = 0
    #                try:
    #                    #Get PSNNAME
    #                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"PS3")).fetchone()[0]
    #                    PSN_NAME = row

    #                    #Set Global Tendency
    #                    conn3.execute("update players set enable_manual_tendency = ? where characterID = ?", (GlobalTendency, str(PSN_NAME),))
    #                    conn3.commit()

    #                    print("GT_MT Command - %s User, Enabled Global Tendency %s" % (DISCORD_NAME,str(global_or_manual)))
    #                    await ctx.send('SUCCESS: Enabled Global Tendency', delete_after=30)
    #                    #await ctx.message.delete()

    #                except:
    #                    print("GT_MT Command - %s account not linked" % (DISCORD_NAME))
    #                    await ctx.send('Account Not Link!', delete_after=30)
    #                    await ctx.send('Please link using "!linkaccount PSN-NAME"', delete_after=30)
    #                    await ctx.message.delete()
    #                    return

    #            elif global_or_manual == "MANUAL":
    #                ManualTendency = 1
    #                try:
    #                    #Get PSNNAME
    #                    row = conn.execute("select PSN_NAME from linkedaccounts where DISCORD_NAME = ? AND VERSION = ?", (str(DISCORD_NAME),"PS3")).fetchone()[0]
    #                    PSN_NAME = row

    #                    #Set Manual Tendency
    #                    conn3.execute("update players set enable_manual_tendency = ? where characterID = ?", (ManualTendency, str(PSN_NAME),))
    #                    conn3.commit()

    #                    print("GT_MT Command - %s User, Enabled Manual Tendency %s" % (DISCORD_NAME,str(global_or_manual)))
    #                    await ctx.send('SUCCESS: Enabled Manual Tendency', delete_after=30)
    #                    #await ctx.message.delete()
    #                except:
    #                    print("GT_MT Command - %s account not linked" % (DISCORD_NAME))
    #                    await ctx.send('Account Not Link!', delete_after=30)
    #                    await ctx.send('Please link using "!linkaccount PSN-NAME"', delete_after=30)
    #                    await ctx.message.delete()
    #                    return

    #            else:
    #                print("GT_MT Command - %s User, Failed to Sanitize Global/MT Value %s" % (DISCORD_NAME,str(global_or_manual)))
    #                await ctx.send('ERROR: Please enter GLOBAL or CUSTOM', delete_after=30)
    #                await ctx.message.delete()
    #                return
    #        else:
    #            Print("GT_MT Command - %s User, Failed to Sanitize Version Value %s" % (DISCORD_NAME,str(global_or_manual)))
    #            await ctx.send('ERROR: Please enter RPCS3 or PS3', delete_after=30)
    #            await ctx.message.delete()
    #            return

        
    ##---- Admin Archstones Discord Intergration Commands
    #@bot.command(name='unlink', help='Unlinks Discord Users PSN Account')
    #@commands.has_any_role(Server_Admin_Role, Server_Host_Role)
    #async def Archstones_RR(ctx, VERSION, DISCORD_NAME):
    #    if ctx.guild.name != GUILD:
    #        return
    #    if ctx.guild.name == GUILD:
    #        VERSION = VERSION.upper()
    #        if VERSION == "RPCS3":
    #            conn.execute("DELETE FROM linkedaccounts WHERE VERSION = ? AND DISCORD_NAME = ?", ("RPCS3", str(DISCORD_NAME)))
    #            conn.commit()
    #            print("Unlink Command - %s Admin, Unlinked User %s" % (str(ctx.message.author),str(DISCORD_NAME)))
    #            await ctx.send('SUCCESS: Unlinked User %s' % str(DISCORD_NAME), delete_after=30)
    #            await ctx.message.delete()
    #        elif VERSION == "PS3":
    #            conn.execute("DELETE FROM linkedaccounts WHERE VERSION = ? AND DISCORD_NAME = ?", ("PS3", str(DISCORD_NAME)))
    #            conn.commit()
    #            print("Unlink Command - %s Admin, Unlinked User %s" % (str(ctx.message.author),str(DISCORD_NAME)))
    #            await ctx.send('SUCCESS: Unlinked User %s' % str(DISCORD_NAME), delete_after=30)
    #            await ctx.message.delete()
    #        else:
    #            Print("Unlink Command - %s Admin, Failed to Sanitize Version Value %s" % (str(ctx.message.author),str(global_or_manual)))
    #            await ctx.send('ERROR: Please enter RPCS3 or PS3', delete_after=30)
    #            await ctx.message.delete()
    #            return
    return

bot.run(TOKEN)