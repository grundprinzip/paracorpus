import search.filesearch as fs
from search.base import *
from time import time


si = SearchIndex("de-nl", searcher=fs.FileSearch)

print "Starting execution..."

start = time()
res = si.search("Land", "de")
end = time()

print "Found %d results in %d" % (len(res), end-start)

si.store()

#for r in s.result:
#    print r
