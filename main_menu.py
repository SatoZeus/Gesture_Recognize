import tkinter as tk
from tkinter import font, Canvas
import subprocess
import threading
import speech_recognition as sr
import time
import random
import math
import sys
from PIL import Image, ImageTk, ImageDraw, ImageFilter

# 程序全局设置
THEME_COLOR = {
    "dark_bg": "#101218",  # 深色背景
    "light_bg": "#151824",  # 浅色背景
    "primary": "#4A86FF",  # 主色
    "secondary": "#36BFFA",  # 次色
    "success": "#34D399",  # 成功色
    "warning": "#FBBF24",  # 警告色
    "danger": "#F87171",  # 危险色
    "text_light": "#FFFFFF",  # 浅色文字
    "text_dim": "#94A3B8"  # 暗色文字
}


# 日志函数 - 输出到控制台
def log_info(message):
    print(f"[INFO] {message}")


def log_speech(message):
    print(f"[语音识别] {message}")


def log_error(message):
    print(f"[错误] {message}", file=sys.stderr)


# 定义粒子效果类
class ParticleSystem:
    def __init__(self, canvas, width, height, count=50):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.particles = []
        self.running = True

        # 创建粒子
        for _ in range(count):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.uniform(1, 3)
            speed = random.uniform(0.2, 1.0)
            angle = random.uniform(0, 2 * math.pi)
            color = random.choice([THEME_COLOR["primary"], THEME_COLOR["secondary"], "#2F80ED"])

            self.particles.append({
                "id": None,
                "x": x,
                "y": y,
                "size": size,
                "speed": speed,
                "angle": angle,
                "color": color
            })

    def update(self):
        if not self.running:
            return

        self.canvas.delete("particle")

        for p in self.particles:
            # 更新位置
            p["x"] += math.cos(p["angle"]) * p["speed"]
            p["y"] += math.sin(p["angle"]) * p["speed"]

            # 边界检查
            if p["x"] < 0:
                p["x"] = self.width
            elif p["x"] > self.width:
                p["x"] = 0

            if p["y"] < 0:
                p["y"] = self.height
            elif p["y"] > self.height:
                p["y"] = 0

            # 绘制粒子
            p["id"] = self.canvas.create_oval(
                p["x"] - p["size"],
                p["y"] - p["size"],
                p["x"] + p["size"],
                p["y"] + p["size"],
                fill=p["color"],
                outline="",
                tags="particle"
            )

        # 连接附近粒子
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i + 1:]:
                dx = p1["x"] - p2["x"]
                dy = p1["y"] - p2["y"]
                distance = math.sqrt(dx * dx + dy * dy)

                if distance < 100:  # 连接距离阈值
                    opacity = int(255 * (1 - distance / 100))
                    if opacity > 30:  # 只画可见连线
                        line_color = f"#{opacity:02x}{opacity:02x}{opacity:02x}"
                        self.canvas.create_line(
                            p1["x"], p1["y"], p2["x"], p2["y"],
                            fill=line_color, width=0.5, tags="particle"
                        )

        self.canvas.after(30, self.update)


