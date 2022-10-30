# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo.py'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!
import os
import shutil
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
import cv2
import time
import mediapipe as mp
import get_uid_from_log
from tkinter import *
from PIL import Image, ImageTk
import get_uid_from_log
from configparser import ConfigParser
import datetime
import math
import numpy
import socket
import threading
from playsound import playsound

#playsound('test.mp3')
# 获取当前系统时间
#导入初始化参数
parse = ConfigParser()
parse.read('config.ini', encoding='utf-8')
trigger_mode = parse.get('trigger_mode', 'trigger_mode')
log_path = parse.get('log_file_path', 'path')
x_left_top=parse.get('monitor_rect', 'x_left_top')
y_left_top=parse.get('monitor_rect', 'y_left_top')
x_right_bottom=parse.get('monitor_rect', 'x_right_bottom')
y_right_bottom=parse.get('monitor_rect', 'y_right_bottom')
x_left_top_nose=int(parse.get('nose_position', 'x_left_top'))
y_left_top_nose=int(parse.get('nose_position', 'y_left_top'))
x_right_bottom_nose=int(parse.get('nose_position', 'x_right_bottom'))
y_right_bottom_nose=int(parse.get('nose_position', 'y_right_bottom'))
time_out=parse.get('check_time_out','time_out')
camera_no=parse.get('camera_no','camera_no')
time_out_start=int(parse.get('check_time_out_start','time_out'))
distance_limit=int(parse.get('finger_distance','distance_limit'))
HOST=parse.get('mes_addr','ip')
PORT=int(parse.get('mes_addr','port'))
station_id=parse.get('mes_info','station_id')
test_plan_group=parse.get('mes_info','test_plan_group')
test_plan_name=parse.get('mes_info','test_plan_name')
hand_position=int(parse.get('hand_position','hand_position'))
nose_position_display=int(parse.get('nose_position_display','nose_position_display'))
hold_time=parse.get('hold_time','time_hold')
save_video_path=parse.get('save_video_path','save_video_path')
save_video_bool=parse.get('save_video_bool','save_video_bool')
mask_x=int(parse.get('mask_size','x'))
mask_y=int(parse.get('mask_size','y'))
img_resolution_x=int(parse.get('img_resolution','x'))
img_resolution_y=int(parse.get('img_resolution','y'))
min_detection_confidence=float(parse.get('confidence','min_detection_confidence'))
min_tracking_confidence=float(parse.get('confidence','min_tracking_confidence'))
#上面是从config初始化所有的参数
mes_counter=1
def msg_transfer_byte(msg):
    msg_byte=bytes(msg, 'utf-8')
    msg_arr=[hex(x) for x in msg_byte]
    print(msg_arr)
    length=len(msg_byte)+2
    print(hex(length))
    msg_arr=['0x00','0x00','0x00']+[hex(length)]+['0x02']+msg_arr+['0x03']
    print(msg_arr)
    msg_hex=''
    for x in msg_arr:
        msg_hex=msg_hex+x[2:4]
    print(msg_hex)
    msg_byte=bytes.fromhex(msg_hex)
    print(msg_byte)
    return msg_byte
def send_msg_mes(uid,result,save_path):
    time = datetime.datetime.now()
    #time_str = time.strftime("%Y%m%d%H%M%S")
    time_str = time.strftime("%Y%m%d")
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
    tcpCliSock.close()


def record_result(uid,result):
    time = datetime.datetime.now()
    f=open('result.txt','a')
    f.write(time.strftime("%Y-%m-%d %H:%M:%S")+'   '+uid+'   '+result+'\n')
    f.close()

mpPose = mp.solutions.holistic  # 姿态识别方法
pose = mpPose.Holistic(static_image_mode=False,  # 静态图模式，False代表置信度高时继续跟踪，True代表实时跟踪检测新的结果
                       # upper_body_only=True,  # 是否只检测上半身
                       smooth_landmarks=True,  # 平滑，一般为True
                       min_detection_confidence=min_detection_confidence,  # 检测置信度
                       min_tracking_confidence=min_tracking_confidence)  # 跟踪置信度
