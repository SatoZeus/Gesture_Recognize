import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font, ttk
import numpy as np
from collections import deque

# 初始化 MediaPipe 手部检测
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 定义颜色常量
DARK_BG = "#121212"
LIGHT_BG = "#FAFAFA"
PRIMARY = "#3B82F6"  # 蓝色
SUCCESS = "#10B981"  # 绿色
WARN = "#F59E0B"  # 橙色
ERROR = "#EF4444"  # 红色
TEXT_DARK = "#1F2937"
TEXT_LIGHT = "#FAFAFA"
TEXT_SECONDARY = "#6B7280"

# 初始化 Tkinter 界面
root = tk.Tk()
root.title("复健魔镜")
root.geometry("1280x800")
root.configure(bg=LIGHT_BG)

# 自定义字体
title_font = font.Font(family="Microsoft YaHei UI", size=26, weight="bold")
subtitle_font = font.Font(family="Microsoft YaHei UI", size=18, weight="bold")
status_font = font.Font(family="Microsoft YaHei UI", size=16)
counter_font = font.Font(family="Microsoft YaHei UI", size=22, weight="bold")
button_font = font.Font(family="Microsoft YaHei UI", size=14, weight="bold")
footer_font = font.Font(family="Microsoft YaHei UI", size=10)


# 创建圆角边框风格函数
def create_rounded_frame(parent, bg_color, width, height, corner_radius=20):
    frame = tk.Frame(parent, bg=bg_color, width=width, height=height)

    # 创建圆角效果的画布
    canvas = tk.Canvas(frame, bg=bg_color, bd=0, highlightthickness=0)
    canvas.place(x=0, y=0, width=width, height=height)

    # 绘制圆角矩形
    canvas.create_rectangle(
        corner_radius, 0, width - corner_radius, height,
        fill=bg_color, outline=bg_color
    )
    canvas.create_rectangle(
        0, corner_radius, width, height - corner_radius,
        fill=bg_color, outline=bg_color
    )
    canvas.create_arc(
        0, 0, corner_radius * 2, corner_radius * 2,
        start=90, extent=90, fill=bg_color, outline=bg_color
    )
    canvas.create_arc(
        width - corner_radius * 2, 0, width, corner_radius * 2,
        start=0, extent=90, fill=bg_color, outline=bg_color
    )
    canvas.create_arc(
        0, height - corner_radius * 2, corner_radius * 2, height,
        start=180, extent=90, fill=bg_color, outline=bg_color
    )
    canvas.create_arc(
        width - corner_radius * 2, height - corner_radius * 2, width, height,
        start=270, extent=90, fill=bg_color, outline=bg_color
    )

    return frame


# 主容器
main_container = tk.Frame(root, bg=LIGHT_BG)
main_container.pack(fill="both", expand=True, padx=30, pady=30)

# **侧边栏** - 使用圆角边框
sidebar = create_rounded_frame(main_container, "#FFFFFF", 280, 700)
sidebar.pack(side="left", fill="y", padx=(0, 20))

# 添加阴影效果的内部容器
sidebar_content = tk.Frame(sidebar, bg="#FFFFFF", bd=0)
sidebar_content.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")

label_sidebar_title = tk.Label(sidebar_content, text="复健魔镜", font=title_font, fg=PRIMARY, bg="#FFFFFF")
label_sidebar_title.pack(pady=(30, 40))

# 状态指示器
status_indicator = tk.Canvas(sidebar_content, width=20, height=20, bg="#FFFFFF", highlightthickness=0)
status_indicator.create_oval(2, 2, 18, 18, fill=TEXT_SECONDARY, outline="")
status_indicator.pack(side="top", pady=(0, 10))

label_status = tk.Label(sidebar_content, text="等待记录手势...", font=status_font, fg=TEXT_DARK, bg="#FFFFFF")
label_status.pack(pady=(0, 30))


# 美化按钮 - 包含悬停效果
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        if self["state"] != "disabled":
            darker_color = self.calculate_darker_color(self["background"])
            self["background"] = darker_color

    def on_leave(self, e):
        if self["state"] != "disabled":
            self["background"] = self.defaultBackground

    def calculate_darker_color(self, hex_color):
        # 将十六进制颜色转换为RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        # 使颜色暗一点
        factor = 0.9
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

        # 转回十六进制
        return f"#{r:02x}{g:02x}{b:02x}"


