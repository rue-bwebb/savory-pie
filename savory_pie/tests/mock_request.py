from StringIO import StringIO
from savory_pie import views

def savory_dispatch(root_resource, method, resource_path='', body=None, GET=None, POST=None):
    view = views.api_view(root_resource)
    request = Request(
        method=method,
        resource_path=resource_path,
        body=body,
        GET=GET,
        POST=POST
    )

    return view(request=request, resource_path=resource_path)


class Request(object):
    def __init__(self, method, host='localhost', resource_path='', body=None, GET=None, POST=None):
        self.host = host
        self.resource_path = resource_path

        self.method = method
        self.body = body
        self.body_file = None

        self.GET = GET or {}
        self.POST = POST or {}
        self.REQUEST = dict(self.GET, **self.POST)

    def get_full_path(self):
        return 'api/' + self.resource_path

    def build_absolute_uri(self, django_path):
        return 'http://' + self.host + '/' + django_path

    def read(self):
        if not self.body_file:
            self.body_file = StringIO(self.body)

        return self.body_file.read()