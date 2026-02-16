from turtle import *

def square(x, y, size, color_name):
    up()
    goto(x, y)
    down()
    color(color_name)
    begin_fill()

    for i in range(4): # 绘制正方形
        forward(size)
        left(90)

    end_fill() # 填充颜色

if __name__ == "__main__":
    setup(420, 420, 0, 0) # 设置窗口大小为420x420，窗口位置为(0, 0)
    hideturtle() # 隐藏 turtle 图标，不显示移动轨迹
    tracer(False) # 关闭 turtle 动画，立即绘制
    square(50, 50, 100, "red") # 绘制一个红色的正方形，中心坐标为(50, 50)，边长为100
    done() # 保持窗口显示
