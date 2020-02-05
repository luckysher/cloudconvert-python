"""
Test cases for Task API endpoints
"""

import unittest

# API key for the Cloud convert Rest API
API_KEY = ""

# API mode
SANDBOX_MODE = True


class TaskTestCase(unittest.TestCase):

    def setUp(self):
        """
        Setup method
        :return:
        """
        print("Setting up Task test cases")
        self.api_key = API_KEY
        self.api_mode = SANDBOX_MODE

    def testTaskCreate(self):
        print("testcase for creating task..")


    def tearDown(self):
        """
        Teardown method
        :return:
        """
        print("Tearing down task test cases..")


if __name__ == '__main__':
    unittest.main()
