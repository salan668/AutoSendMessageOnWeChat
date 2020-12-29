"""
All rights reserved.
--Yang Song (songyangmri@gmail.com)
--2020/12/29
"""
import sys
import win32gui, win32con
import time
import pyperclip

import pyautogui as ag
from PyQt5.QtWidgets import *

from WechatProcess import Contact
from gui import Ui_Form


def window_enumeration_handler(hwnd, top_windows):
    """Add window title and ID to array."""
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


class GuiForm(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(GuiForm, self).__init__(parent)
        self.setupUi(self)

        self.contact = Contact()

        self.buttonContact.clicked.connect(self.Load)
        self.pushButton.clicked.connect(self.Run)

    def Load(self):
        dlg = QFileDialog()
        file_name, _ = dlg.getOpenFileName(self, 'Open JSON file', filter="json files (*.json)")
        if file_name:
            self.contact.LoadConfig(file_name)
            self.lineEditContact.setText(file_name)

    def Run(self):
        ag.PAUSE = 1

        top_windows = []
        win32gui.EnumWindows(window_enumeration_handler, top_windows)
        for (id, title) in sorted(top_windows, reverse=False):
            if win32gui.IsWindowVisible(id) and title and ('Program Manager' not in title) and \
                    ('Microsoft' not in title) and ('Window' not in title):
                win32gui.ShowWindow(id, win32con.SW_MINIMIZE)

        for (id, title) in sorted(top_windows, reverse=False):
            if '微信' in title and win32gui.IsWindowVisible(id):
                print(win32gui.GetWindowText(id))
                win32gui.ShowWindow(id, win32con.SW_NORMAL)
                win32gui.SetForegroundWindow(id)
                break

        for person, content in self.contact.Browse():
            time.sleep(1)
            ag.hotkey('ctrl', 'f')

            pyperclip.copy(person)
            ag.hotkey('ctrl', 'v')

            ag.keyDown('enter')

            pyperclip.copy(content)
            ag.hotkey('ctrl', 'v')

            ag.keyDown('enter')

        win32gui.MessageBox(id, 'Done', '', (win32con.MB_OK | win32con.MB_ICONINFORMATION))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_frame = GuiForm()
    main_frame.show()
    sys.exit(app.exec_())
