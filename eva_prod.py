import socket
from mes_message_transfer import *
from configparser import ConfigParser
import datetime
from config import *
global check_in_result
check_in_result=False
def eva_prod(uid,mes_counter,file_path,pf):
    parse = ConfigParser()
    parse.read('config.ini', encoding='utf-8')
    HOST = parse.get('mes_addr', 'ip')
    PORT = int(parse.get('mes_addr', 'port'))
    pass_key = parse.get('pass_key', 'pass_key')
    time = datetime.datetime.now()
    #time_str = time.strftime("%Y%m%d%H%M%S")
    time_str = time.strftime("%Y%m%d%H%M%S"+'000')
    msg='UNIT_RESULT,EMR3MSRS,'+str(mes_counter)+','+time_str+',<UnitResult tokens=\"4\" uid_in=\"'+uid+'\" result=\"'+pf+'\" info=\"'+file_path+'\" />'
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    tcpCliSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    msg_bool=False
    get_reply_bool=False
    get_reply_msg=''
    time_out=0
    while True:
        if not msg_bool:
            tcpCliSock.send(msg_transfer_byte(msg))
            set_eva_prod_log('TO MES:' + msg)
            print(len(bytes(msg, 'utf-8')))
            time_out=10000
            #print(bytes(msg1, 'utf-8').hex())
            msg_bool=True
        data = tcpCliSock.recv(BUFSIZ)
        print(data)
        set_eva_prod_log('From MES:'+str(data))
        try:
            if 'UNIT_RESULT' in data.decode('utf-8'):
                break
        except:
            a=1

        time_out = time_out - 1
        if time_out == 0:
            break
            #break