# 创建脉冲动画效果 - 修复颜色透明度问题
class PulseEffect:
    def __init__(self, canvas, x, y, color, max_radius=80):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.max_radius = max_radius
        self.circles = []
        self.is_running = True
        # 提取基础颜色（去除#）
        self.r = int(color[1:3], 16)
        self.g = int(color[3:5], 16)
        self.b = int(color[5:7], 16)

    def start(self):
        if self.is_running:
            try:
                self.add_circle()
                self.canvas.after(1000, self.start)  # 每秒添加一个新圆
            except Exception as e:
                log_error(f"脉冲效果启动错误: {str(e)}")

    def add_circle(self):
        try:
            circle_id = self.canvas.create_oval(
                self.x, self.y, self.x, self.y,
                outline=self.color, width=2
            )
            self.circles.append({"id": circle_id, "radius": 0, "opacity": 1.0})
            self.animate_circles()
        except Exception as e:
            log_error(f"添加圆形错误: {str(e)}")

    def animate_circles(self):
        if not self.is_running:
            return

        to_remove = []

        for circle in self.circles:
            try:
                # 增加半径
                circle["radius"] += 1
                new_radius = circle["radius"]

                # 降低透明度
                if new_radius > 5:
                    circle["opacity"] = max(0, 1.0 - (new_radius / self.max_radius))

                # 设置新位置和颜色 - 修复颜色格式问题
                # 使用不透明度调整颜色亮度，而非透明度
                opacity_factor = circle["opacity"]  # 0.0-1.0
                r = int(self.r * opacity_factor)
                g = int(self.g * opacity_factor)
                b = int(self.b * opacity_factor)
                color = f"#{r:02x}{g:02x}{b:02x}"  # 生成有效的RGB颜色

                self.canvas.itemconfig(circle["id"], outline=color)
                self.canvas.coords(
                    circle["id"],
                    self.x - new_radius, self.y - new_radius,
                    self.x + new_radius, self.y + new_radius
                )

                # 标记要移除的圆
                if new_radius >= self.max_radius:
                    to_remove.append(circle)
            except Exception as e:
                log_error(f"圆形动画错误: {str(e)}")
                to_remove.append(circle)  # 出错的圆也要移除

        # 移除完成动画的圆
        for circle in to_remove:
            try:
                self.canvas.delete(circle["id"])
                self.circles.remove(circle)
            except Exception:
                pass  # 忽略移除错误

        if self.circles and self.is_running:
            self.canvas.after(20, self.animate_circles)

    def stop(self):
        self.is_running = False


# 创建优化后的按钮
class HoverButton(tk.Canvas):
    def __init__(self, master, text, command=None, width=200, height=60,
                 bg_color=THEME_COLOR["primary"], hover_color=None,
                 text_color=THEME_COLOR["text_light"], font=None, radius=10, **kwargs):
        super().__init__(master, width=width, height=height,
                         bg=master["bg"], bd=0, highlightthickness=0, **kwargs)

        self.bg_color = bg_color
        self.hover_color = hover_color or self._darker(bg_color, 0.85)
        self.text_color = text_color
        self.corner_radius = radius
        self.command = command
        self.width_val = width
        self.height_val = height

        # 创建按钮背景和文本
        self.bg_id = self.create_rounded_rect(0, 0, width, height, radius, bg_color)
        self.text_id = self.create_text(width / 2, height / 2, text=text,
                                        fill=text_color, font=font, tags="button_text")

        # 创建闪光效果
        self.shine_id = self.create_shine_effect()

        # 绑定事件
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, color):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, fill=color, outline="")

    def create_shine_effect(self):
        # 创建渐变的闪光效果
        width, height = self.width_val, self.height_val

        # 使用非常浅的白色，模拟透明效果
        line_x = -width / 4
        return self.create_line(
            line_x, 0, line_x + width / 3, height,
            width=width / 10, fill="#F0F0F0"  # 使用浅灰色替代半透明白色
        )

    def animate_shine(self):
        if not hasattr(self, 'shine_id'):
            return

        width, height = self.width_val, self.height_val
        self.coords(self.shine_id, -width / 4, 0, -width / 4 + width / 3, height)

        def move_shine():
            current_pos = self.coords(self.shine_id)
            if current_pos[0] < width * 1.2:
                self.move(self.shine_id, 5, 0)
                self.after(20, move_shine)
            else:
                self.coords(self.shine_id, -width / 4, 0, -width / 4 + width / 3, height)

        move_shine()

    def _darker(self, hex_color, factor=0.9):
        # 将颜色变暗
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f"#{int(r * factor):02x}{int(g * factor):02x}{int(b * factor):02x}"

    def _on_enter(self, event):
        self.itemconfig(self.bg_id, fill=self.hover_color)
        self.animate_shine()

    def _on_leave(self, event):
        self.itemconfig(self.bg_id, fill=self.bg_color)

    def _on_press(self, event):
        darker_color = self._darker(self.hover_color)
        self.itemconfig(self.bg_id, fill=darker_color)

    def _on_release(self, event):
        self.itemconfig(self.bg_id, fill=self.hover_color)
        if self.command:
            try:
                self.command()
            except Exception as e:
                log_error(f"按钮命令执行错误: {str(e)}")


