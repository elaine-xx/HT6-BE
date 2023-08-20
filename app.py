from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from hello_world import HelloWorld
from conversation import Conversation

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

api.add_resource(HelloWorld, "/")
api.add_resource(Conversation, "/chat")

if __name__ == "__main__":
  app.run(debug=True)