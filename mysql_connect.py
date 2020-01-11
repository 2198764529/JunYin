import pymysql as pm


class Mysql_connect:
    def __init__(self,):
        self.myDBC = pm.connect("localhost", "root", "root", "FlaskDB")
        self.myDB_cursor = self.myDBC.cursor()
        # self.myDB_cursor.execute("source ./SQL/init.sql;")

    def is_has(self, data):
        self.myDB_cursor.execute(
            "select username from user where username = '%s'" % data["username"]
        )
        return self.myDB_cursor.fetchone() != None

    def is_correct(self, data):
        self.myDB_cursor.execute(
            "select passwd from user where passwd = '%s';" % data["passwd"]
        )

        return self.myDB_cursor.fetchone() != None

    def add(self, data):
        print(
            "insert into user ('%s') values('%s');"
            % ("','".join(data), "','".join(data.values()))
        )
        self.myDB_cursor.execute(
            "insert into user (%s) values('%s');"
            % (",".join(data), "','".join(data.values()))
        )
        self.myDBC.commit()
        return False

    def close(self,):
        print("关闭连接")
        # 提交完成的操作
        # close cursor,connect
        self.myDBC.close()

    def select(self, data):
        self.myDB_cursor.execute("select * from user;")
        return [
            {"username": x[1], "passwd": x[2], "id": x[0]}
            for x in self.myDB_cursor.fetchall()
        ]

    def run(self, data):

        print(self.myDB_cursor.execute("select * from user;"))
