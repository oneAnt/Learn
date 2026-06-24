import tkinter
from tkinter import ttk
from tkinter import messagebox
from Controller import Controller

class View(object):
    """
    视图
    """

    def __init__(self):
        # 创建总窗口
        self.master = tkinter.Tk()
        self.master.title("餐馆订餐管理系统")  # 窗口标题
        self.master.state("zoomed")  # 窗口最大化
        # 创建控制器
        self.controller = Controller()
        self.user = None
        self.price_list = [round(x*0.5, 2) for x in range(0, 2001)]
        self.cost_list = [round(x*0.5, 2) for x in range(0, 2001)]
        self.discount_list = [round(x*0.1, 2) for x in range(0, 11)]
        self.status_list = ["待上菜", "待结账", "已结账"]

    def login_show(self):
        # 创建登录界面
        login_frame = tkinter.Frame(self.master)
        login_frame.pack(fill="both", expand=True)
        # 登录界面
        login_label = tkinter.Label(login_frame, text="用户登录", anchor="center", font=("微软雅黑", 14))
        login_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        # 用户名
        username_label = tkinter.Label(login_frame, text="用户名:", font=("微软雅黑", 12))
        username_label.grid(row=1, column=0)
        username_entry = tkinter.Entry(login_frame)
        username_entry.grid(row=1, column=1)
        # 密码
        password_label = tkinter.Label(login_frame, text="密  码:", font=("微软雅黑", 12))
        password_label.grid(row=2, column=0)
        password_entry = tkinter.Entry(login_frame, show="*")
        password_entry.grid(row=2, column=1)
        # 登录按钮
        login_button = tkinter.Button(login_frame, text="登录",
                                      command=lambda: self.login_click(username_entry.get(), password_entry.get()))
        login_button.grid(row=3, column=0, pady=10, padx=20)

    def login_click(self, username, password):
        # 登录按钮点击事件
        self.user = self.controller.login(username, password)
        if self.user is None:
            messagebox.showerror("登录失败", "用户名或密码错误！")
        else:
            messagebox.showinfo("登录成功", "欢迎使用餐馆订餐管理系统！")
            self.main_show()

    def main_show(self):
        # 创建主界面
        self.clear_master()
        # 主页面布局
        self.main_frame = tkinter.Frame(self.master)
        self.main_frame.pack(fill=tkinter.BOTH, expand=True)
        # 主页面组件
        toolbar = tkinter.Frame(self.main_frame, bg="gray")
        toolbar.pack(side=tkinter.TOP, fill=tkinter.X)
        # 工具栏组件
        menu_show_button = tkinter.Button(toolbar, text="菜单", command=lambda: self.menu_show_all())
        menu_show_button.pack(side=tkinter.LEFT)
        order_dish_button = tkinter.Button(toolbar, text="点菜", command=lambda: self.order_dish_show())
        order_dish_button.pack(side=tkinter.LEFT)
        checkout_button = tkinter.Button(toolbar, text="结账", command=lambda: self.checkout_show())
        checkout_button.pack(side=tkinter.LEFT)
        if self.user["permission"] == "admin":
            del_order_button = tkinter.Button(toolbar, text="删除订单", command=lambda: self.delete_order_show())
            del_order_button.pack(side=tkinter.LEFT)
            statistics_button = tkinter.Button(toolbar, text="订单统计", command=lambda: self.order_statistics_show())
            statistics_button.pack(side=tkinter.LEFT)
            add_dish_button = tkinter.Button(toolbar, text="添加菜品", command=lambda: self.add_dish_show())
            add_dish_button.pack(side=tkinter.LEFT)
            update_dish_button = tkinter.Button(toolbar, text="修改菜品", command=lambda: self.update_dish_show())
            update_dish_button.pack(side=tkinter.LEFT)
            del_dish_button = tkinter.Button(toolbar, text="删除菜品", command=lambda: self.del_dish_show())
            del_dish_button.pack(side=tkinter.LEFT)
            add_user_button = tkinter.Button(toolbar, text="添加用户", command=lambda: self.add_user_show())
            add_user_button.pack(side=tkinter.LEFT)
            del_user_button = tkinter.Button(toolbar, text="删除用户", command=lambda: self.del_user_show())
            del_user_button.pack(side=tkinter.LEFT)
        # 退出
        logout_button = tkinter.Button(toolbar, text="退出登录", command=lambda: self.logout())
        logout_button.pack(side=tkinter.RIGHT)
    
    def add_user_show(self):
        # 添加用户界面
        top_window = tkinter.Toplevel(self.master)
        top_window.title("添加用户")
        # 设置窗口大小
        w, h = 300, 200
        x = (self.master.winfo_screenwidth() - w) // 2
        y = (self.master.winfo_screenheight() - h) // 2
        top_window.geometry(f"{w}x{h}+{x}+{y}")
        # 添加用户页面组件
        add_frame = tkinter.Frame(top_window)
        add_frame.pack(fill=tkinter.BOTH, expand=True)
        # 添加用户页面组件
        username_label = tkinter.Label(add_frame, text="用户名：")
        username_label.grid(row=0, column=0, padx=10, pady=10)
        username_entry = tkinter.Entry(add_frame)
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        # 密码
        password_label = tkinter.Label(add_frame, text="密码：")
        password_label.grid(row=1, column=0, padx=10, pady=10)
        password_entry = tkinter.Entry(add_frame, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        # 权限
        permission_label = tkinter.Label(add_frame, text="权限：")
        permission_label.grid(row=2, column=0, padx=10, pady=10)
        permission_entry = tkinter.Entry(add_frame)
        permission_entry.grid(row=2, column=1, padx=10, pady=10)
        # 确认和取消
        confirm_button = tkinter.Button(add_frame, text="确认", 
                                        command=lambda: self.add_user_confirm(username_entry.get(), password_entry.get(), permission_entry.get(), top_window))
        confirm_button.grid(row=3, column=0, padx=50, pady=10)
        cancel_button = tkinter.Button(add_frame, text="取消", command=lambda: top_window.destroy())
        cancel_button.grid(row=3, column=1, padx=15, pady=10)
    
    def add_user_confirm(self, username, password, permission, top_window):
        # 添加用户确认事件
        tag = self.controller.add_user(username, password, permission)
        if tag:
            messagebox.showinfo("添加用户", "添加用户成功！")
        else:
            messagebox.showerror("添加用户", "添加用户失败！")
        top_window.destroy()

    def del_user_show(self):
        # 删除用户界面
        top_window = tkinter.Toplevel(self.master)
        top_window.title("删除用户")
        # 设置窗口大小
        w, h = 300, 150
        x = (self.master.winfo_screenwidth() - w) // 2
        y = (self.master.winfo_screenheight() - h) // 2
        top_window.geometry(f"{w}x{h}+{x}+{y}")
        # 删除用户页面组件
        add_frame = tkinter.Frame(top_window)
        add_frame.pack(fill=tkinter.BOTH, expand=True)
        username_label = tkinter.Label(add_frame, text="用户名：")
        username_label.grid(row=0, column=0, padx=10, pady=10)
        username_entry = tkinter.Entry(add_frame)
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        # 确认和取消
        confirm_button = tkinter.Button(add_frame, text="确认", 
                                        command=lambda: self.del_user_confirm(username_entry.get(), top_window))
        confirm_button.grid(row=1, column=0, padx=50, pady=10)
        cancel_button = tkinter.Button(add_frame, text="取消", command=lambda: top_window.destroy())
        cancel_button.grid(row=1, column=1, padx=15, pady=10)

    def del_user_confirm(self, username, top_window):
        # 删除用户确认事件
        tag = self.controller.del_user(username)
        if tag:
            messagebox.showinfo("删除用户", "删除用户成功！")
        else:
            messagebox.showerror("删除用户", "删除用户失败！")
        top_window.destroy()

    def menu_show_all(self):
        self.main_show()
        menu_canvas = tkinter.Canvas(self.main_frame, bg="white")
        menu_canvas.pack(fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)
        # 绑定滚动条
        scrollbar = tkinter.Scrollbar(self.main_frame)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        menu_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=menu_canvas.yview)
        # 显示菜单
        dish_list = self.controller.select_dishes()
        i = 1
        for dish in dish_list:
            txt = f"\n菜品编号：{dish["id"]} 菜品名称：{dish["name"]} 价格：{dish["price"]}元 折扣：{dish["discount"]}"
            if self.user["permission"] == "admin":
                txt += f" 成本：{dish["cost"]}元"
            menu_canvas.create_text(10, 30*i, text=txt, anchor=tkinter.NW, font=("微软雅黑", 16))
            i += 1
        menu_canvas.config(scrollregion=menu_canvas.bbox("all"))
    
    def add_dish_show(self):
        # 添加菜品
        top_window = tkinter.Toplevel(self.master)
        top_window.title("添加菜品")
        # 设置窗口大小
        w, h = 300, 300
        x = (self.master.winfo_screenwidth() - w) // 2
        y = (self.master.winfo_screenheight() - h) // 2
        top_window.geometry(f"{w}x{h}+{x}+{y}")
        # 添加菜品页面组件
        add_frame = tkinter.Frame(top_window)
        add_frame.pack(fill=tkinter.BOTH, expand=True)
        # 菜品名
        name_label = tkinter.Label(add_frame, text="菜品名：")
        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry = tkinter.Entry(add_frame)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        # 价格
        price_label = tkinter.Label(add_frame, text="价格:")
        price_label.grid(row=1, column=0, padx=5, pady=10)
        price_spinbox = tkinter.Spinbox(add_frame, values=self.price_list, format="%.2f")
        price_spinbox.grid(row=1, column=1, padx=5, pady=10)
        # 折扣
        discount_label = tkinter.Label(add_frame, text="折扣:")
        discount_label.grid(row=2, column=0, padx=5, pady=10)
        discount_spinbox = tkinter.Spinbox(add_frame, values=self.discount_list, format="%.2f")
        discount_spinbox.grid(row=2, column=1, padx=5, pady=10)
        # 成本
        cost_label = tkinter.Label(add_frame, text="成本:")
        cost_label.grid(row=3, column=0, padx=5, pady=10)
        cost_spinbox = tkinter.Spinbox(add_frame, values=self.cost_list, format="%.2f")
        cost_spinbox.grid(row=3, column=1, padx=5, pady=10)
        # 确认和取消
        confirm_button = tkinter.Button(add_frame, text="确认", 
                                        command=lambda: self.add_dish_confirm(name_entry.get(), price_spinbox.get(), 
                                                                              discount_spinbox.get(), cost_spinbox.get(), top_window))
        confirm_button.grid(row=4, column=0, padx=50, pady=10)
        cancel_button = tkinter.Button(add_frame, text="取消", command=lambda: top_window.destroy())
        cancel_button.grid(row=4, column=1, padx=15, pady=10)

    def add_dish_confirm(self, name, price, discount, cost, top_window):
        # 添加菜品确认
        tag = self.controller.add_dish(name, price, discount, cost)
        if tag:
            messagebox.showinfo("添加菜品", "添加菜品成功！")
        else:
            messagebox.showerror("添加菜品", "添加菜品失败！")
        top_window.destroy()

    def del_dish_show(self):
        # 删除菜品显示
        top_window = tkinter.Toplevel(self.master)
        top_window.title("删除菜品")
        # 设置窗口大小
        w, h = 300, 150
        x = (self.master.winfo_screenwidth() - w) // 2
        y = (self.master.winfo_screenheight() - h) // 2
        top_window.geometry(f"{w}x{h}+{x}+{y}")
        # 删除菜品页面组件
        del_frame = tkinter.Frame(top_window)
        del_frame.pack(fill=tkinter.BOTH, expand=True)
        id_label = tkinter.Label(del_frame, text="菜品id:")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = tkinter.Entry(del_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)
        # 确认和取消
        confirm_button = tkinter.Button(del_frame, text="确认", 
                                        command=lambda: self.del_dish_confirm(id_entry.get(), top_window))
        confirm_button.grid(row=1, column=0, padx=50, pady=10)
        cancel_button = tkinter.Button(del_frame, text="取消", command=lambda: top_window.destroy())
        cancel_button.grid(row=1, column=1, padx=15, pady=10)

    def del_dish_confirm(self, id, top_window):
        # 删除菜品确认
        tag = self.controller.del_dish(id)
        if tag:
            messagebox.showinfo("删除菜品", "删除菜品成功！")
        else:
            messagebox.showerror("删除菜品", "删除菜品失败！")
        top_window.destroy()

    def update_dish_show(self):
        # 更新菜品
        top_window = tkinter.Toplevel(self.master)
        top_window.title("修改菜品")
        # 设置窗口大小
        w, h = 300, 300
        x = (self.master.winfo_screenwidth() - w) // 2
        y = (self.master.winfo_screenheight() - h) // 2
        top_window.geometry(f"{w}x{h}+{x}+{y}")
        # 修改菜品页面组件
        update_frame = tkinter.Frame(top_window)
        update_frame.pack(fill=tkinter.BOTH, expand=True)
        # 菜品id
        id_label = tkinter.Label(update_frame, text="菜品id：")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = tkinter.Entry(update_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)
        # 菜品名
        name_label = tkinter.Label(update_frame, text="菜品名：")
        name_label.grid(row=1, column=0, padx=10, pady=10)
        name_entry = tkinter.Entry(update_frame)
        name_entry.grid(row=1, column=1, padx=10, pady=10)
        # 价格
        price_label = tkinter.Label(update_frame, text="价格:")
        price_label.grid(row=2, column=0, padx=5, pady=10)
        price_spinbox = tkinter.Spinbox(update_frame, values=self.price_list, format="%.2f")
        price_spinbox.grid(row=2, column=1, padx=5, pady=10)
        # 折扣
        discount_label = tkinter.Label(update_frame, text="折扣:")
        discount_label.grid(row=3, column=0, padx=5, pady=10)
        discount_spinbox = tkinter.Spinbox(update_frame, values=self.discount_list, format="%.2f")
        discount_spinbox.grid(row=3, column=1, padx=5, pady=10)
        # 成本
        cost_label = tkinter.Label(update_frame, text="成本:")
        cost_label.grid(row=4, column=0, padx=5, pady=10)
        cost_spinbox = tkinter.Spinbox(update_frame, values=self.cost_list, format="%.2f")
        cost_spinbox.grid(row=4, column=1, padx=5, pady=10)
        # 确认和取消
        confirm_button = tkinter.Button(update_frame, text="确认", 
                                        command=lambda: self.update_dish_confirm(id_entry.get(), name_entry.get(), price_spinbox.get(), 
                                                                              discount_spinbox.get(), cost_spinbox.get(), top_window))
        confirm_button.grid(row=5, column=0, padx=50, pady=10)
        cancel_button = tkinter.Button(update_frame, text="取消", command=lambda: top_window.destroy())
        cancel_button.grid(row=5, column=1, padx=15, pady=10)

    def update_dish_confirm(self, id, name, price, discount, cost, top_window):
        # 修改菜品确认
        tag = self.controller.update_dish(id, name, price, discount, cost)
        if tag > 0:
            messagebox.showinfo("修改菜品", "修改菜品成功！")
        else:
            messagebox.showerror("修改菜品", "修改菜品失败！")
        top_window.destroy()

    # ===== 点菜 =====

    def order_dish_show(self):
        """点菜界面"""
        top = tkinter.Toplevel(self.master)
        top.title("点菜")
        w, h = 580, 680
        x = (self.master.winfo_screenwidth() - w) // 2
        y = (self.master.winfo_screenheight() - h) // 2
        top.geometry(f"{w}x{h}+{x}+{y}")

        # 顶部信息区
        info_frame = tkinter.Frame(top)
        info_frame.pack(fill=tkinter.X, padx=10, pady=5)

        tkinter.Label(info_frame, text="桌号:", font=("微软雅黑", 12)).grid(row=0, column=0, padx=5)
        table_entry = tkinter.Entry(info_frame, width=10)
        table_entry.grid(row=0, column=1, padx=5)

        tkinter.Label(info_frame, text="备注:", font=("微软雅黑", 12)).grid(row=0, column=2, padx=5)
        note_entry = tkinter.Entry(info_frame, width=20)
        note_entry.grid(row=0, column=3, padx=5)

        # 可滚动的菜品列表
        list_frame = tkinter.Frame(top)
        list_frame.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=5)

        canvas = tkinter.Canvas(list_frame, highlightthickness=0)
        scrollbar = tkinter.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tkinter.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 表头
        tkinter.Label(scroll_frame, text="菜品名称", font=("微软雅黑", 10, "bold"),
                       width=16, anchor="w").grid(row=0, column=0, padx=5, pady=2)
        tkinter.Label(scroll_frame, text="单价", font=("微软雅黑", 10, "bold"),
                       width=8, anchor="e").grid(row=0, column=1, padx=5, pady=2)
        tkinter.Label(scroll_frame, text="数量", font=("微软雅黑", 10, "bold"),
                       width=8).grid(row=0, column=2, padx=5, pady=2)
        tkinter.Label(scroll_frame, text="小计", font=("微软雅黑", 10, "bold"),
                       width=10, anchor="e").grid(row=0, column=3, padx=5, pady=2)

        dishes = self.controller.select_dishes()
        dish_vars = []  # 每个元素: {id, name, price, discount, var, sub_label}

        for i, dish in enumerate(dishes):
            row = i + 1
            tkinter.Label(scroll_frame, text=dish['name'],
                           width=16, anchor="w").grid(row=row, column=0, padx=5, pady=3)
            tkinter.Label(scroll_frame, text=f"¥{dish['price']:.2f}",
                           width=8, anchor="e").grid(row=row, column=1, padx=5, pady=3)

            var = tkinter.IntVar(value=0)
            sub_label = tkinter.Label(scroll_frame, text="¥0.00",
                                       width=10, anchor="e")
            sub_label.grid(row=row, column=3, padx=5, pady=3)

            spin = tkinter.Spinbox(scroll_frame, from_=0, to=20,
                                    textvariable=var, width=5)
            spin.grid(row=row, column=2, padx=5, pady=3)

            info = {
                'id': dish['id'], 'name': dish['name'],
                'price': float(dish['price']), 'discount': float(dish['discount']),
                'var': var, 'sub_label': sub_label
            }
            dish_vars.append(info)
            # 数量变化时实时更新小计和总额
            var.trace_add("write",
                          lambda *args, idx=i: self._refresh_order_total(dish_vars, total_label, idx))

        # 底部总金额和确认按钮
        bottom_frame = tkinter.Frame(top)
        bottom_frame.pack(fill=tkinter.X, padx=10, pady=10)

        total_label = tkinter.Label(bottom_frame, text="总金额: ¥0.00",
                                     font=("微软雅黑", 16, "bold"), fg="red")
        total_label.pack()

        btn_frame = tkinter.Frame(bottom_frame)
        btn_frame.pack(pady=8)
        tkinter.Button(btn_frame, text="确认点菜", width=10,
                       command=lambda: self.order_dish_confirm(
                           table_entry.get(), note_entry.get(), dish_vars, top)
                       ).pack(side=tkinter.LEFT, padx=10)
        tkinter.Button(btn_frame, text="取消", width=10,
                       command=top.destroy).pack(side=tkinter.LEFT, padx=10)

    def _refresh_order_total(self, dish_vars, total_label, changed_idx):
        """实时更新单行小计和总金额"""
        info = dish_vars[changed_idx]
        qty = info['var'].get()
        sub = qty * info['price'] * info['discount']
        info['sub_label'].config(text=f"¥{sub:.2f}")

        total = sum(v['var'].get() * v['price'] * v['discount'] for v in dish_vars)
        total_label.config(text=f"总金额: ¥{total:.2f}")

    def order_dish_confirm(self, table_id, note, dish_vars, top):
        """点菜确认"""
        if not table_id.strip():
            messagebox.showwarning("提示", "请输入桌号！")
            return

        dishes = []
        for info in dish_vars:
            qty = info['var'].get()
            if qty > 0:
                dishes.append((info['id'], qty, info['price'], info['discount']))

        if not dishes:
            messagebox.showwarning("提示", "请选择至少一道菜品！")
            return

        tag = self.controller.create_order(
            table_id.strip(), self.user['id'],
            note.strip() or None, dishes
        )
        if tag:
            messagebox.showinfo("点菜成功", f"桌号 {table_id.strip()} 点菜成功！")
            top.destroy()
        else:
            messagebox.showerror("点菜失败", "点菜失败，请重试！")

    # ===== 结账 =====

    def checkout_show(self):
        """结账界面"""
        top = tkinter.Toplevel(self.master)
        top.title("结账")
        w, h = 750, 540
        x = (self.master.winfo_screenwidth() - w) // 2
        y = (self.master.winfo_screenheight() - h) // 2
        top.geometry(f"{w}x{h}+{x}+{y}")

        tkinter.Label(top, text="未结账订单", font=("微软雅黑", 12, "bold")).pack(pady=(10, 0))

        # 订单列表 Treeview
        tree_frame = tkinter.Frame(top)
        tree_frame.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=5)

        columns = ('id', 'table', 'status', 'total', 'waiter', 'time')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=6)
        tree.heading('id', text='订单号')
        tree.heading('table', text='桌号')
        tree.heading('status', text='状态')
        tree.heading('total', text='金额')
        tree.heading('waiter', text='服务员')
        tree.heading('time', text='下单时间')
        tree.column('id', width=60, anchor='center')
        tree.column('table', width=60, anchor='center')
        tree.column('status', width=80, anchor='center')
        tree.column('total', width=90, anchor='center')
        tree.column('waiter', width=80, anchor='center')
        tree.column('time', width=150)

        scrollbar = tkinter.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 加载未结账订单
        orders = self.controller.get_active_orders()
        for o in orders:
            tree.insert('', 'end', values=(
                o['id'], o['table_id'], o['status'],
                f"¥{o['total_price']:.2f}", o['user_id'],
                str(o['create_time'])
            ))

        # 详情展示框
        detail_text = tkinter.Text(top, height=12, state='disabled', font=("微软雅黑", 10))
        detail_text.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=5)

        def on_select(event):
            sel = tree.selection()
            if not sel:
                return
            item = tree.item(sel[0])
            order_id = item['values'][0]
            detail = self.controller.get_order_detail(order_id)
            if not detail:
                return
            o = detail['order']
            lines = [
                f"订单 #{o['id']}  |  桌号: {o['table_id']}  |  服务员: {o['waiter_name']}",
                f"状态: {o['status']}  |  时间: {o['create_time']}",
                f"备注: {o['note'] or '无'}",
                "-" * 60,
                f"{'菜品':<16}{'单价':<10}{'数量':<6}{'折扣':<6}{'小计':<10}",
                "-" * 60,
            ]
            for item in detail['items']:
                lines.append(
                    f"{item['dish_name']:<16}"
                    f"¥{item['unit_price']:<8.2f}"
                    f"{item['quantity']:<6}"
                    f"{item['discount']:<6}"
                    f"¥{item['subtotal']:<8.2f}"
                )
            lines.append("-" * 60)
            lines.append(f"总金额: ¥{o['total_price']:.2f}")
            detail_text.config(state='normal')
            detail_text.delete('1.0', tkinter.END)
            detail_text.insert(tkinter.END, '\n'.join(lines))
            detail_text.config(state='disabled')

        tree.bind('<<TreeviewSelect>>', on_select)

        # 按钮区
        btn_frame = tkinter.Frame(top)
        btn_frame.pack(pady=10)
        tkinter.Button(btn_frame, text="结账", width=10,
                       command=lambda: self.checkout_confirm(tree, top)
                       ).pack(side=tkinter.LEFT, padx=10)
        tkinter.Button(btn_frame, text="关闭", width=10,
                       command=top.destroy).pack(side=tkinter.LEFT, padx=10)

    def checkout_confirm(self, tree, top):
        """结账确认"""
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个订单！")
            return

        item = tree.item(sel[0])
        order_id = item['values'][0]
        total = item['values'][3]

        if messagebox.askyesno("确认结账", f"确认订单 #{order_id} 结账？\n应收金额: {total}"):
            tag = self.controller.checkout_order(order_id)
            if tag:
                messagebox.showinfo("结账成功", f"订单 #{order_id} 结账成功！")
                top.destroy()
            else:
                messagebox.showerror("结账失败", "结账失败，请重试！")

    # ===== 删除订单 =====

    def delete_order_show(self):
        """删除订单界面"""
        top = tkinter.Toplevel(self.master)
        top.title("删除订单")
        w, h = 700, 480
        x = (self.master.winfo_screenwidth() - w) // 2
        y = (self.master.winfo_screenheight() - h) // 2
        top.geometry(f"{w}x{h}+{x}+{y}")

        tkinter.Label(top, text="所有订单（点击选中后删除）", font=("微软雅黑", 12, "bold")).pack(pady=(10, 0))

        tree_frame = tkinter.Frame(top)
        tree_frame.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=5)

        columns = ('id', 'table', 'status', 'total', 'time')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        tree.heading('id', text='订单号')
        tree.heading('table', text='桌号')
        tree.heading('status', text='状态')
        tree.heading('total', text='金额')
        tree.heading('time', text='下单时间')
        tree.column('id', width=70, anchor='center')
        tree.column('table', width=60, anchor='center')
        tree.column('status', width=80, anchor='center')
        tree.column('total', width=90, anchor='center')
        tree.column('time', width=150)

        scrollbar = tkinter.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        orders = self.controller.get_all_orders()
        for o in orders:
            tree.insert('', 'end', values=(
                o['id'], o['table_id'], o['status'],
                f"¥{o['total_price']:.2f}", str(o['create_time'])
            ))

        btn_frame = tkinter.Frame(top)
        btn_frame.pack(pady=10)
        tkinter.Button(btn_frame, text="删除选中订单", width=14,
                       command=lambda: self.delete_order_confirm(tree, top)
                       ).pack(side=tkinter.LEFT, padx=10)
        tkinter.Button(btn_frame, text="关闭", width=10,
                       command=top.destroy).pack(side=tkinter.LEFT, padx=10)

    def delete_order_confirm(self, tree, top):
        """删除订单确认"""
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个订单！")
            return

        item = tree.item(sel[0])
        order_id = item['values'][0]
        status = item['values'][2]

        if not messagebox.askyesno("确认删除",
                                   f"确定要删除订单 #{order_id}（{status}）吗？\n此操作不可恢复！"):
            return

        tag = self.controller.delete_order(order_id)
        if tag:
            messagebox.showinfo("删除成功", f"订单 #{order_id} 已删除！")
            top.destroy()
        else:
            messagebox.showerror("删除失败", "删除订单失败，请重试！")

    # ===== 订单统计 =====

    def order_statistics_show(self):
        """订单统计界面"""
        top = tkinter.Toplevel(self.master)
        top.title("订单统计")
        w, h = 700, 560
        x = (self.master.winfo_screenwidth() - w) // 2
        y = (self.master.winfo_screenheight() - h) // 2
        top.geometry(f"{w}x{h}+{x}+{y}")

        tkinter.Label(top, text="订单统计报表", font=("微软雅黑", 14, "bold")).pack(pady=10)

        # 日期范围
        date_frame = tkinter.Frame(top)
        date_frame.pack(pady=5)

        tkinter.Label(date_frame, text="起始日期:", font=("微软雅黑", 11)).grid(row=0, column=0, padx=5)
        start_entry = tkinter.Entry(date_frame, width=12)
        start_entry.grid(row=0, column=1, padx=5)
        start_entry.insert(0, "2026-01-01")

        tkinter.Label(date_frame, text="截止日期:", font=("微软雅黑", 11)).grid(row=0, column=2, padx=5)
        end_entry = tkinter.Entry(date_frame, width=12)
        end_entry.grid(row=0, column=3, padx=5)
        end_entry.insert(0, "2026-12-31")

        # 统计结果显示
        result_frame = tkinter.Frame(top)
        result_frame.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=5)

        stats_label = tkinter.Label(result_frame, text="", font=("微软雅黑", 12),
                                     justify=tkinter.LEFT, anchor="nw")
        stats_label.pack(anchor="w", pady=5)

        # 热销菜品排行
        tkinter.Label(result_frame, text="热销菜品排行", font=("微软雅黑", 12, "bold"),
                       anchor="w").pack(anchor="w", pady=(10, 0))

        # Treeview for top dishes
        dish_columns = ('rank', 'name', 'quantity', 'sales')
        dish_tree = ttk.Treeview(result_frame, columns=dish_columns, show='headings', height=8)
        dish_tree.heading('rank', text='排名')
        dish_tree.heading('name', text='菜品名称')
        dish_tree.heading('quantity', text='销量')
        dish_tree.heading('sales', text='销售额')
        dish_tree.column('rank', width=50, anchor='center')
        dish_tree.column('name', width=150, anchor='center')
        dish_tree.column('quantity', width=80, anchor='center')
        dish_tree.column('sales', width=100, anchor='center')

        dish_scrollbar = tkinter.Scrollbar(result_frame, orient="vertical", command=dish_tree.yview)
        dish_tree.configure(yscrollcommand=dish_scrollbar.set)
        dish_tree.pack(fill=tkinter.BOTH, expand=True)
        dish_scrollbar.pack(side="right", fill="y")

        def query_stats():
            """查询统计"""
            start = start_entry.get().strip()
            end = end_entry.get().strip()
            if not start or not end:
                messagebox.showwarning("提示", "请输入起始和截止日期！")
                return

            stats = self.controller.get_order_statistics(start, end + " 23:59:59")
            stats_label.config(
                text=f"📊 统计期间: {start} ~ {end}\n"
                     f"   • 已结账订单数: {stats['order_count']} 单\n"
                     f"   • 总营业额: ¥{stats['total_revenue']:.2f}\n"
            )

            # 清空旧数据
            for row in dish_tree.get_children():
                dish_tree.delete(row)

            for idx, d in enumerate(stats['top_dishes'], 1):
                dish_tree.insert('', 'end', values=(
                    idx, d['name'], d['quantity'], f"¥{d['sales']:.2f}"
                ))

        tkinter.Button(top, text="查询统计", width=12,
                       command=query_stats).pack(pady=5)
        tkinter.Button(top, text="关闭", width=10,
                       command=top.destroy).pack(pady=(0, 10))
    
    def logout(self):
        # 退出登录
        self.clear_master()
        self.user = None
        self.login_show()
    
    def mainloop(self):
        # 进入主循环
        self.master.mainloop()

    def clear_master(self):
        # 清空窗口
        for widget in self.master.winfo_children():
            widget.destroy()
