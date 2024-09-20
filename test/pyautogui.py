import pyautogui as pg
import time

# 获取屏幕分辨率
x, y = pg.size()
print(x, y)
# 获取鼠标位置
print(pg.position())
# 移动鼠标，持续时间1s, 1s内鼠标移动到x+100, y+100
pg.moveTo(100, 100, duration=1)

# 鼠标点击
pg.click()

# 鼠标左键点击，点击次数为2, 间隔0.5s, 绝对坐标（x, y）
pg.click(x, y, clicks=2, interval=0.5, button="left")

# 鼠标双击
pg.doubleClick()

# 鼠标右键点击
pg.rightClick()

# 鼠标拖拽, 持续时间1s, 1s内鼠标拖拽到x+100, y+100
pg.drag(100, 100, duration=1)

# 鼠标拖拽，绝对坐标（100, 100),持续时间1s
pg.dragTo(100, 100, duration=1)

# 鼠标按下
pg.mouseDown()

# 鼠标松开
pg.mouseUp()

# 滚动鼠标, 向上滚动100
pg.scroll(100)

# 滚动鼠标，向下滚动100
pg.scroll(-100)

# 键盘输入
pg.typewrite("hello world")

# 键盘输入，间隔0.25s
pg.write("hello world", interval=0.25)

# 按键
pg.press("enter")

# 按键1，按两次, 间隔0.5s
pg.press("1", presses=2, interval=0.5)

# 按键组合
pg.hotkey("ctrl", "c")

# 按住按键
pg.keyDown("ctrl")

# 松开按键
pg.keyUp("ctrl")

# 消息框功能

# 弹出alert框, 消息为'hello world',返回'OK',标题为'title'，按钮为'Got it', 超时时间为1s，1s后自动关闭，超时时返回'Timeout'
pg.alert("hello world", "title", "Got it", timeout=1000)

# 弹出confirm框, 消息为'hello world',返回'OK',标题为'title'，按钮为'Got it', 超时时间为1s，1s后自动关闭，超时时返回'Timeout'
pg.confirm("hello world", "title", ("OK", "Cancel"), timeout=1000)

# 弹出prompt框, 消息为'hello world',返回'OK',标题为'title'，按钮为'Got it', 超时时间为1s，1s后自动关闭，超时时返回'Timeout'
pg.prompt("hello world", "title", ("OK", "Cancel"), timeout=1000)

# 跳出密码框，返回密码
pg.password()

# 截图
pg.screenshot("test.png")

# 截图，指定区域, 左上角(0, 0), 右下角(100, 100)
pg.screenshot("test.png", region=(0, 0, 100, 100))


# 定位功能, 返回图片在屏幕上的位置, (left, top, width, height) , confidence为匹配度, 用于匹配图片的相似度, 如果没有找到返回None
pos = pg.locateOnScreen(
    "test.png", confidence=0.9, grayscale=True, region=(0, 0, 100, 100)
)
print(pos.left, pos.top, pos.width, pos.height)

# 找到图片的中心位置
center = pg.center(pos)
print(center.x, center.y)

# 直接找到图片的中心位置
pos = pg.locateCenterOnScreen(
    "test.png", confidence=0.9, grayscale=True, region=(0, 0, 100, 100)
)

# 多个图片位置
poses = pg.locateAllOnScreen(
    "test.png", confidence=0.9, grayscale=True, region=(0, 0, 100, 100)
)
for pos in poses:
    print(pos.left, pos.top, pos.width, pos.height)

# 提取像素，返回(r, g, b)颜色值
color = pg.pixel(100, 100)
print(color)

im = pg.screenshot()
color = im.getpixel((100, 100))

# 像素匹配, 返回True或False , tolerance为容差值
pg.pixelMatchesColor(100, 100, (255, 255, 255), tolerance=10)

# 根据应用程序的窗口标题，返回窗口的坐标
wins = pg.getWindowsWithTitle("MuMu模拟器12")
print(wins[0].left, wins[0].top, wins[0].width, wins[0].height)
