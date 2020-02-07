from cloudconvert.resource import List, Find, Create, Delete, Wait, Show, Resource, Cancel, Retry


class Upload(Resource):

    @classmethod
    def upload(cls, file_name, task):
        """Upload a resource e.g.
        """
        if not (task.get('operation') == 'import/upload'):
            raise Exception("The task operation is not import/upload")

        import os
        if not os.path.exists(file_name):
            raise Exception("Does not find the exact path of the file: {}".format(file_name))

        form = task.get('result').get('form')
        port_url = form.get('url')
        params = form.get('parameters')
        try:
            file = open(file_name, 'rb')

            files = {'file': file}

            import requests
            res = requests.request(method='POST', url=port_url, files=files, data=params)
            file.close()
            return True if res.status_code == 201 else False

        except Exception as e:
            print("got exception while uploading file")
            print(e)

        return False


class Task(List, Find, Create, Wait, Cancel, Retry, Show, Delete, Upload):
    """Task class wrapping the REST v2/tasks endpoint. Enabling New Task Creation, Showing a task, Waiting for task,
    Finding a task, Deleting a task, Cancelling a running task.

    Usage::
        >>> tasks = Task.all({"page": 5})
        >>> task = Task.find("<TASK_ID>")
        >>> Task.create(name="import/url")
        >>> Task.delete(<TASK_ID>)     # return True or False
        >>> Task.cancel(<TASK_ID>)     # return True or False
    """

    path = "v2/tasks"


Task.convert_resources['tasks'] = Task
Task.convert_resources['task'] = Task

