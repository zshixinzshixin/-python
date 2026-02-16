# 代码功能：绘制一个黄色的五角星
from turtle import *

color('red', 'yellow')  # 设置画笔颜色和填充颜色：红色边框，黄色填充
begin_fill() # 开始填充形状
while True:
    forward(200) # 海龟向前移动200像素
    left(170) # 海龟向左转170度
    # 检查海龟是否回到起点附近（位置坐标接近(0,0)）
    if abs(pos()) < 1:
        break
end_fill() # 结束填充，完成黄色填充
done() # 保持绘图窗口打开，直到用户手动关闭
