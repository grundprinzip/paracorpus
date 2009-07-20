import threading
import os, re
from search import base
from utils import thread_pool as tp

# Search Config and options
POOL_SIZE = 5
FILE_TYPE_LIST = (".txt", ".doc")
DEFAULT_OPTIONS = {"remove_empty_lines": True, "remove_xml": True}

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def search_task(data):
    """
    A search task opens the given file and searches for a 
    search expression. Based on the occurences it will
    create a list of results

    data is an array of [file_name, search_exp]
    """
    result = []

    file_name = data[0]
    search_exp = re.compile(data[1], re.I)
    lang = data[2]

    # Get the search options
    if len(data) == 3:
        options = DEFAULT_OPTIONS
    else:
        options.update(data[3])

    fid = open(file_name)
    try:
        line_counter = 0 
        for line in fid:
            line_counter += 1
            if options["remove_empty_lines"] and len(line) == 0:
                continue
            if options["remove_empty_lines"]:
                line = remove_html_tags(line)

            # Compile the expression and search
            for m in re.finditer(search_exp, line):
                tmp = base.SearchResult(data[1], lang, "", file_name, line_counter, m.start(), m.end())
                result.append(tmp)


    finally:
        fid.close()

    return result


class FileSearch(base.Base):
    """
    This class implements a simple file based search algorithm. 
    The general idea is to scan a full directory with all 
    its files and return a list of matching results
    """

    def start(self, handler=None):

        self.__append_result_lock = threading.Condition(threading.Lock())

        self.started = True
        self.finished = False
        self.result = []

        self.files = self.get_files()
        # All files can now be processed with a nice and 
        # clean thread pool

        self.pool = tp.ThreadPool(POOL_SIZE)
        for f in self.files:
            self.pool.queueTask(search_task, (f, self.options["what"], self.options["lang1"]), self.append_result)
        self.pool.joinAll()

        # Reset State
        self.finished = True
        self.started = False

    def append_result(self, res):
        self.__append_result_lock.acquire()
        self.result += res
        self.__append_result_lock.release()

    def get_files(self):
        # Create a list of all files to scan
        files = []
        for dir in os.walk(self.options["lang1"]):

            for f in dir[2]:
                if os.path.splitext(f)[-1] in FILE_TYPE_LIST:
                    files.append(os.path.join(dir[0], f))
        return files

    def is_finished(self):
        return True if not self.started or self.finished else False
