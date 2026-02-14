import unittest
import importlib.util
from pathlib import Path
from datetime import datetime
from unittest.mock import patch


BACKEND_DIR = Path(__file__).resolve().parents[1]
MODULE_PATH = BACKEND_DIR / "services" / "get_day_tickets.py"

# Load the module directly to avoid importing services/__init__.py and unrelated deps.
spec = importlib.util.spec_from_file_location("get_day_tickets_module", MODULE_PATH)
get_day_tickets_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(get_day_tickets_module)
GetDayTickets = get_day_tickets_module.GetDayTickets


class FakeTicketSource:
  def __init__(self, results):
    self.results = results

  def fetch_tickets(self) -> list[dict]:
    return self.results


class TestGetDayTickets(unittest.TestCase):
  def _build_task(self, type_name, day_name, title, week_of_month="1", importance=None):
    task = {
      "properties": {
        "Type": {"select": {"name": type_name}},
        "Day": {"select": {"name": day_name}},
        "Week of the month": {"select": {"name": week_of_month}},
        "Task name": {"title": [{"plain_text": title}]},
      }
    }
    if importance is not None:
      task["properties"]["Importance"] = {"number": importance}
    return task

  def _call_service(self, results, today=None):
    source = FakeTicketSource(results)
    service = GetDayTickets(source)

    with patch.object(get_day_tickets_module.random, "shuffle"):
      if today is None:
        return service.call()

      with patch.object(get_day_tickets_module, "datetime") as mock_datetime:
        mock_datetime.now.return_value = today
        return service.call()

  def test_daily_todos_selected_on_allowed_day(self):
    # Arrange
    today_monday = datetime(2026, 6, 8)
    tickets = [self._build_task("Daily", "Monday", f"Daily {i}") for i in range(5)]

    # Act
    selected = self._call_service(tickets, today=today_monday)

    # Assert
    self.assertEqual(len(selected), 5)

  def test_daily_todos_not_selected_on_non_allowed_day(self):
    # Arrange
    today_wednesday = datetime(2026, 6, 10)
    tickets = [self._build_task("Daily", "Monday", f"Daily {i}") for i in range(5)]

    # Act
    selected = self._call_service(tickets, today=today_wednesday)

    # Assert
    self.assertEqual(selected, [])

  def test_daily_todo_assignments_are_balanced(self):
    # Arrange
    today_monday = datetime(2026, 6, 8)
    tickets = [self._build_task("Daily", "Monday", f"Daily {i}") for i in range(5)]

    # Act
    selected = self._call_service(tickets, today=today_monday)

    # Assert
    duhamel_count = sum(1 for ticket in selected if ticket["assignee"] == "Duhamel")
    alika_count = sum(1 for ticket in selected if ticket["assignee"] == "Alika")
    self.assertLessEqual(abs(duhamel_count - alika_count), 1)

  def test_weekly_todos_selected_on_correct_day(self):
    # Arrange
    today_monday = datetime(2026, 6, 8)
    tickets = [
      self._build_task("Weekly", "Monday", "Weekly Selected"),
      self._build_task("Weekly", "Tuesday", "Weekly Not Selected"),
    ]

    # Act
    selected = self._call_service(tickets, today=today_monday)

    # Assert
    self.assertEqual(len(selected), 1)
    self.assertEqual(selected[0]["title"], "Weekly Selected")
    self.assertEqual(selected[0]["type"], "Weekly")

  def test_biweekly_todos_selected_on_correct_week(self):
    # Arrange
    today_monday_week_3 = datetime(2026, 6, 15)
    tickets = [
      self._build_task("Biweekly", "Monday", "Biweekly Not Selected"),
      self._build_task("Biweekly", "Monday", "Biweekly Selected"),
    ]

    # Act
    selected = self._call_service(tickets, today=today_monday_week_3)

    # Assert
    self.assertEqual(len(selected), 1)
    self.assertEqual(selected[0]["title"], "Biweekly Selected")
    self.assertEqual(selected[0]["type"], "Biweekly")

  def test_monthly_todos_selected_on_correct_week(self):
    # Arrange
    today_monday_week_2 = datetime(2026, 6, 8)
    # monthly: week_of_month == index%4 + 1
    # given 6 tasks, for week 2 we should get tasks 1 and 5
    tickets = [self._build_task("Monthly", "Monday", f"Monthly {i}") for i in range(6)]

    # Act
    selected = self._call_service(tickets, today=today_monday_week_2)

    # Assert
    selected_titles = sorted(ticket["title"] for ticket in selected)
    self.assertEqual(selected_titles, ["Monthly 1", "Monthly 5"])
    self.assertTrue(all(ticket["type"] == "Monthly" for ticket in selected))

  def test_seasonly_todos_selected_on_correct_month(self):
    # Arrange
    today_monday_april_week_2 = datetime(2026, 4, 6)
    # Seasonly tickets are spread over months in a season (mod 3),
    # then spread over weeks in month (mod 4).
    # so, only tasks 1 and 4 can run in April (1%3 == 1 and 4%3 == 1),
    # then only task 4 can run in week 2 ((4//3)%4 + 1 == 2).
    tickets = [self._build_task("Seasonly", "Monday", f"Seasonly {i}") for i in range(5)]

    # Act
    selected = self._call_service(tickets, today=today_monday_april_week_2)

    # Assert
    selected_titles = sorted(ticket["title"] for ticket in selected)
    self.assertEqual(selected_titles, ["Seasonly 4"])
    self.assertTrue(all(ticket["type"] == "Seasonly" for ticket in selected))

  def test_non_daily_todos_not_selected_on_wrong_day(self):
    # Arrange
    today_monday = datetime(2026, 6, 8)
    tickets = [
      self._build_task("Weekly", "Tuesday", "Weekly Wrong Day"),
      self._build_task("Monthly", "Tuesday", "Monthly Wrong Day"),
      self._build_task("Biweekly", "Tuesday", "Biweekly Wrong Day"),
      self._build_task("Seasonly", "Tuesday", "Seasonly Wrong Day"),
    ]

    # Act
    selected = self._call_service(tickets, today=today_monday)

    # Assert
    self.assertEqual(selected, [])

  def test_low_importance_tasks_get_optional_suffix(self):
    # Arrange
    today_monday = datetime(2026, 6, 8)
    tickets = [
      self._build_task("Weekly", "Monday", "Low Importance", importance=4),
      self._build_task("Weekly", "Monday", "High Importance", importance=20),
    ]

    # Act
    selected = self._call_service(tickets, today=today_monday)

    # Assert
    selected_titles = sorted(ticket["title"] for ticket in selected)
    self.assertEqual(selected_titles, ["High Importance", "Low Importance (optional)"])

  def test_monthly_selection_ignores_other_task_types_for_indexing(self):
    # Arrange
    today_monday_week_2 = datetime(2026, 6, 8)
    tickets = [
      self._build_task("Daily", "Monday", "Daily filler 0"),
      self._build_task("Weekly", "Monday", "Weekly filler 0"),
      self._build_task("Monthly", "Monday", "Monthly 0"),
      self._build_task("Daily", "Monday", "Daily filler 1"),
      self._build_task("Monthly", "Monday", "Monthly 1"),
      self._build_task("Biweekly", "Monday", "Biweekly filler 0"),
      self._build_task("Monthly", "Monday", "Monthly 2"),
      self._build_task("Seasonly", "Monday", "Seasonly filler 0"),
      self._build_task("Monthly", "Monday", "Monthly 3"),
      self._build_task("Weekly", "Monday", "Weekly filler 1"),
      self._build_task("Monthly", "Monday", "Monthly 4"),
      self._build_task("Daily", "Monday", "Daily filler 2"),
      self._build_task("Monthly", "Monday", "Monthly 5"),
    ]

    # Act
    selected = self._call_service(tickets, today=today_monday_week_2)

    # Assert
    selected_monthly_titles = sorted(
      ticket["title"] for ticket in selected if ticket["type"] == "Monthly"
    )
    self.assertEqual(selected_monthly_titles, ["Monthly 1", "Monthly 5"])

  def test_mixed_types_select_expected_tasks(self):
    # Arrange
    today_monday_week_2_june = datetime(2026, 6, 8)
    tickets = [
      self._build_task("Daily", "Monday", "Daily Selected"),
      self._build_task("Weekly", "Monday", "Weekly Selected"),
      self._build_task("Weekly", "Tuesday", "Weekly Not Selected"),
      self._build_task("Biweekly", "Monday", "Biweekly Selected"),
      self._build_task("Biweekly", "Monday", "Biweekly Not Selected"),
      self._build_task("Monthly", "Monday", "Monthly Not Selected"),
      self._build_task("Monthly", "Monday", "Monthly Selected"),
      self._build_task("Seasonly", "Monday", "Seasonly Not Selected 0"),
      self._build_task("Seasonly", "Monday", "Seasonly Not Selected 1"),
      self._build_task("Seasonly", "Monday", "Seasonly Not Selected 2"),
      self._build_task("Seasonly", "Monday", "Seasonly Selected"),
    ]

    # Act
    selected = self._call_service(tickets, today=today_monday_week_2_june)

    # Assert
    selected_titles = sorted(ticket["title"] for ticket in selected)
    self.assertEqual(
      selected_titles,
      [
        "Biweekly Selected",
        "Daily Selected",
        "Monthly Selected",
        "Seasonly Selected",
        "Weekly Selected",
      ],
    )


if __name__ == "__main__":
  unittest.main()
