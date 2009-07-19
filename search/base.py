def smart_truncate(s, width = 1):
    if s[width].isspace():
        return s[0:width];
    else:
        return s[0:width].rsplit(None, 1)[0]


class Base(object):
    """
    The base class for all searches. It keeps the configuration
    options for each subclass and defines the basic interface
    """

    def __init__(self, **kwargs):
        self.options = kwargs 

    def start(self, handler=None):
        raise RuntimeError("Subclass Responsibility")

    def get_result(self):
        raise RuntimeError("Subclass Responsibility")

    def is_finished(self):
        raise RuntimeError("Subclass Responsibility")


class SearchResult(object):

    def __init__(self, w, c, loc, offset, begin, end):
        
        self.what = w
        self.content = c
        self.location = loc
        self.offset = offset
        self.begin = begin
        self.end = end

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "<SearchResult:[%s, %s @ %s[%d,%d,%d]]>" % (self.what, smart_truncate(self.content), self.location, self.offset, self.begin, self.end) 
