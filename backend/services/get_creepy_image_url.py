import random
import json

class GetCreepyImageUrl:
  def __init__(self):
    self.possible_images = []

  def call(self) -> str:
    data = open("./data/images.json", "r").read()
    images = json.loads(data)
    return random.choice(images)