button_record = HoverButton(sidebar_content, text="开始记录", font=button_font, fg=TEXT_LIGHT, bg=PRIMARY,
                            width=16, height=2, relief="flat", bd=0, highlightthickness=0,
                            activebackground=PRIMARY, activeforeground=TEXT_LIGHT, cursor="hand2")
button_record.pack(pady=20)

# 分隔线
separator = tk.Frame(sidebar_content, height=2, bg="#EEEEEE")
separator.pack(fill="x", pady=30)

# 计数器区域
counter_frame = tk.Frame(sidebar_content, bg="#FFFFFF")
counter_frame.pack(pady=10)

action_count = 0
label_counter_title = tk.Label(counter_frame, text="匹配成功次数", font=status_font, fg=TEXT_SECONDARY, bg="#FFFFFF")
label_counter_title.pack()

label_counter = tk.Label(counter_frame, text=f"{action_count}", font=counter_font, fg=SUCCESS, bg="#FFFFFF")
label_counter.pack(pady=10)

# **主要内容区域** - 使用圆角边框
content_frame = create_rounded_frame(main_container, "#FFFFFF", 900, 700)
content_frame.pack(side="right", fill="both", expand=True)

# 内容区域的内部容器
content_inner = tk.Frame(content_frame, bg="#FFFFFF")
content_inner.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

# 标题栏
title_bar = tk.Frame(content_inner, bg="#FFFFFF")
title_bar.pack(fill="x", pady=(10, 20))

label_content_title = tk.Label(title_bar, text="手势识别", font=subtitle_font, fg=TEXT_DARK, bg="#FFFFFF")
label_content_title.pack(side="left")

# 创建双栏布局
display_frame = tk.Frame(content_inner, bg="#FFFFFF")
display_frame.pack(fill="both", expand=True)

# **视频显示区域** - 带圆角边框
video_container = tk.Frame(display_frame, bg="#FFFFFF")
video_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

video_frame = tk.Canvas(video_container, bg="#F3F4F6", highlightthickness=0)
video_frame.pack(fill="both", expand=True)

# **比对截图区域** - 圆角边框和更好的布局
comparison_container = tk.Frame(display_frame, bg="#FFFFFF", width=260)
comparison_container.pack(side="right", fill="y", padx=(10, 0))

label_comparison = tk.Label(comparison_container, text="记录的手势", font=status_font, bg="#FFFFFF", fg=TEXT_DARK)
label_comparison.pack(pady=(0, 10))

gesture_frame = tk.Frame(comparison_container, bg="#F3F4F6", bd=1, relief="solid")
gesture_frame.pack(pady=5)

gesture_canvas = tk.Canvas(gesture_frame, bg="#F3F4F6", width=240, height=320, highlightthickness=0)
gesture_canvas.pack(padx=5, pady=5)

# **底部状态栏**
bottom_bar = tk.Frame(root, bg="#FFFFFF", height=40, bd=0)
bottom_bar.pack(side="bottom", fill="x")

footer_label = tk.Label(bottom_bar, text="© 2025 复健魔镜 · AI 训练辅助系统", font=footer_font, fg=TEXT_SECONDARY,
                        bg="#FFFFFF")
footer_label.pack(pady=10)

# **摄像头初始化**
capture = cv2.VideoCapture(0)
if not capture.isOpened():
    capture = cv2.VideoCapture(1)

recording = False
recorded_finger_states = {}  # 记录左手 & 右手手势
recorded_screenshot = None
previous_state = False
current_state = False


def update_status(message, color=TEXT_DARK):
    """更新状态文本和指示器颜色"""
    label_status.config(text=message, fg=color)
    if color == SUCCESS:
        status_indicator.itemconfig(1, fill=SUCCESS)
    elif color == ERROR:
        status_indicator.itemconfig(1, fill=ERROR)
    elif color == WARN:
        status_indicator.itemconfig(1, fill=WARN)
    else:
        status_indicator.itemconfig(1, fill=PRIMARY)


def start_recording():
    """点击'开始记录'，3 秒后记录手势"""
    update_status("请在 3 秒内摆好手势...", PRIMARY)
    button_record.config(state="disabled")
    # 添加倒计时效果
    countdown(3)


