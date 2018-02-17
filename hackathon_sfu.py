from flask import jsonify, Flask
from flask_graphql import GraphQLView

app = Flask(__name__)
app.add_url_rule('/', 'home', lambda: jsonify({'response': 'ok', 'message': 'hey, patrick\'s data warehouse'}))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
