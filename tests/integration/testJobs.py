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
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijk2Y2M2MTA1OGY4NzExNjllZDUxOGY5YWY3NDBjMjcyMmYzZTNkZjEwMjEzMDdkYjM3OGI5MjIyOTRiMGVmZTVhODRhNzE0Y2QzNzliNDU1In0.eyJhdWQiOiIxIiwianRpIjoiOTZjYzYxMDU4Zjg3MTE2OWVkNTE4ZjlhZjc0MGMyNzIyZjNlM2RmMTAyMTMwN2RiMzc4YjkyMjI5NGIwZWZlNWE4NGE3MTRjZDM3OWI0NTUiLCJpYXQiOjE1ODAyMjMzNzYsIm5iZiI6MTU4MDIyMzM3NiwiZXhwIjo0NzM1ODk2OTc2LCJzdWIiOiI0MDEwMDk0MSIsInNjb3BlcyI6WyJ0YXNrLnJlYWQiLCJ0YXNrLndyaXRlIl19.ARGA_YM00m_VGnXbcJ0i-KrDjoA7GAiM16BQ9BteZNS8MbiW85z1ojn1KdSsKPElsnjj8iO0wOYsQ93oTIiYYAe0_W18-u-xhUj3UZt9WPahAoIzVU1ayeq8aVB9vXu_i7u5dvYFZ3XtFCGdk-61N4YcNU5gVkBz-g0mWSFG2v0NbHCwT8M5F3LGZM9EPnAh3XdAEqpcaLoJoUBLA5S_pE5btOJNMO5l8asp-sOO1WAauoOKlkRW1WYjKELiOhs4vhU8vhP8iS_H7Q6RlPF6CWr3zR1bvPqaCERzOUAdh9Lfg5vigClR0K8GpLKJbOKYcyXSV5Oco2MdWmGX3X7wHElgPAzkprnfELmEP_XEgDao5O1z5ILDsJ8J95VwB9-iTmkTVxJ9AzuFKEhmrifbUmI74YzSD-D4PE0amY6GK-dym8_JslF09FvOo9h4XHaS5Libzcx9nUkkGzFxiSAPSvGUGEsE69DIjQ70U-5Skklglx693Zbqk3AXik7k0Fx6R4hC-EQtBFYGuKvl_UrMqfwqbBBLOfZfZqxotYE2nype3sxjlxSn-4XmYAESUZwL_QqEHzPriSg8m_kNpXlwV4cqTTVjLhEQwTBC8oWlxrM2hB64nGsXow5Xh08"

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
