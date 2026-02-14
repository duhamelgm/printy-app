from notion_client import Client
import random
import os
from datetime import datetime

IMPORTANCE_OPTIONAL_THRESHOLD = 12

class GetDayTickets:
  def __init__(self):
    self.client = Client(auth=os.environ["NOTION_TOKEN"])

  def call(self) -> str:
    tickets = self.client.data_sources.query(
      data_source_id="2ecec1a8-4f5c-8076-89b7-000b295a1032"
    )

    output_tickets = []
    results = tickets["results"]
    today_name = datetime.now().strftime("%A")
    tickets_by_type = {
      "Daily": [],
      "Weekly": [],
      "Biweekly": [],
      "Monthly": [],
      "Seasonly": [],
    }

    for ticket in results:
      type_name = self.safe_dig(ticket, "properties", "Type", "select", "name")
      print(ticket)
      day_name = self.safe_dig(ticket, "properties", "Day", "select", "name")
      if type_name != "Daily" and day_name != today_name:
        continue

      if type_name in tickets_by_type:
        tickets_by_type[type_name].append(ticket)

    if self.should_do_daily():
      for ticket in tickets_by_type["Daily"]:
        output_tickets.append(self.compute_output_tickets(ticket))

    for ticket in tickets_by_type["Weekly"]:
      output_tickets.append(self.compute_output_tickets(ticket))

    # assuming Notion will always give us tickets in the same order,
    # we can use the ticket's position in the list to split into odd and even weeks.
    for index, ticket in enumerate(tickets_by_type["Biweekly"]):
      if self.should_do_biweekly(index):
        output_tickets.append(self.compute_output_tickets(ticket))

    for index, ticket in enumerate(tickets_by_type["Monthly"]):
      if self.should_do_monthly(index):
        output_tickets.append(self.compute_output_tickets(ticket))

    for index, ticket in enumerate(tickets_by_type["Seasonly"]):
      if self.should_do_seasonly(index):
        output_tickets.append(self.compute_output_tickets(ticket))

    random.shuffle(output_tickets)

    grouped_tickets = {}

    for ticket in output_tickets:
      grouped_tickets[ticket["type"]] = grouped_tickets.get(ticket["type"], []) + [ticket]

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
    task_name = self.safe_dig(ticket, "properties", "Task name", "title", 0, "plain_text", default="Unknown Task")
    importance = self.safe_dig(ticket, "properties", "Importance", "number")

    if importance is not None:
      try:
        if float(importance) < IMPORTANCE_OPTIONAL_THRESHOLD:
          task_name = f"{task_name} (optional)"
      except (TypeError, ValueError):
        pass

    return {
      "title": task_name,
      "description": task_name,
      "priority": 'Medium',
      "type": ticket["properties"]["Type"]["select"]["name"],
    }

  def week_of_month(self):
    dt = datetime.now()
    first_day = dt.replace(day=1)
    offset = (first_day.weekday())
    week = (dt.day + offset - 1) // 7

    return min(week, 3) + 1

  def should_do_biweekly(self, index):
    # Spread biweekly tickets across odd/even weeks by index
    return self.week_of_month() % 2 == index % 2

  def should_do_monthly(self, index):
    # Spread monthly tickets across weeks of month using ticket index modulo.
    return self.week_of_month() == index % 4 + 1

  def should_do_seasonly(self, index):
    # First, spread seasonly tickets over months in a season (mod 3),
    # then, spread them over weeks in month (mod 4).
    # e.g. given tasks: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
    # tasks 1, 4, 7, 10, 13 can run in January (1%3 == 1, 4%3 == 1, 7%3 == 1, 10%3 == 1)
    # of tasks that can run in January: tasks 1 and 13 run in week 1: (1//3)%4 + 1 == 1 and (13//3)%4 + 1 == 1
    return (
      datetime.now().month % 3 == index % 3
      and self.week_of_month() == (index // 3) % 4 + 1
    )
    

  def safe_dig(self, obj, *path, default=None):
    for key in path:
        try:
            obj = obj[key]
        except (KeyError, IndexError, TypeError):
            return default
    return obj

  # do dailies on Mondays, Tuesdays, Fridays and Sundays
  def should_do_daily(self):
    return datetime.now().weekday() in [0, 1, 4, 6]
