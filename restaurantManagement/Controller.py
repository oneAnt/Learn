from Model import Model
import bcrypt


class Controller(object):
    """
    控制
    """

    def __init__(self):
        self.model = Model()
        self.user = None

    def login(self, username, password):
        # 登录逻辑
        self.user = self.model.search_user(username)
        user_info = None
        if self.user and bcrypt.checkpw(password.encode("utf-8"), self.user[2].encode("utf-8")):
            user_info = {
                "id": self.user[0],
                "username": self.user[1],
                "permission": self.user[4],
                "create_time": self.user[3]
            }
            print("登录成功")
        else:  
            print("用户名或密码错误")
        return user_info

    def add_user(self, username, password, permission):
        # 添加用户逻辑
        password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        tag = self.model.add_user(username, password, permission)
        if tag:
            print("添加用户成功！")
        else:
            print("添加用户失败！")
        return tag
    
    def del_user(self, username):
        # 删除用户逻辑
        tag = self.model.del_user(username)
        if tag:
            print("删除用户成功！")
        else:
            print("删除用户失败！")
        return tag

    def select_dishes(self):
        dishes = self.model.search_dishes()
        dish_list = []
        if dishes:
            for dish in dishes:
                dish_list.append({
                    'id': dish[0],
                    'name': dish[1],
                    'price': dish[2],
                    'discount': dish[3],
                    'cost': dish[4]
                })
                print("显示菜单！")
        return dish_list
    
    def add_dish(self, name, price, discount, cost):
        tag = self.model.add_dish(name, price, discount, cost)
        if tag:
            print("添加菜品成功！")
        else:
            print("添加菜品失败！")
        return tag

    def del_dish(self, id):
        tag = self.model.del_dish(id)
        if tag:
            print("删除菜品成功！")
        else:
            print("删除菜品失败！")
        return tag

    def update_dish(self, id, name, price, discount, cost):
        tag = self.model.update_dish(id, name, price, discount, cost)
        if tag:
            print("修改菜品成功！")
        else:
            print("修改菜品失败！")
        return tag

    # ===== 订单管理（ai) =====

    def create_order(self, table_id, user_id, note, dishes):
        """创建订单（含明细），失败自动回滚
        dishes: list of (dish_id, quantity, unit_price, discount)
        """
        order_id = self.model.create_order(table_id, user_id, note)
        if not order_id:
            print("创建订单失败！")
            return False
        for dish in dishes:
            dish_id, quantity, unit_price, discount = dish
            tag = self.model.add_order_item(order_id, dish_id, quantity, unit_price, discount)
            if not tag:
                self.model.delete_order(order_id)
                print("添加明细失败，订单已回滚！")
                return False
        self.model.update_order_total(order_id)
        print(f"点菜成功！订单ID: {order_id}")
        return True

    def checkout_order(self, order_id):
        """结账"""
        tag = self.model.update_order_status(order_id, "已结账")
        if tag:
            print(f"结账成功！订单ID: {order_id}")
        else:
            print("结账失败！")
        return tag

    def update_order_status(self, order_id, status):
        """更新订单状态"""
        tag = self.model.update_order_status(order_id, status)
        if tag:
            print(f"订单 {order_id} 状态已更新为 {status}")
        return tag

    def delete_order(self, order_id):
        """删除订单"""
        tag = self.model.delete_order(order_id)
        if tag:
            print(f"删除订单成功！ID: {order_id}")
        else:
            print("删除订单失败！")
        return tag

    def get_all_orders(self):
        """获取所有订单"""
        orders = self.model.get_all_orders()
        if not orders:
            return []
        order_list = []
        for o in orders:
            order_list.append({
                'id': o[0], 'table_id': o[1], 'user_id': o[2],
                'status': o[3], 'total_price': o[4], 'note': o[5],
                'create_time': o[6], 'pay_time': o[7]
            })
        return order_list

    def get_active_orders(self):
        """获取未结账订单"""
        orders = self.model.get_active_orders()
        if not orders:
            return []
        order_list = []
        for o in orders:
            order_list.append({
                'id': o[0], 'table_id': o[1], 'user_id': o[2],
                'status': o[3], 'total_price': o[4], 'note': o[5],
                'create_time': o[6], 'pay_time': o[7]
            })
        return order_list

    def get_order_detail(self, order_id):
        """获取订单详情（含明细和服务员名）"""
        order = self.model.get_order_by_id(order_id)
        if not order:
            return None
        items = self.model.get_order_items(order_id)
        order_dict = {
            'id': order[0], 'table_id': order[1], 'user_id': order[2],
            'status': order[3], 'total_price': order[4], 'note': order[5],
            'create_time': order[6], 'pay_time': order[7],
            'waiter_name': order[8] if len(order) > 8 else ''
        }
        item_list = []
        if items:
            for item in items:
                item_list.append({
                    'id': item[0], 'order_id': item[1], 'dish_id': item[2],
                    'quantity': item[3], 'unit_price': item[4], 'discount': item[5],
                    'subtotal': item[6], 'dish_name': item[7]
                })
        return {'order': order_dict, 'items': item_list}

    def get_order_statistics(self, start_date, end_date):
        """获取统计报表"""
        result = self.model.get_order_statistics(start_date, end_date)
        top_dishes = self.model.get_top_dishes(start_date, end_date)
        stats = {
            'order_count': result[0] if result else 0,
            'total_revenue': float(result[1]) if result and result[1] else 0.0
        }
        dish_list = []
        if top_dishes:
            for d in top_dishes:
                dish_list.append({
                    'name': d[0],
                    'quantity': int(d[1]) if d[1] else 0,
                    'sales': float(d[2]) if d[2] else 0.0
                })
        stats['top_dishes'] = dish_list
        return stats
    