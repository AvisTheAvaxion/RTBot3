# Comments start with a # and look like this. These explain what's happening

import discord #Discord's Official API for making discord stuff (Bots, Webhooks, ect)
from discord.ext import commands #The Bot stuff in Discord API
import rtFuncs #The rtFuncs.py file
import jonFuncs #The JonFuncs.py file
import os #The OS
import time #A Built in Python time function
import re #Used to search strings
from mcstatus import MinecraftServer #A mojang Api for pinging minecraft servers


#Telling the computer that everyone here is a RT Staff Member (Numbers are each person's Id's)
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

#Bot Startup Stuff
intents = discord.Intents.default()
intents.members = True

version = "A3.0.5"

client = commands.Bot(command_prefix="rt!", help_command=None,  intents=intents)

#Once the Bot is done starting up it does this
@client.event
async def on_ready():
    activity = discord.Game(name=f" with redstone |rt!help |{version}")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Red Tech Bot is ready!")

#When someone joins the server
@client.event
async def on_member_join(member):
  joinChannel = await client.fetch_channel(rtFuncs.joinMessageChannel) #Gets the #join channel
  logChannel = await client.fetch_channel(rtFuncs.logMessageChannel) #Gets the #logs channel
  embed = discord.Embed(title= f"{member.name} Joined!", description= f"{member.name} joined the server!", colour= discord.colour.Color.green()) #Creates a Person joined the server embed
  embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
  embed.set_thumbnail(url= member.avatar_url)
  await joinChannel.send(embed= embed) #Sends the embed in #join channel
  await logChannel.send(embed= embed) #Sends the embed in the #logs channel

  embed = discord.Embed(title= f"Welcome to Red Tech {member.name}!", description= f"Please enjoy your stay, be sure to follow the rules in {rtFuncs.rulesChannel}. If you have any questions or concerns, don't be afraid to ask staff!", colour= discord.colour.Color.green()) #Creates a Welcome to RT embed
  await member.send(embed= embed) #DM's it to the person who joined
  guild = await client.fetch_guild(rtFuncs.rtServer) #Gets the RT Server
  memberRole = guild.get_role(rtFuncs.memberRoleId) #Gets the Member Role from RT Server
  await member.add_roles(memberRole) #Gives it to the person who just joined





  f = open("AvisServer/Bots/JonBots/RTBot3/RTMutelist.txt", "r+") #Opens Mutelist.txt
  alreadyMuted = False
  
  mutedRole = guild.get_role(rtFuncs.muteRoleId) #Gets the muted role

  #Checks the Mutelist to see if the person who joined is trying to evade a mute
  for line in f:
    if str(member.id) in line:
      alreadyMuted = True
        
  if alreadyMuted == True: #If they are on the mute list:
    embed=discord.Embed(title="[Notice]", description="It appears you were muted when you left the server, you have been re-muted. If this is a mistake, please let a staff member know.", colour= discord.colour.Colour.orange()) #Created a embed telling them there muted
    await member.send(embed= embed) #Dm's them the embed
    await member.add_roles(mutedRole) #Gives them the muted role
    
  f.close() #Closes Mutelist.txt

#When someone leaves
@client.event
async def on_member_remove(member):
  joinChannel = await client.fetch_channel(rtFuncs.joinMessageChannel) #Gets the #join channel
  logChannel = await client.fetch_channel(rtFuncs.logMessageChannel) #Gets the #log channel
  embed = discord.Embed(title= f"{member.name} Left!", description= f"{member.name} left the server!", colour= discord.colour.Color.red()) #Makes a person left embed
  embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
  embed.set_thumbnail(url= member.avatar_url)
  await joinChannel.send(embed= embed) #Sends it in the join channel
  await logChannel.send(embed= embed) #Sends it in the log channel


