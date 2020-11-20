import os

import requests
from requests.adapters import TimeoutSauce
from gooutsafe import app


REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']


class CustomTimeout(TimeoutSauce):
    def __init__(self, *args, **kwargs):
        if kwargs["connect"] is None:
            kwargs["connect"] = REQUESTS_TIMEOUT_SECONDS
        super().__init__(*args, **kwargs)


# Set it globally, instead of specifying ``timeout=..`` kwarg on each call.
requests.adapters.TimeoutSauce = CustomTimeout