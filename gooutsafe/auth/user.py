class User(object):
    """
    This class represents an authenticated user.
    It is not a model, it is only a lightweight class used
    to represents an authenticated user.
    """
    id = None
    email = None
    is_active = None
    is_admin = None
    authenticated = None
    is_anonymous = False
    type = None
    extra_data = None

    @staticmethod
    def build_from_json(json: dict):
        kw = {key: json[key] for key in ['id', 'email', 'is_active', 'authenticated', 'is_anonymous', 'type']}
        extra = json
        all(map(extra.pop, kw))
        kw['extra'] = extra

        return User(**kw)

    def __init__(self, **kw):
        if kw is None:
            raise RuntimeError('You can\'t build the user with none dict')
        for (key, value) in kw:
            self[key] = value

    def is_authenticated(self):
        return self.authenticated

    def is_lha(self):
        return self.type == 'authority'

    def is_rest_operator(self):
        return self.type == 'operator'

    def is_customer(self):
        return self.type == 'customer'

    def __getattr__(self, item):
        if item in self:
            return self[item]
        elif item in self.extra_data:
            return self.extra_data[item]
        else:
            raise AttributeError('Attribute %s does not exist' % item)

    def __str__(self):
        s = 'User Object\n'
        for (key, value) in self:
            s += "%s=%s\n" % (key, value)
        return s