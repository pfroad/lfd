class Result(object):
    def __init__(self, status=True, data=None, error=None):
        self.status = status
        self.data = data
        self.error = error