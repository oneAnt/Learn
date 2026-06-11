import tkinter as tk
import json
from tkinter import messagebox
import datetime


class BookManageSystem(object):
    def __init__(self, root):
        self.root = root
        self.root.title("图书管理系统")
        self.root.state("zoomed")
        self.page_frame = tk.Frame(self.root)
        self.main_frame = None
        self.page_frame.pack(fill=tk.BOTH, expand=True)
        # 数据
        self.books = self.read_books()
        self.borrows = self.read_borrows()
        # 登录页面
        self.login_tag = False
        self.login_page()

    def clear_page(self, page_frame):
        # 清除当前页面所有组件
        for widget in page_frame.winfo_children():
            widget.destroy()

    def login_page(self):
        # 登录页面
        login_frame= tk.Frame(self.page_frame)
        login_frame.pack(fill=tk.BOTH, expand=True)
        # 登录页面组件 用户名/密码
        username_label = tk.Label(login_frame, text="用户名：")
        username_label.grid(row=0, column=0, padx=10, pady=10)
        username_entry = tk.Entry(login_frame)
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        password_label = tk.Label(login_frame, text="密码：")
        password_label.grid(row=1, column=0, padx=10, pady=10)
        password_entry = tk.Entry(login_frame, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        # 登录按钮
        login_button = tk.Button(login_frame, text="登录", 
                                 command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    
    def login(self, username, password):
        # 验证用户名和密码
        with open("./data/users.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for user in data["users"]:
            if user["username"] == username and user["password"] == password:
                messagebox.showinfo("登录成功", f"欢迎 {username}!")
                self.login_tag = True
                break
        if not self.login_tag:
            messagebox.showerror("登录失败", "请检查用户名或密码！")
        else:
            self.main_page()
    
    def main_page(self):
        self.clear_page(self.page_frame)
        # 主页面布局
        self.main_frame = tk.Frame(self.page_frame)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # 主页面组件
        toolbar = tk.Frame(self.main_frame, bg="white")
        toolbar.pack(side=tk.TOP, fill=tk.X)
        add_button = tk.Button(toolbar, text="添加图书", command=self.add_book)
        add_button.pack(side=tk.LEFT)
        del_button = tk.Button(toolbar, text="删除图书", command=self.del_book)
        del_button.pack(side=tk.LEFT)
        search_button = tk.Button(toolbar, text="搜索图书", command=self.search_book)
        search_button.pack(side=tk.LEFT)
        borrow_button = tk.Button(toolbar, text="借阅图书", command=self.borrow_book)
        borrow_button.pack(side=tk.LEFT)
        return_button = tk.Button(toolbar, text="归还图书", command=self.return_book)
        return_button.pack(side=tk.LEFT)
        record_button = tk.Button(toolbar, text="借阅记录", command=self.show_borrows)
        record_button.pack(side=tk.LEFT)
        quit_button = tk.Button(toolbar, text="退出系统", command=self.quit)
        quit_button.pack(side=tk.RIGHT)
        logout_button = tk.Button(toolbar, text="退出登录", command=self.logout)
        logout_button.pack(side=tk.RIGHT)
    
    def read_books(self):
        with open("./data/books.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["books"]
    
    def save_books(self):
        with open("./data/books.json", "w", encoding="utf-8") as f:
            json.dump({"books": self.books}, f, ensure_ascii=False, indent=4)

    def read_borrows(self):
        with open("./data/borrow.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["borrows"]
    
    def save_borrows(self):
        with open("./data/borrow.json", "w", encoding="utf-8") as f:
            json.dump({"borrows": self.borrows}, f, ensure_ascii=False, indent=4)

    def add_book(self):
        top_window = tk.Toplevel(self.root)
        top_window.title("添加图书")
        # 设置窗口大小
        w, h = 300, 150
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        top_window.geometry(f"{w}x{h}+{x}+{y}")
        # 添加图书页面组件
        add_frame = tk.Frame(top_window)
        add_frame.pack(fill=tk.BOTH, expand=True)
        # 添加图书页面组件
        book_id_label = tk.Label(add_frame, text="图书编号：")
        book_id_label.grid(row=0, column=0, padx=10, pady=10)
        book_id_entry = tk.Entry(add_frame)
        book_id_entry.grid(row=0, column=1, padx=10, pady=10)
        book_name_label = tk.Label(add_frame, text="图书名称：")
        book_name_label.grid(row=1, column=0, padx=10, pady=10)
        book_name_entry = tk.Entry(add_frame)
        book_name_entry.grid(row=1, column=1, padx=10, pady=10)
        # 确认和取消
        confirm_button = tk.Button(add_frame, text="确认", command=lambda: self.add_book_confirm(book_id_entry.get(), book_name_entry.get(), top_window))
        confirm_button.grid(row=2, column=0, padx=50, pady=10)
        cancel_button = tk.Button(add_frame, text="取消", command=lambda: top_window.destroy())
        cancel_button.grid(row=2, column=1, padx=15, pady=10)
    
    def add_book_confirm(self, book_id, book_name, top_window=None):
        if not book_id or not book_name:
            messagebox.showerror("添加失败", "请输入图书编号和名称！")
            return
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        borrow_tag = "否"
        borrow_time = ""
        borrow_person = ""
        book = {
                "图书编号": book_id, 
                "图书名称": book_name,
                "添加时间": time,
                "借阅状态": borrow_tag,
                "借阅时间": borrow_time,
                "借阅人": borrow_person,
                }
        self.books.append(book)
        self.save_books()
        if top_window:
            top_window.destroy()
        messagebox.showinfo("添加成功", f"图书 {book_name} 已添加！")

    def del_book(self):
        top_window = tk.Toplevel(self.root)
        top_window.title("删除图书")
        # 设置窗口大小
        w, h = 300, 150
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        top_window.geometry(f"{w}x{h}+{x}+{y}")
        # 删除图书页面组件
        del_frame = tk.Frame(top_window)
        del_frame.pack(fill=tk.BOTH, expand=True)
        # 删除图书页面组件
        book_id_label = tk.Label(del_frame, text="图书编号")
        book_id_label.grid(row=0, column=0, padx=10, pady=10)
        book_id_entry = tk.Entry(del_frame)
        book_id_entry.grid(row=0, column=1, padx=10, pady=10)
        # 确认和取消
        confirm_button = tk.Button(del_frame, text="确认", command=lambda: self.del_book_confirm(book_id_entry.get(), top_window))
        confirm_button.grid(row=1, column=0, padx=50, pady=10)
        cancel_button = tk.Button(del_frame, text="取消", command=lambda: top_window.destroy())
        cancel_button.grid(row=1, column=1, padx=15, pady=10)

    def del_book_confirm(self, book_id, top_window=None):
        if not book_id:
            messagebox.showerror("删除失败", "请输入图书编号！")
            if top_window:
                top_window.destroy()
            return
        for book in self.books:
            if book["图书编号"] == book_id:
                self.books.remove(book)
                self.save_books()
                if top_window:
                    top_window.destroy()
                messagebox.showinfo("删除成功", f"图书 {book['图书名称']} 已删除！")
                return

    def search_book(self):
        top_window = tk.Toplevel(self.root)
        top_window.title("查询图书")
        # 设置窗口大小
        w, h = 300, 150
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        top_window.geometry(f"{w}x{h}+{x}+{y}")
        # 查询图书页面组件
        search_frame = tk.Frame(top_window)
        search_frame.pack(fill=tk.BOTH, expand=True)
        # 查询图书页面组件
        book_id_label = tk.Label(search_frame, text="图书编号")
        book_id_label.grid(row=0, column=0, padx=10, pady=10)
        book_id_entry = tk.Entry(search_frame)
        book_id_entry.grid(row=0, column=1, padx=10, pady=10)
        # 确认和取消
        confirm_button = tk.Button(search_frame, text="确认", command=lambda: self.search_book_confirm(book_id_entry.get(), top_window))
        confirm_button.grid(row=1, column=0, padx=50, pady=10)
        cancel_button = tk.Button(search_frame, text="取消", command=lambda: top_window.destroy())
        cancel_button.grid(row=1, column=1, padx=15, pady=10)

    def search_book_confirm(self, book_id, top_window=None):
        self.main_page()
        search_canvas = tk.Canvas(self.main_frame, bg="white")
        search_canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        # 绑定滚动条
        scrollbar = tk.Scrollbar(self.main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        search_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=search_canvas.yview)
        # 显示查询结果
        if not book_id:
            # 显示所有图书
            i = 1
            for book in self.books:
                # 处理借阅状态为空的情况
                txt = f"\n图书编号: {book['图书编号']} 图书名称: {book['图书名称']} 添加时间: {book['添加时间']} 借阅状态: {book['借阅状态']} 借阅时间: {book['借阅时间'] or '无'} 借阅人: {book['借阅人'] or '无'}"
                search_canvas.create_text(10, 30*i, text=txt, anchor=tk.NW, font=("微软雅黑", 16))
                i += 1
        else:
            # 显示查询结果
            for book in self.books:
                if book["图书编号"] == book_id:
                    txt = f"\n图书编号: {book['图书编号']} 图书名称: {book['图书名称']} 添加时间: {book['添加时间']} 借阅状态: {book['借阅状态']} 借阅时间: {book['借阅时间'] or '无'} 借阅人: {book['借阅人'] or '无'}"
                    search_canvas.create_text(10, 10, text=txt, anchor=tk.NW, font=("微软雅黑", 16))
                    break
        search_canvas.config(scrollregion=search_canvas.bbox("all"))
        top_window.destroy()

    def borrow_book(self):
        top_window = tk.Toplevel(self.root)
        top_window.title("借阅图书")
        # 设置窗口大小
        w, h = 300, 150
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        top_window.geometry(f"{w}x{h}+{x}+{y}")
        # 借阅图书页面组件
        borrow_frame = tk.Frame(top_window)
        borrow_frame.pack(fill=tk.BOTH, expand=True)
        # 借阅图书页面组件
        book_id_label = tk.Label(borrow_frame, text="图书编号")
        book_id_label.grid(row=0, column=0, padx=10, pady=10)
        book_id_entry = tk.Entry(borrow_frame)
        book_id_entry.grid(row=0, column=1, padx=10, pady=10)
        borrow_person_label = tk.Label(borrow_frame, text="借阅人")
        borrow_person_label.grid(row=1, column=0, padx=10, pady=10)
        borrow_person_entry = tk.Entry(borrow_frame)
        borrow_person_entry.grid(row=1, column=1, padx=10, pady=10)
        # 确认和取消
        confirm_button = tk.Button(borrow_frame, text="确认", command=lambda: self.borrow_book_confirm(book_id_entry.get(), borrow_person_entry.get(), top_window))
        confirm_button.grid(row=2, column=0, padx=50, pady=10)
        cancel_button = tk.Button(borrow_frame, text="取消", command=lambda: top_window.destroy())
        cancel_button.grid(row=2, column=1, padx=15, pady=10)
    
    def borrow_book_confirm(self, book_id, borrow_person, top_window=None):
        if not book_id:
            messagebox.showerror("借阅失败", "请输入图书编号！")
            if top_window:
                top_window.destroy()
            return
        for book in self.books:
            if book["图书编号"] == book_id:
                if book["借阅状态"] == "是":
                    messagebox.showerror("借阅失败", f"图书 {book['图书名称']} 已被借出！")
                    if top_window:
                        top_window.destroy()
                    return
                else:
                    book["借阅状态"] = "是"
                    book["借阅时间"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    book["借阅人"] = borrow_person
                    self.save_books()
                    borrow_record  = {
                        "图书编号": book["图书编号"],
                        "图书名称": book["图书名称"],
                        "借阅人": borrow_person,
                        "借阅时间": book["借阅时间"],
                        "是否归还": "否",
                        "归还时间": "",
                    }
                    self.borrows.append(borrow_record)
                    self.save_borrows()
                    messagebox.showinfo("借阅成功", f"图书 {book['图书名称']} 已借出！")
                    if top_window:
                        top_window.destroy()
                    return

    def return_book(self):
        top_window = tk.Toplevel(self.root)
        top_window.title("归还图书")
        # 设置窗口大小
        w, h = 300, 150
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        top_window.geometry(f"{w}x{h}+{x}+{y}")
        # 归还图书页面组件
        return_frame = tk.Frame(top_window)
        return_frame.pack(fill=tk.BOTH, expand=True)
        # 归还图书页面组件
        book_id_label = tk.Label(return_frame, text="图书编号")
        book_id_label.grid(row=0, column=0, padx=10, pady=10)
        book_id_entry = tk.Entry(return_frame)
        book_id_entry.grid(row=0, column=1, padx=10, pady=10)
        # 确认和取消
        confirm_button = tk.Button(return_frame, text="确认", command=lambda: self.return_book_confirm(book_id_entry.get(), top_window))
        confirm_button.grid(row=2, column=0, padx=50, pady=10)
        cancel_button = tk.Button(return_frame, text="取消", command=lambda: top_window.destroy())
        cancel_button.grid(row=2, column=1, padx=15, pady=10)
    
    def return_book_confirm(self, book_id, top_window=None):
        if not book_id:
            messagebox.showerror("归还失败", "请输入图书编号！")
            if top_window:
                top_window.destroy()
            return
        for book in self.books:
            if book["图书编号"] == book_id:
                if book["借阅状态"] == "否":
                    messagebox.showerror("归还失败", f"图书 {book['图书名称']} 未被借出！")
                    if top_window:
                        top_window.destroy()
                    return
                else:
                    book["借阅状态"] = "否"
                    book["借阅时间"] = ""
                    book["借阅人"] = ""
                    for borrow in self.borrows:
                        if borrow["图书编号"] == book_id and borrow["是否归还"] == "否":
                            borrow["是否归还"] = "是"
                            borrow["归还时间"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            break
                    self.save_books()
                    self.save_borrows()
                    messagebox.showinfo("归还成功", f"图书 {book['图书名称']} 已归还！")
                    if top_window:
                        top_window.destroy()
                    return
    
    def show_borrows(self):
        self.main_page()
        borrow_canvas = tk.Canvas(self.main_frame, bg="white")
        borrow_canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        # 绑定滚动条
        scrollbar = tk.Scrollbar(self.main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        borrow_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=borrow_canvas.yview)
        # 显示借阅记录
        i = 1
        for borrow in self.borrows:
            txt = f"\n图书编号：{borrow['图书编号']} 图书名称：{borrow['图书名称']} 借阅人：{borrow['借阅人']} 借阅时间：{borrow['借阅时间']} 是否归还：{borrow['是否归还']} 归还时间：{borrow['归还时间']}"
            borrow_canvas.create_text(10, 30*i, text=txt, anchor=tk.NW, font=("微软雅黑", 16))
            i += 1
        borrow_canvas.config(scrollregion=borrow_canvas.bbox("all"))

    def quit(self):
        self.save_books()
        self.save_borrows()
        self.root.destroy()
    
    def logout(self):
        self.login_tag = False
        self.clear_page(self.page_frame)
        self.login_page()
