from tkinter import *
import time
from config import *
import os
import datetime
from ui import *
from scanner_reader import *
from serial_read import *
import threading
def finished():
    print(get_check_in_bool())
    print(get_screw_bool())
    if get_check_in_bool()=='3' and get_screw_bool()=='1':
        set_send_eva('1')

def manual_fail():
    if get_check_in_bool() == '3' and get_screw_bool() == '1':
        set_send_eva('2')


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
def save_log(info):
    mkdir('log\\')
    time_now = datetime.datetime.now()
    time_str = time_now.strftime("%Y%m%d")
    f = open('log\\log'+ '_' + time_str + '.txt', 'a', encoding='utf-8')
    realtime = time.strftime("%Y-%m-%d %H:%M:%S ")
    textvar = realtime + info # 系统时间和传入结果
    f.write(textvar+ '\n')
    f.close()


def ui():
    text_log='12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n2\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n12\n123\n'
    root = Tk()
    root.title('电机F521手动MES程序/Motor F521 manual MES application')
    #root.minsize(1920, 1080)  # 最小尺寸
    #root.maxsize(1920, 1080)  # 最大尺寸
    root.geometry('1500x800')
    root.resizable(0, 0)
    frame00 = Frame(root, bd=0, relief=GROOVE,background='black')
    frame00.pack(side=TOP, fill='both', ipadx=0, ipady=0, expand=0)
    product_infor_area_0 = Label(frame00,text='Vitesco Tianjin Motor Line F521 Manual MES ', font=('微软雅黑', 30),fg='white',bg='black')
    product_infor_area_0.pack(side="top", padx=20, pady=5)
    frame01 = Frame(root, bd=0, relief=RIDGE,background='dimgray')
    frame01.pack(side=TOP, fill='both', ipadx=0, ipady=0, expand=0)
    product_infor_area_1 = Label(frame01, text='产品信息/SN:', font=('微软雅黑', 20),fg='white',bg='dimgray')
    product_infor_area_1.pack(side=LEFT, padx=10, pady=0)
    SN_text = Label(frame01,font=('微软雅黑', 20),fg='white',bg='dimgray')
    SN_text.pack(side=LEFT, padx=20, pady=0)
    frame2 = Frame(root, bd=1, relief=GROOVE,bg='gray')
    frame2.pack(side=LEFT, fill='y', ipadx=0, ipady=0, expand=0)

    check_in_label_8 = Label(frame2, text='状态信息/Status: ', font=('微软雅黑', 20),anchor='w',fg='white',bg='gray')
    check_in_label_8.pack(side="top", padx=10, pady=10)
    check_flow_1= Label(frame2, text='扫码\nCheck in', font=('微软雅黑', 17),fg='black',bg='yellow',bd=3,relief='raised',width=8,height=2)
    check_flow_1.pack(side="top", ipadx=10, ipady=10,padx=5, pady=10)
    check_flow_2= Label(frame2, text='⭣', font=('微软雅黑',20),bg='gray',fg='white')
    check_flow_2.pack(side="top", padx=0, pady=0)
    check_flow_3= Label(frame2, text='打螺丝\nScrew', font=('微软雅黑', 17),fg='black',bg='yellow',bd=3,relief='raised',width=8,height=2)
    check_flow_3.pack(side="top", ipadx=10, ipady=5,padx=5, pady=10)
    check_flow_4= Label(frame2, text='⭣', font=('微软雅黑', 20),bg='gray',fg='white')
    check_flow_4.pack(side="top", padx=0, pady=0)
    check_flow_5= Label(frame2, text='记录数据\nRecord', font=('微软雅黑', 17),fg='black',bg='yellow',bd=3,relief='raised',width=8,height=2)
    check_flow_5.pack(side="top", ipadx=10, ipady=5,padx=5, pady=10)
    check_flow_6= Label(frame2, text='⭣', font=('微软雅黑', 20),bg='gray',fg='white')
    check_flow_6.pack(side="top", padx=0, pady=0)
    check_flow_7= Label(frame2, text='完成\nFinished', font=('微软雅黑', 17),fg='black',bg='yellow',bd=3,relief='raised',width=8,height=2)
    check_flow_7.pack(side="top", ipadx=10, ipady=5,padx=5, pady=10)


    frame1 = Frame(root, bd=2, relief=GROOVE,bg='gray')
    frame1.pack(side=TOP, fill=BOTH, ipadx=0, ipady=0, expand=0)
    #video_label = Label(frame1, text='实时画面(蓝框为检测区域)\nRealtime video(Blue Frame is the inspection area)', font=('隶书', 5),fg='white',bg='black')
    #video_label.pack(side="top", padx=20, pady=0)
    panel_img = Label(frame1, text='软件信息/Log', font=('微软雅黑', 20),fg='white',bg='dimgray')
    panel_img.pack(side="left", padx=0, pady=0)
    frame2 = Frame(root, bd=2, relief=GROOVE, bg='gray')
    frame2.pack(side=TOP, fill=BOTH, ipadx=0, ipady=0, expand=0)
    #log_frame = Text(frame2, text='', font=('微软雅黑', 20), fg='black', bg='white',width=50,height=13,anchor='w',justify='left')
    log_frame = Text(frame2,width=176, height=34,wrap=NONE)
    log_frame.pack(side="left",fill='x', padx=0, pady=0)
    frame4 = Frame(root, bd=0, relief=GROOVE, bg='gray')
    frame4.pack(side=TOP, fill=BOTH, ipadx=0, ipady=0, expand=0)
    frame3 = Frame(root, bd=2, relief=GROOVE, bg='gray')
    frame3.pack(side=TOP, fill=BOTH, ipadx=0, ipady=0, expand=0)
    bt1=Button(frame3,text='合格/PASS', font=('微软雅黑', 20),fg='black',bg='yellow',width=20,height=2,command=finished,activebackground='blue',activeforeground='yellow')
    bt1.pack(side="left", fill=BOTH, padx=150, pady=50)
    bt2 = Button(frame3, text='不良/Fail', font=('微软雅黑', 20), fg='black', bg='yellow', width=20, height=2,command=manual_fail,activebackground='blue',activeforeground='yellow')
    bt2.pack(side="left", fill=BOTH, padx=150, pady=50)
    scroll = Scrollbar(frame2)
    # 放到窗口的右侧, 填充Y竖直方向
    scroll.pack(side=RIGHT, fill=Y)

    # 两个控件关联
    scroll.config(command=log_frame.yview)
    log_frame.config(yscrollcommand=scroll.set)
    scroll_x = Scrollbar(frame4,orient = HORIZONTAL)
    # 放到窗口的右侧, 填充Y竖直方向
    scroll_x.pack(side=BOTTOM, fill=X)

    # 两个控件关联
    scroll_x.config(command=log_frame.xview)
    log_frame.config(xscrollcommand=scroll_x.set)
    def showSN(result):
        SN_text.config(text=result)
    # 定义信息显示的方法
    def showinfo(result):
        realtime = time.strftime("%Y-%m-%d %H:%M:%S ")
        textvar = realtime + result  # 系统时间和传入结果
        log_frame.insert('end', textvar)  # 显示在text框里面
        log_frame.insert('end', '\n')  # 换行

    # 定义清除方法
    def clear():
        log_frame.delete(0.0, END)  # 清楚text中的内容，0.0为删除全部
    a=0

    while True:
        sn_text=get_SN()
        if sn_text!='':
            showSN(sn_text)
            #set_SN('')

        checkin_bool=get_check_in_bool()
        #if checkin_bool=='0':
            #check_flow_1.config(bg='yellow')
        if checkin_bool=='1':
            check_flow_1.config(bg='green')
            set_record_bool('0')
            set_screw_bool('0')
            set_finish_bool('0')
            set_check_in_bool('3')
        if checkin_bool=='2':
            check_flow_1.config(bg='red')
            set_record_bool('0')
            set_screw_bool('0')
            set_finish_bool('0')

        screw_bool=get_screw_bool()
        #if checkin_bool=='0':
            #check_flow_1.config(bg='yellow')
        if screw_bool=='1':
            check_flow_3.config(bg='green')
        if screw_bool=='0':
            check_flow_3.config(bg='yellow')

        record_bool=get_record_bool()
        #if checkin_bool=='0':
            #check_flow_1.config(bg='yellow')
        if record_bool=='1':
            check_flow_5.config(bg='green')
        if record_bool=='0':
            check_flow_5.config(bg='yellow')

        finish_bool=get_finish_bool()
        #if checkin_bool=='0':
            #check_flow_1.config(bg='yellow')
        if finish_bool=='1':
            check_flow_7.config(bg='green')
        if finish_bool=='0':
            check_flow_7.config(bg='yellow')
        if finish_bool=='2':
            check_flow_7.config(bg='red')

        scanner_log_text = get_Scanner_log()
        if scanner_log_text != '':
            showinfo(scanner_log_text)
            save_log(scanner_log_text)
            set_Scanner_log('')

        checkin_log_text = get_checkin_log()
        if checkin_log_text != '':
            showinfo(checkin_log_text)
            save_log(checkin_log_text)
            set_checkin_log('')

        serial_log_text = get_serial_log()
        if serial_log_text != '':
            showinfo(serial_log_text)
            save_log(serial_log_text)
            set_serial_log('')

        ui_log_text = get_ui_log()
        if ui_log_text != '':
            showinfo(ui_log_text)
            save_log(ui_log_text)
            set_ui_log('')

        save_serial_log_text = get_save_serial_log()
        if save_serial_log_text != '':
            showinfo(save_serial_log_text)
            save_log(save_serial_log_text)
            set_save_serial_log('')

        eva_prod_log_text = get_eva_prod_log()
        if eva_prod_log_text != '':
            showinfo(eva_prod_log_text)
            save_log(eva_prod_log_text)
            set_eva_prod_log('')

        log_frame.see(END)
        root.update()



