# 1.引用数据库和函数 
from turtle import * 
from gamebase import square 
from random import randint 
from time import sleep 
import tkinter as tk  # 导入tkinter模块


# 2.定义变量 
snake = [[0, 0], [10, 0], [20, 0], [30, 0], [40, 0], [50, 0]] 
apple_x = randint(-20,18)*10 # 苹果的中心坐标为(-200, -200)到(200, 200)之间的随机整数，且是10的倍数 
apple_y = randint(-20,19)*10 # 苹果的中心坐标为(-200, -200)到(200, 200)之间的随机整数，且是10的倍数 
aim_x = 10 
aim_y = 0 
game_started = False  # 游戏是否开始的标志 
start_button = None  # 全局变量，存储开始按钮引用


# 3.定义函数 
def changeAim(x, y): # 改变蛇的移动方向 
    global aim_x, aim_y # 全局变量，在函数中可以使用和修改 
    aim_x = x 
    aim_y = y 

def inside_map(): # 判断坐标是否在窗口内 
    return -200 <= snake[-1][0] <= 180 and -190 <= snake[-1][1] <= 190 

def bindKeys(callback, keys): 
    '''为keys中的每个键绑定callback事件''' 
    for key in keys: 
        onkey(callback, key) 

def inside_snake(): # 判断坐标是否在蛇的身体内 
    for n in range(len(snake) - 1): # 遍历蛇的身体，不包括蛇头 
        if snake[n][0] == snake[-1][0] and snake[n][1] == snake[-1][1]: # 坐标与蛇的身体某一部分重合 
            return True # 坐标在蛇的身体内 
    return False # 坐标不在蛇的身体内 

def reset_game(): # 重置游戏状态函数 
    global snake, apple_x, apple_y, aim_x, aim_y 
    # 重置蛇的初始位置 
    snake = [[0, 0], [10, 0], [20, 0], [30, 0], [40, 0], [50, 0]] 
    # 重置苹果位置 
    apple_x = randint(-20,18)*10 
    apple_y = randint(-20,19)*10 
    # 重置移动方向 
    aim_x = 10 
    aim_y = 0 

def init_start_ui(root): # 初始化开始界面UI函数
    global start_button
    
    # 在按钮上方添加游戏标题 
    title_label = tk.Label(root, text="贪吃蛇游戏", font=("Arial", 16, "bold")) 
    title_label.pack(pady=10) 

    # 添加游戏说明 
    info_label = tk.Label(root, text="使用方向键或WASD控制蛇移动", font=("Arial", 10)) 
    info_label.pack(pady=5) 
    
    # 创建开始按钮 
    start_button = tk.Button(root, text="开始游戏", font=("Arial", 12)) 

    # 定义按钮回调函数 
    def on_start_click(): 
        global game_started 
        if not game_started: 
            game_started = True 
            start_button.pack_forget()  # 隐藏按钮 
            gameLoop()  # 开始游戏循环 

    # 绑定回调函数 
    start_button.config(command=on_start_click) 

    # 放置按钮（使用pack布局，居中显示） 
    start_button.pack(pady=20)
    
    return start_button

def gameLoop(): # 游戏循环函数 
    global apple_x, apple_y, aim_x, aim_y, snake # 全局变量，在函数中可以使用和修改 
    
    all_keys = ["Right", "Left", "Up", "Down", "d", "D", "a", "A", "w", "W", "s", "S"] # 所有方向键（包括大写字母） 
    for key in all_keys: # 清除所有方向键的事件监听器（当蛇改变方向后，之前为其他方向设置的监听器仍然存在，需要清除） 
        onkey(None, key) 
    
    # 重新设置键盘事件监听器 
    listen() 
    if aim_x != -10: # 蛇的移动方向不是向左 
        bindKeys(lambda: changeAim(10, 0), ["Right", "d", "D"]) # 向右移动 
    if aim_x != 10: # 蛇的移动方向不是向右 
        bindKeys(lambda: changeAim(-10, 0), ["Left", "a", "A"]) # 向左移动 
    if aim_y != -10: # 蛇的移动方向不是向下 
        bindKeys(lambda: changeAim(0, 10), ["Up", "w", "W"]) # 向上移动 
    if aim_y != 10: # 蛇的移动方向不是向上 
        bindKeys(lambda: changeAim(0, -10), ["Down", "s", "S"]) # 向下移动 

    # 蛇头移动到新的位置 
    snake.append([snake[-1][0] + aim_x, snake[-1][1] + aim_y]) 

    # snake是否吃到苹果 
    if snake[-1][0] != apple_x or snake[-1][1] != apple_y: # 蛇头没有吃到苹果 
        snake.pop(0) # 蛇身缩短一格 
    else: # 蛇头吃到苹果 
        # 不需要缩短蛇身，只需要重新生成苹果 
        apple_x = randint(-20,18)*10 
        apple_y = randint(-20,19)*10 

    # snake是否超出窗口范围或撞到了蛇身 
    if (not inside_map()) or inside_snake(): # 蛇头超出了窗口范围或撞到了蛇身 
        square(snake[-1][0], snake[-1][1], 10, "red") # 绘制一个红色的蛇头，中心坐标为(snake[-1][0], snake[-1][1])，边长为10 
        update() # 更新窗口显示 
        sleep(2) # 等待2秒 

        # 重置游戏状态 
        reset_game() 

        # return # 游戏结束 
    
    clear() # 清除窗口上的所有绘制 

    # 1.绘制窗口边框 
    square(-210, -200, 410, "black") 
    square(-200, -190, 390, "white") # 绘制一个白色的游戏区域，中心坐标为(-200, -200)，边长为400 

    # 2.绘制苹果 
    square(apple_x, apple_y, 10, "red") 

    # 3.循环绘制蛇身 
    for n in range(len(snake)): 
        segment = snake[n] # 获取蛇身的第n个元素，即坐标列表 
        square(segment[0], segment[1], 10, "green") # 绘制一个绿色的蛇身，中心坐标为(segment[0], segment[1])，边长为10 
    
    # 4.计算游戏速度（蛇越长速度越快） 
    speed = max(100, 400 - len(snake) * 20) 
    ontimer(gameLoop, speed)  # 根据蛇长度调整速度 

    update() # 更新窗口显示 

# 4.主程序 
if __name__ == "__main__": 
    setup(420, 420, 0, 0) # 设置窗口大小为420x420，窗口位置为(0, 0) 
    hideturtle() # 隐藏 turtle 图标，不显示移动轨迹 
    tracer(False) # 关闭 turtle 动画，立即绘制 

    # 获取turtle窗口对应的tkinter主窗口 
    root = getcanvas().master 
    
    # 初始化开始界面UI 
    init_start_ui(root) 

    done() # 启动tkinter主循环