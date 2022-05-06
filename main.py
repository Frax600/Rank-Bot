import discord
import os
import json
import httpx
import re
from keep_alive import keep_alive
import http.client
import smtplib


platforms = ["steam", "epic", "psn", "xbl"]
competitive_ranks = ["Ranked Duel 1v1", "Ranked Doubles 2v2", "Ranked Standard 3v3", "Tournament Matches"]
extra_ranks = ["Hoops", "Rumble", "Dropshot", "Snowday"]
error_messages = ["Error, inténtelo de nuevo más tarde", "Si no tienes amigos en el", "No se encuentra el usuario", "No se han introducido datos", "Se ha producido un error en el servidor"]

def send_error_mail(error="Error de prueba"):
  try: 
    #Create your SMTP session 
    smtp = smtplib.SMTP('smtp.gmail.com', 587) 

   #Use TLS to add security 
    smtp.starttls() 

    #User Authentication 
    smtp.login(os.environ['SENDEREMAIL'],os.environ['EMAILPASSWORD'])

    #Defining The Message 
    message = error

    #Sending the Email
    smtp.sendmail(os.environ['SENDEREMAIL'], os.environ['RECEIVEREMAIL'],message) 

    #Terminating the session 
    smtp.quit() 
    print ("Email sent successfully!") 

  except Exception as ex: 
    print("Something went wrong....",ex)

async def get_rlranks(username, message, platform, mode):
  ranks = ""

  # Platform is selected
  if(platform == "m"):
    platform = "steam"
  elif(platform == "c"):
    platform = "epic"
  elif(platform == "n"):
    platform = "psn"
  elif(platform == "l"):
    platform = "xbl"
  
  conn = http.client.HTTPSConnection("scrapeninja.p.rapidapi.com")
  payload = "{\r\"url\": \"https://api.tracker.gg/api/v2/rocket-league/standard/profile/" + platform + "/" + username + "\"\r}"
  try:
    print("Plataforma: " + platform)
    headers = {
    'content-type': "application/json",
    'X-RapidAPI-Host': "scrapeninja.p.rapidapi.com",
    'X-RapidAPI-Key': "0acd66d402msh3145639099265a7p1497d5jsn68b5531f63fd"
    }
    conn.request("POST", "/scrape", payload, headers)

    res = conn.getresponse()
    data = res.read()

  except Exception as e:
    print(e)
    return "Error, inténtelo de nuevo más tarde"
  try:
    json_data = json.loads(data.decode("utf-8"))
    json_data = json.loads(json_data["body"])
    print("---------JSON----------")
    print(json_data)
    print("--------JSONEND--------")
    if("errors" in json_data):
      return "No se encuentra el usuario"
  except Exception as e:
    print("Errooooooooor")
    print(e)
    send_error_mail(str(e))
    return "Se ha producido un error en el servidor"

  try:

    if(mode == "competitive"):
      ranklist = competitive_ranks
    elif(mode == "extra"):
      ranklist = extra_ranks
    elif(mode == "all"):
      ranklist = competitive_ranks + extra_ranks
      
    loops = len(json_data["data"]["segments"])
    rank1 = 0
    rank2 = 0
    
    print("--------LOOP----------")
    print("Rank List: " + str(ranklist) + "\nLoops: " + str(loops) + "\nPlataforma: " + platform + "\nMode: " + mode)
    for i in range(loops):
      if(json_data["data"]["segments"][i]["metadata"]["name"] in ranklist):
        #If there is 1 competitive rank and 1 extra rank insert space between both
        if(json_data["data"]["segments"][i]["metadata"]["name"] in competitive_ranks):
          rank1 += 1
        elif(json_data["data"]["segments"][i]["metadata"]["name"] in extra_ranks and rank1 > 0 and rank2 == 0):
          rank2 += 1
          ranks += "\n"
          
        print("******dentro de la lista******")
        rankname = json_data["data"]["segments"][i]["metadata"]["name"]
        ranktier = json_data["data"]["segments"][i]["stats"]["tier"]["metadata"]["name"]
        rankdiv = json_data["data"]["segments"][i]["stats"]["division"]["metadata"]["name"]
        rankmmr = str(json_data["data"]["segments"][i]["stats"]["rating"]["value"])
        ranks += rankname + ": " + ranktier + " " + rankdiv + " " +rankmmr + "\n"
        
        print(ranks)
      else:
        print("**********************")
        print(json_data["data"]["segments"][i]["metadata"]["name"])
        print("**********************")
    print("-------LOOPEND--------")
    if(ranks == ""):
       raise Exception("No se encuentra el usuario")
    else:
      ranks = "Plataforma: " + platform + "\n" + ranks
    return ranks
  except Exception as e:
    print(e)
    return "No existen datos para estos modos de juego"

client = discord.Client()

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  if msg.startswith("!hola"):
    await msg.send("¡Qué pasa manco!")

  if re.search("^!ranks \w+.* (steam|epic|psn|xbl)$", msg):
    startname = msg.index(" ") + 1
    endname = msg.rindex(" ")
    username = msg[startname:endname]
    print("Username: " + username)
    platform = msg[-1]
    mode = "competitive"
    ranks = await get_rlranks(username, message, platform, mode)
    await message.channel.send(ranks)

  if re.search("^!extra \w+.* (steam|epic|psn|xbl)$", msg):
    startname = msg.index(" ") + 1
    endname = msg.rindex(" ")
    username = msg[startname:endname]
    platform = msg[-1]
    mode = "extra"
    ranks = await get_rlranks(username, message, platform, mode)
    await message.channel.send(ranks)

  if re.search("^!allranks \w+.* (steam|epic|psn|xbl)$", msg):
    startname = msg.index(" ") + 1
    endname = msg.rindex(" ")
    username = msg[startname:endname]
    platform = msg[-1]
    mode = "all"
    ranks = await get_rlranks(username, message, platform, mode)
    await message.channel.send(ranks)
    
keep_alive()
client.run(os.environ['TOKEN'])