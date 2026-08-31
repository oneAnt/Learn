import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ContactView(object):
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("通讯录")
        self.root.geometry("500x500+400+200")
        # 窗口大小不可调
        self.root.resizable(width=False, height=False)
        # 姓名标签和输入框
        self.name_label = ttk.Label(self.root, text="姓名:")
        self.name_label.place(x=10, y=10, width=40, height=20)
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.place(x=60, y=10, width=150, height=20)
        # 电话标签和输入框
        self.phone_label = ttk.Label(self.root, text="电话:")
        self.phone_label.place(x=220, y=10, width=40, height=20)
        self.phone_entry = ttk.Entry(self.root)
        self.phone_entry.place(x=270, y=10, width=150, height=20)
        # email标签和输入框
        self.email_label = ttk.Label(self.root, text="E-mail:")
        self.email_label.place(x=10, y=50, width=40, height=20)
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.place(x=60, y=50, width=150, height=20)
        # 地址标签和输入框
        self.address_label = ttk.Label(self.root, text="地址:")
        self.address_label.place(x=220, y=50, width=40, height=20)
        self.address_entry = ttk.Entry(self.root)
        self.address_entry.place(x=270, y=50, width=150, height=20)
        # 通讯信息显示
        # 联系人列表框架
        self.frame = ttk.Frame(self.root)
        self.frame.place(x=0, y=180, width=480, height=280)
        # 滚动条
        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # 联系人列表
        self.contact_list = ttk.Treeview(self.frame, columns=("name", "phone", "email", "address"), show="headings", yscrollcommand=self.scrollbar.set)
        self.contact_list.heading("name", text="姓名")
        self.contact_list.heading("phone", text="电话")
        self.contact_list.heading("email", text="邮箱")
        self.contact_list.heading("address", text="地址")
        self.contact_list.column("name", width=100, anchor=tk.CENTER)
        self.contact_list.column("phone", width=100, anchor=tk.CENTER)
        self.contact_list.column("email", width=100, anchor=tk.CENTER)
        self.contact_list.column("address", width=100, anchor=tk.CENTER)
        self.contact_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # 滚动条与列表结合
        self.scrollbar.config(command=self.contact_list.yview)
        # 添加按钮
        self.add_button = ttk.Button(self.root, text="添加")
        self.add_button.place(x=120, y=100, width=80, height=40)
        # 删除按钮
        self.del_button = ttk.Button(self.root, text="删除")
        self.del_button.place(x=240, y=100, width=80, height=40)

    def get_input(self):
        """获取输入数据"""
        input_data = {
            "name": self.name_entry.get().strip(),
            "phone": self.phone_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "address": self.address_entry.get().strip()
        }
        return input_data

    def get_selected_name(self):
        """获取选中项"""
        # 获取选中项的行标识
        selected = self.contact_list.selection()
        if not selected:
            return None
        # 获取选中的姓名
        name = self.contact_list.item(selected[0], "values")[0]
        return name

    def show_contacts(self, contacts):
        """显示所有联系人"""
        # 清空原列表
        for item in self.contact_list.get_children():
            self.contact_list.delete(item)
        # 重新显示
        for row in contacts:
            self.contact_list.insert("", "end", values=(row["name"], row["phone"], row["email"] or "", row["address"] or ""))

    def clear_input(self):
        """清空输入框"""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def show_messagebox(self, message):
        """弹出消息提示框"""
        messagebox.showinfo("提示", message)
