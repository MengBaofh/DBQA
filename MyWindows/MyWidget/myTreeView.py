import pandas as pd
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from MyWindows.MyWidget.myMenu import ContextMenu
from MyWindows.MyWidget.publicMember import pm


class MainLeftTreeView(Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.contextMenu = None
        self.master = master
        self.frame11 = self.master.frame11
        self.addedDataBaseDict = pm.getAddedDataBase()
        self.treeviewSelections = pm.getTreeViewSelections()
        self.eventBind()

    def eventBind(self):
        self.bind("<Button-1>", self.onSelect)
        self.bind("<Button-3>", self.popupMenu)

    def onSelect(self, event):
        """
        treeview选中回调函数
        :return:
        """
        item = self.identify('item', event.x, event.y)
        if item:
            self.selection_set(item)
            if item in self.treeviewSelections:  # 若选中（连接）
                self.treeviewSelections.remove(item)  # 删除选中状态
                if self.addedDataBaseDict[item].isConnected():
                    self.addedDataBaseDict[item].closeDB()  # 断开连接
                self.updateText()
                for widget in self.frame11.winfo_children():
                    widget.destroy()
            else:
                try:
                    self.addedDataBaseDict[item].connectDB()
                    self.treeviewSelections.append(item)
                    tablesName = pm.search(self.addedDataBaseDict[item].getDB(), "SHOW TABLES")[0]
                    self.frame11.getTreeView().updateTableButton(item, tablesName)
                except:
                    showerror("DBQA", f"数据库<{item}>连接失败！")
                else:
                    self.updateText()

    def updateText(self):
        """
        更新选中节点对应的标签状态
        :return:
        """
        for label in self.master.getButtonFrame().winfo_children():
            label.destroy()
        for node in self.get_children():
            Label(self.master.getButtonFrame(), text='√' if node in self.treeviewSelections else '□').pack(fill=X)

    def popupMenu(self, event):
        """
        弹出右键菜单
        :param event:
        :return:
        """
        item = self.identify('item', event.x, event.y)
        if item:
            contextMenu = ContextMenu(self, item, tearoff=False)
            self.selection_set(item)  # 选中并高亮
            contextMenu.post(event.x_root, event.y_root)


class MainRightTreeView(Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.addedDataBaseDict = pm.getAddedDataBase()
        self.treeviewSelections = pm.getTreeViewSelections()

    def updateTableButton(self, dataBaseName: str, tablesName: tuple):
        """
        更新右侧表的按钮
        :param dataBaseName: 数据库别名
        :param tablesName: 表名元组
        :return:
        """
        for widget in self.master.winfo_children():
            widget.destroy()
        self.master.setFrame(dataBaseName, tablesName, self.updateRightTreeView)
        self.master.setTreeView('None', ['None', '...'], pd.DataFrame())

    def updateRightTreeView(self, dataBaseName: str, tableName: str):
        """
        更新右侧treeview
        :param dataBaseName: 数据库别名
        :param tableName: 表名
        :return:
        """
        resultData, resultDescription = pm.search(self.addedDataBaseDict[dataBaseName].getDB(),
                                                  f'SELECT * FROM {tableName}')
        column_names = [column[0] for column in resultDescription]  # 获取列名
        data = pd.DataFrame(resultData)
        if isinstance(data, pd.DataFrame):
            self.master.setTreeView(tableName, column_names, data)


class ParaSelectTreeView(Treeview):
    """
    参数选择treeview
    """
    def __init__(self, master, selections: list, text: str, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.text = text  # 表头
        self.selections = selections  # 可选项标签列表
        self.addedDataBaseDict = pm.getAddedDataBase()
        self.treeviewSelections = pm.getTreeViewSelections()
        self.setTreeView()

    def setTreeView(self):
        self.heading('0', text=self.text, anchor=CENTER)
        for index, availSelection in enumerate(self.selections):
            self.insert('', index, values=availSelection)
        self.bind('<<TreeviewSelect>>', self.onSelect)

    def onSelect(self, event):
        print(self.selection())

    def getMySelection(self):
        """
        获取选择项字段组合字符串
        :return: 'field1, field2, ...'
        """
        return pm.getAnyTreeViewSelection(self)
