from notion_client import Client
import random
import os
from datetime import datetime

class GetDayTickets:
  def __init__(self):
    self.client = Client(auth=os.environ["NOTION_TOKEN"])

  def call(self) -> str:
    tickets = self.client.data_sources.query(
      data_source_id="2ecec1a8-4f5c-8076-89b7-000b295a1032"
    )

    output_tickets = []

    for ticket in tickets["results"]:
      type_name = self.safe_dig(ticket, "properties", "Type", "select", "name")
      day_name = self.safe_dig(ticket, "properties", "Day", "select", "name")
      week_of_month = self.safe_dig(ticket, "properties", "Week of the month", "select", "name")
      print(ticket)

      if type_name == "Daily":
        output_tickets.append(self.compute_output_tickets(ticket))
      
      if type_name == "Weekly" and day_name == datetime.now().strftime("%A"):
        output_tickets.append(self.compute_output_tickets(ticket))

      if type_name == "Monthly" and day_name == datetime.now().strftime("%A") and self.week_of_month() == int(week_of_month):
        output_tickets.append(self.compute_output_tickets(ticket))

    grouped_tickets = {}

    print(output_tickets)

    for ticket in output_tickets:
      grouped_tickets[ticket["type"]] = grouped_tickets.get(ticket["type"], []) + [ticket]

    print(grouped_tickets)

    for type, tickets in grouped_tickets.items():
      if len(tickets) == 1:
        tickets[0]["assignee"] = random.choice(['Duhamel', 'Alika'])
      else:
        half = len(tickets) // 2
        for i in range(half):
          tickets[i]["assignee"] = "Duhamel"
        for i in range(half, len(tickets)):
          tickets[i]["assignee"] = "Alika"

    return [ticket for tickets in grouped_tickets.values() for ticket in tickets]

  def compute_output_tickets(self, ticket: dict) -> dict:
    return {
      "title": ticket["properties"]["Task name"]["title"][0]["plain_text"],
      "description": ticket["properties"]["Task name"]["title"][0]["plain_text"],
      "priority": 'Medium',
      "type": ticket["properties"]["Type"]["select"]["name"],
    }

  def week_of_month(self):
    dt = datetime.now()
    first_day = dt.replace(day=1)
    offset = (first_day.weekday())
    week = (dt.day + offset - 1) // 7

    return min(week, 3) + 1

  def safe_dig(self, obj, *path, default=None):
    for key in path:
        try:
            obj = obj[key]
        except (KeyError, IndexError, TypeError):
            return default
    return obj