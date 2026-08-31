from model import ContactModel
from view import ContactView


class ContactControl(object):
    def __init__(self, view:ContactView):
        self.view = view
        self.model = ContactModel()
        self.del_name = None
        # 绑定事件
        self.view.add_button.config(command=self.add_button_click)
        self.view.del_button.config(command=self.del_button_click)
        # 绑定联系人列表点击事件,当用户点击选中表格某一行时触发
        self.view.contact_list.bind("<<TreeviewSelect>>", self.contact_list_click)
        self.refresh_contacts()

    def add_button_click(self):
        # 添加按钮
        input_info = self.view.get_input()
        # 判断姓名是否已存在
        for row in self.model.get_contacts():
            if input_info["name"] == row["name"]:
                self.view.show_messagebox("姓名已存在！")
                return
        self.model.add_contact(**input_info)
        self.refresh_contacts()
        self.view.show_messagebox("添加成功！")

    def del_button_click(self):
        # 删除按钮
        if self.del_name:
            self.model.delete_contact(self.del_name)
            self.del_name = None
        self.refresh_contacts()
        self.view.show_messagebox("删除成功！")

    def contact_list_click(self, event):
        # 列表点击事件
        name = self.view.get_selected_name()
        self.del_name = name

    def refresh_contacts(self):
        # 刷新列表和清空输入框
        self.view.show_contacts(self.model.get_contacts())
        self.view.clear_input()
