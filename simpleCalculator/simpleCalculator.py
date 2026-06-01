import tkinter as tk


class SimpleCalculator(object):
    def __init__(self, root):
        # 设置窗口属性
        self.root = root
        self.root.title("简易计算器")
        self.root.geometry("300x400")
        # 按钮文本
        self.btn_lists = [
            ["C", "del"],
            ["1", "2", "3", "+"],
            ["4", "5", "6", "-"],
            ["7", "8", "9", "*"],
            ["0", ".", "=", "/"],
        ]
        # 数字和符号
        self.old_num = None
        self.new_num = None
        self.operator = None
        # 显示
        self.show()

    def show(self):
        # 输入框
        entry = tk.Entry(self.root, justify=tk.RIGHT, font=("微软雅黑", 18))
        entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        entry.insert(0, "0")
        # 阻止手动输入
        entry.bind("<Key>", lambda e: "break")
        # 按钮布局
        for btn_row in self.btn_lists:
            # 行布局
            btn_frame = tk.Frame(self.root)
            btn_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            for btn_text in btn_row:
                # 列布局
                btn = tk.Button(btn_frame, text=btn_text, font=("微软雅黑", 12),
                                command=lambda x=btn_text, e=entry: self.click_btn(x, e))
                btn.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.BOTH, expand=True)

    def click_btn(self, btn_text, entry):
        # 错误处理
        if entry.get() == "Error":
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        # 按钮功能
        if btn_text == "C":
            # 清空
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        elif btn_text == "del":
            # 删除
            if len(entry.get()) == 1:
                entry.delete(0, tk.END)
                entry.insert(0, "0")
            else:
                entry.delete(len(entry.get()) - 1)
        elif btn_text == "+":
            # 加
            self.operator = "+"
            self.old_num = entry.get()
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        elif btn_text == "-":
            # 减
            self.operator = "-"
            self.old_num = entry.get()
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        elif btn_text == "*":
            # 乘
            self.operator = "*"
            self.old_num = entry.get()
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        elif btn_text == "/":
            # 除
            self.operator = "/"
            self.old_num = entry.get()
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        elif btn_text == "=":
            # 等于
            self.new_num = entry.get()
            result = self.calculator(float(self.old_num), float(self.new_num), self.operator)
            entry.delete(0, tk.END)
            entry.insert(0, result)
            self.old_num = None
            self.new_num = None
            self.operator = None
        elif btn_text == ".":
            # 小数点
            if "." not in entry.get():
                entry.insert(tk.END, btn_text)
        else:
            if entry.get() == "0":
                entry.delete(0, tk.END)
            entry.insert(tk.END, btn_text)

    def calculator(self, num_1, num_2, operator):
        # 计算
        if operator == "+":
            result = num_1 + num_2
        elif operator == "-":
            result = num_1 - num_2
        elif operator == "*":
            result = num_1 * num_2
        elif operator == "/" and num_2 != 0:
            result = num_1 / num_2
        else:
            result = "Error"
        return result
