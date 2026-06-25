import unittest

from suno_easy import SunoClient, Task, TaskKind


class TestTask(unittest.TestCase):
    def test_task_str_and_repr(self):
        task = Task(
            task_id="abc123",
            kind=TaskKind.MUSIC,
            _client=SunoClient(api_key="k"),
            _parse=lambda d: [],
        )
        self.assertEqual(str(task), "abc123")
        self.assertEqual(task.task_id, "abc123")
        self.assertIn("music", repr(task))


if __name__ == "__main__":
    unittest.main()
