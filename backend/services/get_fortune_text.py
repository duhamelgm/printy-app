import random

class GetFortuneText:
  def __init__(self):
    self.possible_fortunes = []

  def call(self) -> str:
    data = open("./data/fortunes", "r").read()
    fortunes = data.split("%")
    for fortune in fortunes:
      self.possible_fortunes.append(fortune.strip())
    return random.choice(self.possible_fortunes)