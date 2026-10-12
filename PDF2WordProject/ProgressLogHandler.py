import logging
import re


class ProgressLogHandler(logging.Handler):
    """
    拦截 pdf2docx 日志，把其中的进度信息换算成百分比并回调

    日志示例:
        [1/4] Opening document...   -> 打开文档
        [2/4] Analyzing document... -> 分析文档
        [3/4] Parsing pages...      -> 逐页解析
        (1/5) Page 1                -> 第1页/共5页
        [4/4] Creating pages...     -> 生成 Word
    """
    # 每个阶段映射到进度条上的百分比区间: (起始, 结束)
    STAGES = {
        "[1/4]": (0, 5),
        "[2/4]": (5, 10),
        "[3/4]": (10, 60),
        "[4/4]": (60, 100),
    }

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.start = 0
        self.end = 100

    def emit(self, record):
        msg = record.getMessage()
        # 阶段切换: 更新当前进度区间
        for key, (start, end) in self.STAGES.items():
            if key in msg:
                self.start, self.end = start, end
                self.callback(start)
                return
        # 页级进度: (1/5) Page 1
        m = re.search(r"\((\d+)/(\d+)\)", msg)
        if m:
            i, total = int(m.group(1)), int(m.group(2))
            self.callback(self.start + (self.end - self.start) * i / total)