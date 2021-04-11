import os
import time
import tkinter as tk
import win32con, win32api
from PIL import Image, ImageTk

def windows():
    win = tk.Tk()
    win.title("原神启动器")
    win.resizable(False, False)

    # 读取显示屏的分辨率
    screenWidth = win.winfo_screenwidth()
    screenHeight = win.winfo_screenheight()

    # 读取最新的原神背景图片
    img_dir = "bg"
    img_name = readLatestFiles(img_dir)
    img_path = os.path.join(img_dir, img_name)
    img = readImage(img_path)
    width = img.width()
    height = img.height()

    # 设置窗口居中
    x = (screenWidth - width) / 2
    y = (screenHeight - height) / 2
    win.geometry("%dx%d+%d+%d" %(width, height, x, y))

    # 设置背景图片
    canvas = tk.Canvas(win, width=width, height=height)
    canvas.create_image(width/2, height/2, image=img)
    canvas.pack()

    # 设置官服启动按钮
    mhy_button = tk.Button(win, text="米哈游官服", font=20,
                           width=25, height=3, bg="orange",
                           activebackground="darkorange",
                           bd=1, command=lambda : startGenshin(1))
    mhy_button.place(x=1020, y=550)

    # 设置B服启动按钮
    bili_button = tk.Button(win, text="BiliBili服", font=20,
                            width=25, height=3, bg="orange",
                            activebackground="darkorange",
                            bd=1, command=lambda : startGenshin(14))
    bili_button.place(x=1020, y=630)

    win.mainloop()

def readLatestFiles(dir):
    # 读取最新的图片
    images = []
    # read images from the given directory
    for root, subdir, files in os.walk(dir):
        images = files

    diff = []
    current_time = time.time()
    # 计算时间差
    for img in images:
        img_path = os.path.join(dir, img)
        img_time = os.stat(img_path).st_ctime
        diff.append(current_time - img_time)

    # 返回时间差最小的也就是最新的文件名
    return images[diff.index(min(diff))]

def readImage(img_path):
    # 读取原神bg下的图片
    img = Image.open(img_path)
    return ImageTk.PhotoImage(img)

def startGenshin(channel):
    # 启动原神，config.ini从此程序运行的目录读取，不从原游戏文件夹内读取
    game_dir = "Genshin Impact Game"
    switchChannel(channel)
    genshinexe = os.path.join(game_dir, "YuanShen.exe")
    win32api.ShellExecute(0, "open", genshinexe, "", "", 1)

def switchChannel(channel):
    # 检测此程序目录下有没有config.ini文件，若无直接创建对应的config，若有则进行改写
    if not os.path.exists("config.ini"):
        cfg = "[General]\nchannel=" + str(channel) + "\ncps=bilibili\ngame_version=1.4.0\nsub_channel=1"
        with open("config.ini", "w") as f:
            f.write(cfg)
    else:
        new_cfg = ""
        with open("config.ini", "r") as cfg:
            for line in cfg.readlines():
                if "channel" in line:
                    new_cfg += "channel=" + str(channel) + "\n"
                else:
                    new_cfg += line
        # 将隐藏的文件变成可读写
        win32api.SetFileAttributes("config.ini", win32con.FILE_ATTRIBUTE_NORMAL)
        with open("config.ini", "w") as cfg:
            cfg.write(new_cfg)
    # 重新将文件变成隐藏状态
    win32api.SetFileAttributes("config.ini", win32con.FILE_ATTRIBUTE_HIDDEN)

if __name__ == "__main__":
    windows()