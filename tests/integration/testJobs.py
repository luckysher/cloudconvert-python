###################################################################
##      Test case for jobs                                       ##
##                                                               ##
## How to run ? :                                                ##
##                $ python tests/integration/testJobs.py         ##
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
#cloudconvert.sandbox = True


class JobsTestCase(unittest.TestCase):

    def setUp(self):
        """
        Test case setup method
        :return:
        """
        print("Setting up job test case")
        self.cloudconvert = cloudconvert

        # setup the client with the provided API key by configuring
        self.cloudconvert.configure()

    def testUploadAndDownloadFiles(self):
        """
        Test case for uploading and downloading files
        :return:
        """
        print("Test case for uploading and downloading files...")
        job = self.cloudconvert.Job.create(operation="jobs", payload={
            'tag': 'integration-test-upload-download',
            'tasks': {
                'import-it': {
                    'operation': 'import/upload'
                },
                'export-it': {
                    'input': 'import-it',
                    'operation': 'export/url'
                }
            }
        })

        import_task = None
        # fetch task with name "import-id"
        for task in job["data"]["tasks"]:
            task_name = task.get("name")
            if task_name == "import-it":
                import_task = task

            if task_name == "export-it":
                export_task = task

        import_task_id = import_task.get("id")
        export_task_id = export_task.get("id")

        # fetch the finished task
        import_task = cloudconvert.Task.find(id=import_task_id)

        # do upload
        uploaded = cloudconvert.Task.upload(file_name="path/to/file/upload.ext", task=import_task)

        if uploaded:
            print("Uploaded file successfully..")

            # fetch the finished export task
            exported_task = cloudconvert.Task.find(id=export_task_id)

            # get exported url
            exported_url = exported_task.get("data").get("result").get("files")[0].get("url")
            fileName = exported_task.get("data").get("result").get("files")[0].get("filename")

            # now download the exported file
            cloudconvert.download(url=exported_url, filename=fileName)


    def tearDown(self):
        """
        Teardown method
        :return:
        """
        print("Tearing down test case for job..")


if __name__ == '__main__':
    unittest.main()
