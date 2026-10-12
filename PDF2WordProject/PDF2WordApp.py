import tkinter as tk
import threading
import logging
from tkinter import filedialog, messagebox, ttk
from pdf2docx import Converter
from ProgressLogHandler import ProgressLogHandler


class PDF2WordApp(object):
    """
    PDF转Word
    """
    def __init__(self):
        self.root = tk.Tk()
        self.pdf_path = None
        self.word_path = None
        self.show_label = None
        self.progress = None
        self.progress_label = None
        # 窗口标题
        self.root.title("PDF转Word")
        # 窗口大小
        self.root.geometry("400x350")
        # 窗口不可调整大小
        self.root.resizable(False, False)
        # 初始化UI
        self.init_ui()

    def init_ui(self):
        """
        UI界面
        :return:
        """
        # 标题
        tk.Label(self.root, text="PDF转Word工具",
                 font=("Microsoft YaHei", 14, "bold")).pack(pady=10)
        # 选择文件按钮
        tk.Button(self.root, text="选择PDF文件",
                  command=self.select_file).pack(pady=10)
        # 转换按钮
        tk.Button(self.root, text="转换",
                  command=self.convert_btn).pack(pady=10)
        # 进度条（只创建一次，通过 config 更新）
        self.progress = ttk.Progressbar(self.root, length=300,
                                        maximum=100, mode="determinate")
        self.progress.pack(pady=5)
        # 进度百分比文字
        self.progress_label = tk.Label(self.root, text="进度：0%")
        self.progress_label.pack()

    def select_file(self):
        """
        选择文件
        """
        # 获取pdf
        self.pdf_path = tk.filedialog.askopenfilename(title="选择PDF", filetypes=[("PDF文档", "*.pdf")])
        # 显示文件名
        self.show_label = tk.Label(self.root, text=self.pdf_path, wraplength=400,
                 justify="center")
        self.show_label.pack(pady=10)

    def convert_btn(self):
        """
        转换操作
        """
        # 转换
        if self.pdf_path is None:
            messagebox.showerror("错误", "请选择PDF文件")
            return
        self.word_path = self.pdf_path.replace(".pdf", ".docx")
        # 重置进度
        self.set_progress(0)
        # 转换
        threading.Thread(target=self.convert).start()

    def set_progress(self, percent):
        """
        更新进度条
        """
        # 该方法在子线程中被调用，用 after 转发到主线程执行 UI 更新，保证线程安全
        def _update():
            self.progress.config(value=percent)
            self.progress_label.config(text=f"进度：{percent:.0f}%")
        self.root.after(0, _update)

    def convert(self):
        """
        pdf转docx
        """
        # 挂载日志处理器，实时捕获转换进度
        handler = ProgressLogHandler(self.set_progress)
        logger = logging.getLogger()
        logger.addHandler(handler)
        try:
            cv = Converter(self.pdf_path)
            cv.convert(self.word_path)
            cv.close()
            # 兜底：确保进度显示 100%
            self.set_progress(100)
            self.root.after(0, lambda: messagebox.showinfo("成功", "转换完成"))
        except Exception as e:
            # 先取出错误信息，避免 lambda 执行时 except 变量 e 已被销毁
            error_msg = str(e)
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
        finally:
            # 必须移除 handler，否则多次转换后 handler 累积、回调重复触发
            logger.removeHandler(handler)

    def run(self):
        """
        app启动
        """
        self.root.mainloop()
