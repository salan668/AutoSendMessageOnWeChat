"""
All rights reserved.
--Yang Song (songyangmri@gmail.com)
--2020/12/28
"""
import json
import pyautogui as ag
import pyperclip
import time

# search_window = (330, 80)
# first_person = (388, 246)

DEFAULT_KEY = '为了避免重名的默认消息'
content_dict = {
    DEFAULT_KEY: '默认消息',
    '文件传输助手': '',
    # '张敬': 'python消息'
}

class Contact(object):
    def __init__(self, contact=None):
        if contact is None:
            self.contact = {}
        else:
            self.contact = contact

        self._UpdateDefaultMessage()

    def _UpdateDefaultMessage(self):
        if DEFAULT_KEY in self.contact.keys():
            self.default_message = self.contact[DEFAULT_KEY]
        else:
            self.default_message = ''

    def Browse(self):
        for person, content in self.contact.items():
            if person == DEFAULT_KEY:
                continue

            if content:
                yield person, content
            else:
                yield person, self.default_message

    def LoadConfig(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.contact = json.load(f)
            self._UpdateDefaultMessage()

    def SaveConfig(self, store_path):
        with open(store_path, 'w', encoding='utf-8') as f:
            json.dump(self.contact, f, indent=2, ensure_ascii=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ag.PAUSE = 0.5

    print(ag.position())
    width, height = ag.size()
    print(width, height)

    # contact = Contact(content_dict)
    # contact.SaveConfig('contact_test.json')
    # del contact

    contact = Contact()
    contact.LoadConfig('contact_test.json')

    time.sleep(5)

    for person, content in contact.Browse():
        ag.hotkey('ctrl', 'f')

        pyperclip.copy(person)
        ag.hotkey('ctrl', 'v')

        ag.keyDown('enter')

        pyperclip.copy(content)
        ag.hotkey('ctrl', 'v')

        ag.keyDown('enter')


