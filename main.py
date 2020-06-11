# encoding:utf-8
import cv2 as cv
from com.dtmilano.android.viewclient import ViewClient
import datetime
import os
from PIL import Image
import time
import win32con
import win32gui
import win32ui


def check_screenshot(tpl_name, target_name):
    tpl = cv.imread(tpl_name)
    target = cv.imread(target_name)
    # methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCORR_NORMED, cv.TM_CCOEFF_NORMED]
    methods = [cv.TM_SQDIFF_NORMED]
    # th, tw = tpl.shape[:2]
    for md in methods:
        result = cv.matchTemplate(target, tpl, md)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # print min_val
        if min_val < 0.005:
            # print min_loc
            return min_loc
    return None


def get_desk(cnt):
    # 获取桌面
    hdesktop = win32gui.GetDesktopWindow()

    # 分辨率适配
    # width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    # height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    # left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    # top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    left = 4
    top = 32
    width = 554
    height = 986
    # 创建设备描述表
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    # 创建一个内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)  # 为bitmap开辟空间
    mem_dc.SelectObject(screenshot)  # 将截图保存到Bitmap中
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)  # 截取从左上角（0，0）长宽为（w，h）的图片

    # 保存到文件
    time_tup = time.localtime(time.time())
    format_time = "%Y-%m-%d_%a_%H-%M-%S"
    cur_time = time.strftime(format_time, time_tup)
    filename = 'screenshots\{}_{}.bmp'.format(cur_time, cnt)
    print filename
    screenshot.SaveBitmapFile(mem_dc, filename)

    # 释放内存
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

    return filename


def clean():
    pass


def test():
    for i in range(1, 60):
        filename = 'img\%s.png' % i
        check_screenshot('template.jpg', filename)


def test2():
    vc = ViewClient(*ViewClient.connectToDeviceOrExit())
    for i in range(1, 9):
        view = vc.findViewById("id/no_id/%d" % i)
        if view:
            print view.__tinyStr__()
            # view.touch()


def test3():
    img = Image.open('img\\20200601233104.png')
    new_img = img.crop((348, 1060, 730, 1190))
    new_img.save("ok.png")


def test4():
    from airtest.core.api import snapshot
    snapshot('screenshot.png')


if __name__ == '__main__':
    device, serialno = ViewClient.connectToDeviceOrExit(verbose=False)
    point = 0
    adb_path = 'adb'
    while True:
        now = datetime.datetime.now()
        filename = '{}.png'.format(now.strftime("%Y%m%d%H%M%S"))
        minicapcommand = "adb\\adb.exe shell \" LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1080x1920@540x960/0 -s > /sdcard/{}".format(
            filename)
        # print(minicapcommand)
        os.popen(minicapcommand)
        time.sleep(0.2)
        minicapcommand2 = "adb\\adb.exe pull /sdcard/{} img\\".format(filename)
        os.popen(minicapcommand2)
        res = check_screenshot('target.png', 'img/{}'.format(filename))
        if res and 350 < res[0] < 370:
            print 'start grab @ {}'.format(res)
            device.touch(868, 1760)
        res = check_screenshot('ok.png', 'img/{}'.format(filename))
        if res:
            print res
            if res[1] < 540:
                point -= 19
                print 'grab fail, - 19 point, total: {}'.format(point)
            else:
                point += 20

                print 'grab success, + 20 point, total: {}'.format(point)
            device.touch(536, 1121)



