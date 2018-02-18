import graphene
from db_connection import WeatherDB


class WeatherData(graphene.ObjectType):
  temp = graphene.Float()
  humidity = graphene.Float()
  date = graphene.String(required=False)

class TweetsId(graphene.ObjectType):
  id = graphene.Int()

class Query(graphene.ObjectType):
  weather = graphene.List(WeatherData, limit=graphene.Int())
  tweets_id = graphene.List(TweetsId, limit=graphene.Int())


  def resolve_weather(self, info, limit):
    db = WeatherDB()
    weather_data_list = db.get_data_limited(limit)
    rv = list(map(lambda x: WeatherData(temp=x[1], humidity=x[2], date=x[3]), weather_data_list))
    return rv

  # def resolve_tweets_id(self, info, limit):


  def resolve_hello(self, info):
    return 'World'


schema = graphene.Schema(query=Query)