# 语音波形可视化
class WaveformVisualizer:
    def __init__(self, canvas, x, y, width, height, color=THEME_COLOR["primary"]):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = False
        self.bars = []
        self.bar_count = 20
        self.bar_width = width / (self.bar_count * 2)

        # 创建初始波形
        self.create_bars()

    def create_bars(self):
        for i in range(self.bar_count):
            x_pos = self.x + i * self.bar_width * 2
            height = 5  # 初始高度
            bar_id = self.canvas.create_rectangle(
                x_pos, self.y - height / 2,
                       x_pos + self.bar_width, self.y + height / 2,
                fill=self.color, outline=""
            )
            self.bars.append(bar_id)

    def start_animation(self):
        self.active = True
        self.animate()

    def stop_animation(self):
        self.active = False
        # 恢复初始状态
        for bar_id in self.bars:
            try:
                self.canvas.coords(
                    bar_id,
                    self.canvas.coords(bar_id)[0],
                    self.y - 2.5,
                    self.canvas.coords(bar_id)[2],
                    self.y + 2.5
                )
            except:
                pass  # Ignore errors if the canvas or item no longer exists

    def animate(self):
        if not self.active:
            return

        for bar_id in self.bars:
            try:
                # 随机生成新高度
                if self.active:
                    new_height = random.randint(5, int(self.height))
                else:
                    new_height = 5

                # 更新柱形高度
                x1, _, x2, _ = self.canvas.coords(bar_id)
                self.canvas.coords(
                    bar_id,
                    x1, self.y - new_height / 2,
                    x2, self.y + new_height / 2
                )
            except:
                pass  # Ignore errors if the canvas or item no longer exists

        if self.active:
            self.canvas.after(100, self.animate)


