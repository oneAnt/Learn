import tkinter as tk
from tkinter import ttk
import datetime
import json


class AccountBookApp(object):
    def __init__(self, root):
        self.root = root
        self.file_path = "./data/accounts.json"
        self.accounts = None
        self.read_json()
        # 设置窗口标题和全屏
        self.root.title("记账簿")
        self.root.state("zoomed")
        self.root.resizable(width=False, height=False)
        # 创建工具栏
        self.toolbar = tk.Frame(self.root, bg="lightgray")
        self.toolbar.pack(side="top", fill="x")
        # 创建工具栏按钮
        self.add_button = tk.Button(self.toolbar, text="添加账目", command=self.add_account)
        self.add_button.pack(side="left")
        self.del_button = tk.Button(self.toolbar, text="删除账目", command=self.del_account)
        self.del_button.pack(side="left")
        self.update_button = tk.Button(self.toolbar, text="修改账目", command=self.update_account)
        self.update_button.pack(side="left")
        self.show_button = tk.Button(self.toolbar, text="显示账目", command=self.show_accounts)
        self.show_button.pack(side="left")
        self.quit_button = tk.Button(self.toolbar, text="退出", command=self.root.destroy)
        self.quit_button.pack(side="right")
        self.save_button = tk.Button(self.toolbar, text="保存", command=self.write_json)
        self.save_button.pack(side="right")
        # 创建画布
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        # 显示账目
        self.show_accounts()

    def add_account(self):
        # 打开添加账目窗口
        add_window = tk.Toplevel(self.root)
        add_window.title("添加账目")
        # 设置窗口大小
        w, h = 300, 220
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        add_window.geometry(f"{w}x{h}+{x}+{y}")
        # 窗口组件
        add_frame = tk.Frame(add_window)
        add_frame.pack(fill="both", expand=True)
        # 创建账目类型和选项框
        type_label = tk.Label(add_frame, text="账目类型：")
        type_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        type_var = tk.StringVar()
        types = ["收入", "支出"]
        type_cb = ttk.Combobox(add_frame, values=types, textvariable=type_var)
        type_cb.current(0)
        type_var.set(types[0])
        type_cb.grid(row=0, column=1)
        # 创建账目金额
        money_label = tk.Label(add_frame, text="账目金额：")
        money_label.grid(row=1, column=0, sticky="w", padx=20)
        money_entry = ttk.Entry(add_frame, width=22)
        money_entry.grid(row=1, column=1)
        # 创建账目原因
        cause_label = tk.Label(add_frame, text="备注：")
        cause_label.grid(row=2, column=0, sticky="w", padx=20, pady=20)
        cause_entry = ttk.Entry(add_frame, width=22)
        cause_entry.grid(row=2, column=1)
        # 确定和取消按钮
        confirm_button = ttk.Button(add_frame, text="确定", command=lambda: self.confirm_account(add_window, category=type_var.get(), money=money_entry.get(), cause=cause_entry.get()))
        confirm_button.grid(row=3, column=0, padx=20, pady=5)
        cancel_button = ttk.Button(add_frame, text="取消", command=add_window.destroy)
        cancel_button.grid(row=3, column=1, padx=20, pady=5)

    def del_account(self):
        # 打开添加账目窗口
        del_window = tk.Toplevel(self.root)
        del_window.title("删除账目")
        # 设置窗口大小
        w, h = 300, 220
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        del_window.geometry(f"{w}x{h}+{x}+{y}")
        # 窗口组件
        del_frame = tk.Frame(del_window)
        del_frame.pack(fill="both", expand=True)
        # 创建删除条目序号
        num_label = tk.Label(del_frame, text="删除条目序号：")
        num_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        num_entry = ttk.Entry(del_frame, width=22)
        num_entry.insert(0, "1")
        num_entry.grid(row=0, column=1)
        # 确定和取消按钮
        confirm_button = ttk.Button(del_frame, text="确定", command=lambda: self.confirm_account(del_window, num=num_entry.get()))
        confirm_button.grid(row=1, column=0, padx=20, pady=5)
        cancel_button = ttk.Button(del_frame, text="取消", command=del_window.destroy)
        cancel_button.grid(row=1, column=1, padx=20, pady=5)
    
    def update_account(self):
        # 打开添加账目窗口
        update_window = tk.Toplevel(self.root)
        update_window.title("修改账目")
        # 设置窗口大小
        w, h = 300, 280
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        update_window.geometry(f"{w}x{h}+{x}+{y}")
        # 窗口组件
        update_frame = tk.Frame(update_window)
        update_frame.pack(fill="both", expand=True)
        # 获取修改条目序号
        num_label = tk.Label(update_frame, text="修改条目序号：")
        num_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        num_entry = ttk.Entry(update_frame, width=22)
        num_entry.insert(0, "1")
        num_entry.grid(row=0, column=1)
        # 创建账目类型和选项框
        type_label = tk.Label(update_frame, text="账目类型：")
        type_label.grid(row=1, column=0, sticky="w", padx=20, pady=20)
        type_var = tk.StringVar()
        types = ["收入", "支出"]
        type_cb = ttk.Combobox(update_frame, values=types, textvariable=type_var)
        type_cb.current(0)
        type_var.set(types[0])
        type_cb.grid(row=1, column=1)
        # 创建账目金额
        money_label = tk.Label(update_frame, text="账目金额：")
        money_label.grid(row=2, column=0, sticky="w", padx=20)
        money_entry = ttk.Entry(update_frame, width=22)
        money_entry.grid(row=2, column=1)
        # 创建账目原因
        cause_label = tk.Label(update_frame, text="备注：")
        cause_label.grid(row=3, column=0, sticky="w", padx=20, pady=20)
        cause_entry = ttk.Entry(update_frame, width=22)
        cause_entry.grid(row=3, column=1)
        # 确定和取消按钮
        confirm_button = ttk.Button(update_frame, text="确定", command=lambda: self.confirm_account(update_window, num=num_entry.get(), category=type_var.get(), money=money_entry.get(), cause=cause_entry.get()))
        confirm_button.grid(row=4, column=0, padx=20, pady=5)
        cancel_button = ttk.Button(update_frame, text="取消", command=update_window.destroy)
        cancel_button.grid(row=4, column=1, padx=20, pady=5)


    def confirm_account(self, window, category=None, money=None, cause=None, num=None):
        # 获取时间
        now_time = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        # 判断操作类型
        if window.title() == "添加账目":
            # 更新账目列表
            self.accounts.append({"category": category, "time": now_time, "cause": cause, "money": money})
        elif window.title() == "删除账目":
            # 删除账目
            try:
                num = int(num)
                self.accounts.pop(num-1)
            except Exception:
               return
        elif window.title() == "修改账目":
            # 修改账目
            try:
                num = int(num)
                account = {"category": category, "time": now_time, "cause": cause, "money": money}
                self.accounts[num-1] = account
            except Exception:
                return
        # 写入JSON文件并显示账目
        self.write_json()
        self.show_accounts()
        # 关闭添加账目窗口
        window.destroy()

    def show_accounts(self):
        """显示所有账目记录"""
        # 清空画布
        print(self.accounts)
        self.canvas.delete("all")
        x = 20
        y = 20
        num = 1
        # 显示账目记录
        for account in self.accounts:
            txt = f"{num}  {account['category']} --- 时间：{account['time'] }  原因：{account['cause']}  金额：{account['money']}"
            self.canvas.create_text(x, y, text=txt, anchor="w",font=("微软雅黑",16))
            y += 25
            num += 1
        self.canvas.update()

    def read_json(self):
        """读取JSON文件"""
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.accounts = data.get("accounts")

    def write_json(self):
        """写入JSON文件"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            data = {
                        "account_id_sum": len(self.accounts),
                        "accounts": [
                            {
                                "category": account["category"],
                                "time": account["time"],
                                "cause": account["cause"],
                                "money": account["money"],
                            }for account in self.accounts
                        ] 
                    }
            json.dump(data, f, ensure_ascii=False, indent=4)


