from flask import jsonify, request
from flask_restful import Resource
import replicate, tiktoken

class Conversation(Resource):
  def __init__(self):
    self.client = replicate.Client(api_token="r8_KT8pMcfUFYr5s5zH6BeXii08fi5xMYk1wcjzb")
    self.history = ""

  def get(self):
    return {"message": "Send a POST request to start a conversation"}, 200
  
  def post(self):
    data = request.get_json()
    question = data.get("question")
    history = data.get("history")
    image_url = data.get("image_url")
    answer = self.submit_question(question, history, image_url)
    return { "answer": answer, "history": self.history }, 200

  def submit_question(self, question, history, image_url):
    history = self.history.strip() + '\n' + f'user: {question}'.strip()
    history = self.adjust_history(history)

    answer = self.client.run(
      "daanelson/minigpt-4:b96a2f33cc8e4b0aa23eacfce731b9c41a7d9466d9ed4e167375587b54db9423",
      input={
        "prompt": history,
        "image": image_url, # open(image_url, 'rb'),
        "num_beams": 1,
        "temperature": 0.05
      }
    ).strip()

    self.history = history + '\n' + f'assistant: {answer}'
    return answer

  def adjust_history(self, history):
    num_tokens = len(tiktoken.get_encoding("cl100k_base").encode(history)) * 1.25

    while num_tokens >= 2000:
        history = history[history[history.find('user:')+1:].find('user:')+1:].strip()
        num_tokens = len(tiktoken.get_encoding("cl100k_base").encode(history)) * 1.25

    return history