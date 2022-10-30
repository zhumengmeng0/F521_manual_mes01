import serial  # 导入串口包
import time
from checkin import check_in_result
from ui import *
from config import *
import datetime
import config
import eva_prod
from configparser import ConfigParser
import os
def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


def serial_read():
    parse = ConfigParser()
    parse.read('config.ini', encoding='utf-8')
    serial_port = parse.get('serial_port', 'serial_port')
    save_path = parse.get('save_path', 'save_path')
    ser = serial.Serial(serial_port, 9600, timeout=5)  # 开启com3口，波特率115200，超时5
    set_serial_log('打开串口/open serial:COM4,9600')
    ser.flushInput()  # 清空缓冲区
    time_now = datetime.datetime.now()
    time_str_day = time_now.strftime("%Y%m%d")
    time_str = time_now.strftime("%Y%m%d%H%M%S")
    time_str_hms=time.strftime("%Y-%m-%d %H:%M:%S")
    A=0
    while True:
        if A>0:
            A=A-1
        check_in_bool=get_check_in_bool()
        count = ser.inWaiting() # 获取串口缓冲区数据
        if count !=0 :
            recv = ser.read(ser.in_waiting).decode("gbk")  # 读出串口数据，数据采用gbk编码
            print(time.time()," ---  recv --> ", recv)  # 打印一下子
            if check_in_bool=='3':
                uid = get_SN()
                if A==0:
                    mkdir(save_path+time_str_day+'\\')
                    file_path=save_path+time_str_day+'\\'+uid+'_'+time_str+'.txt'
                A=5

                set_serial_log('From serial: '+recv)
                set_screw_bool('1')
                f=open(file_path,'a')
                f.write(time_str_hms+'  '+recv+'\n')
                f.close()
                set_save_serial_log('Save to: ' + uid+'_'+time_str+'.txt')

            else:
                print('check in not success,not record to txt')
        if get_send_eva()=='1' and get_record_bool()!='1':
            set_send_eva('0')
            mes_counter = get_mes_counter()
            eva_prod.eva_prod(uid, mes_counter, file_path,'P')
            set_mes_counter(mes_counter + 1)
            set_record_bool('1')
            if get_check_in_bool() == '3' and get_screw_bool() == '1' and get_record_bool() == '1':
                set_finish_bool('1')
                set_check_in_bool('0')
                set_ui_log(get_SN() + '操作完成/process finished')

        if get_send_eva()=='2' and get_record_bool()!='1':
            set_send_eva('0')
            mes_counter = get_mes_counter()
            eva_prod.eva_prod(uid, mes_counter, file_path,'F')
            set_mes_counter(mes_counter + 1)
            set_record_bool('1')
            if get_check_in_bool() == '3' and get_screw_bool() == '1' and get_record_bool() == '1':
                set_finish_bool('2')
                set_check_in_bool('0')
                set_ui_log(get_SN() + '手动下线/manual fail')
        time.sleep(0.1)  # 延时0.1秒，免得CPU出问题





