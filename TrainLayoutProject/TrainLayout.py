import tkinter as tk
import json
from DialogModule import AddModifyDialog

class TrainLayoutAPP(object):
    # 初始化
    def __init__(self, root):
        self.root = root
        # 设置窗口标题、logo
        self.root.title("铁运机列车位置图")
        self.root.iconbitmap("./img/train.ico")
        self.root.resizable(width=False, height=False)
        # 设置窗口大小(默认最大化)
        try:
            self.root.state("zoomed") # 全屏
        except Exception:
            pass

        # 创建画布
        self.canvas_w = 1000
        self.canvas_h = 600
        self.canvas = tk.Canvas(self.root, width = self.canvas_w, height = self.canvas_h, background = "#f0f0f0")
        # 画布会自动扩展/收缩以填满整个窗口
        self.canvas.pack(fill = tk.BOTH, expand = True)
        # 获取画布实际大小（因为画布会自动调整大小，所以需要在窗口显示后获取）
        self.root.update()
        self.canvas_w = self.canvas.winfo_width()
        self.canvas_h = self.canvas.winfo_height()

        # 创建工具栏
        toolbar = tk.Frame(root, bg="#b7b7b7")
        toolbar.pack(fill="x")
        # 添加车辆按钮
        tk.Button(toolbar, text="添加车辆", command = self.add_train).pack(side = "left")
        # 删除车辆按钮
        tk.Button(toolbar, text="删除车辆", command = self.del_train).pack(side = "left")
        # 修改车辆按钮
        tk.Button(toolbar, text="修改车辆", command=self.update_train).pack(side = "left")
        # 退出按钮
        tk.Button(toolbar, text="退出", command = self.app_close).pack(side = "right")
        # 保存按钮
        tk.Button(toolbar, text="保存", command = self.app_save).pack(side ="right")

        # 画布分为四个象限（运行车、站修线、库修车、其它）
        self.regions = [
            {'name': '运行车'},   # 第一象限
            {'name': '站修线'},   # 第二象限
            {'name': '库修车'},   # 第三象限
            {'name': '其它'}      # 第四象限
        ]
        # 绘制区域划分
        self.draw_regions()

        # 加载Json文件数据并绘制车辆位置
        self.trains = []
        self.read_json()

        # 车辆拖动相关属性
        self.selected_tag = None  # 当前选中的车辆标签
        self.dragging = None  # 当前正在拖拽的车辆标签
        self.last_x = 0       # 上一次鼠标X坐标
        self.last_y = 0       # 上一次鼠标Y坐标

        # 创建右键上下文菜单
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label='删除', command=self.del_train)
        self.menu.add_command(label='修改', command=self.update_train)

    # 绘制区域划分
    def draw_regions(self):
        """
        绘制四个区域划分（将画布分为四个象限）

        该方法负责在画布上绘制四个区域的边界线和标签，
        每个区域占据画布的一个象限，从上到下、从左到右依次排列。
        
        区域布局：
        ┌─────────┬─────────┐
        │   0     │    1    │  ← 上半部分
        │ 左上    │   右上  │
        ├─────────┼─────────┤
        │   2     │    3    │  ← 下半部分
        │ 左下    │   右下  │
        └─────────┴─────────┘
        """
        # 获取画布宽度和高度（从实例属性中获取）
        w = self.canvas_w
        h = self.canvas_h
        # 计算画布中心点坐标（使用整数除法确保坐标为整数）
        half_w = w // 2  # 水平方向中点
        half_h = h // 2  # 垂直方向中点
        # 定义四个象限的坐标范围
        # 每个元组格式为: (左上角x, 左上角y, 右下角x, 右下角y)
        self.coords = [
            (0, 0, half_w, half_h),        # 象限0: 左上区域
            (half_w, 0, w, half_h),        # 象限1: 右上区域
            (0, half_h, half_w, h),        # 象限2: 左下区域
            (half_w, half_h, w, h)         # 象限3: 右下区域
        ]
        # 设置标签字体大小
        font_size = 20
        # 计算标签垂直偏移量，确保标签有足够的间距（最小16像素）
        y_offset = max(16, font_size + 6)
        # 遍历每个象限，绘制矩形边框和区域标签
        for i, rect_coords in enumerate(self.coords):
            # 在画布上绘制矩形边框
            self.canvas.create_rectangle(
                *rect_coords,              # 矩形坐标（解包元组）
                outline = '#333333',     # 边框颜色
                width = 4                  # 边框宽度
            )
            # 计算标签文本的中心点x坐标（区域水平中心）
            cx = (rect_coords[0] + rect_coords[2]) // 2
            # 计算标签文本的y坐标（区域顶部偏移y_offset）
            ty = rect_coords[1] + y_offset
            # 在区域顶部绘制区域名称标签
            self.canvas.create_text(
                cx, ty,                              # 文本位置
                text=self.regions[i]['name'],        # 从regions配置中获取区域名称
                font=('微软雅黑', font_size, 'bold'), # 字体样式
                fill='#2f4074'                     # 文本颜色
            )

    # 添加车辆
    def add_train(self):
        # 打开添加/修改车辆对话框，获取用户输入的车辆信息
        dialog = AddModifyDialog(self.root)
        # 如果用户点击了“确定”按钮，dialog.result 将包含一个元组 (车辆类型, 颜色, 车号)
        if dialog.result:
            vtype, color, number = dialog.result
            # 默认将车辆添加到第四个象限中心（其它区域）
            region_coords = self.coords[3]
            # 计算第四个象限中心点坐标
            print(f"Region 3 coords: {region_coords}")
            x = (region_coords[0]+region_coords[2])//2
            y = (region_coords[1]+region_coords[3])//2
            # 绘制车辆图标
            self.create_train(vtype, color, number, x, y)

    # 画布上绘制车辆图标
    def create_train(self, vtype, color, number, x, y, train_id=None, tag = None, save = True):
        # 车辆图标矩形大小
        w = 120
        h = 50
        # 计算矩形左上角和右下角坐标
        x1 = x - w//2
        y1 = y - h//2
        x2 = x + w//2
        y2 = y + h//2
        # 生成唯一ID
        if train_id is None:
            train_id = self.train_id
            self.train_id += 1
        # 生成唯一标签用于绑定事件
        if tag is None:
            tag = f"train_{train_id}"
        # 绘制车辆图标矩形
        rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#000', width=1, tags=(tag,'train'))
        # 绘制车辆图标文本（显示车号和类型）
        txt = self.canvas.create_text(x, y, text=f'{number}\n{vtype}', tags=(tag,'train'), font=('Arial', 10))
        # 将车辆信息保存到实例属性中
        self.trains.append({'type': vtype, 'color': color, 'number': number, 
                            'id': train_id, 'x': x, 'y': y, 'tag': tag,
                            'rect': rect, 'text': txt})
        # 绑定鼠标事件（左键按下、左键释放、鼠标移动、右键点击）到车辆图标
        self.canvas.tag_bind(tag, '<Button-1>', lambda e, t=tag: self.on_train_press(e, t))
        self.canvas.tag_bind(tag, '<ButtonRelease-1>', lambda e, t=tag: self.on_train_release(e, t))
        self.canvas.tag_bind(tag, '<B1-Motion>', lambda e, t=tag: self.on_train_move(e, t))
        self.canvas.tag_bind(tag, '<Button-3>', lambda e, t=tag: self.on_train_right(e, t))
        # 添加车辆后自动保存状态
        if save:
            self.app_save()

    # 删除车辆
    def del_train(self):
        if self.selected_tag:
            # 查找选中的车辆图标
            for train in self.trains:
                if train["tag"] == self.selected_tag:
                    data = train
                    break
            # 从实例属性中移除选中的车辆图标
            self.trains.remove(data)
            # 从画布上删除选中的车辆图标
            self.canvas.delete(data['rect'], data['text'])
            # 清除选中状态
            self.selected_tag = None
            # 删除后自动保存状态
            print(f"已删除选中车辆: {data['type'], data['number']}")
            self.app_save()

    # 修改车辆
    def update_train(self):
        if self.selected_tag:
            # 查找选中的车辆图标
            for train in self.trains:
                if train["tag"] == self.selected_tag:
                    data = train
                    break
            # 打开修改车辆对话框，获取用户输入的车辆信息
            dialog = AddModifyDialog(self.root)
            # 如果用户点击了“确定”按钮，dialog.result 将包含一个元组 (车辆类型, 颜色, 车号)
            if dialog.result:
                vtype, color, number = dialog.result
                # 更新实例属性中的车辆信息
                data['type'] = vtype
                data['color'] = color
                data['number'] = number
                # 更新画布上的车辆图标
                self.canvas.itemconfig(data['text'], text=f'{number}\n{vtype}')
                self.canvas.itemconfig(data['rect'], fill=color)
                # 更新JSON数据中的车辆信息
                self.app_save()

    # 保存
    def app_save(self):
        # 保存当前车辆数据到JSON文件
        with open("./data/trainLayout.json", "w", encoding="utf-8") as f:
            data = {
                "train_id": self.train_id,
                "trains": [
                    {
                        "type": train['type'],
                        "color": train['color'],
                        "number": train['number'],
                        "id": train['id'],
                        "x": train['x'],
                        "y": train['y'],
                        "tag": train['tag'],
                        "rect": train['rect'],
                        "text": train['text']
                    } for train in self.trains
                ]
            }
            # 保存JSON数据到文件
            json.dump(data, f, indent = 4)

    # 退出
    def app_close(self):
        self.app_save()
        self.root.destroy()

    # 读取json文件
    def read_json(self):
        # 从JSON文件加载车辆数据
        with open("./data/trainLayout.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # 从JSON数据中提取train_id和trains列表
            self.train_id = data.get("train_id")
            # 打印加载的train_id和trains数据（调试用）
            print(f"Loaded train_id: {self.train_id}")
            print(f"Loaded trains: {data.get('trains')}")
            # 遍历trains列表，重新绘制每辆车
            if self.train_id is None:
                self.train_id = 1
            # 如果trains列表为空或不存在则直接返回，不进行绘制
            if data.get("trains") is None or data.get("trains") == []:
                return
            # 遍历trains列表，重新绘制每辆车
            for train in data.get("trains"):
                self.create_train(train['type'], train['color'], train['number'], train['x'], train['y'], 
                                  train_id=train['id'], tag=train['tag'], save=False)

    # 车辆按下事件
    def on_train_press(self, event, tag):
        # 选中当前车辆
        self.select_train(tag)
        # 开始拖动
        self.dragging = tag
        self.last_x = event.x
        self.last_y = event.y
        # 提升当前车辆到最前端
        self.canvas.tag_raise(tag)

    # 车辆释放事件
    def on_train_release(self, event, tag):
        # 释放拖动
        if self.dragging == tag:
            # 释放当前车辆
            self.dragging = None
            # 保存当前状态
            self.app_save()

    # 车辆移动事件
    def on_train_move(self, event, tag):
        # 移动当前车辆
        if self.dragging != tag:
            return
        # 计算鼠标移动的距离
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        # 移动当前车辆图标
        self.canvas.move(tag, dx, dy)
        for train in self.trains:
            if train['tag'] == tag:
                train['x'] += dx
                train['y'] += dy
                break
        # 更新上次移动的坐标
        self.last_x = event.x
        self.last_y = event.y

    # 车辆右键事件
    def on_train_right(self, event, tag):
        # 在 position 显示右键菜单，锚定到鼠标位置
        self.select_train(tag)
        try:
            # 显示右键菜单
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            # 释放菜单的grab（确保菜单正常工作）
            self.menu.grab_release()

    # 选中车辆
    def select_train(self, tag):
        # 取消选中当前车辆的轮廓框
        if self.selected_tag:
            # 重置轮廓框宽度为1
            for train in self.trains:
                if train['tag'] == self.selected_tag:
                    self.canvas.itemconfig(train['rect'], width=1)
                    break
        # 选中当前车辆的轮廓框
        self.selected_tag = tag
        for train in self.trains:
            if train['tag'] == tag:
                data = train
                self.canvas.itemconfig(data['rect'], width=3)
                break
