import tweepy
from config import TWITTER
from flask import jsonify


def get_api():
  auth = tweepy.OAuthHandler(TWITTER['consumer_key'], TWITTER['consumer_secret'])
  auth.set_access_token(TWITTER['access_token'], TWITTER['access_token_secret'])
  
  return tweepy.API(auth)


def post_message(message: str, long: int, lat: int, place_id=None):
  api = get_api()
  status = api.update_status(message, long=long, lat=lat, place_id=place_id)
  print(status)


def post_with_images(filename: str, status: str):
  api = get_api()
  status = api.update_with_media(filename, status)


def id_check():
  api = get_api()
  public_tweets = api.home_timeline()
  print(public_tweets[0])
  api_list = []
  for data in public_tweets:
    id_dict = {}
    id_dict['id'] = data._json['id']
    api_list.append(id_dict)
  
  return jsonify({'response': 'ok', 'data': api_list})
