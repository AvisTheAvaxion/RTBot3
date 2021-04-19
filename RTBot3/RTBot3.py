import discord
from discord.ext import commands
import rtFuncs
import jonFuncs
import os
import time
import re
from mcstatus import MinecraftServer




global devMode
devMode = False


staff = {
  457954086667550751: "Jon",
  474020409113706521: "Qwerty",
  743515744045629441: "Hex",
  725124517642633286: "Cash",
  722884741552013414: "Comic",
  763234934386327575: "Backward",
  472803710632984576: "Carmilla",
  121022640298131457: "Tdubs",
  #364905148083994626: "Avis",
}


intents = discord.Intents.default()
intents.members = True

version = "A3.0.5"

client = commands.Bot(command_prefix="rt!", help_command=None,  intents=intents)

@client.event
async def on_ready():
    activity = discord.Game(name=f" with redstone |rt!help |{version}")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Red Tech Bot is ready!")

@client.event
async def on_member_join(member):
  joinChannel = await client.fetch_channel(rtFuncs.joinMessageChannel)
  logChannel = await client.fetch_channel(rtFuncs.logMessageChannel)
  embed = discord.Embed(title= f"{member.name} Joined!", description= f"{member.name} joined the server!", colour= discord.colour.Color.green())
  embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
  embed.set_thumbnail(url= member.avatar_url)
  await joinChannel.send(embed= embed)
  await logChannel.send(embed= embed)

  embed = discord.Embed(title= f"Welcome to Red Tech {member.name}!", description= f"Please enjoy your stay, be sure to follow the rules in {rtFuncs.rulesChannel}. If you have any questions or concerns, don't be afraid to ask staff!", colour= discord.colour.Color.green())
  await member.send(embed= embed)
  guild = await client.fetch_guild(rtFuncs.rtServer)
  memberRole = guild.get_role(rtFuncs.memberRoleId)
  await member.add_roles(memberRole)





  f = open("AvisServer/Bots/JonBots/RTBot3/RTMutelist.txt", "r+")
  alreadyMuted = False
  
  guild = await client.fetch_guild(rtFuncs.rtServer)
  mutedRole = guild.get_role(rtFuncs.muteRoleId)

        
  for line in f:
    if str(member.id) in line:
      alreadyMuted = True
        
  if alreadyMuted == True:
    embed=discord.Embed(title="[Notice]", description="It appears you were muted when you left the server, you have been re-muted. If this is a mistake, please let a staff member know.", colour= discord.colour.Colour.orange())
    await member.send(embed= embed)
    await member.add_roles(mutedRole)
    
  f.close()

@client.event
async def on_member_remove(member):
  joinChannel = await client.fetch_channel(rtFuncs.joinMessageChannel)
  logChannel = await client.fetch_channel(rtFuncs.logMessageChannel)
  embed = discord.Embed(title= f"{member.name} Left!", description= f"{member.name} left the server!", colour= discord.colour.Color.red())
  embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
  embed.set_thumbnail(url= member.avatar_url)
  await joinChannel.send(embed= embed)
  await logChannel.send(embed= embed)


@client.command()
async def shutdown(ctx):
  embed = discord.Embed(title= "⚠️ Warning: Shutdown Command ⚠️", description= "Please wait: Verifying credentials", colour= discord.colour.Color.orange())
  msg = await ctx.send(embed= embed)
  time.sleep(5)

  if ctx.message.author.id in staff:
    avis = await client.fetch_user(364905148083994626)
    await avis.send(f"Red Tech Bot was shut down by {ctx.message.author}")
    embed = discord.Embed(title= "⚠️ Warning: Shutdown Command ⚠️", description= f"Creditionals verified ({ctx.message.author.name}) : Commencing shutdown!", colour= discord.colour.Colour.orange())
    await msg.edit(embed= embed)
    logChannel = await client.fetch_channel(rtFuncs.logMessageChannel)
    await logChannel.send(embed= embed)
    await ctx.message.add_reaction("✅")
    await client.close()
    print(f"Red Tech bot Shutdown confirmed by {ctx.message.author}!")

  else:
    embed = discord.Embed(title= "⚠️ Warning: Shutdown Command ⚠️", description= "Invalid creditials: Aborting shutdown!", colour= discord.colour.Colour.orange())
    await msg.edit(embed= embed)
    await ctx.message.add_reaction("❌")
    
