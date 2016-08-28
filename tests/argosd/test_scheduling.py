import unittest
from queue import PriorityQueue

from argosd.scheduling import TaskScheduler, TaskRunner
from argosd.tasks import RSSFeedParserTask, BaseTask


class SchedulingTestCase(unittest.TestCase):

    def test_queue_ordering(self):
        """Test if tasks are retrieved from the queue in the correct order"""
        queue = PriorityQueue()
        taskscheduler = TaskScheduler(queue)
        taskrunner = TaskRunner(queue)

        # Create 3 tasks with different priority
        task_one = RSSFeedParserTask()
        task_one.priority = BaseTask.PRIORITY_LOW

        task_two = RSSFeedParserTask()
        task_two.priority = BaseTask.PRIORITY_NORMAL

        task_three = RSSFeedParserTask()
        task_three.priority = BaseTask.PRIORITY_HIGH

        # Add all tasks to the queue
        taskscheduler._add_to_queue(task_one)
        taskscheduler._add_to_queue(task_two)
        taskscheduler._add_to_queue(task_three)

        # Check order of tasks in queue, PRIORITY_HIGH should be first
        task = taskrunner._get_task_from_queue()
        self.assertEqual(task.priority, BaseTask.PRIORITY_HIGH)

        task = taskrunner._get_task_from_queue()
        self.assertEqual(task.priority, BaseTask.PRIORITY_NORMAL)

        task = taskrunner._get_task_from_queue()
        self.assertEqual(task.priority, BaseTask.PRIORITY_LOW)
