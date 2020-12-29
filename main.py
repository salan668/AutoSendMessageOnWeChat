"""
命令行： python main.py "contact_test.json"

"""
import sys
import os
import win32gui, win32con
import time
import pyperclip

import pyautogui as ag
from PyQt5.QtWidgets import QMessageBox

from WechatProcess import Contact

from guiForm import GuiForm

def window_enumeration_handler(hwnd, top_windows):
    """Add window title and ID to array."""
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

if __name__ == '__main__':
    print(sys.argv)
    assert(len(sys.argv) == 2)
    config_path = sys.argv[1]
    assert(os.path.exists(config_path))

    ag.PAUSE = 1

    contact = Contact()
    contact.LoadConfig(config_path)
    print(contact.contact)

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

    for person, content in contact.Browse():
        time.sleep(1)
        ag.hotkey('ctrl', 'f')

        pyperclip.copy(person)
        ag.hotkey('ctrl', 'v')

        ag.keyDown('enter')

        pyperclip.copy(content)
        ag.hotkey('ctrl', 'v')

        ag.keyDown('enter')

    win32gui.MessageBox(id, 'Done', '', (win32con.MB_OK | win32con.MB_ICONINFORMATION))
