class global_var:
  '''需要定义全局变量的放在这里，最好定义一个初始值'''
  SN = ''
  Scanner_log=''
  checkin_log=''
  eva_prod_log = ''
  serial_log=''
  ui_log=''
  save_serial_log=''
  check_in_bool='0' #0表示默认，1表示checkin 成功，2表示checkin 失败,3表示checkin完成
  screw_bool = '0'  # 0表示默认，1表示checkin 成功，2表示checkin 失败
  record_bool = '0'  # 0表示默认，1表示checkin 成功，2表示checkin 失败
  finish_bool = '0'  # 0表示默认，1表示checkin 成功，2表示checkin 失败
  clear_bool='0' #0表示不处理，1表示清理
  mes_counter=1
  send_eva='0'# 0表示默认，1表示PASS 成功，2表示Fail

# 对于每个全局变量，都需要定义get_value和set_value接口
def set_SN(name):
  global_var.SN = name
def get_SN():
  return global_var.SN

def set_check_in_bool(name):
  global_var.check_in_bool = name
def get_check_in_bool():
  return global_var.check_in_bool

def set_screw_bool(name):
  global_var.screw_bool = name
def get_screw_bool():
  return global_var.screw_bool

def set_record_bool(name):
  global_var.record_bool = name
def get_record_bool():
  return global_var.record_bool

def set_finish_bool(name):
  global_var.finish_bool = name
def get_finish_bool():
  return global_var.finish_bool

def set_Scanner_log(name):
  global_var.Scanner_log = name
def get_Scanner_log():
  return global_var.Scanner_log

def set_checkin_log(name):
  global_var.checkin_log = name
def get_checkin_log():
  return global_var.checkin_log

def set_eva_prod_log(name):
  global_var.eva_prod_log = name
def get_eva_prod_log():
  return global_var.eva_prod_log

def set_serial_log(name):
  global_var.serial_log = name
def get_serial_log():
  return global_var.serial_log

def set_ui_log(name):
  global_var.ui_log = name
def get_ui_log():
  return global_var.ui_log

def set_save_serial_log(name):
  global_var.save_serial_log = name
def get_save_serial_log():
  return global_var.save_serial_log

def set_mes_counter(name):
  global_var.mes_counter = name
def get_mes_counter():
  return global_var.mes_counter

def set_send_eva(name):
  global_var.send_eva = name
def get_send_eva():
  return global_var.send_eva