def countdown(count):
    """倒计时动画"""
    if count > 0:
        update_status(f"请准备，{count} 秒后记录...", WARN)
        root.after(1000, countdown, count - 1)
    else:
        record_hand()


def record_hand():
    """记录手势并保存截图"""
    global recording, recorded_finger_states, recorded_screenshot

    ret, frame = capture.read()
    if not ret or frame is None:
        update_status("记录失败，请重试", ERROR)
        button_record.config(state="normal")
        return

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    recorded_finger_states.clear()  # 清空之前的手势数据
    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = handedness.classification[0].label  # "Left" or "Right"
            recorded_finger_states[hand_label] = get_finger_fold_state(hand_landmarks)

    if recorded_finger_states:
        recorded_screenshot = Image.fromarray(frame_rgb)
        update_gesture_display()
        update_status("手势记录成功！请尝试复现", SUCCESS)
        recording = True
    else:
        update_status("未检测到手势，请重试", ERROR)

    button_record.config(state="normal")


button_record.config(command=start_recording)


def get_finger_fold_state(hand_landmarks):
    """计算手指折叠状态"""
    finger_fold = []
    landmarks = hand_landmarks.landmark

    for finger_tip, finger_pip in [
        (mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP),
        (mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
        (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
        (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
        (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP),
    ]:
        finger_fold.append(landmarks[finger_tip].y > landmarks[finger_pip].y)

    return tuple(finger_fold)


def update_gesture_display():
    """在 Canvas 上显示手势截图"""
    if recorded_screenshot:
        screenshot_resized = recorded_screenshot.resize((240, 320))
        img = ImageTk.PhotoImage(screenshot_resized)
        gesture_canvas.create_image(120, 160, image=img)
        gesture_canvas.image = img  # 防止垃圾回收


def update_frame():
    """摄像头画面更新 + 手势匹配"""
    global action_count, recorded_finger_states, previous_state, current_state

    ret, frame = capture.read()
    if not ret or frame is None:
        root.after(40, update_frame)
        return

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    detected_finger_states = {}

    # 绘制更美观的手部追踪效果
    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = handedness.classification[0].label
            detected_finger_states[hand_label] = get_finger_fold_state(hand_landmarks)

            # 自定义绘制样式
            drawing_spec = mp_drawing.DrawingSpec(
                color=(66, 133, 244),  # 蓝色
                thickness=2,
                circle_radius=2
            )
            connection_spec = mp_drawing.DrawingSpec(
                color=(0, 230, 118),  # 绿色
                thickness=2
            )
            mp_drawing.draw_landmarks(
                frame_rgb,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=connection_spec
            )

    if recording:
        current_state = detected_finger_states == recorded_finger_states
        if current_state:
            if not previous_state:  # 只有在状态变化时更新
                action_count += 1
                label_counter.config(text=f"{action_count}")
                update_status("匹配成功！", SUCCESS)
        else:
            if previous_state:  # 状态变化时更新
                update_status("请继续尝试匹配手势", TEXT_DARK)
        previous_state = current_state

    # 调整图像大小使其适应画布并保持纵横比
    h, w = frame_rgb.shape[:2]
    canvas_w = video_frame.winfo_width()
    canvas_h = video_frame.winfo_height()

    if canvas_w > 1 and canvas_h > 1:  # 确保画布已初始化
        # 计算适当的缩放比例
        scale = min(canvas_w / w, canvas_h / h)
        new_w, new_h = int(w * scale), int(h * scale)

        # 缩放图像
        resized_frame = cv2.resize(frame_rgb, (new_w, new_h))
        img = Image.fromarray(resized_frame)
        img = ImageTk.PhotoImage(image=img)

        # 居中显示图像
        x_offset = (canvas_w - new_w) // 2
        y_offset = (canvas_h - new_h) // 2

        video_frame.delete("all")
        video_frame.create_image(x_offset, y_offset, anchor="nw", image=img)
        video_frame.image = img

    root.after(40, update_frame)


# 确保程序正常退出时释放摄像头
root.protocol("WM_DELETE_WINDOW", lambda: (capture.release(), root.destroy()))

# 首次更新状态
update_status("等待记录手势...", TEXT_DARK)

# 开始程序循环
update_frame()
root.mainloop()