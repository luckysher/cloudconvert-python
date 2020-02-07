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
API_KEY = "API_KEY"

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
            "url": "input/file/url"
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
