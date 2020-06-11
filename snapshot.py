# encoding:utf-8
import time

import win32api
import win32con
import win32gui
import win32ui


def get_desk():
    # 获取桌面
    hdesktop = win32gui.GetDesktopWindow()

    # 分辨率适配
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

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
    screenshot.SaveBitmapFile(mem_dc, '{}.jpg'.format(cur_time))

    # 释放内存
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())


if __name__ == '__main__':
    get_desk()
