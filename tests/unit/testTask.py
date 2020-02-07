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
import cloudconvert


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

        res = self.cloudconvert.Task.create(operation="import/url", payload=new_import_url_task)

        assert 'id' in list(res.keys()), "Unable to create 'import/url' task"

    def testWaitTask(self):
        """
        Wait Task
        :return:
        """
        print("testcase for waiting task..")
        task_id = "be76cadf-33de-42f7-8c7f-9df787a09951"
        res = self.cloudconvert.Task.wait(id=task_id)

        assert 'id' in list(res.keys()), "Unable to create wait task"

    def testShowTask(self):
        """
        Show Task
        :return:
        """
        print("testcase for show task..")
        task_id = "be76cadf-33de-42f7-8c7f-9df787a09951"
        res = self.cloudconvert.Task.show(id=task_id)

        assert 'id' in list(res.keys()), "Unable to create show task"

    def testListTask(self):
        """
        List Task
        :return:
        """
        print("testcase for listing tasks..")

        res = self.cloudconvert.Task.all()
        # res = self.cloudconvert.Task.all(params={'page':10})

        assert isinstance(res, list), "Unable to fetch the task list"

    def testRetryTask(self):
        """
        Retry Task
        :return:
        """
        print("testcase for retrying a task")
        task_id = "be76cadf-33de-42f7-8c7f-9df787a09951"
        res = self.cloudconvert.Task.retry(id=task_id)

        assert 'id' in list(res.keys()), "Unable to retry task"

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