# 改进的语音识别函数 - 提高精度并增加详细日志
def enhanced_voice_recognition():
    # 手势识别的多种表述
    gesture_keywords = ["手势识别", "开启手势", "进入手势", "手势模式", "检测手势",
                        "手势", "识别手势", "启动手势", "查看手势", "复健手势"]

    # 姿势识别的多种表述
    pose_keywords = ["姿势识别", "开启姿势", "进入姿势", "姿势模式", "检测姿势",
                     "姿势", "识别姿势", "启动姿势", "查看姿势", "复健姿势"]

    # 检查语音识别模块是否正常加载
    try:
        recognizer = sr.Recognizer()
        log_speech("初始化语音识别模块成功")
    except Exception as e:
        log_error(f"语音识别模块初始化失败: {str(e)}")
        label_result.config(text=f"语音识别模块初始化失败: {str(e)}", fg=THEME_COLOR["danger"])
        return

    # 更新状态显示并启动波形动画
    label_result.config(text="请说出指令...", fg=THEME_COLOR["text_light"])
    waveform.start_animation()
    log_speech("开始等待语音输入...")

    try:
        # 尝试获取麦克风
        mic = sr.Microphone()
        log_speech("麦克风初始化成功")
    except Exception as e:
        log_error(f"麦克风访问失败: {str(e)}")
        label_result.config(text=f"麦克风访问失败: {str(e)}", fg=THEME_COLOR["danger"])
        waveform.stop_animation()
        return

    with mic as source:
        try:
            # 增加环境噪声适应
            log_speech("正在调整环境噪声...")
            recognizer.dynamic_energy_threshold = True
            recognizer.adjust_for_ambient_noise(source, duration=1.0)  # 增加噪声适应时间

            # 调整参数以提高准确性
            recognizer.energy_threshold = 280  # 降低阈值以更容易检测语音
            recognizer.pause_threshold = 0.6  # 减小停顿阈值以更好地捕捉语句
            recognizer.phrase_threshold = 0.3  # 降低短语阈值
            recognizer.non_speaking_duration = 0.4  # 缩短非讲话持续时间

            log_speech(
                f"噪声参数设置完成: 能量阈值={recognizer.energy_threshold}, 停顿阈值={recognizer.pause_threshold}")

            # 等待并获取音频
            log_speech("正在监听...")
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)
            log_speech("已捕获语音内容，准备识别")
        except sr.WaitTimeoutError:
            log_speech("等待超时，未检测到语音")
            label_result.config(text="未检测到语音，请重试", fg=THEME_COLOR["warning"])
            waveform.stop_animation()
            return
        except Exception as e:
            log_error(f"录音出错: {str(e)}")
            label_result.config(text=f"录音出错: {str(e)}", fg=THEME_COLOR["warning"])
            waveform.stop_animation()
            return

    # 停止波形动画
    waveform.stop_animation()

    try:
        # 尝试识别语音（使用中文）
        label_result.config(text="正在处理...", fg=THEME_COLOR["text_dim"])
        log_speech("正在转换语音到文字...")

        # 尝试多次识别以提高准确性
        try_count = 0
        max_tries = 2
        command = None

        while try_count < max_tries:
            try:
                # 使用Google的语音识别API
                command = recognizer.recognize_google(audio, language="zh-CN")
                log_speech(f"识别结果 (尝试 {try_count + 1}): {command}")
                break
            except sr.UnknownValueError:
                try_count += 1
                if try_count < max_tries:
                    log_speech(f"第{try_count}次识别失败，重试中...")
                    continue
                else:
                    raise
            except Exception:
                raise

        if not command:
            raise sr.UnknownValueError("多次尝试后仍未能识别语音")

        # 在界面显示识别结果
        label_result.config(text=f"识别结果：{command}")
        log_speech(f"最终识别结果: 「{command}」")

        # 转换为小写并去除空格以增强匹配能力
        processed_command = command.lower().replace(" ", "")
        log_speech(f"处理后命令: {processed_command}")

        # 检查是否匹配手势识别关键词
        if any(keyword in processed_command for keyword in gesture_keywords):
            matched_keyword = next((k for k in gesture_keywords if k in processed_command), None)
            log_speech(f"匹配到手势识别关键词: {matched_keyword}")
            label_result.config(text=f"正在启动手势识别...", fg=THEME_COLOR["success"])
            fade_and_launch("hands_recognize.py")

        # 检查是否匹配姿势识别关键词
        elif any(keyword in processed_command for keyword in pose_keywords):
            matched_keyword = next((k for k in pose_keywords if k in processed_command), None)
            log_speech(f"匹配到姿势识别关键词: {matched_keyword}")
            label_result.config(text=f"正在启动姿势识别...", fg=THEME_COLOR["success"])
            fade_and_launch("pose_recognize.py")

        # 处理"退出"或"关闭"指令
        elif any(keyword in processed_command for keyword in ["退出", "关闭", "结束", "再见"]):
            matched_keyword = next((k for k in ["退出", "关闭", "结束", "再见"] if k in processed_command), None)
            log_speech(f"匹配到退出关键词: {matched_keyword}")
            label_result.config(text="正在关闭程序...", fg=THEME_COLOR["danger"])
            fade_out_and_close()

        # 处理不明确的指令
        else:
            log_speech("未匹配到任何关键词")
            label_result.config(text="指令不明确，请说\"手势识别\"或\"姿势识别\"", fg=THEME_COLOR["warning"])

    except sr.UnknownValueError:
        log_speech("无法识别语音内容")
        label_result.config(text="无法识别您的语音，请重试", fg=THEME_COLOR["warning"])
    except sr.RequestError as e:
        log_error(f"语音识别服务请求错误: {e}")
        label_result.config(text=f"语音识别服务暂时不可用: {e}", fg=THEME_COLOR["danger"])
    except Exception as e:
        log_error(f"语音识别处理错误: {str(e)}")
        label_result.config(text=f"处理出错: {str(e)}", fg=THEME_COLOR["danger"])


