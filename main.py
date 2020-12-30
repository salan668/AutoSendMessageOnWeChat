"""
命令行： python main.py "contact_test.json"

"""

import sys
import qdarkstyle

from PyQt5.QtWidgets import *

from guiForm import GuiForm

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    main_frame = GuiForm()
    main_frame.show()
    sys.exit(app.exec_())
