import gettext
from ui import mainui
from ui import main_window as mw

# Set the gettext application stuff
gettext.install("paracorpus")

import sys
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)

window = mw.ParaCorpusMainWindow()
window.prepare(mainui.Ui_MainWindow())
window.show()

sys.exit(app.exec_())
