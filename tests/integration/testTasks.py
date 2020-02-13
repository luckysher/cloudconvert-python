###################################################################
##      Test case for tasks                                      ##
##                                                               ##
## How to run ? :                                                ##
##                $ python tests/integration/testTasks.py        ##
###################################################################

import sys
import os
sys.path.append(os.getcwd())

import unittest
import cloudconvert
from cloudconvert.config import API_KEY

cloudconvert.API_KEY = API_KEY

# Set API client in sandbox mode
cloudconvert.sandbox = True


class TasksTestCase(unittest.TestCase):

    def setUp(self):
        """
        Test case setup method
        :return:
        """
        print("Setting up task test case")
        self.cloudconvert = cloudconvert

        # setup the client with the provided API key by configuring
        self.cloudconvert.configure()

    def testImportUrlTask(self):
        """
        Test case for uploading file
        :return:
        """
        print("Test case for 'import/url' file...")
        new_task = {
            "url": "file/url/to/upload"
        }

        task = cloudconvert.Task.create(operation="import/url", payload=new_task)

        # do wait for the task
        wait_task = cloudconvert.Task.wait(id=task["id"])

        # delete the task
        deleted = cloudconvert.Task.delete(id=wait_task["id"])

        print("task deleted with Id: {}".format(wait_task["id"]) if deleted else "unable to delete the task: {}".format(wait_task["id"]))

    def tearDown(self):
        """
        Teardown method
        :return:
        """
        print("Tearing down test case for task..")


if __name__ == '__main__':
    unittest.main()
