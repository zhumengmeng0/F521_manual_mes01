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