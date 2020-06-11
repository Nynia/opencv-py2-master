# encoding:utf-8

import datetime
import os,time

# d = atx.connect() # 如果多个手机连接电脑，则需要填入对应的设备号
# # while True:
# #     now = datetime.datetime.now()
# #     snapfile = 'C:\\Users\sk_ks\PycharmProjects\opencv-py2-master\img\%s.png' % now.strftime("%Y%m%d%H%M%S")
# #     d.screenshot(snapfile)
adb_path = 'adb'
while True:
    now = datetime.datetime.now()
    filename = '{}.png'.format(now.strftime("%Y%m%d%H%M%S"))
    minicapcommand = "adb\\adb.exe shell \" LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1080x1920@1080x1920/0 -s > /sdcard/{}".format(filename)
    print(minicapcommand)
    os.popen(minicapcommand)
    time.sleep(1)
    minicapcommand2 = "adb\\adb.exe pull /sdcard/{} img\\".format(filename)
    os.popen(minicapcommand2)
    print(minicapcommand2)

