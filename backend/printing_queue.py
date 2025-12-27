from redis import Redis
import os

env = os.environ.get("PYTHON_ENV")

if env == "development":
  redis_client = Redis.from_url(os.getenv("REDIS_URL"))
else:
  redis_client = Redis.from_url(os.getenv("REDIS_URL"), ssl_cert_reqs=None)

def enqueue_print(print_id: int) -> None:
  redis_client.lpush("printing_queue", print_id)

def queue_size() -> int:
  return redis_client.llen("printing_queue")