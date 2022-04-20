import discord
import os
import json
import httpx
from keep_alive import keep_alive

platforms = ["steam", "epic", "psn", "xbl"]
competitive_ranks = ["Ranked Duel 1v1", "Ranked Doubles 2v2", "Ranked Standard 3v3"]
extra_ranks = ["Hoops", "Rumble", "Dropshot", "Snowday"]

async def get_rlranks(username, message, platform, mode, platformid=0):
  ranks = ""
  
  clienthttp = httpx.AsyncClient(http2=True)
  try:
    print("Plataforma: " + platform)
    response = await clienthttp.get('https://api.tracker.gg/api/v2/rocket-league/standard/profile/' + platform + "/" + username)
  except Exception as e:
    print(e)
    return "Error, inténtelo de nuevo más tarde"
  try:
    json_data = json.loads(response.text)
    print("---------JSON----------")
    print(json_data)
    print("--------JSONEND--------")
    if("errors" in json_data):
      print("Error no encontrado")
      print("pid:" + str(platformid))
      platformid += 1
      print("pid:" + str(platformid))
      if(platformid >= len(platforms)):
        return "No se encuentra el usuario"
      platform = platforms[platformid]
      return await get_rlranks(username, message, platform, mode, platformid)
  except Exception as e:
    print(e)
    return "No se han introducido datos"

  try:

    """
    minus = 0
    if(json_data["data"]["segments"][0]["type"] == "overview"):
      minus = 1
    rank1v1 = json_data["data"]["segments"][2 - minus]["stats"]["tier"]["metadata"]["name"]
    div1v1 = json_data["data"]["segments"][2 - minus]["stats"]["division"]["metadata"]["name"]
    mmr1v1 = json_data["data"]["segments"][2 - minus]["stats"]["rating"]["value"]
    rank2v2 = json_data["data"]["segments"][3 - minus]["stats"]["tier"]["metadata"]["name"]
    div2v2 = json_data["data"]["segments"][3 - minus]["stats"]["division"]["metadata"]["name"]
    mmr2v2 = json_data["data"]["segments"][3 - minus]["stats"]["rating"]["value"]
    rank3v3 = json_data["data"]["segments"][4 - minus]["stats"]["tier"]["metadata"]["name"]
    div3v3 = json_data["data"]["segments"][4 - minus]["stats"]["division"]["metadata"]["name"]
    mmr3v3 = json_data["data"]["segments"][4 - minus]["stats"]["rating"]["value"]
    ranks = "Ranked Duel 1v1: " + rank1v1 + "  " + div1v1 + "  " + str(mmr1v1) + "\nRanked Doubles 2v2: " + rank2v2 + "  " + div2v2 + "  " + str(mmr2v2) + "\nRanked Standard 3v3: " + rank3v3 + "  " + div3v3 + "  " + str(mmr3v3)
    """
    
    minus = 0
    if(mode == "competitive"):
      pos = 2
      loops = 3
      ranklist = competitive_ranks
    elif(mode == "extra"):
      pos = 5
      loops = 4
      ranklist = extra_ranks

    print("--------LOOP----------")
    print("Pos: " + str(pos) + "\nLoops: " + str(loops) + "\nRank List: " + str(ranklist) + "\nPlataforma: " + platform + "\nMode: " + mode)
    for i in range(loops):
      if(json_data["data"]["segments"][1]["metadata"]["name"] != "Un-Ranked"):
        minus = 1
      if(json_data["data"]["segments"][pos - minus]["metadata"]["name"] in ranklist):
        print("******dentro de la lista******")
        rankname = json_data["data"]["segments"][pos - minus]["metadata"]["name"]
        ranktier = json_data["data"]["segments"][pos - minus]["stats"]["tier"]["metadata"]["name"]
        rankdiv = json_data["data"]["segments"][pos - minus]["stats"]["division"]["metadata"]["name"]
        rankmmr = str(json_data["data"]["segments"][pos - minus]["stats"]["rating"]["value"])
        ranks += rankname + ": " + ranktier + " " + rankdiv + " " +rankmmr + "\n"
        pos += 1
        
        print(ranks)
    print("-------LOOPEND--------")
    if(ranks == ""):
       raise Exception("No se encuentra el usuario")
    else:
      ranks = "Plataforma: " + platform + "\n" + ranks
    return ranks
  except:
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

  if msg.startswith("!ranks(") and msg.endswith(")"):
    lenght = len(msg)
    username = msg[7:lenght-1]
    platform = platforms[0]
    mode = "competitive"
    ranks = await get_rlranks(username, message, platform, mode)
    await message.channel.send(ranks)

  if msg.startswith("!extra(") and msg.endswith(")"):
    lenght = len(msg)
    username = msg[7:lenght-1]
    platform = platforms[0]
    mode = "extra"
    ranks = await get_rlranks(username, message, platform, mode)
    await message.channel.send(ranks)
    
keep_alive()
client.run(os.environ['TOKEN'])
