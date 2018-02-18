from flask import jsonify, Flask, g, request
from flask_graphql import GraphQLView

from db_connection import WeatherDB
from graphql import schema

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
  if not hasattr(g, 'db_list'):
    return
  for conn in g.db_list:
    connection = getattr(g, conn)
    connection.close()


def handle_weather():
  if request.method == 'POST':
    hum_temp = request.form
    db = WeatherDB()
    db.insert_data(hum_temp['hum'], hum_temp['tem'])
    return jsonify({'response': 'ok', 'message': 'stored to database'})
  elif request.method == 'GET':
    limit = request.args['limit']
    db = WeatherDB()
    weather_list = db.get_data_limited(limit)
    weather_list2 = []
    print(weather_list)

    for data in weather_list:
      print(data)
      weather_dict = {}
      weather_dict['id'] = data[0]
      weather_dict['hum'] = data[1]
      weather_dict['tem'] = data[2]
      weather_dict['time'] = data[3]
      weather_list2.append(weather_dict)

    return jsonify({'response': 'ok', 'data': weather_list2})
  return jsonify({'message': 'works'})


app.add_url_rule('/', 'home', lambda: jsonify({'response': 'ok', 'message': 'hey, mountain madness hackathon'}))
app.add_url_rule('/weather', 'weather', handle_weather, methods=['GET', 'POST'])
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001)
