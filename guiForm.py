"""
All rights reserved.
--Yang Song (songyangmri@gmail.com)
--2020/12/29
"""
import base64
import os
from io import BytesIO
import sys
import win32gui, win32con
import time
import pyperclip

import pyautogui as ag
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PIL import ImageQt, Image

from WechatProcess import Contact
from gui import Ui_Form

from pic2str import ali, wechat


def window_enumeration_handler(hwnd, top_windows):
    """Add window title and ID to array."""
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def ConvertByte2Image(code, picture_name):
    with open(picture_name, 'wb') as f:
        f.write(base64.b64decode(code))


class ClockCount(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        pass


class GuiForm(QWidget, Ui_Form):
    def __init__(self, parent=None):
        # self.thread = ClockCount()
        super(GuiForm, self).__init__(parent)
        self.setupUi(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ClockCount)
        self.remain_time = 10

        ConvertByte2Image(ali, 'ali.png')
        self.label_5.setPixmap(QtGui.QPixmap('ali.png'))
        os.remove('ali.png')
        ConvertByte2Image(wechat, 'wechat.png')
        self.label_6.setPixmap(QtGui.QPixmap('wechat.png'))
        os.remove('wechat.png')

        self.contact = Contact()

        self.buttonContact.clicked.connect(self.Load)
        self.pushButton.clicked.connect(self.Run)


    def Load(self):
        dlg = QFileDialog()
        file_name, _ = dlg.getOpenFileName(self, 'Open JSON file', filter="json files (*.json)")
        if file_name:
            self.contact.LoadConfig(file_name)
            self.lineEditContact.setText(file_name)

    def ClockCount(self):
        if self.remain_time > 0:
            self.remain_time -= 1
        else:
            self.timer.stop()
        self.labelRemainTime.setText('激活微信剩余时间：\n{}s'.format(self.remain_time))

    def Run(self):
        ag.PAUSE = 1

        self.timer.start(1000)

        for person, content in self.contact.Browse():
            time.sleep(1)
            ag.hotkey('ctrl', 'f')

            pyperclip.copy(person)
            ag.hotkey('ctrl', 'v')

            ag.keyDown('enter')

            pyperclip.copy(content)
            ag.hotkey('ctrl', 'v')

            ag.keyDown('enter')

        QMessageBox.about(self, 'Done', 'Done')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_frame = GuiForm()
    main_frame.show()
    sys.exit(app.exec_())
