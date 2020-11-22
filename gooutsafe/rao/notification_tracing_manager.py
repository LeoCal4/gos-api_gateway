from gooutsafe import app
from flask import abort
import requests

class NotificationTracingManager:

    NOTIFICATION_ENDPOINT = app.config['NOTIFICATION_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def retrieve_by_target_user_id(cls,user_id: int):
        try:
            response = requests.get("%s/notifications/%s" % (cls.NOTIFICATION_ENDPOINT, str(user_id)), 
                        timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            if response.status_code == 200:
                #there are notifications
                return json_payload
            elif response.status_code == 404:
                return []
            else:
                raise RuntimeError('Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        pass


    @classmethod
    def get_contact_tracing_list(cls,customer_id: int):
        #TODO
        pass