@client.command()
async def ping(ctx):
  tic = time.perf_counter()
  latency = client.latency
  msg = await ctx.channel.send("*Computing Latency*")
  toc = time.perf_counter()
  await msg.edit(content= f"Pong: {round(latency * 1000)}ms | {(toc - tic) * 1000:0.0f}ms")

@client.command()
async def profile(ctx):
  try:
    user = ctx.message.mentions[0]
    userid = user.id
  except IndexError:
    user = ctx.message.author
    userid = user.id
    
    try:
      userid = ctx.message.content.strip("rt!profile ")
      userid = int(userid)
      user = await client.fetch_user(userid)
       
    except ValueError:
      user = ctx.message.author
      userid = user.id
    
    except discord.errors.NotFound:
      await ctx.send("No account found. If you belive this is a mistake please contact a Red Tech Administrator.")
      return ""    
    
        
  f = open("AvisServer/Bots/JonBots/RTBot3/RTLogs.txt", "r")
  accountFound = False

  for line in f:
    if str(user.id) in line:
      line = line.replace("-", "")
      line = line.replace("$", "-")
      line_content = line.split(" ")
      clearance_level = line_content[2]
      position = line_content[3].replace("_", " ")
      ign = line_content[4]
      accountFound = True
  f.close()
      
      
  if accountFound == True:
    embed = discord.Embed(title= user.name, description= "IGN: " + ign, colour= discord.colour.Color.red())
    embed.set_author(name= "Red Tech™ Official Keycard", icon_url= rtFuncs.rtlogo)
    embed.set_thumbnail(url= user.avatar_url)
    embed.add_field(name= f"Clearance Level: {clearance_level}", value= "_ _", inline= True)
    embed.add_field(name= f"Position: {position}", value= "_ _", inline= True)
    embed.set_footer(text= "Property of Red Tech, Do not redistribute")
      
    await ctx.send(embed= embed)
        
  else:
    await ctx.send("No account found. If you belive this is a mistake please contact a Red Tech Administrator.")

@client.command()
async def dj(ctx):
  await ctx.send("Fetching server info, please wait...")
  server = MinecraftServer.lookup("minecraft.digitaljesuit.com:25565")

  status = server.status()
  
  embed = discord.Embed(title= "Digital Jesuit", description= "Info about Digital Jesuit", colour= discord.colour.Color.blue())
  embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
  embed.set_thumbnail(url= "https://cdn.discordapp.com/icons/546412536522735629/dde78cbf87e204472d40b416df64cfbd.png?size=2048")
  embed.add_field(name= "Players Online", value= status.players.online, inline= True)
  embed.add_field(name= "Ping", value= status.latency, inline= True)
  embed.add_field(name= "Server Address", value= "minecraft.digitaljesuit.com", inline= True)
  embed.add_field(name= "Server Invite Link:", value= jonFuncs.djDisc(), inline= False)
  await ctx.send(embed= embed)

@client.command()
async def twitch(ctx):
 await ctx.send(jonFuncs.twitch())

@client.command(aliases=["rt", "mc", "invite"])
async def redtech(ctx):
  embed = discord.Embed(title= "Red Tech™", description= "Redstone Technologies™", colour= discord.colour.Color.red())
  embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
  embed.add_field(name= "Members", value= ctx.guild.member_count, inline= False)
  embed.add_field(name= "Invite link", value= jonFuncs.rtDisc(), inline= False)
  await ctx.send(embed= embed)

@client.command()
async def aus(ctx):
  await ctx.send(jonFuncs.asDisc())

@client.command()
async def logo(ctx):
  await ctx.send(rtFuncs.rtlogo)

