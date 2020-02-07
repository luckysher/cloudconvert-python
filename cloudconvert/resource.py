import uuid
import urllib
import cloudconvert.utils as util
from cloudconvert.cloudconvertrestclient import default_client


class Resource(object):
    """Base class for all REST services
    """
    convert_resources = {}

    def __init__(self, attributes=None, api_client=None):
        attributes = attributes or {}
        self.__dict__['api_client'] = api_client or default_client()

        super(Resource, self).__setattr__('__data__', {})
        super(Resource, self).__setattr__('error', None)
        super(Resource, self).__setattr__('headers', {})
        super(Resource, self).__setattr__('header', {})
        super(Resource, self).__setattr__('request_id', None)
        self.merge(attributes)

    def generate_request_id(self):
        """Generate uniq request id
        """
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())
        return self.request_id

    def http_headers(self):
        """Generate HTTP header
        """
        return util.merge_dict(self.header, self.headers,
                               {'CloudConvert-Request-Id': self.generate_request_id()})

    def __str__(self):
        return self.__data__.__str__()

    def __repr__(self):
        return self.__data__.__str__()

    def __getattr__(self, name):
        return self.__data__.get(name)

    def __setattr__(self, name, value):
        try:
            # Handle attributes(error, header, request_id)
            super(Resource, self).__getattribute__(name)
            super(Resource, self).__setattr__(name, value)
        except AttributeError:
            self.__data__[name] = self.convert(name, value)

    def __contains__(self, item):
        return item in self.__data__

    def success(self):
        return self.error is None

    def merge(self, new_attributes):
        """Merge new attributes e.g. response from a post to Resource
        """
        for k, v in new_attributes.items():
            setattr(self, k, v)

    def convert(self, name, value):
        """Convert the attribute values to configured class
        """
        if isinstance(value, dict):
            cls = self.convert_resources.get(name, Resource)
            return cls(value, api_client=self.api_client)
        elif isinstance(value, list):
            new_list = []
            for obj in value:
                new_list.append(self.convert(name, obj))
            return new_list
        else:
            return value

    def __getitem__(self, key):
        return self.__data__[key]

    def __setitem__(self, key, value):
        self.__data__[key] = self.convert(key, value)

    def to_dict(self):

        def parse_object(value):
            if isinstance(value, Resource):
                return value.to_dict()
            elif isinstance(value, list):
                return list(map(parse_object, value))
            else:
                return value

        return dict((key, parse_object(value)) for (key, value) in self.__data__.items())

    def to_json(self):

        def parse_object(value):
            if isinstance(value, Resource):
                return value.to_dict()
            elif isinstance(value, list):
                return list(map(parse_object, value))
            else:
                return value

        return dict((key, parse_object(value)) for (key, value) in self.__data__.items())


class Find(Resource):
    @classmethod
    def find(cls, id):
        """Locate resource e.g. job with given id
        Usage::
            >>> job = Job.find("s9fsf9-s9f9sf9s-ggfgf9-fg9fg")
        """
        api_client = default_client()

        url = util.join_url(cls.path, str(id))
        res = api_client.get(url)
        return res


class List(Resource):

    list_class = Resource

    @classmethod
    def all(cls, params=None):
        """Get list of payments as on
        https://cloudconvert.com/api/v2/tasks#tasks-list
        Usage::
            >>> tasks_list = tasks.all({'status': 'waiting'})
        """
        api_client = default_client()

        if params is None:
            url = cls.path
        else:
            url = util.join_url_params(cls.path, params)

        try:
            response = api_client.get(url)
            res = cls.list_class(response, api_client=api_client)
            return res.to_json()
        except AttributeError:
            # To handle the case when response is JSON Array
            if isinstance(response, list):
                new_resp = [cls.list_class(elem, api_client=api_client) for elem in response]
                return new_resp


class Create(Resource):

    @classmethod
    def create(cls, operation=None, payload={}):
        """Creates a resource e.g. task
        Usage::
            >>> task = Task({})
            >>> task.create(name=TASK_NAME) # return newly created task
        """

        api_client = default_client()
        url = util.join_url('v2', operation or '')
        new_attributes = api_client.post(url, payload, headers={})
        return new_attributes


class Upload(Resource):

    @classmethod
    def upload(cls, file_name, task):
        """Upload a resource e.g.
        """
        if not (task.get('data').get('operation') == 'import/upload'):
            raise Exception("The task operation is not import/upload'")

        import os
        if not os.path.exists(file_name):
            raise Exception("Does not find the exact path of the file: {}".format(file_name))

        form = task.get('data').get('result').get('form')
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


class Cancel(Resource):
    @classmethod
    def cancel(cls, id):
        """Cancel a resource for given Id e.g. task
        Usage::
            >>> Task.cancel("4534d-34gsf-54cxv-9cxv") # return True or False
        """
        api_client = default_client()
        url = util.join_url(cls.path, str(id), "cancel")
        api_resource = Resource()
        new_attributes = api_client.post(url, {}, {})
        api_resource.error = None
        api_resource.merge(new_attributes)
        return api_resource.success()


class Retry(Resource):
    @classmethod
    def retry(cls, id):
        """Retry a resource for given Id e.g. task
        Usage::
            >>> Task.retry("4534d-34gsf-54cxv-9cxv")
        """
        api_client = default_client()

        url = util.join_url(cls.path, str(id), "retry")
        res = api_client.post(url)
        return res


class Wait(Resource):
    @classmethod
    def wait(cls, id):
        """Wait resource e.g. job with given id
        Usage::
            >>> job = job.wait("s9fsf9-s9f9sf9s-ggfgf9-fg9fg")
        """
        api_client = default_client()

        url = util.join_url(cls.path, str(id), "wait")
        res = api_client.get(url)
        return res


class Show(Resource):
    @classmethod
    def show(cls, id):
        """show resource e.g. job with given id
        Usage::
            >>> job = Job.show("s9fsf9-s9f9sf9s-ggfgf9-fg9fg")
        """
        api_client = default_client()
        url = util.join_url(cls.path, str(id))
        res = api_client.get(url)
        return res


class Delete(Resource):
    @classmethod
    def delete(cls, id):
        """Deletes a resource e.g. task
        Usage::
            >>> Task.delete(TASK_ID)
        """
        api_client = default_client()
        url = util.join_url(cls.path, str(id))
        api_resource = Resource()
        new_attributes = api_client.delete(url)
        api_resource.error = None
        api_resource.merge(new_attributes)
        return api_resource.success()


class Post(Resource):
    @classmethod
    def post(cls, operation, payload=None):
        """Constructs url with passed in headers and makes post request via
        post method in rest client api class.
        Usage::
            >>> Task.post("create", {})
        """
        api_client = default_client()
        attributes = payload or {}
        url = util.join_url(cls.path, operation)
        print(url)
        return url
        if not isinstance(attributes, Resource):
            attributes = Resource(attributes, api=api_client)
        new_attributes = cls.api_client.post(url, attributes.to_dict(), attributes.http_headers())
        if isinstance(cls, Resource):
            cls.error = None
            cls.merge(new_attributes)
            return cls.success()
        else:
            return cls(new_attributes, api=api_client)