@client.command()
async def shutdown(ctx): #rt!shutdown command
  embed = discord.Embed(title= "⚠️ Warning: Shutdown Command ⚠️", description= "Please wait: Verifying credentials", colour= discord.colour.Color.orange()) #Creates a embed
  msg = await ctx.send(embed= embed) #Sends it
  time.sleep(5) #Waits 5 secs, giving person time to read it

  if ctx.message.author.id in staff:#Checks if person who sent the command is a staff member
    avis = await client.fetch_user(364905148083994626) #Get's Avis's id
    await avis.send(f"Red Tech Bot was shut down by {ctx.message.author}") #Dm's Avis saying who shut down the bot so Avis knows it's broke and needs to be fixed
    embed = discord.Embed(title= "⚠️ Warning: Shutdown Command ⚠️", description= f"Creditionals verified ({ctx.message.author.name}) : Commencing shutdown!", colour= discord.colour.Colour.orange()) #Creates embed
    await msg.edit(embed= embed) #edits the first embed to show the new embed
    logChannel = await client.fetch_channel(rtFuncs.logMessageChannel) #gets log channel
    await logChannel.send(embed= embed) #sends embed in log channel
    await ctx.message.add_reaction("✅") #reply's to rt!shutdown message with ✅
    print(f"Red Tech bot Shutdown confirmed by {ctx.message.author}!") #prints bot shutdown message in console
    await client.close() #shuts down the bot


  else: #if the person isn't a staff member
    embed = discord.Embed(title= "⚠️ Warning: Shutdown Command ⚠️", description= "Invalid creditials: Aborting shutdown!", colour= discord.colour.Colour.orange())
    await msg.edit(embed= embed) #edits original embed to show this one just created
    await ctx.message.add_reaction("❌") #Reacts to rt!shutdown with ❌
    
@client.command()
async def ping(ctx): #ping command
  tic = time.perf_counter() #gets time 1
  latency = client.latency #checks the latency
  msg = await ctx.channel.send("*Computing Latency*") #sends a message
  toc = time.perf_counter() #gets time 2
  await msg.edit(content= f"Pong: {round(latency * 1000)}ms | {(toc - tic) * 1000:0.0f}ms")#edits message with the users ping

@client.command()
async def profile(ctx): #Profile command
  try:
    user = ctx.message.mentions[0] #sets user to the person mentioned in rt!profile
    userid = user.id #sets userid to the person mentioned's id
  except IndexError: #if no one was pinged in rt!profile
    user = ctx.message.author #gets the person who did rt!profile
    userid = user.id #gets the persons id
    
    try: #tries to find an id since no one was mentioned
      userid = ctx.message.content.strip("rt!profile ") #gets rid of rt!profile
      userid = int(userid) #converts id to an integer
      user = await client.fetch_user(userid) #gets the account linked with the id
       
    except ValueError: #if there is no id
      user = ctx.message.author #gets the person who did rt!profile
      userid = user.id #gets there id
    
    except discord.errors.NotFound: #If there is no author or id
      await ctx.send("No account found. If you belive this is a mistake please contact a Red Tech Administrator.") #sends a message saying no account found
      return ""    
    
        
  f = open("AvisServer/Bots/JonBots/RTBot3/RTLogs.txt", "r") #opens RTLogs.txt (clearnce logs)
  accountFound = False

  #checks logs for an id
  for line in f:
    if str(user.id) in line:
      line = line.replace("-", "")
      line = line.replace("$", "-")
      line_content = line.split(" ")
      clearance_level = line_content[2]
      position = line_content[3].replace("_", " ")
      ign = line_content[4]
      accountFound = True
  f.close() #closes the logs
      
      
  if accountFound == True: #if profile is found
    embed = discord.Embed(title= user.name, description= "IGN: " + ign, colour= discord.colour.Color.red()) #creates profile embed
    embed.set_author(name= "Red Tech™ Official Keycard", icon_url= rtFuncs.rtlogo)
    embed.set_thumbnail(url= user.avatar_url)
    embed.add_field(name= f"Clearance Level: {clearance_level}", value= "_ _", inline= True)
    embed.add_field(name= f"Position: {position}", value= "_ _", inline= True)
    embed.set_footer(text= "Property of Red Tech, Do not redistribute")
      
    await ctx.send(embed= embed) #sends profile embed
        
  else: #if no profile is found
    await ctx.send("No account found. If you belive this is a mistake please contact a Red Tech Administrator.")

