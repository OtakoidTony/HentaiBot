import requests


def nekofun(endpoint:str):
  r = requests.get("http://api.nekos.fun:8080/api/" + endpoint)
  if r.status_code != 200:
    return("An error has occurred")
  else:
    return(r.json()["url"])

