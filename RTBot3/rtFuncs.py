global rtlogo
rtlogo = "https://media.discordapp.net/attachments/831179512129519657/831982397938860052/Red_Tech_Logo_PNG.PNG?width=831&height=402"
global joinMessageChannel
global botLoggingChannel
rtServer = 775914661463326730
joinMessageChannel = 832411023397879818
logMessageChannel = 832405426128814120
rulesChannel = "<#827592943853502526>"
muteRoleId = 833546378953097246
memberRoleId = 831225101839106058

def test():
  
  return "There is nothing to test right now"




def help():
  import discord
  
  embed = discord.Embed(title= "Help", description= "You asked for help", colour= discord.colour.Colour.red())

  embed.set_author(name= "Red Tech™ Bot", icon_url= rtlogo)

  embed.add_field(name= "help", value= "A helpful command", inline= False)
  embed.add_field(name= "profile <user>", value= "Displays a users Keycard information", inline= False)
  embed.add_field(name= "ping", value= "Displays your ping", inline= False)
  embed.add_field(name= "dj", value= "Displays server information for Digital Jesuit", inline= False)
  embed.add_field(name= "twitch", value= "Plugs Jon's twitch channel", inline= False)
  embed.add_field(name= "redtech/rt/mc/invite", value= "Displays an invite link to Red Tech", inline= False)
  embed.add_field(name= "aus", value= "Displays and invite link to Australis", inline= False)
  embed.add_field(name= "logo", value= "Displays the Red_Tech Logo", inline= False)
  embed.add_field(name= "hist/history", value= "Displays the history of Red Tech", inline= False)
  embed.add_field(name= "blackbox/bb", value= "Pings all unclassified Red Tech Blackboxes", inline= False)
  embed.add_field(name= "nick <nickname>", value= "Allows a user to change there nickname, can be cleared with rt!nick clear", inline= False)
  embed.add_field(name= "test", value= "testing command, usally does nothing", inline= False)
  embed.add_field(name= "bob", value= "this is most likely going to be deleted", inline= False)

  embed.set_footer(text= "Property of Red Tech, Do not redistribute") 

  return embed




async def getUser(ctx, client, command):
  import discord
  try:
    user = ctx.message.mentions[0]
    userid = user.id
  except IndexError:
    user = ctx.message.author
    userid = user.id
    
    try:
      userid = ctx.message.content.strip(command)
      userid = int(userid)
      user = await client.fetch_user(userid)
       
    except ValueError:
      user = ctx.message.author
      userid = user.id
    
    except discord.errors.NotFound:
      await ctx.send("No account found with this id")
      return None
  return user














def blackBox():
  import discord
  embed = discord.Embed(title= "Red Tech Black Box Data", description= "", colour= discord.colour.Colour.dark_purple())

  embed.add_field(name= "Snowdin Facility:   :x:(Timed out after 5000ms)", value= "_ _", inline= False)
  embed.add_field(name= "Australis Facility:  :x:(Timed out after 5000ms)", value= "_ _", inline= False)
  embed.add_field(name= "Jungle Facility:       :x:(Timed out after 5000ms)", value= "_ _", inline= False)
  embed.add_field(name= "  Main Facility:          :white_check_mark:Ping Successful", value= "_ _", inline= False)

  

  
  return embed



def history():
  import discord

  embed = discord.Embed(title= "The History Of Red Tech", description= "Red_Tech was created by Jon_Jon_TTV.  It has been confirmed that there was another server in which Jon was working with redstone before Jon came to Digital Jesuit, but the reason for the sudden switch of servers is still unknown to this day.  Initially planning to make a small town for him and his friends, Jon spent a brief period in Snowdin, using that time to gather materials and scout a site for his town.  After a week or so, Jon went to a snowy tundra right outside of Snowdin and established his town.  After a few weeks in the server, it had become clear to Jon that this server lacked widespread knowledge about redstone and other technologies.  Therefore, he made a company called Red_Tech, short for Redstone Technologies.  Things went along smoothly for quite some time, eventually expanding to about 52 chunks.  A month after starting construction, the company opened for orders from other server members.  However, this order service closed shortly after due to the overwhelming amount of orders placed and the general lack of staff, plus the difficulty of actually installing said orders. Red_Tech therefore became a research facility, planning to do big reveals about every 2 months of what they have been working on.  Despite this, Red_Tech staff will usually still give tours of the town upon request, although always avoiding a door labeled Staff Only.  It is unknown what lies behind this door.  Red_Tech has been called by many the \"Silicon Valley of Digital Jesuit\", and demand for a position as an engineer at the company is at an all time high.  Recently, Red_Tech has joined forces with Australis due to budget issues, the promise of a massive urban center, and of course because Jon hated the snow.  After a couple of days of closure to resolve the world edit issues, Red_Tech opened again.", colour= discord.colour.Color.red())

  embed1 = discord.Embed(title= "", description= "While operating in Australis, Red Tech accomplished many things including the construction of a Warehouse and Creeper farm. In addition, more staff were brought on to the team, and the AI Bob was developed to manage the facilities and Discord. Alas, due to land size constraints, Red Tech and Australis decided to part ways on good terms. Now, Red Tech is currently working on a new facility that will be even bigger and better than the previous one and will help the company enter a new age of redstone development and creation.", colour = discord.colour.Color.red())

  list1 = [embed, embed1]
  return list1


def bob():
  return "Bob is just a rumor. Go back to your business"
