import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import unittest
import search.base
import search.filesearch as fs

class TestSerarch(unittest.TestCase):

    def setUp(self):
        self.data = [os.path.join("test", "top", "de", "f3.txt"), "andere", "de"]
        self.subject = fs.FileSearch(lang1=os.path.join("test", "top", "de"))

    def test_get_files(self):
        files = self.subject.get_files()
        self.assertEqual(len(files), 5)
        self.assertEqual(files[0], os.path.join("test", "top", "de", "ep-00-01-17.txt"))


    def test_search_task_simple(self):
        self.assertEqual(type(fs.search_task(self.data)), type([]))

    def test_search_taks_with_file(self):
        result = fs.search_task(self.data)

        t = result[0]
        #print t
        self.assertEqual(t.offset, 4)

        t = result[1]
        self.assertEqual(t.offset, 6)


    def test_search_with_mult_inc_on_file(self):
        result = fs.search_task([os.path.join("test", "top", "de", "f3.txt"), "es", "de"])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].offset, 1)
        self.assertEqual(result[1].offset, 1)

    def test_other_offset(self):
        si = search.base.SearchIndex(os.path.join("test", "top"), searcher=fs.FileSearch)
        res = si.search("martinmartin", "de")
        self.assertEqual(si.find_ref_for_result("nl", res[0]), "SaskiaSaskia")

    def test_self_offset(self):
        si = search.base.SearchIndex(os.path.join("test", "top"), searcher=fs.FileSearch)
        res = si.search("martinmartin", "de")
        
        self.assertEqual(si.find_line_for_result(res[0]), "MartinMartin")


if __name__ == "__main__":
    unittest.main()
        