# 检测置信度大于0.5代表检测到了，若此时跟踪置信度大于0.5就继续跟踪，小于就沿用上一次，避免一次又一次重复使用模型
# 导入绘图方法
mpDraw = mp.solutions.drawing_utils
def paint_mask(img,x_left,x_right,y_left,y_right):
    for m in range(x_left, y_right):
        for n in range(y_left, y_right):
            if m % 10 == 0 and n % 10 == 0:  # 将10 * 10的方格内的像素颜色，设置与[m,n]点颜色相同
                for i in range(10):
                    for j in range(10):
                        b, g, r = img[m, n]
                        img[i + m, j + n] = (b, g, r)
    return img
def get_img_ana(img):
    nose_bool = False
    # 导入姿态跟踪方法

    #print(1)
    arr_single = []
    count_action = 0
    count_pass = 0
    count_fail = 0
    display_pass = 0
    display_fail = 0
    left_hand_bool = False
    right_hand_bool = False
    finger_distance=9999

    size = img.shape
    h = img.shape[0]
    w = img.shape[1]

    # 将导入的BGR格式图像转为RGB格式
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #print(2)
    # 将图像传给姿态识别模型
    results = pose.process(imgRGB)
    #print(3)
    # 查看体态关键点坐标，返回x,y,z,visibility
    #print(results.pose_landmarks)

    # 如果检测到体态就执行下面内容，没检测到就不执行
    parse.read('config.ini', encoding='utf-8')
    x_left_top = parse.get('monitor_rect', 'x_left_top')
    y_left_top = parse.get('monitor_rect', 'y_left_top')
    x_right_bottom = parse.get('monitor_rect', 'x_right_bottom')
    y_right_bottom = parse.get('monitor_rect', 'y_right_bottom')
    #a = (250, 340, 630, 470)
    a = (int(x_left_top), int(y_left_top), int(x_right_bottom), int(y_right_bottom))
    # 左上角和右下角
    cv2.rectangle(img, (a[0], a[1]), (a[2], a[3]), (255, 0, 0), 2)
    if results.pose_landmarks:
        nose_x= str(round(results.pose_landmarks.landmark[0].x * w, 5))
        nose_y = str(round(results.pose_landmarks.landmark[0].y * h, 5))
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        nose_x_float=int(float(nose_x))
        nose_y_float=int(float(nose_y))
        mask_x=150
        mask_y=150
        x_left_mask=nose_x_float-mask_x
        x_right_mask=nose_x_float+mask_x
        y_left_mask = nose_y_float - mask_y
        y_right_mask = nose_y_float + mask_y

        #img_mask=img
        #img=paint_mask(img,x_left_mask,x_right_mask,y_left_mask,y_right_mask)

        if x_left_mask>0 and y_left_mask>0 and x_right_mask>0 and y_right_mask>0:
            '''
            Grayimg = cv2.cvtColor(img_mask, cv2.COLOR_BGR2GRAY)
            img2 = np.zeros_like(img_mask)
            #img2[:, :, 0] = Grayimg
            #img2[:, :, 1] = Grayimg
            #img2[:, :, 2] = Grayimg
            img_mask= cv2.GaussianBlur(img2, (0, 0), 15)
            '''
            #Mask1 = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)

            img_mask = cv2.imread('mask.png')
            #img_mask = cv2.resize(img_mask, (y_right_mask-y_left_mask, x_right_mask-x_left_mask))  # 修改为480*640
            #img_mask=

            img_mask_raw=img[y_left_mask:y_right_mask,x_left_mask:x_right_mask]
            cv2.circle(img_mask_raw,(150,150),150,(0,0,0),-1)
            print(img_mask.shape)
            print(img_mask_raw.shape)
            #cv2.circle(img,(nose_x_float,nose_y_float),100,mask=img_mask)
            #img= cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=Mask1)
            img_mask_add=cv2.add(img_mask,img_mask_raw)
            img[y_left_mask:y_right_mask, x_left_mask:x_right_mask]=img_mask_add


    if results.pose_landmarks and results.left_hand_landmarks and results.right_hand_landmarks:
        # 绘制姿态坐标点，img为画板，传入姿态点坐标，坐标连线
        #print('--------------')

        x_left = str(round(results.left_hand_landmarks.landmark[hand_position].x * w, 5))
        y_left = str(round(results.left_hand_landmarks.landmark[hand_position].y * h, 5))
        nose_x= str(round(results.pose_landmarks.landmark[0].x * w, 5))
        nose_y = str(round(results.pose_landmarks.landmark[0].y * h, 5))
        if float(x_left) > a[0] and float(x_left) < a[2] and float(y_left) > a[1] and float(y_left) < a[3]:
            left_hand_bool = True
        x_right = str(round(results.right_hand_landmarks.landmark[hand_position].x * w, 5))
        y_right = str(round(results.right_hand_landmarks.landmark[hand_position].y * h, 5))
        if float(x_right) > a[0] and float(x_right) < a[2] and float(y_right) > a[1] and float(y_right) < a[3]:
            right_hand_bool = True
        finger_distance=math.sqrt(numpy.square(float(x_left)-float(x_right))+numpy.square(float(y_left)-float(y_right)))
        # print(frames_to_timecode(fps, i))
        # print(results.pose_landmarks)
        # print(results.left_hand_landmarks)
        #print(str(results.pose_landmarks).split('landmark'))
        #print(str(results.left_hand_landmarks).split('landmark'))
        #print(str(results.right_hand_landmarks).split('landmark'))
        '''
        for i in range(1, len(str(results.pose_landmarks).split('landmark'))):
            position = str(results.pose_landmarks).split('landmark')[i].replace('\n', '').replace(' ',
                                                                                                  '').replace(
                '{', '').replace('}', '')
            position = position.replace('x:', '').replace('y:', ',').replace('z:', ',').replace('visibility:',
                                                                                                ',').replace(
                'visibilit', '')
            # print(position)
            arr_position = position.split(',')
            new_postion = []
            for each in arr_position:
                each_float = round(float(each), 5)
                new_postion.append((each_float))
            print(new_postion)
            text = text + ' ' + str(results.pose_landmarks).split('landmark')[i].replace('\n', '').replace(' ',
                                                                                                           '').replace(
                '{', '').replace('}', '')
            arr_single.append(str(new_postion))
        for i in range(1, len(str(results.left_hand_landmarks).split('landmark'))):
            position = str(results.left_hand_landmarks).split('landmark')[i].replace('\n', '').replace(' ',
                                                                                                       '').replace(
                '{', '').replace('}', '')
            position = position.replace('x:', '').replace('y:', ',').replace('z:', ',').replace('visibility:',
                                                                                                ',').replace(
                'visibilit', '')
            # print(position)
            arr_position = position.split(',')
            new_postion = []
            for each in arr_position:
                each_float = round(float(each), 5)
                new_postion.append((each_float))
            print(new_postion)
            text = text + ' ' + str(results.left_hand_landmarks).split('landmark')[i].replace('\n', '').replace(
                ' ', '').replace('{', '').replace('}', '')
            arr_single.append(str(new_postion))
        for i in range(1, len(str(results.right_hand_landmarks).split('landmark'))):
            position = str(results.right_hand_landmarks).split('landmark')[i].replace('\n', '').replace(' ',
                                                                                                        '').replace(
                '{', '').replace('}', '')
            position = position.replace('x:', '').replace('y:', ',').replace('z:', ',').replace('visibility:',
                                                                                                ',').replace(
                'visibilit', '')
            # print(position)
            arr_position = position.split(',')
            new_postion = []
            for each in arr_position:
                each_float = round(float(each), 5)
                new_postion.append((each_float))
            # print(new_postion)
            text = text + ' ' + str(results.pose_landmarks).split('landmark')[i].replace('\n', '').replace(' ',
                                                                                                           '').replace(
                '{', '').replace('}', '')
            arr_single.append(str(new_postion))
        print('--------------')
        '''

        #time.sleep(0.1)

        #cv2.putText(img, ('count_pass=' + str(count_pass)), (70, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0),
                    #2)
        #print(1)


        #if nose_position_display > 0:
        cv2.putText(img, ('Left_hand:' + x_left), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.putText(img, ('Right_hand:' + x_right), (10, 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        #if float(nose_x)< x_right_bottom_nose and float(nose_x)>x_left_top_nose and float(nose_y)<y_right_bottom_nose and float(nose_y)>y_left_top_nose:
            #cv2.putText(img, ('in the work position'), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            #nose_bool=True

        mpDraw.draw_landmarks(img, results.left_hand_landmarks, mpPose.HAND_CONNECTIONS)
        mpDraw.draw_landmarks(img, results.right_hand_landmarks, mpPose.HAND_CONNECTIONS)

        #else:
            #cv2.putText(img, ('out of work position'), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    return img,left_hand_bool,right_hand_bool,finger_distance,nose_bool
def set_image_to_tk(tk_label, img_path, img_size=None):
    img_open = img_path
    if img_size is not None:
        height, width = img_size
        img_h, img_w = img_open.size

        if img_w > width:
            size = (width, int(height * img_w / img_h))
            img_open = img_open.resize(size, Image.ANTIALIAS)

        elif img_h > height:
            size = (int(width * img_h / img_w), height)
            img_open = img_open.resize(size, Image.ANTIALIAS)

    img = ImageTk.PhotoImage(img_open)
    tk_label.config(image=img)
    tk_label.image = img
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

def ui():
    parse.read('config.ini', encoding='utf-8')
    img_resolution_x = int(parse.get('img_resolution', 'x'))
    img_resolution_y = int(parse.get('img_resolution', 'y'))
    last_uid = get_uid_from_log.get_uid_from_log(log_path)[1]
    root = Tk()
    root.title('DQ200 FPC Video Stream AI motion inspection')
    #root.minsize(1920, 1080)  # 最小尺寸
    #root.maxsize(1920, 1080)  # 最大尺寸
    root.geometry('1800x1080')
    root.resizable(0, 0)
    #frame1 = Frame(root, bd=2, relief=GROOVE)
    #frame1.pack(side=TOP, fill=BOTH, ipadx=0, ipady=5, expand=0)
    #视频显示区域 frame1
    frame00 = Frame(root, bd=0, relief=GROOVE,background='black')
    frame00.pack(side=TOP, fill='both', ipadx=0, ipady=0, expand=0)
    product_infor_area_0 = Label(frame00,text='Vitesco Tianjin Video Stream AI', font=('微软雅黑', 30),fg='yellow',bg='black')
    product_infor_area_0.pack(side="top", padx=20, pady=5)
    frame01 = Frame(root, bd=0, relief=RIDGE,background='dimgray')
    frame01.pack(side=TOP, fill='both', ipadx=0, ipady=0, expand=0)
    product_infor_area_1 = Label(frame01, text='产品信息/SN:', font=('微软雅黑', 20),fg='white',bg='dimgray')
    product_infor_area_1.pack(side=LEFT, padx=10, pady=0)
    product_infor_area_2 = Label(frame01, text='', font=('微软雅黑', 20),fg='white',bg='dimgray')
    product_infor_area_2.pack(side=LEFT, padx=20, pady=0)

    video_stream = cv2.VideoCapture(int(camera_no))
    video_stream.set(cv2.CAP_PROP_FRAME_WIDTH, img_resolution_x)
    video_stream.set(cv2.CAP_PROP_FRAME_HEIGHT, img_resolution_y)
    #video_stream = cv2.VideoCapture('FF1_4.mp4')
    frame2 = Frame(root, bd=1, relief=GROOVE,bg='gray')
    frame2.pack(side=LEFT, fill='y', ipadx=0, ipady=0, expand=0)

    check_in_label_8 = Label(frame2, text='状态信息/Status: ', font=('微软雅黑', 20),anchor='w',fg='white',bg='gray')
    check_in_label_8.pack(side="top", padx=10, pady=10)
    check_flow_1= Label(frame2, text='产品进入\nCheck in', font=('微软雅黑', 17),fg='black',bg='yellow',bd=3,relief='raised')
    check_flow_1.pack(side="top", ipadx=10, ipady=10,padx=5, pady=10)
    check_flow_2= Label(frame2, text='⭣', font=('微软雅黑',20),bg='gray',fg='white')
    check_flow_2.pack(side="top", padx=0, pady=0)
    check_flow_3= Label(frame2, text='动作检测\nInspection', font=('微软雅黑', 17),fg='black',bg='yellow',bd=3,relief='raised')
    check_flow_3.pack(side="top", ipadx=10, ipady=5,padx=5, pady=10)
    check_flow_4= Label(frame2, text='⭣', font=('微软雅黑', 20),bg='gray',fg='white')
    check_flow_4.pack(side="top", padx=0, pady=0)
    check_flow_5= Label(frame2, text='判定结果\nResult', font=('微软雅黑', 17),fg='black',bg='yellow',bd=3,relief='raised')
    check_flow_5.pack(side="top", ipadx=10, ipady=5,padx=5, pady=10)
    check_result= Label(frame2, text='        ', font=('微软雅黑', 30,"bold"),fg='red',bg='yellow')
    check_result.pack(side="top", ipadx=15, ipady=35,padx=0, pady=10)
    frame1 = Frame(root, bd=2, relief=GROOVE,bg='black')
    frame1.pack(side=LEFT, fill='y', ipadx=0, ipady=0, expand=0)
    #video_label = Label(frame1, text='实时画面(蓝框为检测区域)\nRealtime video(Blue Frame is the inspection area)', font=('隶书', 5),fg='white',bg='black')
    #video_label.pack(side="top", padx=20, pady=0)
    panel_img = Label(frame1, text='产品原图', font=('微软雅黑', 50))
    panel_img.pack(side="top", padx=0, pady=0)

    check_time_out=0
    check_time=0
    check_limit=5
    final_result=False
    check_result_delay=0
    check_result_bool=False
    video = cv2.VideoWriter('temp.mp4', cv2.VideoWriter_fourcc('I', '4', '2', '0'), 30,
                            (img_resolution_x, img_resolution_y))  # 创建.avi
    video_path=''

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.

    while True:
        #try:
            uid=last_uid
            try:
                uid=get_uid_from_log.get_uid_from_log(log_path)[1]
            except:
                a=1
            ret, frame = video_stream.read()
            frame = cv2.resize(frame, (img_resolution_x, img_resolution_y), interpolation=cv2.INTER_AREA)
            frame, left_hand_bool, right_hand_bool,finger_distance,nose_bool = get_img_ana(frame)
            if finger_distance<9999:
                #print('finger_distance:'+str(finger_distance))
                a=1
            if uid != last_uid:
                #check_in_label_2.config(text='开始检测',fg='green')
                check_time_out=int(time_out)
                product_infor_area_2.config(text=uid)
                check_flow_1.config(bg='green')
                check_flow_3.config(bg='yellow')
                check_flow_5.config(bg='yellow')
                check_result.config(text='        ')
                last_uid=uid
                time=datetime.datetime.now()
                #time_str=time.strftime("%Y%m%d%H%M%S")
                time_str = time.strftime("%Y%m%d")
                mkdir(save_video_path+station_id+'\\')
                mkdir(save_video_path + station_id + '\\'+time_str+'\\')
                video_path = save_video_path+station_id+'\\' +time_str+'\\'+ uid+ '.mp4'
                os.remove('temp.mp4')
                video = cv2.VideoWriter('temp.mp4', cv2.VideoWriter_fourcc('I', '4', '2', '0'), 10,(640, 480))  # 创建.avi

            if check_time_out>0:
                check_time_out=check_time_out-1
            if check_time_out>time_out_start:
                if (left_hand_bool or right_hand_bool) and nose_bool :

                    check_time_out=time_out_start
            #if check_time_out==0:
                #check_in_label_2.config(text='等待产品', fg='brown')
            if check_time_out<=time_out_start and check_time_out>0:
                video.write(frame)
                #video.release()
            #video.write(frame)
            if check_time_out>0 and left_hand_bool and right_hand_bool and finger_distance<distance_limit and nose_bool:
                check_time=check_time+1
            #cv2.putText(frame, ('check_time:'+str(check_time)), (10, 90), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            #cv2.putText(frame, ('check_time_out:' + str(check_time_out)), (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            #cv2.putText(frame, ('check_result_delay:' + str(check_result_delay)), (10, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            #cv2.putText(frame, ('check_result_bool:' + str(check_result_bool)), (10, 180), cv2.FONT_HERSHEY_PLAIN, 2,
                #(0, 255, 0), 2)
            if check_time>int(hold_time):
                check_flow_3.config(bg='green')
                check_result_delay=15
                check_time_out=0
                check_time=0
                check_result_bool=True

            #if check_time>check_limit:
                #check_time_out=0
                #check_time=0
                #check_in_label_4.config(text='PASS',fg='green')
                #check_in_label_2.config(text = '等待产品', font = ('隶书', 30), fg = 'brown')
            if check_time_out==1:
                check_flow_3.config(bg='green')
                check_result_delay = 15
                check_result_bool=False
                #check_flow_5.config(bg='green')
                #check_result.config(text='FAIL', fg='red')
                #record_result(uid,'FAIL')
            if check_result_delay>0:
                check_result_delay=check_result_delay-1
            if check_result_delay==5:
                video.release()
                if check_result_bool:
                    check_flow_5.config(bg='green')
                    check_result.config(text='PASS', fg='green')
                    record_result(uid,'PASS')
                    result_mes='2'
                    if trigger_mode == 'MES':
                        t = threading.Thread(target=send_msg_mes, args=(uid, result_mes, 'none',))
                        t.start()
                    if save_video_bool=='1':
                        shutil.copy('temp.mp4',video_path)
                        if trigger_mode == 'MES':
                            t = threading.Thread(target=send_msg_mes, args=(uid, result_mes, video_path,))
                            t.start()
                else:
                    check_flow_5.config(bg='green')
                    check_result.config(text='FAIL', fg='red')
                    record_result(uid,'FAIL')
                    result_mes = '1'
                    shutil.copy('temp.mp4' , video_path)
                    if trigger_mode=='MES':
                        t = threading.Thread(target=send_msg_mes, args=(uid, result_mes,video_path,))
                        t.start()


            #if check_result_delay==1:
                #check_flow_1.config(bg='yellow')
                #check_flow_3.config(bg='yellow')
                #check_flow_5.config(bg='yellow')
                #video.release()
                #if check_result_bool:
                    #os.remove(video_path)
                #check_in_label_4.config(text='FAIL', fg='red')
            #product_infor_area_2.config(text=get_uid_from_log.get_uid_from_log('tracer.txt')[1])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            set_image_to_tk(panel_img, im)
            root.update()
        #except:
            a=1
    #root.mainloop()
if __name__ == '__main__':
    ui()
    #last_uid = get_uid_from_log.get_uid_from_log(log_path)[1]
    #send_msg_mes(last_uid,'2')
    #msg_transfer_byte('IDENTIFICATION,'+station_id+','+str(mes_counter)+','+'1')




