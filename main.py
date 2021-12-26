from flask import *
import os
from pathlib import Path
import json
from googletrans import Translator
from twilio.twiml.messaging_response import MessagingResponse
import wolframalpha
import requests
import random
from random import randint
from dotenv import load_dotenv

wolf = wolframalpha.Client("A9AG4X-LJU6W6K2H4")
app = Flask("Test")



def trans(text,tar):

  url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

  payload = "q="+text+"&target="+tar+"&source=en"

  headers = {
    'content-type': "application/x-www-form-urlencoded",
    'accept-encoding': "application/gzip",
    'x-rapidapi-host': "google-translate1.p.rapidapi.com",
    'x-rapidapi-key': "af4d40d1f6msh1e797cce9e63df2p17d201jsnf96424be5e00"
    }

  response = requests.request("POST", url, data=payload, headers=headers).json()

  return response["data"]["translations"][0]["translatedText"]




def news(cat):
  for i in range(15):
    num = randint(0, 15)
  url = "https://newsapi.org/v2/top-headlines?country=us&category="+cat+"&apiKey=a1088ecc51cc4e79bfef8b781e51bdaf"
  response = requests.get(url).json()
  return response['articles'][num]['url']

def ask(query):
  question = query
  res = wolf.query(question)
  answer = next(res.results).text
  return answer

def photo(cat):
  for i in range(10):
    num = randint(0, 10)
  url = "https://api.unsplash.com/search/photos?query="+cat+"&client_id=qkC7OqWL5ofAkQTbNJ2uP4T-sWR0eewEP0W_bqtbc2c"
  response = requests.get(url).json()
  return response['results'][num]['urls']["regular"]


@app.route("/sms", methods=['GET', 'POST'])
def sms():

  txt = request.values.get('Body', '')
  rspns = MessagingResponse()
  msg = rspns.message()


  if txt[:4] == "News":
    txt = txt[5:]
    msg.body(news(txt))

  elif txt[:9] == "Wallpaper":
    txt = txt[10:]
    msg.body(photo(txt))

  elif txt[:9] == "Translate":
    tar = txt[10:12]
    txt = txt[13:]
    txt = trans(txt,tar)
    txt = "- - - \n" + "\n" + txt
    msg.body(txt)

  else:
    txt = ask(txt)
    txt = "- - - \n" + "\n" + txt
    msg.body(txt)

  return str(rspns)

app.run()

