"""
登录/注册测试
"""

import pymysql
import bcrypt
import os
from dotenv import load_dotenv


def add_user(username, password, cursor):
    # 加密密码
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    # 插入用户
    sql = "insert into users(username, password) values(%s, %s)"
    params = (username, password)
    cursor.execute(sql, params)


def login(username, password, cursor):
    sql = "select * from users where username = %s"
    params = (username,)
    # 查找数据库
    cursor.execute(sql, params)
    user = cursor.fetchone()
    tag = False
    # 检查用户是否存在
    if user is None:
        print("用户名不存在")
    else:
        # 检查密码是否正确
        if bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8")):
            tag = True
        else:
            print("密码错误")
    return tag


def regedit(username, password, cursor):
    # 检查用户是否存在
    sql = "select * from users where username = %s"
    tag = False
    params = (username,)
    cursor.execute(sql, params)
    user = cursor.fetchone()
    if user is None:
        add_user(username, password, cursor)
        tag = True
    else:
        print("用户名已存在")
    return tag


load_dotenv("mysql_info.env")

if __name__ == "__main__":
    # 数据库连接信息
    host = os.getenv("MYSQL_HOST")
    port = int(os.getenv("MYSQL_PORT"))
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    db = os.getenv("MYSQL_DB")
    charset = os.getenv("MYSQL_CHARSET")
    mysql_conn = None
    mysql_cursor = None

    try:
        # 连接数据库
        mysql_conn = pymysql.Connection(host=host, port=port, user=user, password=password, database=db, charset=charset)
        mysql_cursor = mysql_conn.cursor()
        print("数据库连接成功")
        while True:
            # 添加用户
            username = input("请输入用户名：")
            password = input("请输入密码：")
            tag = regedit(username, password, mysql_cursor)
            if tag:
                mysql_conn.commit()
                print("用户注册成功")
            print("是否继续添加用户？(y/n)")
            if input("请输入：") in ("n", "N", "no", "NO", "No", "nO"):
                break
        # 登录
        username = input("请输入用户名：")
        password = input("请输入密码：")
        tag = login(username, password, mysql_cursor)
        if tag:
            print("登录成功")
    except Exception as e:
        print(e)
        # 回滚事务
        mysql_conn.rollback()
        print("数据库连接失败, 回滚事务")
    finally:
        # 关闭数据库连接
        mysql_cursor.close()
        mysql_conn.close()
        print("数据库连接已关闭")
