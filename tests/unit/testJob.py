###################################################################
##      Test cases for Cloud Convert API jobs endpoints          ##
##                                                               ##
## How to run ? :                                                ##
##                $ python testJob.py                           ##
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

        assert 'id' in list(res.keys()), "Unable to create new job"

    def testWaitJob(self):
        """
        Wait Job
        :return:
        """
        print("testcase for waiting job..")
        job_id = "e03ed877-4964-4876-b1e2-8a5e597f9e71"
        res = self.cloudconvert.Job.wait(id=job_id)
        assert 'id' in list(res.keys()), "Unable to create wait job"

    def testShowJob(self):
        """
        Show Job
        :return:
        """
        print("testcase for show job..")
        job_id = "e03ed877-4964-4876-b1e2-8a5e597f9e71"
        res = self.cloudconvert.Job.show(id=job_id)
        assert 'id' in list(res.keys()), "Unable to create show job"

    def testListJob(self):
        """
        List Jobs
        :return:
        """
        print("testcase for listing Jobs..")

        res = self.cloudconvert.Job.all()
        # res = self.cloudconvert.Job.all(params={'page':10})
        assert isinstance(res, list), "Unable to fetch the job list"

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
