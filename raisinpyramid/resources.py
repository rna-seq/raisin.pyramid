"""Implementation of the Root object"""

class Root(object):
    """Root object for Pyramid"""

    def __init__(self, request):
        self.request = request
