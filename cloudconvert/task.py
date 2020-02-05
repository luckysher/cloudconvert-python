from cloudconvert.resource import List, Find, Create, Post, Delete, Wait, Show, Resource, Cancel, Retry, Upload


class Task(List, Find, Create, Post, Wait, Cancel, Retry, Show, Delete, Upload):
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

