import os
import sys
import types
import unittest
import importlib.util
from pathlib import Path
from datetime import datetime
from unittest.mock import MagicMock, patch


BACKEND_DIR = Path(__file__).resolve().parents[1]
MODULE_PATH = BACKEND_DIR / "services" / "get_day_tickets.py"

if "notion_client" not in sys.modules:
  notion_client_module = types.ModuleType("notion_client")
  notion_client_module.Client = MagicMock()
  sys.modules["notion_client"] = notion_client_module

# Load the module directly to avoid importing services/__init__.py and unrelated deps.
spec = importlib.util.spec_from_file_location("get_day_tickets_module", MODULE_PATH)
get_day_tickets_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(get_day_tickets_module)
GetDayTickets = get_day_tickets_module.GetDayTickets


class TestGetDayTickets(unittest.TestCase):
  def _build_task(self, type_name, day_name, title, week_of_month="1"):
    return {
      "properties": {
        "Type": {"select": {"name": type_name}},
        "Day": {"select": {"name": day_name}},
        "Week of the month": {"select": {"name": week_of_month}},
        "Task name": {"title": [{"plain_text": title}]},
      }
    }

  def _call_service(self, results, is_today_saturday=False, today=None):
    with patch.dict(os.environ, {"NOTION_TOKEN": "test-token"}, clear=False):
      with patch.object(get_day_tickets_module.random, "shuffle"):
        with patch.object(GetDayTickets, "is_today_saturday", return_value=is_today_saturday):
          with patch.object(get_day_tickets_module, "Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            mock_client.data_sources.query.return_value = {"results": results}

            if today is None:
              tickets = GetDayTickets().call()
            else:
              with patch.object(get_day_tickets_module, "datetime") as mock_datetime:
                mock_datetime.now.return_value = today
                tickets = GetDayTickets().call()

            mock_client.data_sources.query.assert_called_once_with(
              data_source_id="2ecec1a8-4f5c-8076-89b7-000b295a1032"
            )
            return tickets

  def test_daily_todos_selected_when_not_saturday(self):
    # Arrange
    tickets = [self._build_task("Daily", "Monday", f"Daily {i}") for i in range(5)]

    # Act
    selected = self._call_service(tickets, is_today_saturday=False)

    # Assert
    self.assertEqual(len(selected), 5)

  def test_daily_todos_not_selected_on_saturday(self):
    # Arrange
    tickets = [self._build_task("Daily", "Monday", f"Daily {i}") for i in range(5)]

    # Act
    selected = self._call_service(tickets, is_today_saturday=True)

    # Assert
    self.assertEqual(selected, [])

  def test_daily_todo_assignments_are_balanced(self):
    # Arrange
    tickets = [self._build_task("Daily", "Monday", f"Daily {i}") for i in range(5)]

    # Act
    selected = self._call_service(tickets, is_today_saturday=False)

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
    today_monday_january = datetime(2026, 1, 5)
    # seasonly: month%3 == index%3
    # given 5 tasks, for January (1) we should get tasks 1 and 4
    tickets = [self._build_task("Seasonly", "Monday", f"Seasonly {i}") for i in range(5)]

    # Act
    selected = self._call_service(tickets, today=today_monday_january)

    # Assert
    selected_titles = sorted(ticket["title"] for ticket in selected)
    self.assertEqual(selected_titles, ["Seasonly 1", "Seasonly 4"])
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


if __name__ == "__main__":
  unittest.main()