# 启动语音识别线程
def start_voice_recognition():
    # 禁用语音按钮防止重复点击
    button_voice.config(state="disabled")
    log_info("开始语音识别过程")

    # 创建脉冲动画效果
    try:
        pulse_effect.start()
    except Exception as e:
        log_error(f"脉冲效果启动失败: {str(e)}")

    # 在新线程中启动语音识别
    def voice_thread():
        try:
            enhanced_voice_recognition()
        except Exception as e:
            log_error(f"语音识别线程出错: {e}")
            label_result.config(text=f"语音识别出错: {str(e)[:50]}...", fg=THEME_COLOR["danger"])
        finally:
            # 重新启用语音按钮
            root.after(0, lambda: button_voice.config(state="normal"))
            log_info("语音识别过程结束，按钮已重新启用")

    threading.Thread(target=voice_thread, daemon=True).start()


# 淡出并关闭程序
def fade_out_and_close():
    log_info("正在关闭程序...")

    def fade():
        alpha = root.attributes("-alpha")
        if alpha > 0:
            alpha -= 0.05
            root.attributes("-alpha", alpha)
            root.after(30, fade)
        else:
            root.destroy()

    fade()


# 淡出并跳转至其他脚本
def fade_and_launch(script_name):
    log_info(f"准备启动脚本: {script_name}")
    # 先显示过渡动画效果
    label_result.config(text=f"正在启动...", fg=THEME_COLOR["success"])

    def delayed_fade():
        def fade():
            alpha = root.attributes("-alpha")
            if alpha > 0:
                alpha -= 0.05
                root.attributes("-alpha", alpha)
                root.after(30, fade)
            else:
                log_info(f"正在启动: {script_name}")
                root.destroy()
                subprocess.Popen(["python", script_name])

        fade()

    # 使用after代替time.sleep，避免UI冻结
    root.after(500, delayed_fade)


# 创建内容面板（简化版的玻璃效果）
def create_content_panel(parent, width, height):
    # 创建基础框架
    panel = tk.Frame(parent, width=width, height=height, bg=THEME_COLOR["light_bg"],
                     highlightbackground=THEME_COLOR["primary"], highlightthickness=2)
    panel.pack_propagate(False)  # 防止框架大小根据内容自动调整
    return panel


log_info("程序启动...")

# 主界面初始化
root = tk.Tk()
root.title("康复魔镜")

# 使用固定大小的窗口，解决缩放问题
window_width, window_height = 900, 700
root.geometry(f"{window_width}x{window_height}+100+50")
root.resizable(False, False)  # 禁止调整窗口大小以避免缩放问题
root.configure(bg=THEME_COLOR["dark_bg"])
root.attributes("-alpha", 1.0)

# 创建全屏背景画布（用于粒子效果）
bg_canvas = Canvas(root, bg=THEME_COLOR["dark_bg"], highlightthickness=0)
bg_canvas.place(x=0, y=0, width=window_width, height=window_height)

# 初始化粒子系统
log_info("初始化粒子系统...")
particle_system = ParticleSystem(bg_canvas, window_width, window_height, count=80)
particle_system.update()

# 创建主内容面板
panel_width = int(window_width * 0.7)
panel_height = int(window_height * 0.75)
panel_x = (window_width - panel_width) // 2
panel_y = (window_height - panel_height) // 2

# 使用定位而不是复杂的玻璃效果
main_frame = create_content_panel(root, panel_width, panel_height)
main_frame.place(x=panel_x, y=panel_y)

# 自定义字体
title_font = font.Font(family="Microsoft YaHei UI", size=30, weight="bold")
button_font = font.Font(family="Microsoft YaHei UI", size=14, weight="bold")
status_font = font.Font(family="Microsoft YaHei UI", size=12)

