import pandas as pd
from tkinter import *
from tkinter.ttk import *
from Pmw import Balloon
from MyWindows.MyWidget.myButton import AddDataBaseButton, SearchButton
from MyWindows.MyWidget.myTreeView import MainLeftTreeView, MainRightTreeView


class Frame0(Frame):
    root = None
    pBar = None
    balloon = None
    addDataBaseButton = None
    searchButton = None

    def __init__(self, root, frame10, **kw):
        super().__init__(root, **kw)
        self.root = root
        self.frame10 = frame10
        self.balloon = Balloon(self.root)  # 主窗口气泡提示信息
        self.setButton()

    def setButton(self):
        self.addDataBaseButton = AddDataBaseButton(self, self.frame10)
        self.searchButton = SearchButton(self)
        self.balloon.bind(self.addDataBaseButton, '添加数据库')
        self.balloon.bind(self.searchButton, '查询数据')
        self.addDataBaseButton.place(relx=0, rely=0, relheight=1, relwidth=0.05)
        self.searchButton.place(relx=0.05, rely=0, relheight=1, relwidth=0.05)


class ButtonFrame(Frame):
    """
    存放按钮或标签的容器
    """
    root = None

    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        self.root = root
        self.rowconfigure(0, weight=1)  # 组件横向充满
        self.columnconfigure(0, weight=1)


class Frame10(Frame):
    root = None
    buttonFrame = None
    leftTreeView = None

    def __init__(self, root, frame11, **kw):
        super().__init__(root, **kw)
        self.root = root
        self.frame11 = frame11
        self.rowconfigure(0, weight=1)  # 组件横向充满
        self.columnconfigure(0, weight=1)
        self.setFrame()
        self.setTreeView()

    def setFrame(self):
        self.buttonFrame = ButtonFrame(self)  # 存放按钮的容器
        self.buttonFrame.place(relx=0, rely=0, relheight=1, relwidth=0.1)

    def setTreeView(self):
        self.leftTreeView = MainLeftTreeView(self, show="tree")
        self.leftTreeView.place(relx=0.1, rely=0, relheight=1, relwidth=0.9)

    def getButtonFrame(self):
        return self.buttonFrame

    def getTreeView(self):
        return self.leftTreeView


class Frame11(Frame):
    root = None
    treeView = None
    sroll_11_x_b = None
    sroll_11_x = None
    sroll_11_y = None
    totalRow = None
    buttonCanvas = None
    buttonFrame = None

    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        self.root = root
        self.rowconfigure(0, weight=1)  # 组件横向充满
        self.columnconfigure(0, weight=1)
        self.setFrame(None, (), None)
        self.setTreeView('None', ['None', '...'], pd.DataFrame())

    def on_configure(self, event):
        # 配置 Canvas 的视窗大小为内部内容的大小
        self.buttonCanvas.configure(scrollregion=self.buttonCanvas.bbox('all'))

    def setFrame(self, dataBaseName: str, tablesName: tuple, method):
        self.buttonCanvas = Canvas(self)  # 创建画布实现滚动
        self.buttonFrame = ButtonFrame(self.buttonCanvas)  # 存放按钮的容器
        self.buttonFrame.bind('<Configure>', self.on_configure)
        for table in tablesName:  # 注意table仍然是一个元组
            Button(self.buttonFrame, text=f'{table[0]}',
                   command=lambda t=table[0]: method(dataBaseName, t)).pack(fill=BOTH, side=LEFT)
        self.buttonCanvas.create_window((0, 0), window=self.buttonFrame, anchor='nw')  # 将frame放到画布中
        self.buttonCanvas.place(relx=0, rely=0, relheight=0.04, relwidth=1)

    def setTreeView(self, tableName: str, columns: list, data: pd.DataFrame):
        """
        生成treeview
        :param tableName: 表名
        :param columns: treeview的标题行
        :param data: 数据框
        :return:
        """
        data_list = data.values.tolist()
        totalRow = data.shape[0]  # 数据的总行数
        totalCol = data.shape[1] if data_list else len(columns)
        self.treeView = MainRightTreeView(self, show='headings', columns=columns)
        for column in columns:
            self.treeView.heading(column, text=column, anchor=CENTER)
        for index, rowData in enumerate(data_list):
            self.treeView.insert('', index, values=rowData)
        self.treeView.insert('', totalRow, values=['|---(None)---'] * totalCol)
        self.treeView.insert('', totalRow + 1, values=[f'当前所在表：{tableName}'])
        self.treeView.place(relx=0, rely=0.07, relheight=0.9, relwidth=0.98)
        self.setScrollBar()

    def setScrollBar(self):
        self.sroll_11_x_b = Scrollbar(self, orient=HORIZONTAL, command=self.buttonCanvas.xview)  # 按钮的水平条
        self.sroll_11_x = Scrollbar(self, orient=HORIZONTAL, command=self.treeView.xview)  # TREE的水平条
        self.sroll_11_y = Scrollbar(self, orient=VERTICAL, command=self.treeView.yview)
        self.sroll_11_x_b.place(relx=0, rely=0.04, relheight=0.03, relwidth=0.98)
        self.sroll_11_x.place(relx=0, rely=0.97, relheight=0.03, relwidth=0.98)
        self.sroll_11_y.place(relx=0.98, rely=0.05, relheight=0.95, relwidth=0.02)
        self.buttonCanvas['xscrollcommand'] = self.sroll_11_x_b.set
        self.treeView['xscrollcommand'] = self.sroll_11_x.set
        self.treeView['yscrollcommand'] = self.sroll_11_y.set

    def getButtonFrame(self):
        return self.buttonFrame

    def getTreeView(self):
        return self.treeView


class Frame2(Frame):

    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        self.root = root
