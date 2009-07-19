import search.filesearch as fs


s = fs.FileSearch(lang1="test/top/de", what="andere")

print s.get_files()

print "Starting execution..."
s.start()

print "Found %d results" % len(s.result)

for r in s.result:
    print r
