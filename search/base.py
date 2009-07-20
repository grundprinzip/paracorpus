import linecache, re, os
import cPickle as pickle
import threading


def smart_truncate(s, width = 10):
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

    def __init__(self, w, lang, c, loc, offset, begin, end):
        
        self.what = w
        self.lang = lang
        self.content = c
        self.location = loc
        self.offset = offset
        self.begin = begin
        self.end = end

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "<SearchResult:[%s, %s @ %s[%d,%d,%d]]>" % (self.what, smart_truncate(self.content), self.location, self.offset, self.begin, self.end) 

class ThreadedSearch(threading.Thread):

    def __init__(self, context, what, lang, callback):
        threading.Thread.__init__(self)
        self.ctx = context
        self.lang = lang
        self.what = what
        self.callback = callback

    def run(self):
        res = self.ctx.search(str(self.what), str(self.lang))
        self.callback(res)


class SearchIndex(object):
    """
    Persistence around different searches to speed up the overall corpus
    search
    """
    def __init__(self, base, searcher=None):
        self.data = {}
        self.base = base
        self.searcher = searcher

    def make_key(self, what, lang):
        return (lang.lower(), what)

    def search(self, what, lang1):
        """
        Perform the search and store it in a local cache
        """
        if not self.data.has_key(self.make_key(what, lang1)):
            instance = self.searcher(what=what,lang1=os.path.join(str(self.base), str(lang1)))
            instance.start()
            self.data[self.make_key(what, lang1)] = instance.result
          
        return self.data[self.make_key(what, lang1)]

    def deferred_search(self, what, lang1, callback):
        """
        Create a thread object that can be used to start the search
        and pass a callback to the thread so that
        it is called when its finished
        """
        return ThreadedSearch(self, what, lang1, callback)

    def store(self):
        fid = open("search_index_.idx", "w+")
        pickle.Pickler(fid, pickle.HIGHEST_PROTOCOL).dump(self)
        fid.close()

    def find_ref_for_result(self, lang, match):
        """
        Analyze the search result and open the corresponding file
        and display the result
        """
        file_name = os.path.join(str(self.base), lang, os.path.basename(match.location))
        return linecache.getline(str(file_name), match.offset).strip()
    
    def find_line_for_result(self, match):
        """
        Return the actual text line for this mathc
        """
        return linecache.getline(match.location, match.offset).strip()

    @classmethod 
    def load(self, file):
        fid = open(file, "rb")
        obj = pickle.Unpickler(fid).load()
        fid.close()
        return obj