@client.command()
async def dj(ctx): #dj command
  await ctx.send("Fetching server info, please wait...") #sends pls wait message in discord
  server = MinecraftServer.lookup("minecraft.digitaljesuit.com:25565") #pings Dj

  status = server.status() #gets dj info
  
  embed = discord.Embed(title= "Digital Jesuit", description= "Info about Digital Jesuit", colour= discord.colour.Color.blue()) #creates an embed with dj info
  embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
  embed.set_thumbnail(url= "https://cdn.discordapp.com/icons/546412536522735629/dde78cbf87e204472d40b416df64cfbd.png?size=2048")
  embed.add_field(name= "Players Online", value= status.players.online, inline= True)
  embed.add_field(name= "Ping", value= status.latency, inline= True)
  embed.add_field(name= "Server Address", value= "minecraft.digitaljesuit.com", inline= True)
  embed.add_field(name= "Server Invite Link:", value= jonFuncs.djDisc(), inline= False)
  await ctx.send(embed= embed) #sends embed

@client.command()
async def twitch(ctx): #twitch command
 await ctx.send(jonFuncs.twitch()) #calls twitch function to get a link to jon's twitch, which it sends in discord

@client.command(aliases=["rt", "mc", "invite"]) #sets rt, mc and invites as aliases for the command
async def redtech(ctx): #redtech command
  embed = discord.Embed(title= "Red Tech™", description= "Redstone Technologies™", colour= discord.colour.Color.red()) #creates an embed
  embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
  embed.add_field(name= "Members", value= ctx.guild.member_count, inline= False)
  embed.add_field(name= "Invite link", value= jonFuncs.rtDisc(), inline= False)
  await ctx.send(embed= embed) #sends embed

@client.command()
async def aus(ctx):
  await ctx.send(jonFuncs.asDisc()) #calls asDisc function from jonFuncs to get a link to the Australis discord, which it sends in discord

@client.command()
async def logo(ctx): #logo command
  await ctx.send(rtFuncs.rtlogo) #calls logo function from rtFuncs to get the RT Logo, which it sends in discord

@client.command()
async def help(ctx): #help command
  await ctx.send(embed= rtFuncs.help()) #calls help function from rtFuncs to get the help embed, which it sends in discord

@client.command(aliases=["history"]) #sets history as an alias
async def hist(ctx): #hist command
  embeds = rtFuncs.history() #calls history function from rtFuncs to get 2 embeds explaining the history of Red Tech, which it sends in discord
  await ctx.send(embed= embeds[0]) #send embed 1
  await ctx.send(embed= embeds[1]) #send embed 2

@client.command()
async def bob(ctx): #bob command
  await ctx.send(rtFuncs.bob()) #calls bob function from rtFuncs to get the "bob is just a rumor", which it sends in discord

@client.command(aliases=["bb"])
async def blackbox(ctx): #blackbox command
  await ctx.send("Attempting to ping Red Tech Blackboxes") #sends ping message
  time.sleep(5) #totally pings rt servers, def not sleeping for 5 secs
  await ctx.send(embed= rtFuncs.blackBox()) #calls blackBox function from rtFuncs to get a embed with the black box data, which it sends in discord

