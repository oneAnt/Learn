import sqlite3

class ContactModel(object):
    """联系人模型"""
    def __init__(self):
        self.init_db()

    def init_db(self):
        """初始化数据库"""
        conn = self.get_connection()
        cursor = conn.cursor()
        # 创建表
        create_table_sql = "CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT NOT NULL, email TEXT, address TEXT)"
        cursor.execute(create_table_sql)
        # 提交事务
        conn.commit()
        # 关闭游标和连接
        cursor.close()
        conn.close()

    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect('contacts_sqlite.db')
        # 设置行工厂
        conn.row_factory = sqlite3.Row
        return conn

    def do_sql(self, sql, params=()):
        """执行SQL语句"""
        conn = self.get_connection()
        cursor = conn.cursor()
        data = None
        # 执行SQL语句
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
            data = cursor.fetchall()
        # 提交事务
        conn.commit()
        # 关闭游标和连接
        cursor.close()
        conn.close()
        return data

    def add_contact(self, name, phone, email, address):
        """添加联系人"""
        add_sql = "INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)"
        self.do_sql(add_sql, (name, phone, email, address))

    def delete_contact(self, name):
        """删除联系人"""
        delete_sql = "DELETE FROM contacts WHERE name = ?"
        self.do_sql(delete_sql, (name,))

    def get_contacts(self):
        """获取所有联系人信息"""
        select_sql = "SELECT * FROM contacts"
        info = self.do_sql(select_sql)
        return info
