###################################################################
##      Test cases for Cloud Convert API tasks endpoints         ##
##                                                               ##
## How to run ? :                                                ##
##                $ python tests/unit/testTask.py                ##
###################################################################

import sys
import os
sys.path.append(os.getcwd())

import unittest
import requests_mock
import cloudconvert
import json

# API key for the Cloud convert Rest API
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijk2Y2M2MTA1OGY4NzExNjllZDUxOGY5YWY3NDBjMjcyMmYzZTNkZjEwMjEzMDdkYjM3OGI5MjIyOTRiMGVmZTVhODRhNzE0Y2QzNzliNDU1In0.eyJhdWQiOiIxIiwianRpIjoiOTZjYzYxMDU4Zjg3MTE2OWVkNTE4ZjlhZjc0MGMyNzIyZjNlM2RmMTAyMTMwN2RiMzc4YjkyMjI5NGIwZWZlNWE4NGE3MTRjZDM3OWI0NTUiLCJpYXQiOjE1ODAyMjMzNzYsIm5iZiI6MTU4MDIyMzM3NiwiZXhwIjo0NzM1ODk2OTc2LCJzdWIiOiI0MDEwMDk0MSIsInNjb3BlcyI6WyJ0YXNrLnJlYWQiLCJ0YXNrLndyaXRlIl19.ARGA_YM00m_VGnXbcJ0i-KrDjoA7GAiM16BQ9BteZNS8MbiW85z1ojn1KdSsKPElsnjj8iO0wOYsQ93oTIiYYAe0_W18-u-xhUj3UZt9WPahAoIzVU1ayeq8aVB9vXu_i7u5dvYFZ3XtFCGdk-61N4YcNU5gVkBz-g0mWSFG2v0NbHCwT8M5F3LGZM9EPnAh3XdAEqpcaLoJoUBLA5S_pE5btOJNMO5l8asp-sOO1WAauoOKlkRW1WYjKELiOhs4vhU8vhP8iS_H7Q6RlPF6CWr3zR1bvPqaCERzOUAdh9Lfg5vigClR0K8GpLKJbOKYcyXSV5Oco2MdWmGX3X7wHElgPAzkprnfELmEP_XEgDao5O1z5ILDsJ8J95VwB9-iTmkTVxJ9AzuFKEhmrifbUmI74YzSD-D4PE0amY6GK-dym8_JslF09FvOo9h4XHaS5Libzcx9nUkkGzFxiSAPSvGUGEsE69DIjQ70U-5Skklglx693Zbqk3AXik7k0Fx6R4hC-EQtBFYGuKvl_UrMqfwqbBBLOfZfZqxotYE2nype3sxjlxSn-4XmYAESUZwL_QqEHzPriSg8m_kNpXlwV4cqTTVjLhEQwTBC8oWlxrM2hB64nGsXow5Xh08waKBGZCqy7zixz7pWwPiNU0rn1LgOLdawYX1Yq3Soau9STfE"

cloudconvert.API_KEY = API_KEY

# Set API client in sandbox mode
# cloudconvert.sandbox = True


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
        self.responses_path = os.path.join(os.getcwd(), "tests/unit/responses")

    def testCreateTask(self):
        """
        Create Task
        :return:
        """
        print("testcase for creating task..")

        # create dict for new task
        new_import_url_task = {
            "url": "https://file-examples.com/wp-content/uploads/2017/02/file-sample_100kB.docx"
        }

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "createTask.json")) as f:
                response_json = json.load(f)

            m.post("https://api.cloudconvert.com/v2/import/url", json=response_json)
            task = self.cloudconvert.Task.create(operation="import/url", payload=new_import_url_task)

            self.assertEqual(first=task['id'], second="66bd538e-1500-4e4b-b908-0e429b357e77")
            print(m.called)

    def testWaitTask(self):
        """
        Wait Task
        :return:
        """
        print("testcase for waiting task..")

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "task.json")) as f:
                response_json = json.load(f)

            task_id = "4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b"
            m.get("https://api.cloudconvert.com/v2/tasks/{}/wait".format(task_id), json=response_json)

            task = self.cloudconvert.Task.wait(id=task_id)

            self.assertEqual(first=task['id'], second="4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b")
            print(m.called)

    def testShowTask(self):
        """
        Show Task
        :return:
        """
        print("testcase for show task..")

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "task.json")) as f:
                response_json = json.load(f)

            task_id = "4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b"
            m.get("https://api.cloudconvert.com/v2/tasks/{}".format(task_id), json=response_json)

            task = self.cloudconvert.Task.show(id=task_id)

            self.assertEqual(first=task['id'], second="4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b")
            print(m.called)

    def testListTask(self):
        """
        List Task
        :return:
        """
        print("testcase for listing tasks..")

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "tasks.json")) as f:
                response_json = json.load(f)

            m.get("https://api.cloudconvert.com/v2/tasks", json=response_json)
            tasks = self.cloudconvert.Task.all()

            self.assertEqual(isinstance(tasks, list), True)
            print(m.called)

    def testRetryTask(self):
        """
        Retry Task
        :return:
        """
        print("testcase for retrying a task")
        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "retry.json")) as f:
                response_json = json.load(f)

            task_id = "66bd538e-1500-4e4b-b908-0e429b357e77"
            m.post("https://api.cloudconvert.com/v2/tasks/{}/retry".format(task_id), json=response_json)
            tasks = self.cloudconvert.Task.retry(task_id)

            self.assertEqual(tasks["retry_of_task_id"], task_id)
            print(m.called)

    def testDeleteTask(self):
        """
        Delete Task
        :return:
        """
        print("testcase for delete task..")

        with requests_mock.mock() as m:

            task_id = "4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b"
            m.delete("https://api.cloudconvert.com/v2/tasks/{}".format(task_id), json={})

            isDeleted = self.cloudconvert.Task.delete(id=task_id)
            self.assertEqual(first=isDeleted, second=True)
            print(m.called)

    def testDownloadOutput(self):
        """
        Testcase to download output file
        :return:
        """
        res = cloudconvert.download(filename="path/to/save/file.ext", url="https://storage.de.cloud.ovh.net/v1/AUTH_b2cffe8f45324c2bba39e8db1aedb58f/cloudconvert-files/141cbea1-af92-49b3-aa8e-d085cf8b69f7/sample.docx?temp_url_sig=ee07b3353e8f5b0d478fd32d0a1c522c3285edc2&temp_url_expires=1580838826")
        print(res)

    def tearDown(self):
        """
        Teardown method
        :return:
        """
        print("Tearing down task test cases..")


if __name__ == '__main__':
    unittest.main()
