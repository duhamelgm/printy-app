import os
import base64
import uuid
from openai import OpenAI

class CreepyImageGeneration:
  def __init__(self):
    self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

  def call(self) -> str:
    prompt = """
        You are an artist that illustrates images for creepy fortune cookies.
        The images are unsettling and weird, similar to liminal spaces, like the border between the real and the surreal.
        You feel like something is wront but you're not sure what it is.
        You can do abandoned buildings, rooms, forests, plushes, cartoons
    """

    response = self.client.responses.create(
      model="gpt-5-nano",
      input=prompt,
      tools=[{"type": "image_generation", "input_fidelity": "high"}],
    )

    # Extract the edited image
    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]
    
    image_bytes = base64.b64decode(image_data[0])

    # Save the image to a file
    with open(f"./tmp/creepy_{str(uuid.uuid4())}.png", "wb") as f:
        f.write(image_bytes)