@client.command()
async def nick(ctx): #nick command
  try:
    msg = ctx.message.content #saves the rt!nick message
    nickname = msg[7:] #gets rid of the rt!nick part, leaving the nickname
    user = ctx.message.author #gets the person who did rt!nick
    await user.edit(nick= nickname) # changes there nickname to what they put after rt!nick
    
    if ctx.message.content == "rt!nick clear": #if the person wants to clear there nickname
      await user.edit(nick= None) #clears there nick name
      embed = discord.Embed(title="Nickname Cleared!", description= "Your nickname has been cleared!", colour= discord.colour.Color.green()) #makes an embed saying nickname cleared
      embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
      msg = await ctx.send(embed= embed) #sends the embed
      await msg.delete(delay= 3) #waits 3 secs before deleting the embed
      await ctx.message.delete(delay= 3) #waits 3 secs before deleting the rt!nick message

    
    else: #if they didn't clear there nickname
      embed = discord.Embed(title="Nickname Changed!", description= f"Your nickname has been changed to {nickname}!", colour= discord.colour.Color.green()) #makes a embed saying nick changed
      embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
      msg = await ctx.channel.send(embed= embed) #sends the embed
      await msg.delete(delay= 3) #waits 3 secs before deleting the embed
      await ctx.message.delete(delay = 3) #waits 3 secs before deleting the rt!nick message

  except discord.Forbidden: #if the bot doesn't have perms to change someones nickname
    embed = discord.Embed(title="Error", description= "I don't have permission to change your nickname!", colour= discord.colour.Color.red()) #makes an embed saying it doesn't have perms
    embed.set_author(name= "Red Tech™ Bot", icon_url= rtFuncs.rtlogo)
    msg = await ctx.channel.send(embed= embed) #sends the embed

@client.command()
async def kick(ctx): #kick command
  try:
      target = ctx.message.mentions[0] #check to see if someone is mentioned

  except IndexError: #if no one is mentioned
    embed = discord.Embed(title= "Error", description= "No member mentioned to kick", colour= discord.colour.Color.red()) #makes and embed saying no one mentioned to kick
    await ctx.send(embed = embed) #sends embed
    return "" #stops the command
      
  if ctx.message.author.id == ctx.message.mentions[0].id: #if the person is trying to kick themselves
    embed = discord.Embed(title= "Why?", description= "Why are you trying to kick yourself?", colour= discord.colour.Color.blue()) #makes an embed asking why
    await ctx.send(embed= embed) #sends embed
    return "" #stops the command

  elif ctx.message.author.id not in staff: #if the person who did rt!kick isn't a staff member
    embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red()) #makes an embed saying they have to be staff
    await ctx.send(embed= embed) #sends embed
    return "" #stops the command
  
  else: #if the person who did rt!kick is a staff member
    msg = ctx.message.content #gets the rt!kick message

    #splits the mention from the rest of the message to get the reason
    x = re.search("<@!\d+> ?(.*)", msg)
    if x != None:
      text = f'{target.name} was kicked from the server'
      if x.group(1) == "":
        text += "!"
        reason = "None"
      else:
        text += (" for: " + x.group(1))
        reason = x.group(1)
    
      if target.id in staff: #if someone tries to kick a staff
        embed = discord.Embed(title= "Error", description= "You can't kick other staff", colour= discord.colour.Color.red()) #makes an embed saying you can't kick staff
        await ctx.send(embed= embed) #sends the embed

        if target.id == 457954086667550751: #if someone tries to kick Jon
          await ctx.send("https://static.wikia.nocookie.net/24005259-b85f-4770-a051-abadd75daace") #sends an image saying "So you have chosen death"
        
      else: #if the person getting kicked isn't a staff
        try:
          await target.kick(reason= reason) #kick the user
          embed = discord.Embed(title= "Kick Successful!", description= text, colour= discord.colour.Color.green()) #make an embed saying the person was kicked
          await ctx.send(embed= embed) #send embed
          logChannel = await client.fetch_channel(rtFuncs.logMessageChannel) #get log channel
          await logChannel.send(embed= embed) #send embed in log channel


        except discord.Forbidden: #if the bot doesn't have kick perms
          embed = discord.Embed(title= "Error", description= "I don't have permission to kick this person", colour= discord.colour.Color.red()) #make an embed saying it doesn't have perms
          await ctx.send(embed= embed) #send embed

