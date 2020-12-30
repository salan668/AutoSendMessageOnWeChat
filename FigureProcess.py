"""
All rights reserved.
--Yang Song (songyangmri@gmail.com)
--2020/12/30
"""

import base64


def pic2str(file, functionName):
    with open(file, 'rb') as f:
        content = '{} = {}\n'.format(functionName, base64.b64encode(f.read()))

    with open('pic2str.py', 'a') as f:
        f.write(content)


if __name__ == '__main__':
    pic2str(r'src\alipay.jpg', 'ali')
    pic2str(r'src\wechatpay.jpg', 'wechat')
