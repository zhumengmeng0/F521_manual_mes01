import socket
from mes_message_transfer import *
from configparser import ConfigParser
import datetime

def send_msg_mes(uid,result,save_path,mes_counter):
    parse = ConfigParser()
    parse.read('config.ini', encoding='utf-8')
    HOST = parse.get('mes_addr', 'ip')
    PORT = int(parse.get('mes_addr', 'port'))
    time = datetime.datetime.now()
    #time_str = time.strftime("%Y%m%d%H%M%S")
    time_str = time.strftime("%Y%m%d")
    msg='UNIT_RESULT,EMR3MSRSM,'+str(mes_counter)+','+time_str+',<UnitResult tokens=\"4\" uid_in=\"'+uid+'\" result=\"'+result+'\" info=\"'+save_path+'\" />'
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    tcpCliSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    msg_bool=False
    while True:
        if not msg_bool:
            tcpCliSock.send(msg_transfer_byte(msg))
            print(len(bytes(msg, 'utf-8')))
            #print(bytes(msg1, 'utf-8').hex())
            msg_bool=True
        data = tcpCliSock.recv(BUFSIZ)
        print(data)
        if data and 'UNIT_RESULT' in data.decode('utf-8'):
            print(len(data))
            break
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