@client.command()
async def ban(ctx): #ban command
  try:
      target = ctx.message.mentions[0] #check if someone was mentioned

  except IndexError: #if no one was mentioned
    embed = discord.Embed(title= "Error", description= "No member mentioned to ban", colour= discord.colour.Color.red()) #make an embed saying no one was mentioned
    await ctx.send(embed = embed) #send embed
    return "" #stop command
      
  if ctx.message.author.id == ctx.message.mentions[0].id: #if someone tried to ban themselves
    embed = discord.Embed(title= "Why?", description= "Why are you trying to ban yourself?", colour= discord.colour.Color.blue()) #make an embed asking why
    await ctx.send(embed= embed) #send embed
    return "" #stop command

  elif ctx.message.author.id not in staff: #if person who did rt!kick isn't a staff
    embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red()) #make an embed saying they must be staff
    await ctx.send(embed= embed) #send embed
    return "" #stop command
  
  else: #if the person who did rt!ban is a staff
    msg = ctx.message.content
    
    #splits the mention from the rest of the message to get the reason

    x = re.search("<@!\d+> ?(.*)", msg)
    if x != None:
      text = f'{target.name} was banned from the server'
      if x.group(1) == "":
        text += "!"
        reason = "None"
      else:
        text += (" for: " + x.group(1))
        reason = x.group(1)
    
      if target.id in staff: #if someone tries to ban a staff member
        embed = discord.Embed(title= "Error", description= "You can't ban other staff", colour= discord.colour.Color.red()) #make an embed saying you can't ban staff
        await ctx.send(embed= embed) #send embed

        if target.id == 457954086667550751: #if someone tries to ban Jon
          await ctx.send("https://static.wikia.nocookie.net/24005259-b85f-4770-a051-abadd75daace") #so you have chosen death
        
      else: #if the person getting banned isn't staff
        try:
          await target.ban(reason= reason) #ban the person
          embed = discord.Embed(title= "Ban Successful!", description= text, colour= discord.colour.Color.green()) #make an embed saying ban succesfull
          await ctx.send(embed= embed) #send embed
          logChannel = await client.fetch_channel(rtFuncs.logMessageChannel) #get log channel
          await logChannel.send(embed= embed) #send embed in log channel

        except discord.Forbidden: #if the bot doesn't have perms to ban the person
          embed = discord.Embed(title= "Error", description= "I don't have permission to ban this person", colour= discord.colour.Color.red()) #make embed saying it doesn't have perms
          await ctx.send(embed= embed) #send embed

@client.command()
async def unban(ctx): #unban command
  try:
    if ctx.message.mentions[0].id == ctx.message.author.id: #if someone tried to ban themself
      embed = discord.Embed(title= "Why?", description= "You aren't even banned?", colour= discord.colour.Color.blue()) #make embed asking why
      await ctx.send(embed= embed) #send embed
  
  except IndexError:
    if ctx.message.author.id not in staff: #if the person isn't a staff
      embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red()) #make embed saying you have to be staff
      await ctx.send(embed= embed) #send embed
    
    else: #if the person is a staff
      user = await rtFuncs.getUser(ctx, client, "rt!unban") #splits rt!unban to get the id
      if user == None: #if there is no id
        return "" #stops the command
    
  
      if user == ctx.message.author: #if the person to unban is the person who did rt!unban
        embed = discord.Embed(title= "Error", description= "No member mentioned to unban", colour= discord.colour.Color.red()) #make embed saying no one mentioned
        await ctx.send(embed = embed) #send embed
  
      else: #if the person to unban isn't staff
        guild = await client.fetch_guild(rtFuncs.rtServer) #gets the Red Tech server

        try:
          await guild.unban(user) #unbans the person
          embed = discord.Embed(title= "Unban Successful!", description= f"{user.name} was unbanned from the server", colour= discord.colour.Color.green()) #makes a embed saying unban successful
          await ctx.send(embed= embed) #sends embed
          logChannel = await client.fetch_channel(rtFuncs.logMessageChannel) #gets log channel
          await logChannel.send(embed= embed) #sends embed
    
        except discord.Forbidden: #if the bot doesn't have perms to unban the person
          embed = discord.Embed(title= "Error", description= f"I don't have permission to unban {user.name}!", colour= discord.colour.Color.red()) #make an embed saying it doesn't have perms
          await ctx.send(embed= embed) #send embed
        
        except discord.NotFound: #if it can't find the ban (the person isn''t banned)
          embed = discord.Embed(title= "Error", description= f"{user.name} is not banned", colour= discord.colour.Colour.red()) #make an embed saying person isn't banned
          await ctx.send(embed= embed) #send embed

