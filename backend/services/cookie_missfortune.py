import os

from openai import OpenAI


class CookieMissfortune:
  def __init__(self):
    api_key = os.getenv("OPENAI_API_KEY")
    self.client = OpenAI(api_key=api_key) if api_key else OpenAI()

  def call(self) -> str:
    prompt = """
      You work in a company that creates text for fortune cookies, these are different fortune cookies, 
      they give fortunes that have some missfortune in them, they're sarcastic and dry, 
      but specially unsettling, creepy and weird.
      giving a similar feeling to liminal spaces, like the border between the real and the surreal.
      you feel like something is wront but you're not sure what it is.
      You also like to add puns related:
      - Communism
      - Coding and tech
      - Art
      - Random nonsense that sounds funny and like a fortune, similar to brain rot
      However this puns are not too obvious, they should be subtle and only obvious to people who know the joke.
      All the fortunes are written like something that would happen in the future to the reader, like a fortune cookie.
      Very very rarely it's a chinese proverb, in chinese
      You can only use one pun at a time, and it should be related to the topic of the fortune.
      All the fortunes are one sentence or two sentences long.
      You work giving an output of 2 fortunes at a time, using a json array, where every item is a string.
    """

    response = self.client.responses.create(
      model="gpt-5-nano",
      input=prompt,
    )

    return response.output_text