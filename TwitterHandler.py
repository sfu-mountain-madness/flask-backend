import tweepy
from config import TWITTER


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
