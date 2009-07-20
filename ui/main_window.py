from PyQt4 import QtGui
import os

from search.base import SearchIndex
import search.filesearch as fs

class ParaCorpusMainWindow(QtGui.QMainWindow):

    def prepare(self, wrapper):
        self.val = ""
        self.index = 0
        self.setWrapper(wrapper)
        self.wrapper.setupUi(self)

        # Changes to table
        self.wrapper.tblResult.setColumnCount(2)
        self.wrapper.tblResult.setColumnWidth(0, 50)
        self.wrapper.tblResult.setColumnWidth(1, 50)

        self.wrapper.tblResult.setHorizontalHeaderLabels(["Lang1", "Lang2"])

    def setWrapper(self, wrapper):
        self.wrapper = wrapper
        # initialize the search index
        self.search_index = SearchIndex("", searcher=fs.FileSearch)

    def searchClicked(self):
        val = str(self.wrapper.txtKeyword.text())
        self.lang1 = str(self.wrapper.cmblang1.currentText())
        self.lang2 = str(self.wrapper.cmblang2.currentText())
        
        # offsets
        if self.val != val:
            self.index = 0

        self.val = val
        # Execute the search
        self.wrapper.statusbar.showMessage("Searching...")
        self.search_index.deferred_search(str(self.val), str(self.lang1), self.callback_finished).start()

    def loadData(self):
        dirs = os.listdir(self.directory)
        # Filter the hidden dirs
        dirs = filter(lambda x: x[0] != ".", dirs)
        # Now set the values for the combo list
        for d in dirs:
            self.wrapper.cmblang1.addItem(d)
            self.wrapper.cmblang2.addItem(d)

    def loadClicked(self):
        print "Loaded"
        file = QtGui.QFileDialog.getOpenFileName(self, "Browse for Index")
        self.search_index = SearchIndex.load(str(file))
        self.directory = str(self.search_index.base)
        self.loadData()

    def saveClicked(self):
        print "Saved"
        self.search_index.base = self.directory
        self.search_index.store()

    def nextClicked(self):
        print "Next Clicked"
        if self.index + 100 < self.result_size:
            self.index += 100

        self.callback_finished(self.search_index.search(self.val, self.lang1))

    def prevClicked(self):
        print "Prev Clicked"
        if self.index < 100:
            self.index = 0
        else:
            self.index -= 100
        self.callback_finished(self.search_index.search(self.val, self.lang1))

    def callback_finished(self, result):

        self.result_size = len(result)
        self.wrapper.lblTotal.setText(str(self.result_size))
        self.wrapper.statusbar.showMessage("Finished Searching")
       
        self.wrapper.tblResult.horizontalHeader().resizeSection(0, 250)
        self.wrapper.tblResult.horizontalHeader().resizeSection(1, 250)
        if self.index + 100  > len(result):
            overall = len(result) - self.index
        else:
            overall = 100

        self.wrapper.tblResult.setRowCount(overall)
        
        # iterate over each result and 
        for res in range(overall):

            self.wrapper.tblResult.verticalHeader().resizeSection(res, 150)

            item_l1 = QtGui.QTableWidgetItem()
            item_l1.setText(self.search_index.find_line_for_result(result[self.index + res]))
            self.wrapper.tblResult.setItem(res, 0, item_l1)

            item_l2 = QtGui.QTableWidgetItem()
            item_l2.setText(self.search_index.find_ref_for_result(str(self.lang2), result[self.index + res]))
            self.wrapper.tblResult.setItem(res, 1, item_l2)


    def browseCorpusClicked(self):
        """Store where the parallel corpus is located"""
        self.directory = QtGui.QFileDialog.getExistingDirectory(self, "Browse for Corpus")

        # get the languages for this directory
        self.search_index.base = str(self.directory)
        self.loadData()

