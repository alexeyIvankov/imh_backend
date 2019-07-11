
class HTTPException(Exception):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code

    def __str__(self):
        if self.code != None:
            return  repr(self.message) + repr(self.code)
        else:
            return repr(self.message)