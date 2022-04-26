import discord
import os
import json
import httpx
import re
from keep_alive import keep_alive



platforms = ["steam", "epic", "psn", "xbl"]
competitive_ranks = ["Ranked Duel 1v1", "Ranked Doubles 2v2", "Ranked Standard 3v3"]
extra_ranks = ["Hoops", "Rumble", "Dropshot", "Snowday"]
error_messages = ["Error, inténtelo de nuevo más tarde", "No se encuentra el usuario", "No se han introducido datos", "Se ha producido un error en el servidor"]

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
  
  clienthttp = httpx.AsyncClient(http2=True)
  try:
    print("Plataforma: " + platform)
    headers = {"Host": "api.tracker.gg", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
    response = await clienthttp.get('https://api.tracker.gg/api/v2/rocket-league/standard/profile/' + platform + "/" + username, headers=headers)
    print("Version: " + response.http_version+
         "\nError: " + str(response.status_code))
  except Exception as e:
    print(e)
    return "Error, inténtelo de nuevo más tarde"
  print(response.text)
  try:
    json_data = json.loads(response.text)
    print("---------JSON----------")
    print(json_data)
    print("--------JSONEND--------")
    if("errors" in json_data):
      print("Error no encontrado")
      return "No se encuentra el usuario"
  except Exception as e:
    print(e)
    return "Se ha producido un error en el servidor"

  try:

    """
    minus = 0
    if(mode == "competitive"):
      pos = 2
      ranklist = competitive_ranks
      loops = 3
    elif(mode == "extra"):
      pos = 5
      ranklist = extra_ranks
      loops = 4
    loops2 = len(json_data["data"]["segments"])
    print("loops2: " + str(loops2))

    print("--------LOOP----------")
    print("Pos: " + str(pos) + "\nLoops: " + str(loops) + "\nRank List: " + str(ranklist) + "\nPlataforma: " + platform + "\nMode: " + mode)
    for i in range(loops):
      if(json_data["data"]["segments"][1]["metadata"]["name"] != "Un-Ranked"):
        minus = 1
        print("minus: " + str(minus))
      if(json_data["data"]["segments"][pos - minus]["metadata"]["name"] in ranklist):
        print("******dentro de la lista******")
        rankname = json_data["data"]["segments"][pos - minus]["metadata"]["name"]
        ranktier = json_data["data"]["segments"][pos - minus]["stats"]["tier"]["metadata"]["name"]
        rankdiv = json_data["data"]["segments"][pos - minus]["stats"]["division"]["metadata"]["name"]
        rankmmr = str(json_data["data"]["segments"][pos - minus]["stats"]["rating"]["value"])
        ranks += rankname + ": " + ranktier + " " + rankdiv + " " +rankmmr + "\n"
        pos += 1
        
        print(ranks)
      else:
        print("**********************")
        print(json_data["data"]["segments"][pos - minus]["metadata"]["name"])
        print("**********************")
    print("-------LOOPEND--------")
    if(ranks == ""):
       raise Exception("No se encuentra el usuario")
    else:
      ranks = "Plataforma: " + platform + "\n" + ranks
    return ranks
  except:
      return "No existen datos para estos modos de juego 1"
    """

    if(mode == "competitive"):
      ranklist = competitive_ranks
    elif(mode == "extra"):
      ranklist = extra_ranks
    loops = len(json_data["data"]["segments"])
    
    print("--------LOOP----------")
    print("Rank List: " + str(ranklist) + "\nLoops: " + str(loops) + "\nPlataforma: " + platform + "\nMode: " + mode)
    for i in range(loops):
      if(json_data["data"]["segments"][i]["metadata"]["name"] in ranklist):
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
  except:
      return "No existen datos para estos modos de juego"

async def get_all_rlranks(username, message, platform):
  mode = "competitive"
  rank1 = await get_rlranks(username, message, platform, mode)
  print("-------rank1--------")
  print(rank1)
  if(rank1 in error_messages):
    return rank1
  else:
    if(rank1 == "No existen datos para estos modos de juego"):
      rank1 = ""
    ranks = rank1
  
  mode = "extra"
  rank2 = await get_rlranks(username, message, platform, mode)
  print("-------rank2--------")
  print(rank2)
  if(rank2 in error_messages):
    return rank2
  else:
    if(rank2 == "No existen datos para estos modos de juego"):
      rank2 = ""
    else:
      endlinepos = rank2.index("\n")
      rank2 = rank2[endlinepos:]
    ranks += rank2
    
    if(ranks == ""):
      return "No existen datos para estos modos de juego"
    else:
      return ranks
    
  """
  mode = "competitive"
  rank1 = await get_rlranks(username, message, platform, mode)
  print("-------rank1--------")
  print(rank1)
  if(rank1 in error_messages):
    return rank1
  else:
    ranks = rank1
    mode = "extra"
    rank2 = await get_rlranks(username, message, platform, mode)
    print("-------rank2--------")
    print(rank2)
    if(rank2 not in error_messages):
      if(rank2 == "No existen datos para estos modos de juego"):
        return ranks
      else:
        endlinepos = rank2.index("\n")
        rank2 = rank2[endlinepos:]
        ranks += rank2
        return ranks
    else:
      return ranks

prueba = "^!ranks\(\w*\) (steam|epic|psn|xbl)$"
  """

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
    ranks = await get_all_rlranks(username, message, platform)
    await message.channel.send(ranks)
    
keep_alive()
client.run(os.environ['TOKEN'])