@client.command()
async def help(ctx):
  await ctx.send(embed= rtFuncs.help())

@client.command(aliases=["history"])
async def hist(ctx):
  embeds = rtFuncs.history()
  await ctx.send(embed= embeds[0])
  await ctx.send(embed= embeds[1])

@client.command()
async def bob(ctx):
  await ctx.send(rtFuncs.bob())

@client.command(aliases=["bb"])
async def blackbox(ctx):
  await ctx.send("Attempting to ping Red Tech Blackboxes")
  time.sleep(5)
  await ctx.send(embed= rtFuncs.blackBox())

@client.command()
async def nick(ctx):
  try:
    msg = ctx.message.content
    nickname = msg[7:]
    user = ctx.message.author
    await user.edit(nick= nickname)
    
    if ctx.message.content == "rt!nick clear":
      await user.edit(nick= None)
      embed = discord.Embed(title="Nickname Cleared!", description= "Your nickname has been cleared!", colour= discord.colour.Color.green())
      embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
      msg = await ctx.send(embed= embed)
      time.sleep(3)
      await msg.delete()
      await ctx.message.delete()

    
    else:
      embed = discord.Embed(title="Nickname Changed!", description= f"Your nickname has been changed to {nickname}!", colour= discord.colour.Color.green())
      embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
      msg = await ctx.channel.send(embed= embed)
      time.sleep(3)
      await msg.delete()
      await ctx.message.delete()

  except discord.Forbidden:
    embed = discord.Embed(title="Error", description= "I don't have permission to change your nickname!", colour= discord.colour.Color.red())
    embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
    msg = await ctx.channel.send(embed= embed)

@client.command()
async def kick(ctx):
  try:
      target = ctx.message.mentions[0]

  except IndexError:
    embed = discord.Embed(title= "Error", description= "No member mentioned to kick", colour= discord.colour.Color.red())
    await ctx.send(embed = embed)
    return ""
      
  if ctx.message.author.id == ctx.message.mentions[0].id:
    embed = discord.Embed(title= "Why?", description= "Why are you trying to kick yourself?", colour= discord.colour.Color.blue())
    await ctx.send(embed= embed)
    return ""

  elif ctx.message.author.id not in staff:
    embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red())
    await ctx.send(embed= embed)
    return ""
  
  else:
    msg = ctx.message.content
  
    x = re.search("<@!\d+> ?(.*)", msg)
    if x != None:
      text = f'{target.name} was kicked from the server'
      if x.group(1) == "":
        text += "!"
        reason = "None"
      else:
        text += (" for: " + x.group(1))
        reason = x.group(1)
    
      if target.id in staff:
        embed = discord.Embed(title= "Error", description= "You can't kick other staff", colour= discord.colour.Color.red())
        await ctx.send(embed= embed)

        if target.id == 457954086667550751:
          await ctx.send("https://static.wikia.nocookie.net/24005259-b85f-4770-a051-abadd75daace")
        
      else:
        try:
          await target.kick(reason= reason)
          embed = discord.Embed(title= "Kick Successful!", description= text, colour= discord.colour.Color.green())
          await ctx.send(embed= embed)
          logChannel = await client.fetch_channel(rtFuncs.logMessageChannel)
          await logChannel.send(embed= embed)


        except discord.Forbidden:
          embed = discord.Embed(title= "Error", description= "I don't have permission to kick this person", colour= discord.colour.Color.red())
          await ctx.send(embed= embed)