@client.command(aliases=["purge"]) #sets rt!purge as an alias
async def clear(ctx): #clear command
  if ctx.message.author.id not in staff: #if the person isn't staff
    embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red()) #make an embed saying you must be staff
    await ctx.send(embed= embed) #send embed
  
  else: #if the person is staff
    amount = ctx.message.content.strip("rt!clear ") #gets rid of rt!clear if they used it
    amount = amount.strip("rt!purge ") #gets rid of rt!purge if they used it
    try:
      amount = int(amount) #gets the amount of messages to delete
      await ctx.message.delete() #deletes the rt!clear/rt!purge message
      await ctx.channel.purge(limit= amount) #deletes the amount of messages specified
      embed = discord.Embed(title= "Purge Successful!", description= f"{amount} messages deleted successfully", colour= discord.colour.Color.green()) #makes and embed saying purge successful
      purgeMsg = await ctx.send(embed= embed) #sends embed
      await purgeMsg.delete(delay= 5) #deletes embed saying purge successful after 5 secs
    
    except ValueError: #if there isn't a number of messages to delete
      embed = discord.Embed(title= "Error", description= "Invalid number", colour= discord.colour.Color.red()) #makes an embed saying invalid number
      await ctx.send(embed= embed) #sends embed

@client.command()
async def mute(ctx): #mute command
  try:
    ctx.message.mentions[0].id #checks to see if anyone is mentions

  except IndexError: #if no one is mentioned
    embed = discord.Embed(title= "Error", description= "No member mentioned to mute", colour= discord.colour.Color.red()) #makes and embed saying no one was mentioned
    await ctx.send(embed= embed) #sends embed
    return "" #stops the command

  if ctx.message.mentions[0].id == ctx.message.author.id: #if someone tries to mute themselves
    embed = discord.Embed(title= "Why?", description= "Why are you trying to mute yourself?", colour= discord.colour.Color.blue()) #makes and embed asking why
    await ctx.send(embed= embed) #sends the embed
    return "" #stops the command

  if ctx.message.author.id not in staff: #if the person who did rt!mute isn't a staff
    embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red()) #makes and embed saying they must be a staff member
    await ctx.send(embed= embed) #sends the embed
  
  else: #if the person who did rt!mute is a staff member
    mutedRole = ctx.guild.get_role(rtFuncs.muteRoleId) #gets the muted role

    if mutedRole in ctx.message.mentions[0].roles: #if the person is already muted
      embed = discord.Embed(title= "Error", description= "This person is already muted", colour= discord.colour.Color.red()) #makes embed saying they are already muted
      await ctx.send(embed= embed) #sends embed
    
    else: #if they aren't muted
      if ctx.message.mentions[0].id in staff: #if the person getting muted is a staff
        embed = discord.Embed(title= "Error", description= "You can't mute other staff", colour= discord.colour.Color.red()) #makes an embed saying you can't mute staff
        await ctx.send(embed= embed) #sends it
        if ctx.message.mentions[0].id == 457954086667550751: #if the person getting muted is Jon
          await ctx.send("https://static.wikia.nocookie.net/24005259-b85f-4770-a051-abadd75daace") #so you have chosen death
      
      else: #if the person getting muted isn't a staff
        f = open("AvisServer/Bots/JonBots/RTBot3/RTMutelist.txt", "r+") #opens the mute list
        alreadyMuted = False
        
        for line in f: #check to see if the person is in the mute list
          if str(ctx.message.mentions[0].id) in line:
            alreadyMuted = True
        
        if alreadyMuted == True: #they are in mute list
          await ctx.message.mentions[0].add_roles(mutedRole) #gives them the muted role
          embed = discord.Embed(title= "Mute Successful!", description= f"{ctx.message.mentions[0].name} was successfully muted", colour= discord.colour.Color.green()) #makes embed saying mute successful
          await ctx.send(embed= embed) #sends embed

        
        else: #if they aren't in the mute list
          await ctx.message.mentions[0].add_roles(mutedRole) #mutes them
          f.write(f"{ctx.message.mentions[0].id} : {ctx.message.mentions[0]}\n") #adds them to the mute list
          f.close() #closes the mute list
          embed = discord.Embed(title= "Mute Successful!", description= f"{ctx.message.mentions[0].name} was successfully muted", colour= discord.colour.Color.green()) #makes embed saying mute successful
          await ctx.send(embed= embed) #sends embed

