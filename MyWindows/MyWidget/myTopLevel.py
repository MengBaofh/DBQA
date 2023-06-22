import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from Pmw import Balloon
from tkinter.messagebox import showwarning, showerror
from MyWindows.MyWidget.myTreeView import ParaSelectTreeView
from MyWindows.MyWidget.publicMember import pm


class ParaInputTop(Toplevel):
    """
    参数输入弹窗类
    """
    width = 350
    height = 350

    def __init__(self, parameters: dict, master, method, **kw):
        super().__init__(master, kw)
        self.master = master
        self.vars = {}
        self.balloon = Balloon(self.master)
        self.parameters = parameters
        self.method = method
        self.setVars()
        self.setParaInputTop()
        self.setLabelEntry()

    def setVars(self):
        for parameter, default in self.parameters.items():
            self.vars[parameter] = IntVar() if type(default) == int else StringVar()
            self.vars[parameter].set(default)

    def setParaInputTop(self):
        self.title('连接数据库')
        self.iconbitmap('MyImage/sys.ico')
        self.geometry(f'{self.width}x{self.height}+300+200')
        # self.attributes('-topmost', 'true')  # 保持窗口最上
        self.lift()

    def setLabelEntry(self):
        n = len(self.vars)
        x, y = 0.2, 0.15
        for parameter, var in self.vars.items():
            Label(self, text=parameter, relief='groove', anchor='center') \
                .place(relx=x, rely=y, relheight=0.07, relwidth=0.25)
            Entry(self, textvariable=self.vars[parameter], justify='center') \
                .place(relx=x + 0.35, rely=y, relheight=0.07, relwidth=0.25)
            y += 0.6 / n
        Button(self, text='确定', command=lambda: self.method(self.vars, self.master, self)) \
            .place(relx=0.3, rely=0.9, relheight=0.07, relwidth=0.4)


class ParaSelectTop(Toplevel):
    """
    参数选则下拉框弹窗类
    """
    width = 350
    height = 350

    def __init__(self, parameters: dict, master, method, isProgressive=False, function=None, **kw):
        super().__init__(master, kw)
        self.master = master
        self.vars = {}  # 题目:对应存储变量对象
        self.balloon = Balloon(self.master)
        self.parameters = parameters  # 题目:[选项1, 选项2, ...]
        self.method = method
        self.isProgressive = isProgressive  # 是否递进式下拉框
        self.function = function  # 递进规则
        self.setVars()
        self.setParaSelectTop()
        self.setLabelDropDown()

    def setVars(self):
        # 设置存储变量
        for parameter, default in self.parameters.items():
            self.vars[parameter] = StringVar()
            self.vars[parameter].set(default[0])

    def setParaSelectTop(self):
        self.title('查询数据')
        self.iconbitmap('MyImage/sys.ico')
        self.geometry(f'{self.width}x{self.height}+300+200')
        # self.attributes('-topmost', 'true')  # 保持窗口最上
        self.lift()

    def dropdownChanged(self, event):
        # 下拉框选项改变时的回调函数
        formerVar = list(self.vars.items())[0][1]
        if formerVar.get() == '请先选中数据库': return
        for parameter, var in list(self.vars.items())[1:]:
            self.parameters[parameter] = self.function(formerVar.get())
            formerVar = var
        self.setLabelDropDown()

    def setLabelDropDown(self):
        n = len(self.vars)
        x, y = 0.2, 0.15
        for parameter, var in self.vars.items():
            Label(self, text=parameter, relief='groove', anchor='center') \
                .place(relx=x, rely=y, relheight=0.07, relwidth=0.25)
            if not self.isProgressive:
                ttk.Combobox(self, values=self.parameters[parameter], textvariable=self.vars[parameter],
                             justify='center', state='readonly').place(relx=x + 0.35, rely=y, relheight=0.07,
                                                                       relwidth=0.35)
            else:
                combobox = ttk.Combobox(self, values=self.parameters[parameter], textvariable=self.vars[parameter],
                                        justify='center', state='readonly')
                combobox.bind("<<ComboboxSelected>>", self.dropdownChanged)  # 绑定选择事件
                combobox.place(relx=x + 0.35, rely=y, relheight=0.07, relwidth=0.35)
            y += 0.6 / n
        Button(self, text='确定', command=lambda: self.method(self.vars)) \
            .place(relx=0.3, rely=0.9, relheight=0.07, relwidth=0.4)


