import tkinter as tk
from view import ContactView
from control import ContactControl


def main():
    # 创建主窗口
    root = tk.Tk()
    contact_view = ContactView(root)
    ContactControl(contact_view)
    root.mainloop()


if __name__ == "__main__":
    main()
