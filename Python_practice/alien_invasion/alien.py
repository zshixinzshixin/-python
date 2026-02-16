import pygame
from pygame.sprite import Sprite
from resource_manager import resource_path

class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置rect属性
        alien_image_path = resource_path('images/alien.bmp')
        self.image = pygame.image.load(alien_image_path)
        self.rect = self.image.get_rect()

        # 设置外星人初始位置（屏幕左上角附近）
        self.rect.x = self.rect.width # 左边距 = 外星人宽度
        self.rect.y = self.rect.height # 上边距 = 外星人高度
        
        # 存储外星人的精确位置
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """"检测外星人是否到达屏幕边缘"""
        screen_rect = self.screen.get_rect() # 获取屏幕的rect
        # 检测右边缘和左边缘
        return(self.rect.right >= screen_rect.right or self.rect.left <= 0) # 更加简洁
        # if self.rect.right >= screen_rect.right or self.rect.left <= 0:
        #     return True
        # return False

    def update(self):
        """向左或向右移动外星人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction # 使用速度和方向的乘积计算移动量
        self.rect.x = self.x # 更新外星人rect位置

        
