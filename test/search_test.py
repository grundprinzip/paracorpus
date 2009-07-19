import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import unittest
import search.filesearch as fs

class TestSerarch(unittest.TestCase):

    def setUp(self):
        self.data = ["test/top/de/f3.txt", "andere"]
        self.subject = fs.FileSearch(lang1="test/top/de")

    def test_get_files(self):
        files = self.subject.get_files()
        self.assertEqual(len(files), 4)
        self.assertEqual(files[0], "test/top/de/f1.txt")


    def test_search_task_simple(self):
        self.assertEqual(type(fs.search_task(self.data)), type([]))

    def test_search_taks_with_file(self):
        result = fs.search_task(self.data)

        t = result[0]
        self.assertEqual(t.offset, 3)

        t = result[1]
        self.assertEqual(t.offset, 5)


    def test_search_with_mult_inc_on_file(self):
        result = fs.search_task(["test/top/de/f3.txt", "es"])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].offset, 0)
        self.assertEqual(result[1].offset, 0)


if __name__ == "__main__":
    unittest.main()
        
