# 代码功能：飞船类
import pygame
from pygame.sprite import Sprite
from resource_manager import resource_path

class Ship(Sprite):
    """"管理飞船的类"""

    def __init__(self, ai_game):
        """"初始化飞船并设置其初始位置"""
        super().__init__() # 调用父类Sprite的初始化方法

        self.screen = ai_game.screen
        self.settings = ai_game.settings # 获取游戏设置
        self.screen_rect = ai_game.screen.get_rect()
 
        # 加载飞船图像并获取其外接矩形
        ship_image_path = resource_path('images/ship.bmp')
        self.image = pygame.image.load(ship_image_path)
        self.rect = self.image.get_rect()

        # 初始位置和移动标志
        self.rect.midbottom = self.screen_rect.midbottom # 每艘飞船都放在屏幕底部的中央
        self.moving_right = False # 向右移动标志，初始时不移动
        self.moving_left = False # 向左移动标志，初始时不移动

        # self.x存储精确的浮点数位置，self.rect.x存储实际显示的整数像素位置，两者配合实现平滑移动
        self.x = float(self.rect.x)


    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新飞船的属性x的值，而不是其外接矩形rect的属性x值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 根据self.x更新rect对象的x值（取整数部分）
        self.rect.x = self.x

    def blitme(self):
        """在制定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom

        # 重置用于跟踪飞船确切位置的属性
        self.x = float(self.rect.x)