@client.command()
async def ban(ctx):
  try:
      target = ctx.message.mentions[0]

  except IndexError:
    embed = discord.Embed(title= "Error", description= "No member mentioned to ban", colour= discord.colour.Color.red())
    await ctx.send(embed = embed)
    return ""
      
  if ctx.message.author.id == ctx.message.mentions[0].id:
    embed = discord.Embed(title= "Why?", description= "Why are you trying to ban yourself?", colour= discord.colour.Color.blue())
    await ctx.send(embed= embed)
    return ""

  elif ctx.message.author.id not in staff:
    embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red())
    await ctx.send(embed= embed)
    return ""
  
  else:
    msg = ctx.message.content

    x = re.search("<@!\d+> ?(.*)", msg)
    if x != None:
      text = f'{target.name} was banned from the server'
      if x.group(1) == "":
        text += "!"
        reason = "None"
      else:
        text += (" for: " + x.group(1))
        reason = x.group(1)
    
      if target.id in staff:
        embed = discord.Embed(title= "Error", description= "You can't ban other staff", colour= discord.colour.Color.red())
        await ctx.send(embed= embed)

        if target.id == 457954086667550751:
          await ctx.send("https://static.wikia.nocookie.net/24005259-b85f-4770-a051-abadd75daace")
        
      else:
        try:
          await target.ban(reason= reason)
          embed = discord.Embed(title= "Ban Successful!", description= text, colour= discord.colour.Color.green())
          await ctx.send(embed= embed)
          logChannel = await client.fetch_channel(rtFuncs.logMessageChannel)
          await logChannel.send(embed= embed)

        except discord.Forbidden:
          embed = discord.Embed(title= "Error", description= "I don't have permission to ban this person", colour= discord.colour.Color.red())
          await ctx.send(embed= embed)

@client.command()
async def unban(ctx):
  try:
    if ctx.message.mentions[0].id == ctx.message.author.id:
      embed = discord.Embed(title= "Why?", description= "You aren't even banned?", colour= discord.colour.Color.blue())
      await ctx.send(embed= embed)
  
  except IndexError:
    if ctx.message.author.id not in staff:
      embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red())
      await ctx.send(embed= embed)
    
    else:
      user = await rtFuncs.getUser(ctx, client, "rt!unban")
      if user == None:
        return ""
    
  
      if user == ctx.message.author:
        embed = discord.Embed(title= "Error", description= "No member mentioned to unban", colour= discord.colour.Color.red())
        await ctx.send(embed = embed)
  
      else:
        guild = await client.fetch_guild(rtFuncs.rtServer)
        # Test Account =  475432259055386625

        try:
          await guild.unban(user)
          embed = discord.Embed(title= "Unban Successful!", description= f"{user.name} was unbanned from the server", colour= discord.colour.Color.green())
          await ctx.send(embed= embed)
          logChannel = await client.fetch_channel(rtFuncs.logMessageChannel)
          await logChannel.send(embed= embed)
    
        except discord.Forbidden:
          embed = discord.Embed(title= "Error", description= f"I don't have permission to unban {user.name}!", colour= discord.colour.Color.red())
          await ctx.send(embed= embed)
        
        except discord.NotFound:
          embed = discord.Embed(title= "Error", description= f"{user.name} is not banned", colour= discord.colour.Colour.red())
          await ctx.send(embed= embed)

@client.command(aliases=["purge"])
async def clear(ctx):
  if ctx.message.author.id not in staff:
    embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red())
    await ctx.send(embed= embed)
  
  else:
    amount = ctx.message.content.strip("rt!clear ")
    amount = amount.strip("rt!purge ")
    try:
      amount = int(amount)
      await ctx.message.delete()
      await ctx.channel.purge(limit= amount)
      embed = discord.Embed(title= "Purge Successful!", description= f"{amount} messages deleted successfully", colour= discord.colour.Color.green())
      purgeMsg = await ctx.send(embed= embed)
      await purgeMsg.delete(delay= 5)
    
    except ValueError:
      embed = discord.Embed(title= "Error", description= "Invalid number", colour= discord.colour.Color.red())
      await ctx.send(embed= embed)

