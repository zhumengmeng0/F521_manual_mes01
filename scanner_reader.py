from pynput import mouse,keyboard
from checkin import *
from config import *

def scanner_read():
    global sn_text
    CODE = ""
    # 处理键盘输入的数据
    global a
    a=1
    def on_release(key):
        global CODE
        try:
            CODE += key.char
        except Exception as e:
            try:
                if key == key.enter:
                    if "" in CODE:
                        message = CODE
                        set_SN(message.upper())
                        set_Scanner_log('扫码/scan')
                        print(check_in(message.upper(),a))
                        print(message)
                        CODE = ""
            except Exception as e:
                CODE = ""

    #监听键盘扫码枪输入
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
    print('start listen')



