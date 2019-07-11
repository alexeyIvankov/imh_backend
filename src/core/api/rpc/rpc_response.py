
from django.http import HttpResponse
import json


class Error(object):
    message:str
    code:int

class Success(object):
    data:object

class Response(object):
    success:Success
    error:Error

    def json(self):
        my_json = json.dumps(self, default=lambda o: o.__dict__,
                   sort_keys=True, indent=4)
        return HttpResponse(my_json, content_type='application/json')


