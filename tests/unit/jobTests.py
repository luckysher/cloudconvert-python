###################################################################
##      Test cases for Cloud Convert API jobs endpoints          ##
##                                                               ##
## How to run ? :                                                ##
##                $ python jobTests.py                           ##
###################################################################

import sys
import os
sys.path.append(os.getcwd())

import unittest
import cloudconvert


# API key for the Cloud convert Rest API
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjA3N2YwMjZiMzlmNTBmNGE1MzljNmE5N2UwNTJhZmM0NDIxY2FmZWY5ZjMyZjE3Y2M4ZjI0M2NjYzc4NjlkMzFkODM2MzM4MmIwZjZlYjNjIn0.eyJhdWQiOiIxIiwianRpIjoiMDc3ZjAyNmIzOWY1MGY0YTUzOWM2YTk3ZTA1MmFmYzQ0MjFjYWZlZjlmMzJmMTdjYzhmMjQzY2NjNzg2OWQzMWQ4MzYzMzgyYjBmNmViM2MiLCJpYXQiOjE1ODAzMTQzNTAsIm5iZiI6MTU4MDMxNDM1MCwiZXhwIjo0NzM1OTg3OTUwLCJzdWIiOiI0MDEwMDk0MSIsInNjb3BlcyI6WyJ0YXNrLnJlYWQiLCJ0YXNrLndyaXRlIl19.LkvUT0WDG4_08DFVA9JbFQvq7FxZmNGepN0NsFkXoxbRkBd4vXV8tbfcjpI1cP-CXudz86Ea11RKynTTBYuZlAne5Cy5KNt5-vgrj_m75DcaB5XohsbvS5uo98FspKl3wNhLSqnJb0dFr9eer8589vvVL8HUL4yv_tah_d4dZEZR0MF0LPQFe9l9gS8d7UtTAmIli0j7-LPUbLYH8tQ1-BuhrQKtjEEFbqJsdJInEFAAM6kCRcXu0frj_R2Xv04RXbVJ4_JvSFV_4a05fIIscCd8tyr5PvIRuU2C3Pevr620kknSz3T2KiJlSQq1aq_XSLRq4fu_9XApyjtKu0Ln45dfQ2w4J7bk8rQTJhvKaejfi2QlH-Hrg1M32mFn2fmFsXaWdfCOyv7nX2PBipI-S10H1O6NHtKP0nRM9m25H2vpFzoj2kVjSOUGw545tnt_0yG2cmynORYuzsNRU5fYRMcAwYCY_OWVz3ATUdPeiosoVzKsauRXOhTM1GG6OJ9DX1nUDtZOv00oLQwVZE5GtjUFYv12t0Tqjj8VzTH_GWfEBxphNvjfekWKpFGmKXUIiAlePHWbI6yZeLJxk5zek3StZB-7cRJqj4wDcLo5-wRZ6-JpTQ9Kmu7g2TAD8gOjxoZt7pvTaTEulD"

cloudconvert.API_KEY = API_KEY

# By Default API mode is in sandbox mode
# cloudconvert.sandbox = False


class JobTestCase(unittest.TestCase):

    def setUp(self):
        """
        Test case setup method
        :return:
        """
        print("Setting up Job test cases")
        self.cloudconvert = cloudconvert

        # setup the client with the provided API key by configuring
        self.cloudconvert.configure()

    def testCreateJob(self):
        """
        Create Job
        :return:
        """
        print("testcase for creating Job..")

        # create dict for new Job
        job_with_single_task = {
            "tasks": {
                "sandbox-task-import-file": {
                    "operation": "import/url",
                    "url": "https://file-examples.com/wp-content/uploads/2017/02/file-sample_100kB.docx"
                }
            }
        }
        res = self.cloudconvert.Job.create(operation="jobs", payload=job_with_single_task)

        assert 'id' in list(res.get('data').keys()), "Unable to create new job"

    def testWaitJob(self):
        """
        Wait Job
        :return:
        """
        print("testcase for waiting job..")
        job_id = "e03ed877-4964-4876-b1e2-8a5e597f9e71"
        res = self.cloudconvert.Job.wait(id=job_id)
        assert 'id' in list(res.get('data').keys()), "Unable to create wait job"

    def testShowJob(self):
        """
        Show Job
        :return:
        """
        print("testcase for show job..")
        job_id = "e03ed877-4964-4876-b1e2-8a5e597f9e71"
        res = self.cloudconvert.Job.show(id=job_id)
        assert 'id' in list(res.get('data').keys()), "Unable to create show job"

    def testListJob(self):
        """
        List Jobs
        :return:
        """
        print("testcase for listing Jobs..")

        res = self.cloudconvert.Job.all()
        # res = self.cloudconvert.Job.all(params={'page':10})
        assert isinstance(res.get('data'), list), "Unable to fetch the job list"

    def testDeleteJob(self):
        """
        Delete Job
        :return:
        """
        print("testcase for delete job..")
        job_id = "be76cadf-33de-42f7-8c7f-9df787a09951"
        res = self.cloudconvert.Job.delete(id=job_id)
        assert res == True,  "Unable to delete job"

    def tearDown(self):
        """
        Teardown method
        :return:
        """
        print("Tearing down job test cases..")


if __name__ == '__main__':
    unittest.main()
