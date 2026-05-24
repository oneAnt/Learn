import tkinter as tk
from tkinter import simpledialog, colorchooser, ttk

# 添加/修改车辆对话框类
class AddModifyDialog(simpledialog.Dialog):
    def __init__(self, parent):
        """
        初始化添加/修改车辆对话框
        
        Args:
            parent: 父窗口对象，对话框将在该窗口上弹出
        """
        # 初始化父类
        super().__init__(parent, title = '添加/修改车辆')

    def body(self, master):
        """
        创建对话框的主体内容（表单区域）
        
        该方法由 tkinter.Dialog 框架自动调用，用于构建对话框的界面元素。
        表单包含三个字段：车辆类型（下拉选择）、颜色（按钮选择）、车号（输入框）。
        
        Args:
            master: 对话框的主容器控件（Frame）
            
        Returns:
            返回默认焦点控件（车辆类型下拉框）
        """
        # 第一行：车辆类型标签
        tk.Label(master, text = '车辆类型:').grid(row = 0, column = 0)
        # 车辆类型使用下拉选择框
        self.type_var = tk.StringVar()
        types = ['电机车','自翻车', '轨道车', '平板车']
        # 创建下拉选择框
        self.type_cb = ttk.Combobox(master, values = types, textvariable = self.type_var)
        # 设置默认选项为第一个类型（电机车）
        self.type_cb.grid(row = 0, column = 1)

        # 第二行：颜色选择标签
        tk.Label(master, text = '颜色:').grid(row = 1, column = 0)
        # 创建颜色选择按钮
        self.color_btn = tk.Button(master, text = '选择颜色', command = self.choose_color, width = 20)
        self.color_btn.grid(row = 1, column = 1)

        # 第三行：车号标签
        tk.Label(master, text = '车号:').grid(row = 2, column = 0)
        # 创建车号输入框
        self.number_entry = tk.Entry(master)
        self.number_entry.grid(row = 2, column = 1)
        # 初始化默认颜色为灰色
        self.selected_color = '#cccccc'
        # 返回默认焦点控件（车辆类型下拉框）
        return self.type_cb

    def choose_color(self):
        """
        打开颜色选择对话框，让用户选择车辆颜色
        
        该方法作为颜色选择按钮的回调函数，点击按钮时触发。
        使用 tkinter 的 colorchooser 模块弹出系统颜色选择器，
        用户选择颜色后更新按钮背景色以直观显示当前选择。
        """
        # 打开颜色选择对话框，初始颜色为当前选中颜色
        c = colorchooser.askcolor(color=self.selected_color, parent=self)
        # 如果用户选择了颜色
        if c and c[1]:
            # 更新实例属性 selected_color 为用户选择的颜色
            self.selected_color = c[1]
            # 更新颜色按钮的背景色为用户选择的颜色
            self.color_btn.config(bg=self.selected_color)

    def apply(self):
        """
        处理用户点击确定按钮后的逻辑
        
        该方法由 tkinter.Dialog 框架自动调用，用于收集用户在表单中输入的数据，
        并将其存储到 self.result 中，供调用方获取。
        
        返回的数据格式为元组：(车辆类型, 颜色, 车号)
        """
        # 获取用户选择的车辆类型（从下拉框变量中获取）
        vtype = self.type_var.get()
        # 获取用户选择的颜色（从实例属性中获取）
        color = self.selected_color
        # 获取用户输入的车号（从输入框中获取）
        number = self.number_entry.get()
        # 将结果存储到实例属性 self.result 中，供调用方获取
        self.result = (vtype, color, number)
