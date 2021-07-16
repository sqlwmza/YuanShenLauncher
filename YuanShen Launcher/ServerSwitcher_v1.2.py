import tkinter as tk

import win32api
from PIL import Image, ImageTk


def windows():
    # 原神启动器游戏路径, 启动器config, 游戏安装路径
    game_launcher_path = './'
    launcher_config_path = game_launcher_path + '/config.ini'
    launcher_config = readConfig(launcher_config_path)
    game_install_path = launcher_config['game_install_path']

    win = tk.Tk()
    win.title('原神启动器')
    win.iconbitmap(game_launcher_path + '/launcher.exe')
    win.resizable(False, False)

    # 读取显示屏的分辨率
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # 读取最新的原神背景图片
    img_name = launcher_config['game_dynamic_bg_name']
    img_path = game_launcher_path + '/bg/' + img_name
    img = ImageTk.PhotoImage(Image.open(img_path))
    width = img.width()
    height = img.height()

    # 设置窗口居中
    x = (screen_width - width) / 2
    y = (screen_height - height) / 2
    win.geometry('%dx%d+%d+%d' % (width, height, x, y))

    # 设置背景图片
    canvas = tk.Canvas(win, width=width, height=height)
    canvas.create_image(width / 2, height / 2, image=img)
    canvas.pack()

    # 设置官服启动按钮
    mhy_button = tk.Button(win, text='米哈游官服', font=20, width=25, height=3, bg='orange', activebackground='darkorange',
                           bd=1, relief='ridge', command=lambda: startGenshin(game_install_path, '1'))
    mhy_button.place(x=1020, y=550)

    # 设置B服启动按钮
    bili_button = tk.Button(win, text='哔哩哔哩B服', font=20, width=25, height=3, bg='orange', activebackground='darkorange',
                            bd=1, relief='ridge', command=lambda: startGenshin(game_install_path, '14'))
    bili_button.place(x=1020, y=630)

    win.mainloop()


def readConfig(config_path):
    # 读取dir路径下的config.ini文件
    config = {}
    with open(config_path, 'r', encoding='utf-8') as f:
        config_content = f.read()
        config_lines = config_content.split(']\n')[1].splitlines()
        for line in config_lines:
            if '=' not in line:
                break
            part = line.split('=')
            config[part[0]] = part[1]
    return config


def startGenshin(dir, channel):
    # 从游戏安装目录读取config.ini
    game_config_path = dir + '/config.ini'
    default_config = {'1': '[General]\nchannel=1\ncps=mihoyo\nsub_channel=1\ngame_version={}',
                      '14': '[General]\nchannel=14\ncps=bilibili\nsub_channel=0\ngame_version={}'}
    game_config = readConfig(game_config_path)

    if channel != game_config['channel']:
        cfg = default_config[channel].format(game_config['game_version'])

        with open(game_config_path, 'w', encoding='utf-8') as f:
            f.write(cfg)

    genshinexe = dir + '/YuanShen.exe'
    win32api.ShellExecute(0, 'open', genshinexe, '', '', 1)


if __name__ == '__main__':
    windows()