@client.command()
async def unmute(ctx): #unmute command
  try:
    ctx.message.mentions[0].id #checks to see if someone was mentioned

  except IndexError: #if no one was mentioned
    embed = discord.Embed(title= "Error", description= "No member mentioned to unmute", colour= discord.colour.Color.red()) #makes embed saying no one was mentioned
    await ctx.send(embed= embed) #sends embed
    return "" #stops the command

  if ctx.message.mentions[0].id == ctx.message.author.id: #if someone tried to unmute themselves
    embed = discord.Embed(title= "Why?", description= "You aren't even muted?", colour= discord.colour.Color.blue()) #makes embed asking why
    await ctx.send(embed= embed) #sends embed
    return "" #stops the command

  if ctx.message.author.id not in staff: #if the person who did rt!unmute isn't a staff
    embed = discord.Embed(title= "Error", description= "You must be a staff member to use this command!", colour= discord.colour.Color.red()) #makes an embed saying they have to be staff
    await ctx.send(embed= embed) #sends embed
  
  else: #if the person is a staff
    mutedRole = ctx.guild.get_role(rtFuncs.muteRoleId)
    f = open("AvisServer/Bots/JonBots/RTBot3/RTMutelist.txt", "r+") #opens the mute list
    fileContent = f.read() #gets the contents of the mute list
    f.close() #closes the mute list

    fileContent = fileContent.splitlines() #organizes the mute list
    
    userId = str(ctx.message.mentions[0].id) #get's the id of the person being unmuted
    personMuted = False

    i = 0
    for user in fileContent: #get's the mute entry of the person being unmuted
      if userId in user:
        popthis = i
        personMuted = True

      i = i + 1

    

    if personMuted == False: #if no entry is found
      embed = discord.Embed(title= "Error", description= f"{ctx.message.mentions[0].name} is not muted", colour= discord.colour.Colour.red()) #makes embed saying person isn't muted
      await ctx.send(embed= embed) #sends embed
    
    else: #if entry is found
      fileContent.pop(popthis) #removes the entry
      newFileContent = ""
      for i in fileContent: #updates the list with the removed entry
        newFileContent = newFileContent + i + "\n"
      
      
      await ctx.message.mentions[0].remove_roles(mutedRole) #removes the muted role
      f = open("AvisServer/Bots/JonBots/RTBot3/RTMutelist.txt", "w") #opens the mute list
      f.write(newFileContent) #saves the changes (removed mute entry)
      embed = discord.Embed(title= "Unmute Successful!", description= f"{ctx.message.mentions[0].name} was unmuted", colour= discord.colour.Color.green()) #makes an embed saying unmute successful
      await ctx.send(embed= embed) #sends embed






@client.command()
async def staffCheck(ctx): #staff check
  if ctx.author.id in staff: #if the person who did rt!staffcheck is a staff
    await ctx.send("Staff = True") #sends Staff = True in discord

  elif ctx.author.id not in staff: #if the person who did rt!staffcheck isn't a staff
    await ctx.send("Staff = False") #sends Staff = False in discord
  
  else: #if the person is using a quantum computer and is both a staff, and not a staff, at the same time
    await ctx.send("Error") #sends an error message



token = os.environ['RTB3Token'] #gets the bot token (basically it's passwords)
client.run(token) #starts the bot