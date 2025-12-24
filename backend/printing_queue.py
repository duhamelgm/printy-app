from redis import Redis
import os

redis_client = Redis.from_url(os.getenv("REDIS_URL"), ssl_cert_reqs=None)

def enqueue_print(print_id: int) -> None:
  redis_client.lpush("printing_queue", print_id)