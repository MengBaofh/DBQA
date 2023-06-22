import matplotlib
import MyWindows.mainWindow as mWin
from tkinter import Tk
from tkinter.messagebox import *


def StopAll():
    if askyesno('DBQA', '确定要退出吗？'):
        root.quit()
        root.destroy()
        exit()


if __name__ == '__main__':
    matplotlib.use('TkAgg')
    root = Tk()
    root.iconbitmap('MyImage/sys.ico')
    root.protocol('WM_DELETE_WINDOW', StopAll)
    a = mWin.MainWindow(root)
    a.mainloop()  # 不断刷新主窗口
