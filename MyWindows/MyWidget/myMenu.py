from tkinter import *
from tkinter.messagebox import showinfo, showwarning, showerror
from MyWindows.MyWidget.publicMember import pm


class MenuBar(Menu):
    """
    主窗口菜单栏
    """

    def __init__(self, root, frames, cnf={}, **kw):
        super().__init__(root, cnf, **kw)
        self.root: Tk = root
        self.frame0: Frame = frames[0]
        self.frame10: Frame = frames[1]
        self.addMenu()

    def addMenu(self):
        about_menu = AboutMenu(self, tearoff=False)
        self.add_cascade(label='关于', menu=about_menu)


class AboutMenu(Menu):
    """
    '关于'菜单
    """

    def __init__(self, master, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.master: MenuBar = master
        self.add_command(label='软件信息', command=self.show_about)  # 绑定事件

    @staticmethod
    def show_about():
        """
        软件信息
        """
        showinfo('DBQA', '作者：方豪\n版本：1.0.0')


class ContextMenu(Menu):
    """
    左侧treeview的右键菜单
    """

    def __init__(self, master, name, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.master = master  # MainLeftTreeView
        self.name = name
        self.addedDataBaseDict = pm.getAddedDataBase()  # 数据库别名：数据库对象；浅拷贝
        self.treeViewSelections = pm.getTreeViewSelections()  # 选中的节点名列表
        self.dataBase = self.addedDataBaseDict.get(self.name)  # 待操作的数据库对象
        self.add_command(label='连接数据库', command=self.connectDB)
        self.add_command(label='断开连接', command=self.closeDB)
        self.add_command(label='移除数据库', command=self.deleteDB)  # 绑定事件

    def connectDB(self):
        """
        连接数据库
        :return:
        """
        if not self.dataBase.isConnected():  # 若未连接
            try:
                self.dataBase.connectDB()
                self.treeViewSelections.append(self.name)  # 选中
            except:
                showerror("DBQA", f"数据库<{self.name}>连接失败！")
            else:
                self.master.updateText()
                tablesName = pm.search(self.addedDataBaseDict[self.name].getDB(), "SHOW TABLES")
                self.master.frame11.getTreeView().updateTableButton(self.name, tablesName)
        else:
            showwarning("DBQA", f"数据库<{self.name}>已连接！")

    def closeDB(self):
        """
        断开连接
        :return:
        """
        if self.dataBase.isConnected():  # 若为连接状态
            self.dataBase.closeDB()  # 断开连接
            self.treeViewSelections.remove(self.name)  # 清除选中状态
            self.master.updateText()
            for widget in self.master.frame11.winfo_children():  # 清除右侧treeview
                widget.destroy()

    def deleteDB(self):
        """
        移除数据库
        :return:
        """
        if self.name in self.treeViewSelections:  # 选中状态时不可移除
            showerror("DBQA", f"请先取消选中数据库<{self.name}>！")
            return
        self.closeDB()  # 断开数据库连接
        self.addedDataBaseDict.pop(self.name, None)  # 删除addedDataBase字典中的数据库对象缓存
        self.master.delete(self.name)  # 删除结点
        self.master.updateText()
        showinfo("DBQA", f"数据库<{self.name}>已安全删除！")
