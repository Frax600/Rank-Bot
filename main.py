import discord
import os
import requests
import json
import httpx
from keep_alive import keep_alive

async def get_rluser(username, message):
  """
  request
  
  url = 'https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/itsjoaquinei'
  Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',"Referer":"https://www.google.com"}
  response = requests.get(url, headers = Headers)
  #json_data = json.loads(response.text)
  #platform = json_data[0][0]
  #return platform
  return response
  """
  """
  hyper
  
  s = requests.Session()
  s.mount('https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/itsjoaquinei', HTTP20Adapter())
  r = s.get('https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/itsjoaquinei')
  print(r.status_code)
  return "r.status.code"
  """

  
  clienthttp = httpx.AsyncClient(http2=True)
  try:
    response = await clienthttp.get('https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/' + username)
  except Exception as e:
    print(e)
    return "Error, inténtelo de nuevo más adelante"
  try:
    json_data = json.loads(response.text)
  except:
    return "No se han introducido datos"

  try:
    rank1v1 = json_data["data"]["segments"][2]["stats"]["tier"]["metadata"]["name"]
    div1v1 = json_data["data"]["segments"][2]["stats"]["division"]["metadata"]["name"]
    mmr1v1 = json_data["data"]["segments"][2]["stats"]["rating"]["value"]
    rank2v2 = json_data["data"]["segments"][3]["stats"]["tier"]["metadata"]["name"]
    div2v2 = json_data["data"]["segments"][3]["stats"]["division"]["metadata"]["name"]
    mmr2v2 = json_data["data"]["segments"][3]["stats"]["rating"]["value"]
    rank3v3 = json_data["data"]["segments"][4]["stats"]["tier"]["metadata"]["name"]
    div3v3 = json_data["data"]["segments"][4]["stats"]["division"]["metadata"]["name"]
    mmr3v3 = json_data["data"]["segments"][4]["stats"]["rating"]["value"]
    ranks = "Ranked Duel 1v1: " + rank1v1 + "  " + div1v1 + "  " + str(mmr1v1) + "\nRanked Doubles 2v2: " + rank2v2 + "  " + div2v2 + "  " + str(mmr2v2) + "\nRanked Standard 3v3: " + rank3v3 + "  " + div3v3 + "  " + str(mmr3v3)
    return ranks
  except:
    return "No se encuentra el usuario"


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
    ranks = await get_rluser(username, message)
    await message.channel.send(ranks)
    
keep_alive()
client.run(os.environ['TOKEN'])
