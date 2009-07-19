import search.filesearch as fs
from search.base import *
from time import time


si = SearchIndex.load("search_index_de-nl")

start = time()
res = si.search("Land","de")
end = time()

print "Found %d results in %d" % (len(res), end-start)
