from tkinter import *
from tkinter.messagebox import showerror
from tkinter.ttk import *
from pymysql.err import *
from MyWindows.MyWidget.publicMember import pm
from MyWindows.MyWidget.myTreeView import ParaSelectTreeView
from MyWindows.MyWidget.myTopLevel import ParaOutputByTreeViewTop, ParaMulSelectTop, ParaInputTop, ParaSelectTop, \
    AnalyseTopLevel


class CustomButton(Button):
    """
    自定义按钮类
    """
    image = None
    update_id = None  # 用于存储延时更新的标识符
    paraTopLevel = None
    paraSelectTopLevel = None

    def __init__(self, master, image_path, command):
        super().__init__(master)
        self.master = master
        self.image_path = image_path
        self['command'] = command
        self.bind("<Configure>", self.scheduleAdjustImage)

    def scheduleAdjustImage(self, event):
        """
        延时更新调整图像大小，防止卡顿
        :param event: 事件对象
        """
        if self.update_id is None:
            self.update_id = self.after(100, self.adjustImage)

    def adjustImage(self):
        """
        图片自适应按钮大小
        :return:
        """
        self.image = pm.imageLoader(self.image_path, (self.winfo_width() - 10, self.winfo_height() - 10))[2]
        self['image'] = self.image
        self.update_id = None  # 重置延时更新的标识符

    def popupParaTopLevel(self, parameters: dict, master, method):
        """
        弹出参数输入弹窗，且保证同时仅存在一个弹窗
        :param parameters: 参数字典
        :param master: 父组件
        :param method: “确定”调用方法
        :return:
        """
        if self.paraTopLevel:
            self.paraTopLevel.destroy()
        self.paraTopLevel = ParaInputTop(parameters, master, method)

    def popupParaSelectTopLevel(self, parameters: dict, master, method, isProgressive=False, function=None):
        """
        弹出参数选则下拉框弹窗，且保证同时仅存在一个弹窗
        :param parameters: 参数字典
        :param master: 父组件
        :param method: “确定”调用方法
        :param isProgressive: 是否递进式下拉框
        :param function: 递进规则
        :return:
        """
        if self.paraSelectTopLevel:
            self.paraSelectTopLevel.destroy()
        self.paraSelectTopLevel = ParaSelectTop(parameters, master, method, isProgressive, function)

    def getTopLevel(self):
        return self.paraTopLevel, self.paraSelectTopLevel


class AddDataBaseButton(CustomButton):
    """
    添加数据库按钮
    """

    def __init__(self, master, frame10):
        self.topLevel = None
        super().__init__(master, 'MyImage/open.png', lambda: super(AddDataBaseButton, self).popupParaTopLevel(
            {'数据库别名': '', 'host': 'localhost', '端口': 3306, '用户名': 'root', '密码': '', '数据库名称': 'mysql',
             '编码': 'utf8'}, frame10, pm.addDataBase))


class SearchButton(CustomButton):
    """
    查询和分析按钮
    """
    paraSelectTreeView = None
    outputTreeViewTopLevel = None
    addWhereButton = None
    where = []  # where语句列表(构造where语句:myWhere = ' AND '.join(where))

    def __init__(self, master):
        self.selectTable = None
        self.selectDataBase = None
        self.column_names = None
        self.addedDataBaseDict = pm.getAddedDataBase()  # 数据库别名：数据库对象；浅拷贝字典
        self.treeViewSelections = pm.getTreeViewSelections()  # 选中的节点名列表
        super().__init__(master, 'MyImage/search.png', lambda: super(SearchButton, self).popupParaSelectTopLevel(
            {'选择数据库': [i for i in self.treeViewSelections] if self.treeViewSelections else ['请先选中数据库'],
             '选择表': ['请先选择数据库']}, self, self.outputCtrlTop, True, self.updateTables))

    def updateTables(self, dataBase):
        # 根据数据库名更新表的下拉框（此处为选择数据库的回调函数）
        return list(pm.search(self.addedDataBaseDict[dataBase].getDB(), 'SHOW TABLES')[0])

    def outputCtrlTop(self, myVars: dict):
        # 弹出字段选择及条件控制窗口
        for widget in super().getTopLevel()[1].winfo_children():
            widget.destroy()
        self.selectDataBase = self.addedDataBaseDict[myVars['选择数据库'].get()].getDB()
        self.selectTable = myVars['选择表'].get()
        resultDescription = pm.search(self.selectDataBase, f'SELECT * FROM {self.selectTable}')[1]
        self.column_names = [column[0] for column in resultDescription]
        self.paraSelectTreeView = ParaSelectTreeView(super().getTopLevel()[1], self.column_names,
                                                     '请选择待查询的字段(使用ctrl间隔多选，shift连续多选)',
                                                     show='headings', columns='0')
        self.paraSelectTreeView.place(relx=0.05, rely=0, relheight=0.5, relwidth=0.9)
        self.setCtrlButton()

    def setCtrlButton(self):
        # 设置条件控制按钮
        self.addWhereButton = AddWhereButton(super().getTopLevel()[1], self.selectTable, self.column_names,
                                             self.paraSelectTreeView)
        self.addWhereButton.place(relx=0.1, rely=0.6, relheight=0.1, relwidth=0.3)
        Button(super().getTopLevel()[1], text='确定', command=self.popupResultTreeViewTop). \
            place(relx=0.3, rely=0.8, relheight=0.1, relwidth=0.4)

    def popupResultTreeViewTop(self):
        # 以treeview的形式输出结果
        sql = f'SELECT {self.paraSelectTreeView.getMySelection()} FROM {self.selectTable}'
        if self.where:
            myWhere = ' AND '.join(self.where)
            sql += f' WHERE {myWhere}'
        try:
            result, resultDescription = pm.search(self.selectDataBase, sql)
        except ProgrammingError:
            showerror('DBQA', f'输入的查询语句有误：\n{sql}')
        except OperationalError:
            showerror('DBQA', f'查询语句中含有未知的值：\n{sql}')
        else:
            columnName = [column[0] for column in resultDescription]
            ParaOutputByTreeViewTop(self.selectTable, result, columnName, '对已选数据进行分析', AnalyseTopLevel, self)


class AddWhereButton(Button):
    """
    添加where条件按钮
    """
    baseOperators = ['>', '>=', '<', '<=', '=', '<>',
                     'LIKE', 'NOT LIKE',
                     'IS NULL', 'IS NOT NULL',
                     'BETWEEN', 'NOT BETWEEN',
                     'IN', 'NOT IN']

    def __init__(self, master, table, selections, treeView):
        super().__init__(master)
        self['text'] = 'where'
        self['command'] = lambda: ParaMulSelectTop(master,
                                                   f'SELECT {treeView.getMySelection()} FROM {table} WHERE ',
                                                   ['值1', '条件', '值2'],
                                                   [selections, self.baseOperators,
                                                    ['可自定义(若为字符串需用""括起来)'] + selections])