# 创建logo和标题区域
logo_frame = tk.Frame(main_frame, bg=THEME_COLOR["light_bg"])
logo_frame.pack(pady=(40, 20))

# 添加图标（用圆形替代）
logo_size = 80
logo_canvas = tk.Canvas(logo_frame, width=logo_size, height=logo_size,
                        bg=THEME_COLOR["light_bg"], highlightthickness=0)
logo_canvas.pack()

# 创建圆形图标底色
logo_canvas.create_oval(5, 5, 75, 75, fill=THEME_COLOR["primary"], outline="")

# 在圆形中心绘制图形
logo_canvas.create_text(40, 40, text="康复",
                        font=font.Font(family="Microsoft YaHei UI", size=24, weight="bold"),
                        fill="white")

# 为Logo添加脉冲效果
pulse_effect = PulseEffect(logo_canvas, 40, 40, color=THEME_COLOR["primary"], max_radius=75)

# 标题文字
label_title = tk.Label(main_frame, text="康 复 魔 镜", font=title_font, bg=THEME_COLOR["light_bg"],
                       fg=THEME_COLOR["text_light"])
label_title.pack(pady=(5, 30))

# 智能助手标语
label_subtitle = tk.Label(main_frame, text="AI 辅助康复训练系统",
                          font=("Microsoft YaHei UI", 14),
                          bg=THEME_COLOR["light_bg"], fg=THEME_COLOR["text_dim"])
label_subtitle.pack(pady=(0, 40))

# 按钮容器
buttons_frame = tk.Frame(main_frame, bg=THEME_COLOR["light_bg"])
buttons_frame.pack(pady=10)

# 按钮尺寸
btn_width = 180
btn_height = 50

# 手势识别按钮
button_gesture = HoverButton(
    buttons_frame,
    text="手势识别",
    command=lambda: fade_and_launch("hands_recognize.py"),
    width=btn_width, height=btn_height,
    bg_color=THEME_COLOR["primary"],
    font=button_font
)
button_gesture.grid(row=0, column=0, padx=15, pady=10)

# 姿势识别按钮
button_pose = HoverButton(
    buttons_frame,
    text="姿势识别",
    command=lambda: fade_and_launch("pose_recognize.py"),
    width=btn_width, height=btn_height,
    bg_color=THEME_COLOR["success"],
    font=button_font
)
button_pose.grid(row=0, column=1, padx=15, pady=10)

# 语音控制按钮 - 使用实际语音识别功能
button_voice = HoverButton(
    main_frame,
    text="语音控制",
    command=start_voice_recognition,  # 使用实际的语音识别函数
    width=btn_width, height=btn_height,
    bg_color=THEME_COLOR["secondary"],
    font=button_font
)
button_voice.pack(pady=20)

# 语音波形可视化组件
waveform_canvas = tk.Canvas(main_frame, width=250, height=40,
                            bg=THEME_COLOR["light_bg"], highlightthickness=0)
waveform_canvas.pack(pady=5)
waveform = WaveformVisualizer(waveform_canvas, 45, 20, 160, 30, color=THEME_COLOR["secondary"])

# 语音识别结果提示
label_result = tk.Label(main_frame,
                        text="点击\"语音控制\"按钮开始语音交互",
                        font=status_font,
                        bg=THEME_COLOR["light_bg"],
                        fg=THEME_COLOR["text_dim"],
                        wraplength=panel_width - 40)  # 允许文本换行
label_result.pack(pady=15)

# 底部版权信息
footer_label = tk.Label(root, text="© 2025 康复魔镜 · AI辅助康复训练系统",
                        font=("Microsoft YaHei UI", 10),
                        bg=THEME_COLOR["dark_bg"], fg=THEME_COLOR["text_dim"])
footer_label.pack(side="bottom", pady=15)

log_info("主界面初始化完成，启动主循环")

# 启动主循环
root.mainloop()