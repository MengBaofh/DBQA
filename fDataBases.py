from tkinter.messagebox import showinfo

from pymysql import connect


class FDataBase:
    db = None

    def __init__(self, name: str, host: str, port: int, user: str, passwd: str, dbType: str, charset: str = 'utf8'):
        self.name = name
        self.host = host
        self.port = port
        self.user = user
        self.password = passwd
        self.dbType = dbType
        self.charset = charset

    def connectDB(self):
        """
        连接数据库
        :return:
        """
        self.db = connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.dbType,
                          charset=self.charset)
        showinfo("DBQA", f"数据库<{self.name}>连接成功！")

    def isConnected(self):
        """
        数据库是否连接
        :return:
        """
        if self.db:
            if self.db.open:
                return True
        return False

    def getDB(self):
        """
        获取已连接上的数据库，若未连接则为None
        :return:
        """
        return self.db

    def closeDB(self):
        """
        断开数据库连接
        :return:
        """
        self.db.close()
        showinfo("DBQA", f"成功断开数据库<{self.name}>的连接。")
