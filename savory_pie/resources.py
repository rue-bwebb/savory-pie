from django.core.exceptions import ObjectDoesNotExist

#protocol Resource:
#   def get(self, api_request): dict
#   def post(self, api_request)
#   def put(self, api_request): resource_path
#   def delete(self, api_request)
#   def get_child_resource(self, path_fragment, light): Resource or None


class APIResource(object):
    def __init__(self):
        self._child_resources = dict()

    def register(self, name, resource):
        self._child_resources[name] = resource
        return self

    def register_class(self, name, resource_class):
        return self.register(name, resource_class())

    def get_child_resource(self, path_fragment, light):
        return self._child_resources.get(path_fragment, None)


class QuerySetResource(object):
    # resource_class
    def __init__(self, queryset=None):
        self.queryset = queryset or self.resource_class.model_class.objects.all()

    def filter_queryset(self, **kwargs):
        return self.queryset.filter(**kwargs)

    def to_resource(self, model):
        return self.resource_class(model)

    def prepare(self, queryset):
        try:
            return self.resource_class.prepare(queryset)
        except KeyError:
            return queryset

    def get(self, api_request):
        queryset = self.prepare(self.filter_queryset(**api_request.GET))

        objects = []
        for model in queryset:
            resource = self.to_resource(model)
            objects.append(resource.get(api_request.synthetic_get(str(resource.key))))

        return {
            'objects': objects
        }

    def post(self, api_request):
        # This is a bit of an abuse of HTTP semantics...
        # - creates an initially unaddressable resource
        # - then PUT-s to the unaddressable resource - using the original POST request
        # After that is done, the resource becomes addressable -- via its key

        # NOTE: This is contrast to get which is called with an internal
        # sub-request with the appropriate URI.

        resource = self.resource_class.create_resource()
        resource.put(api_request.synthetic_put('does-not-exist'))
        return api_request.resource_path + '/' + resource.pk

    def get_child_resource(self, path_fragment):
        try:
            model = self.resource_class.get_from_queryset(
                self.prepare(self.queryset),
                path_fragment
            )
            return self.to_resource(model)
        except ObjectDoesNotExist:
            return None


class ModelResource(object):
    # model_class
    published_key = ('pk', int)
    fields = []

    @classmethod
    def get_from_queryset(cls, queryset, path_fragment):
        attr, type_ = cls.published_key

        kwargs = dict()
        kwargs[attr] = type_(path_fragment)
        return queryset.get(**kwargs)

    @classmethod
    def create_resource(cls):
        return cls(cls.model_class())

    @classmethod
    def prepare(cls, queryset):
        prepared_queryset = queryset
        for field in cls.fields:
            prepared_queryset = field.prepare(prepared_queryset)
        return prepared_queryset

    def __init__(self, model):
        self.model = model

    @property
    def key(self):
        attr, type_ = self.published_key
        return str(getattr(self.model, attr))

    def get(self, api_request):
        target_dict = dict()

        for field in self.fields:
            field.handle_outgoing(api_request, self.model, target_dict)

        return target_dict

    def put(self, api_request):
        print 'api_request.body_dict', api_request.body_dict

        for field in self.fields:
            field.handle_incoming(api_request, api_request.body_dict, self.model)

        self.model.save()

    def delete(self, api_request):
        self.model.delete()
