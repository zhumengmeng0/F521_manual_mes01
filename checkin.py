import socket
from mes_message_transfer import *
from configparser import ConfigParser
import datetime
from config import *
global check_in_result
check_in_result=False
def check_in(uid,mes_counter):
    parse = ConfigParser()
    parse.read('config.ini', encoding='utf-8')
    HOST = parse.get('mes_addr', 'ip')
    PORT = int(parse.get('mes_addr', 'port'))
    pass_key = parse.get('pass_key', 'pass_key')
    time = datetime.datetime.now()
    #time_str = time.strftime("%Y%m%d%H%M%S")
    time_str = time.strftime("%Y%m%d%H%M%S"+'000')
    msg='UNIT_CHECKIN,EMR3MSRSM,'+str(mes_counter)+','+time_str+',<UnitCheckin tokens=\"2\" uid_in=\"'+uid+'\" />'
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
            set_checkin_log('TO MES:' + msg)
            print(len(bytes(msg, 'utf-8')))
            a=1000
            #print(bytes(msg1, 'utf-8').hex())
            msg_bool=True
        data = tcpCliSock.recv(BUFSIZ)
        print(data)
        set_checkin_log('From MES:'+str(data))
        #print(data)
        if data :
            #print(data)
            try:
                if 'UNIT_CHECKIN' in data.decode('utf-8'):
                    get_reply_bool=True
                    get_reply_msg=data.decode('utf-8')
            except:
                a=1
        if get_reply_bool:
            if pass_key in get_reply_msg:
                check_in_result=True
                set_check_in_bool('1')
                return 'pass'

            else:
                check_in_result=False
                set_check_in_bool('2')
                return 'fail'

            break
        time_out = time_out - 1
        if time_out == 0:
            break
            #break


'''
    msg1='IDENTIFICATION,'+station_id+','+str(mes_counter)+','+'1'
    msg2='SAVE_TESTPLAN,DQFHVI,'+str(mes_counter)+','+time_str+',<SaveTestplan uid_in="'+uid+'" tp_group="'+test_plan_group+'" tp_name="'+test_plan_name+'" hands_val="'+result+'" info="'+save_path+'"/>'
   # msg2 = 'SAVE_TESTPLAN,DQFHVI,' + str(
        #mes_counter) + ',' + time_str + ',<SaveTestplan uid_in="' + uid + '" tp_group="' + test_plan_group + '" tp_name="' + test_plan_name + '" hands_val="' + result + '"/>'
    #HOST = 'localhost'
    #PORT = 21567
    msg1_bool=False
    msg2_bool=False
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    tcpCliSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    while True:
        if not msg1_bool:
            tcpCliSock.send(msg_transfer_byte(msg1))
            print(len(bytes(msg1, 'utf-8')))
            #print(bytes(msg1, 'utf-8').hex())
            msg1_bool=True
        data = tcpCliSock.recv(BUFSIZ)
        print(data)
        if data and 'IDENTIFICATION' in data.decode('utf-8'):
            print(data.decode('utf-8'))
            tcpCliSock.send(msg_transfer_byte(msg2))
            print('send:' + msg2)
        if data and 'SAVE_TESTPLAN' in data.decode('utf-8'):
            print(data)
            break
'''