@client.command()
async def mute(ctx):
  try:
    ctx.message.mentions[0].id

  except IndexError:
    embed = discord.Embed(title= "Error", description= "No member mentioned to mute", colour= discord.colour.Color.red())
    await ctx.send(embed= embed)
    return ""

  if ctx.message.mentions[0].id == ctx.message.author.id:
    embed = discord.Embed(title= "Why?", description= "Why are you trying to mute yourself?", colour= discord.colour.Color.blue())
    await ctx.send(embed= embed)
    return ""

  if ctx.message.author.id not in staff:
    embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red())
    await ctx.send(embed= embed)
  
  else:
    mutedRole = ctx.guild.get_role(rtFuncs.muteRoleId)

    if mutedRole in ctx.message.mentions[0].roles:
      embed = discord.Embed(title= "Error", description= "This person is already muted", colour= discord.colour.Color.red())
      await ctx.send(embed= embed)
    
    else:
      if ctx.message.mentions[0].id in staff:
        embed = discord.Embed(title= "Error", description= "You can't mute other staff", colour= discord.colour.Color.red())
        await ctx.send(embed= embed)
        if ctx.message.mentions[0].id == 457954086667550751:
          await ctx.send("https://static.wikia.nocookie.net/24005259-b85f-4770-a051-abadd75daace")
      
      else:
        f = open("AvisServer/Bots/JonBots/RTBot3/RTMutelist.txt", "r+")
        alreadyMuted = False
        
        for line in f:
          if str(ctx.message.mentions[0].id) in line:
            alreadyMuted = True
        
        if alreadyMuted == True:
          await ctx.message.mentions[0].add_roles(mutedRole)
          embed = discord.Embed(title= "Mute Successful!", description= f"{ctx.message.mentions[0].name} was successfully muted", colour= discord.colour.Color.green())
          await ctx.send(embed= embed)

        
        else:
          await ctx.message.mentions[0].add_roles(mutedRole)
          f.write(f"{ctx.message.mentions[0].id} : {ctx.message.mentions[0]}\n")
          f.close()
          embed = discord.Embed(title= "Mute Successful!", description= f"{ctx.message.mentions[0].name} was successfully muted", colour= discord.colour.Color.green())
          await ctx.send(embed= embed)

@client.command()
async def unmute(ctx):
  try:
    ctx.message.mentions[0].id

  except IndexError:
    embed = discord.Embed(title= "Error", description= "No member mentioned to unmute", colour= discord.colour.Color.red())
    await ctx.send(embed= embed)
    return ""

  if ctx.message.mentions[0].id == ctx.message.author.id:
    embed = discord.Embed(title= "Why?", description= "You aren't even muted?", colour= discord.colour.Color.blue())
    await ctx.send(embed= embed)
    return ""

  if ctx.message.author.id not in staff:
    embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red())
    await ctx.send(embed= embed)
  
  else:
    mutedRole = ctx.guild.get_role(rtFuncs.muteRoleId)
    f = open("AvisServer/Bots/JonBots/RTBot3/RTMutelist.txt", "r+")
    fileContent = f.read()
    f.close()

    fileContent = fileContent.splitlines()
    
    userId = str(ctx.message.mentions[0].id)
    personMuted = False

    i = 0
    for user in fileContent:
      if userId in user:
        popthis = i
        personMuted = True

      i = i + 1

    

    if personMuted == False:
      embed = discord.Embed(title= "Error", description= f"{ctx.message.mentions[0].name} is not muted", colour= discord.colour.Colour.red())
      await ctx.send(embed= embed)
    
    else:
      fileContent.pop(popthis)
      newFileContent = ""
      for i in fileContent:
        newFileContent = newFileContent + i + "\n"
      
      
      await ctx.message.mentions[0].remove_roles(mutedRole)
      f = open("AvisServer/Bots/JonBots/RTBot3/RTMutelist.txt", "w")
      f.write(newFileContent)
      embed = discord.Embed(title= "Unmute Successful!", description= f"{ctx.message.mentions[0].name} was unmuted", colour= discord.colour.Color.green())
      await ctx.send(embed= embed)






@client.command()
async def staffCheck(ctx):
  if devMode == True:
    if ctx.author.id in staff:
      await ctx.send("Staff = True")

    elif ctx.author.id not in staff:
      await ctx.send("Staff = False")
  
    else:
      await ctx.send("Error")



token = os.environ['RTB3Token']
client.run(token)