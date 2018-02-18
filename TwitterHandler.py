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


def post_with_images():
  api = get_api()
  status = api.update_with_media("./images/rainbow.jpg")


def get_tweets_list():
  api = get_api()
  public_tweets = api.home_timeline(count=5, exclude_replies=True, trim_user=True)
  id_list = []
  for data in public_tweets:
    id_list.append(data._json['id_str'])
  return id_list
