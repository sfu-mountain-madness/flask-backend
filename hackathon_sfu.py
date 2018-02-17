from flask import jsonify, Flask
from flask_graphql import GraphQLView

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
  if not hasattr(g, 'db_list'):
    return
  for conn in g.db_list:
    connection = getattr(g, conn)
    connection.close()


app.add_url_rule('/', 'home', lambda: jsonify({'response': 'ok', 'message': 'hey, patrick\'s data warehouse'}))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