class ParaMulSelectTop(Toplevel):
    """
    参数选则多下拉框弹窗类，点击按钮可添加下拉框
    """
    width = 535
    height = 350
    frame = None
    canvas = None
    sroll_y = None
    vars = []  # stringVar对象列表
    varCount = 0

    def __init__(self, master, title: str, headings, availSelections, label: str, **kw):
        super().__init__(master, kw)
        self.master = master
        self.balloon = Balloon(self.master)
        self.myTitle = title
        self.headings = headings  # 下拉框表头，[第一个下拉框表头, 第二个下拉框表头, 第三个下拉框表头]
        self.availSelections = availSelections  # 下拉框可选项，[[第一个下拉框], [第二个下拉框], [第三个下拉框]]
        self.label = label
        if self.label == 'where':  # where? having? orderBy?
            self.target = self.master.master.where
        elif self.label == 'having':
            self.target = self.master.master.having
        elif self.label == 'orderBy':
            self.target = self.master.master.orderBy
        self.columnNum = len(self.headings)
        self.scale = self.columnNum / 3
        self.rescale = 3 / self.columnNum
        if self.target:
            self.updateVars()
        self.setParaMulSelectTop()
        self.setInputFrame()

    def updateVars(self):
        for index, item in enumerate(self.target):
            for i in range(self.columnNum):
                self.vars[index * self.columnNum + i] = StringVar()
                self.vars[index * self.columnNum + i].set(item.split()[i])
                self.varCount += 1

    def setParaMulSelectTop(self):
        self.title(self.myTitle)
        self.width = int(self.width * self.scale)
        self.height = int(self.height * self.scale)
        self.iconbitmap('MyImage/sys.ico')
        self.geometry(f'{self.width}x{self.height}+100+200')
        self.resizable(False, False)
        # self.attributes('-topmost', 'true')  # 保持窗口最上
        self.lift()

    def on_configure(self, event):
        # 配置 Canvas 的视窗大小为内部内容的大小
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def setInputFrame(self):
        for i in range(self.columnNum):
            Label(self, text=self.headings[i]).place(relx=(0.03 + i * 0.33) * self.rescale,
                                                     rely=0, relheight=0.1,
                                                     relwidth=0.27 * self.rescale)
        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas, relief='groove')
        self.frame.bind('<Configure>', self.on_configure)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')  # 将frame放到画布中
        self.canvas.place(relx=0.03, rely=0.1, relheight=0.35, relwidth=0.93)
        if self.target:
            for i in range(self.varCount // self.columnNum):
                for j in range(self.columnNum):
                    print(self.varCount)
                    ttk.Combobox(self.frame, values=self.availSelections[j],
                                 textvariable=self.vars[i * self.columnNum + j],
                                 justify='center').grid(row=i, column=j)
        self.setScrollBar()
        self.setButton()

    def setScrollBar(self):
        self.sroll_y = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.sroll_y.place(relx=0.96, rely=0, relheight=0.5, relwidth=0.04)
        self.canvas['yscrollcommand'] = self.sroll_y.set

    def setButton(self):
        Button(self, text='添加', command=self.addCondition).place(relx=0.2, rely=0.5, relheight=0.1, relwidth=0.2)
        Button(self, text='删除底部条件', command=self.delCondition).place(relx=0.6, rely=0.5, relheight=0.1,
                                                                           relwidth=0.2)
        Button(self, text='保存', command=self.saveCondition).place(relx=0.3, rely=0.7, relheight=0.1, relwidth=0.4)

    def addCondition(self):
        # 一次加一行，一行三个下拉框
        if self.varCount > 0:
            for i in range(self.columnNum):
                if self.vars[-(i + 1)].get() == '':
                    showwarning('DBQA', '请先补全上一条查询条件！')
                    return
        for i in range(self.columnNum):
            myVar = StringVar()
            self.vars.append(myVar)
            ttk.Combobox(self.frame, values=self.availSelections[i], textvariable=myVar,
                         justify='center').grid(row=self.varCount // self.columnNum, column=i)
            self.varCount += 1

    def delCondition(self):
        # 一次删一行，一行三个下拉框
        if self.varCount == 0: return
        for i in range(3):
            self.frame.winfo_children()[-1].destroy()
            self.vars.pop(self.varCount - 1)
            self.varCount -= 1

    def saveCondition(self):
        if self.varCount > 0:
            for i in range(self.columnNum):
                if self.vars[-(i + 1)].get() == '':
                    showwarning('DBQA', '检测到输入的查询条件不全！')
                    return
        each = ''
        targets = []
        for i in range(self.varCount):
            myStr = self.vars[i].get()
            each += myStr
            each += ' '
            if not (i + 1) % self.columnNum:
                targets.append(each)
                each = ''
        # self.target = targets[:]
        if self.label == 'where':
            self.master.master.where = targets[:]
        elif self.label == 'having':
            self.master.master.having = targets[:]
        elif self.label == 'orderBy':
            self.master.master.orderBy = targets[:]
        self.destroy()


class ParaOutputByTreeViewTop(Toplevel):
    """
    参数输出弹窗类，以treeview形式
    """
    width = 600
    height = 350
    sroll_11_y = None
    sroll_11_x = None
    treeview = None

    def __init__(self, selectTable: str, result, column, buttonText: str, buttonFunc, master, **kw):
        super().__init__(master, kw)
        self.selectTable = selectTable  # 窗口title
        self.result = result  # 结果
        self.column = column  # 表头
        self.buttonText = buttonText  # 按钮文本
        self.buttonFunc = buttonFunc  # 按钮command
        self.master = master
        self.setParaOutputByTreeViewTop()
        self.setTreeView()
        self.setButton()

    def setParaOutputByTreeViewTop(self):
        self.title(f'{self.selectTable}')
        self.iconbitmap('MyImage/sys.ico')
        self.geometry(f'{self.width}x{self.height}+100+200')
        # self.attributes('-topmost', 'true')  # 保持窗口最上
        self.lift()

    def setTreeView(self):
        data = pd.DataFrame(self.result)
        data_list = data.values.tolist()
        totalRow = data.shape[0]  # 数据的总行数
        totalCol = data.shape[1] if data_list else len(self.column)
        self.treeview = Treeview(self, show='headings', columns=self.column)
        for column in self.column:
            self.treeview.heading(column, text=column, anchor=CENTER)
        for index, rowData in enumerate(self.result):
            self.treeview.insert('', index, values=rowData)
        self.treeview.insert('', totalRow, values=['|---(None)---'] * totalCol)
        self.treeview.place(relx=0.03, rely=0, relheight=0.75, relwidth=0.94)
        self.setScrollBar()

    def setScrollBar(self):
        self.sroll_11_x = Scrollbar(self, orient=HORIZONTAL, command=self.treeview.xview)  # TREE的水平条
        self.sroll_11_y = Scrollbar(self, orient=VERTICAL, command=self.treeview.yview)
        self.sroll_11_x.place(relx=0.03, rely=0.75, relheight=0.05, relwidth=0.94)
        self.sroll_11_y.place(relx=0.97, rely=0, relheight=0.8, relwidth=0.03)
        self.treeview['xscrollcommand'] = self.sroll_11_x.set
        self.treeview['yscrollcommand'] = self.sroll_11_y.set

    def setButton(self):
        Button(self, text=self.buttonText,
               command=lambda: self.buttonFunc(self, self.result, self.column) if self.buttonFunc else None). \
            place(relx=0.3, rely=0.85, relheight=0.1, relwidth=0.4)

    def getTreeViewSelection(self):
        """
        获取选择项字段组合字符串
        :return: 'field1, field2, ...'
        """
        return pm.getAnyTreeViewSelection(self.treeview)


class AnalyseTopLevel(Toplevel):
    """
    数据分析弹窗类
    """
    width = 400
    height = 350
    sroll_11_y = None
    sroll_11_x = None
    treeview = None
    paraSelectTreeView = None

    def __init__(self, master, data, column, **kw):
        super().__init__(master, kw)
        if not data:
            self.destroy()
            showerror('DBQA', '选中的数据为空，无法分析！')
        self.master = master
        self.data = data
        self.column = column
        self.df = pd.DataFrame(data)
        self.df.columns = self.column
        self.setAnalyseTopLevel()
        self.setParaSelectTreeView()

    def setAnalyseTopLevel(self):
        self.title('数据分析')
        self.iconbitmap('MyImage/sys.ico')
        self.geometry(f'{self.width}x{self.height}+200+200')
        # self.attributes('-topmost', 'true')  # 保持窗口最上\
        self.lift()

    def setParaSelectTreeView(self):
        self.paraSelectTreeView = ParaSelectTreeView(self, self.column, '请选择要分析的字段：',
                                                     show='headings', columns='0')
        self.paraSelectTreeView.place(relx=0.05, rely=0, relheight=0.65, relwidth=0.9)
        Button(self, text='求均值', command=self.getMean).place(relx=0.1, rely=0.7, relheight=0.1, relwidth=0.2)
        Button(self, text='求方差', command=self.getVar).place(relx=0.4, rely=0.7, relheight=0.1, relwidth=0.2)
        Button(self, text='求最大值', command=self.getMax).place(relx=0.7, rely=0.7, relheight=0.1, relwidth=0.2)
        Button(self, text='求最小值', command=self.getMin).place(relx=0.1, rely=0.85, relheight=0.1, relwidth=0.2)
        Button(self, text='绘制折线图', command=self.getLineChart).place(relx=0.4, rely=0.85, relheight=0.1,
                                                                         relwidth=0.2)

    def setParaOutputByTreeViewTop(self, title, result, selectedCols, buttonText='确定', buttonFunc=None):
        ParaOutputByTreeViewTop(title, result, selectedCols, buttonText, buttonFunc, self)

    def getMean(self):
        if not self.paraSelectTreeView.getMySelection():
            showwarning('DBQA', '请先选择要分析的字段！')
            return
        selectedCols = self.paraSelectTreeView.getMySelection().split(', ')
        self.setParaOutputByTreeViewTop('均值', [pm.mean(self.df, selectedCols)], selectedCols)

    def getVar(self):
        if not self.paraSelectTreeView.getMySelection():
            showwarning('DBQA', '请先选择要分析的字段！')
            return
        selectedCols = self.paraSelectTreeView.getMySelection().split(', ')
        self.setParaOutputByTreeViewTop('方差', [pm.var(self.df, selectedCols)], selectedCols)

    def getMax(self):
        if not self.paraSelectTreeView.getMySelection():
            showwarning('DBQA', '请先选择要分析的字段！')
            return
        selectedCols = self.paraSelectTreeView.getMySelection().split(', ')
        self.setParaOutputByTreeViewTop('最大值', [pm.max(self.df, selectedCols)], selectedCols)

    def getMin(self):
        if not self.paraSelectTreeView.getMySelection():
            showwarning('DBQA', '请先选择要分析的字段！')
            return
        selectedCols = self.paraSelectTreeView.getMySelection().split(', ')
        self.setParaOutputByTreeViewTop('最小值', [pm.min(self.df, selectedCols)], selectedCols)

    def getLineChart(self):
        if not self.paraSelectTreeView.getMySelection():
            showwarning('DBQA', '请先选择要分析的字段！')
            return
        selectedCols = self.paraSelectTreeView.getMySelection().split(', ')
        pm.lineChart(self.df[selectedCols], selectedCols)

# if __name__ == '__main__':
#     root = Tk()
#     Button(root, text='1',
#            command=lambda: ParaOutputByTreeViewTop('table1', (('1-', 2, 3), ('1', 3, 6)), ['col1', 'col2', 'col3'],
#                                                    '对已选数据进行分析', AnalyseTopLevel, root)).pack()
#     root.mainloop()  # 不断刷新主窗口
