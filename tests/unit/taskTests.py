###################################################################
##      Test cases for Cloud Convert API tasks endpoints         ##
##                                                               ##
## How to run ? :                                                ##
##                $ python taskTests.py                          ##
###################################################################

import sys
import os
sys.path.append(os.getcwd())

import unittest
import cloudconvert


# API key for the Cloud convert Rest API
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjA3N2YwMjZiMzlmNTBmNGE1MzljNmE5N2UwNTJhZmM0NDIxY2FmZWY5ZjMyZjE3Y2M4ZjI0M2NjYzc4NjlkMzFkODM2MzM4MmIwZjZlYjNjIn0.eyJhdWQiOiIxIiwianRpIjoiMDc3ZjAyNmIzOWY1MGY0YTUzOWM2YTk3ZTA1MmFmYzQ0MjFjYWZlZjlmMzJmMTdjYzhmMjQzY2NjNzg2OWQzMWQ4MzYzMzgyYjBmNmViM2MiLCJpYXQiOjE1ODAzMTQzNTAsIm5iZiI6MTU4MDMxNDM1MCwiZXhwIjo0NzM1OTg3OTUwLCJzdWIiOiI0MDEwMDk0MSIsInNjb3BlcyI6WyJ0YXNrLnJlYWQiLCJ0YXNrLndyaXRlIl19.LkvUT0WDG4_08DFVA9JbFQvq7FxZmNGepN0NsFkXoxbRkBd4vXV8tbfcjpI1cP-CXudz86Ea11RKynTTBYuZlAne5Cy5KNt5-vgrj_m75DcaB5XohsbvS5uo98FspKl3wNhLSqnJb0dFr9eer8589vvVL8HUL4yv_tah_d4dZEZR0MF0LPQFe9l9gS8d7UtTAmIli0j7-LPUbLYH8tQ1-BuhrQKtjEEFbqJsdJInEFAAM6kCRcXu0frj_R2Xv04RXbVJ4_JvSFV_4a05fIIscCd8tyr5PvIRuU2C3Pevr620kknSz3T2KiJlSQq1aq_XSLRq4fu_9XApyjtKu0Ln45dfQ2w4J7bk8rQTJhvKaejfi2QlH-Hrg1M32mFn2fmFsXaWdfCOyv7nX2PBipI-S10H1O6NHtKP0nRM9m25H2vpFzoj2kVjSOUGw545tnt_0yG2cmynORYuzsNRU5fYRMcAwYCY_OWVz3ATUdPeiosoVzKsauRXOhTM1GG6OJ9DX1nUDtZOv00oLQwVZE5GtjUFYv12t0Tqjj8VzTH_GWfEBxphNvjfekWKpFGmKXUIiAlePHWbI6yZeLJxk5zek3StZB-7cRJqj4wDcLo5-wRZ6-JpTQ9Kmu7g2TAD8gOjxoZt7pvTaTE"


cloudconvert.API_KEY = API_KEY

# By Default API mode is in sandbox mode
# cloudconvert.sandbox = False


class TaskTestCase(unittest.TestCase):

    def setUp(self):
        """
        Test case setup method
        :return:
        """
        print("Setting up Task test cases")
        self.cloudconvert = cloudconvert

        # setup the client with the provided API key by configuring
        self.cloudconvert.configure()

    def testCreateTask(self):
        """
        Create Task
        :return:
        """
        print("testcase for creating task..")

        # create dict for new task
        new_import_url_task = {
            "url": "https://file-examples.com/wp-content/uploads/2017/02/file-sample_100kB.doc"
        }

        res = self.cloudconvert.Task.create(operation="import/url", payload=new_import_url_task)

        assert 'id' in list(res.get('data').keys()), "Unable to create 'import/url' task"

    def testWaitTask(self):
        """
        Wait Task
        :return:
        """
        print("testcase for waiting task..")
        task_id = "be76cadf-33de-42f7-8c7f-9df787a09951"
        res = self.cloudconvert.Task.wait(id=task_id)

        assert 'id' in list(res.get('data').keys()), "Unable to create wait task"

    def testShowTask(self):
        """
        Show Task
        :return:
        """
        print("testcase for show task..")
        task_id = "be76cadf-33de-42f7-8c7f-9df787a09951"
        res = self.cloudconvert.Task.show(id=task_id)

        assert 'id' in list(res.get('data').keys()), "Unable to create show task"

    def testListTask(self):
        """
        List Task
        :return:
        """
        print("testcase for listing tasks..")

        res = self.cloudconvert.Task.all()
        # res = self.cloudconvert.Task.all(params={'page':10})

        assert isinstance(res.get('data'), list), "Unable to fetch the task list"

    def testRetryTask(self):
        """
        Retry Task
        :return:
        """
        print("testcase for retrying a task")
        task_id = "be76cadf-33de-42f7-8c7f-9df787a09951"
        res = self.cloudconvert.Task.retry(id=task_id)

        assert 'id' in list(res.get('data').keys()), "Unable to retry task"

    def testDeleteTask(self):
        """
        Delete Task
        :return:
        """
        print("testcase for delete task..")
        task_id = "be76cadf-33de-42f7-8c7f-9df787a09951"
        res = self.cloudconvert.Task.delete(id=task_id)
        assert res == True,  "Unable to delete task"

    def testCancelTask(self):
        """
        Cancel Task
        :return:
        """
        print("testcase for Cancelling a task in waiting / processing status")
        task_id = "be76cadf-33de-42f7-8c7f-9df787a09951"
        res = self.cloudconvert.Task.cancel(id=task_id)
        assert res == True, "Unable to cancel task"

    def tearDown(self):
        """
        Teardown method
        :return:
        """
        print("Tearing down task test cases..")


if __name__ == '__main__':
    unittest.main()
