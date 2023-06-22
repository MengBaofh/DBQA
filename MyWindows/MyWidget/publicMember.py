import pandas as pd
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import ImageTk, Image
from matplotlib import pyplot as plt

from fDataBases import FDataBase

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号


class PublicMember:
    # 所有PublicNumber类共享,仅在最初类创建时执行一次
    IOutPutDir = 'ImageOutPut'

    def __init__(self):
        # self.paraSelectTopLevel = None
        # self.paraTopLevel = None
        self.gdf = pd.DataFrame()
        self.image_open_origin = None
        self.image_load = None
        self.image_open = None
        self.treeViewSelections = []  # 选中的节点名列表
        self.addedDataBase = {}  # 数据库名：数据库对象

    def imageLoader(self, path: str, size: tuple):
        """
        图片加载器
        :param path: 路径
        :param size: 显示的大小
        :return:
        """
        self.image_open_origin = Image.open(path)  # 原始图片
        self.image_open = Image.open(path).resize(size)  # 裁剪后的图片
        self.image_load = ImageTk.PhotoImage(self.image_open)  # 加载后的已裁剪图片
        return self.image_open_origin, self.image_open, self.image_load

    def addDataBase(self, dbVars, master, topLevel):
        """
        添加数据库
        :param master: frame10
        :param dbVars: 数据库参数
        :param topLevel: 弹窗对象
        :return:
        """
        topLevel.destroy()
        name = dbVars['数据库别名'].get()
        host = dbVars['host'].get()
        port = dbVars['端口'].get()
        user = dbVars['用户名'].get()
        passwd = dbVars['密码'].get()
        dbType = dbVars['数据库名称'].get()
        charset = dbVars['编码'].get()
        try:
            master.getTreeView().insert('', '0', name, text=name)
        except TclError:
            showerror('DBQA', f'检测到<{name}>数据库已添加，请勿重复添加！')
        else:
            self.addedDataBase[name] = FDataBase(name, host, port, user, passwd, dbType, charset)
            master.getTreeView().updateText()
            showinfo('DBQA', f'成功添加<{name}>数据库！')

    def getAddedDataBase(self):
        """
        获取已连接的数据库字典
        :return: dict
        """
        return self.addedDataBase

    def getTreeViewSelections(self):
        """
        获取左侧tree选中的结点名列表
        :return:
        """
        return self.treeViewSelections

    @staticmethod
    def search(dataBase, sql: str):
        """
        数据库查询
        :param dataBase: 待操作的数据库连接对象
        :param sql: 查询语句
        :return: 结果元组和元数据，用元数据获取列名column_names = [column[0] for column in resultDescription]
        """
        cursor = dataBase.cursor()  # 创建游标对象
        cursor.execute(sql)  # 执行查询语句
        result = cursor.fetchall()  # 获取查询结果
        resultDescription = cursor.description
        cursor.close()  # 关闭游标
        return result, resultDescription

    @staticmethod
    def mean(df: pd.DataFrame, cols: list):
        # 依次求指定cols的均值
        for col in cols:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                showerror('DBQA', f'数据类型转换失败：at column<{col}>')
                return []
            else:
                return [df[col].mean() for col in cols]

    @staticmethod
    def var(df: pd.DataFrame, cols: list):
        # 依次求指定cols的方差
        for col in cols:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                showerror('DBQA', f'数据类型转换失败：at column<{col}>')
                return []
            else:
                return [df[col].var() for col in cols]

    @staticmethod
    def max(df: pd.DataFrame, cols: list):
        # 依次求指定cols的最大值
        for col in cols:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                showerror('DBQA', f'数据类型转换失败：at column<{col}>')
                return []
            else:
                return [df[col].max() for col in cols]

    @staticmethod
    def min(df: pd.DataFrame, cols: list):
        # 依次求指定cols的均值
        for col in cols:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                showerror('DBQA', f'数据类型转换失败：at column<{col}>')
                return []
            else:
                return [df[col].min() for col in cols]

    @staticmethod
    def lineChart(df: pd.DataFrame, cols: list):
        # 绘制df各列的折线图
        for col in cols:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                showerror('DBQA', f'数据类型转换失败：at column<{col}>')
                return
        fig, ax = plt.subplots()  # 创建图表对象
        for column in df.columns:  # 遍历DataFrame的每一列，绘制折线图
            ax.plot(df.index, df[column], label=column)
        # 添加标题和坐标轴标签
        ax.set_title('折线图')
        ax.set_xlabel('记录')
        ax.set_ylabel('数值')
        ax.legend()  # 显示图例
        ax.grid(True)  # 显示网格
        plt.show()  # 显示图形


pm = PublicMember()
