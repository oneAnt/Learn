import pymysql
import os
from dotenv import load_dotenv


load_dotenv("./mysql_info.env")


class Model(object):
    """
    模型
    """

    def __init__(self):
        # 数据库信息
        self.host = os.getenv("MYSQL_HOST")
        self.port = int(os.getenv("MYSQL_PORT"))
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.db = os.getenv("MYSQL_DB")
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)
        self.cursor = self.conn.cursor()

    def search_user(self, username):
        # 查询用户
        sql = "select * from users where username=%s"
        user = None
        try:
            self.cursor.execute(sql, username)
            user = self.cursor.fetchone()
        except Exception as e:
            print(e)
        return user

    def add_user(self, username, password, permission):
        # 添加用户
        sql = "insert into users (username, password, permission) values (%s, %s, %s)"
        params = (username, password, permission)
        tag = False
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            tag = True
        except Exception as e:
            # 错误回滚
            self.conn.rollback()
            print(e)
        finally:
            return tag

    def del_user(self, username):
        # 删除用户
        tag = False
        # 查看当前用户是否存在
        if not self.search_user(username):
            return tag
        sql = "delete from users where username=%s"
        try:
            self.cursor.execute(sql, username)
            self.conn.commit()
            tag = True
        except Exception as e:
            self.conn.rollback()
            print(e)
        finally:
            return tag

    def search_dishes(self):
        # 查询菜单
        sql = "select * from dishes"
        dishes = None
        try:
            self.cursor.execute(sql)
            dishes = self.cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            return dishes

    def add_dish(self, name, price, discount, cost):
        # 添加菜品
        sql = "insert into dishes(`name`, price, discount, cost) values(%s, %s, %s, %s)"
        params = (name, price, discount, cost)
        tag = False
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            tag = True
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            return tag

    def del_dish(self, id):
        sql = "select * from dishes where id=%s"
        tag = False
        try:
            dish = self.cursor.execute(sql, id)
            if dish:
                sql = "delete from dishes where id=%s"
                self.cursor.execute(sql, id)
                self.conn.commit()
                tag = True
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            return tag

    def update_dish(self, id, name, price, discount, cost):
        sql = "select * from dishes where id=%s"
        tag = False
        try:
            dish = self.cursor.execute(sql, id)
            if dish:
                sql = "update dishes set `name`=%s, price=%s, discount=%s, cost=%s where id=%s"
                params = (name, price, discount, cost, id)
                self.cursor.execute(sql, params)
                self.conn.commit()
                tag = True
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            return tag

    # ===== 订单管理(ai) =====

    def create_order(self, table_id, user_id, note=None):
        """创建订单，返回自增ID"""
        sql = "INSERT INTO orders (table_id, user_id, note) VALUES (%s, %s, %s)"
        params = (table_id, user_id, note)
        order_id = None
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            order_id = self.cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            print(e)
        return order_id

    def add_order_item(self, order_id, dish_id, quantity, unit_price, discount):
        """添加订单明细"""
        subtotal = round(float(unit_price) * float(discount) * int(quantity), 2)
        sql = "INSERT INTO order_items (order_id, dish_id, quantity, unit_price, discount, subtotal) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (order_id, dish_id, quantity, unit_price, discount, subtotal)
        tag = False
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            tag = True
        except Exception as e:
            self.conn.rollback()
            print(e)
        return tag

    def update_order_total(self, order_id):
        """重新计算订单总金额"""
        sql = "UPDATE orders SET total_price = (SELECT COALESCE(SUM(subtotal), 0) FROM order_items WHERE order_id = %s) WHERE id = %s"
        try:
            self.cursor.execute(sql, (order_id, order_id))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e)
            return False

    def get_active_orders(self):
        """获取未结账订单（待上菜 + 待结账）"""
        sql = "SELECT * FROM orders WHERE status != '已结账' ORDER BY create_time DESC"
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    def get_all_orders(self):
        """获取所有订单"""
        sql = "SELECT * FROM orders ORDER BY create_time DESC"
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    def get_order_by_id(self, order_id):
        """获取单个订单（关联服务员用户名）"""
        sql = """SELECT o.*, u.username
                 FROM orders o
                 JOIN users u ON o.user_id = u.id
                 WHERE o.id = %s"""
        try:
            self.cursor.execute(sql, order_id)
            return self.cursor.fetchone()
        except Exception as e:
            print(e)
            return None

    def get_order_items(self, order_id):
        """获取订单明细（关联菜品名）"""
        sql = """SELECT oi.*, d.name AS dish_name
                 FROM order_items oi
                 JOIN dishes d ON oi.dish_id = d.id
                 WHERE oi.order_id = %s"""
        try:
            self.cursor.execute(sql, order_id)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    def update_order_status(self, order_id, status):
        """更新订单状态，结账时自动记录pay_time"""
        if status == "已结账":
            sql = "UPDATE orders SET status = %s, pay_time = NOW() WHERE id = %s"
        else:
            sql = "UPDATE orders SET status = %s WHERE id = %s"
        tag = False
        try:
            self.cursor.execute(sql, (status, order_id))
            self.conn.commit()
            tag = True
        except Exception as e:
            self.conn.rollback()
            print(e)
        return tag

    def delete_order(self, order_id):
        """删除订单及其明细"""
        tag = False
        try:
            self.cursor.execute("DELETE FROM order_items WHERE order_id = %s", order_id)
            self.cursor.execute("DELETE FROM orders WHERE id = %s", order_id)
            self.conn.commit()
            tag = True
        except Exception as e:
            self.conn.rollback()
            print(e)
        return tag

    def get_order_statistics(self, start_date, end_date):
        """获取日期范围内的订单统计"""
        sql = """SELECT COUNT(*) AS order_count, COALESCE(SUM(total_price), 0) AS total_revenue
                 FROM orders
                 WHERE status = '已结账' AND pay_time BETWEEN %s AND %s"""
        try:
            self.cursor.execute(sql, (start_date, end_date))
            return self.cursor.fetchone()
        except Exception as e:
            print(e)
            return None

    def get_top_dishes(self, start_date, end_date):
        """获取日期范围内的热销菜品排行"""
        sql = """SELECT d.name, SUM(oi.quantity) AS total_qty, SUM(oi.subtotal) AS total_sales
                 FROM order_items oi
                 JOIN orders o ON oi.order_id = o.id
                 JOIN dishes d ON oi.dish_id = d.id
                 WHERE o.status = '已结账' AND o.pay_time BETWEEN %s AND %s
                 GROUP BY d.id, d.name
                 ORDER BY total_qty DESC
                 LIMIT 10"""
        try:
            self.cursor.execute(sql, (start_date, end_date))
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
