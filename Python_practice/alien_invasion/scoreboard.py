import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """"展示得分信息的类"""

    def __init__(self, ai_game):
        # 获取游戏屏幕、设置和统计信息
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.ai_game = ai_game

        # 显示得分使用的字体设置
        self.text_color = (30, 30, 30) # 深灰色
        self.font = pygame.font.SysFont(None, 48) # 默认字体，49号

        # 准备初始得分图像
        self.prep_score()
        # 准备最高分图像
        self.prep_high_score()
        # 准备等级图像
        self.prep_level()
        # 准备飞船图像
        self.prep_ships()
        
    def prep_score(self):
        """"将得分转换为图像"""
        # 将得分摄入到最近的10的整数倍
        round_score = round(self.stats.score, -1) # 第二个参数为-1表示舍入到10位

        # 将数值转换为字符串
        score_str = "{:,}".format(round_score) # 格式化为1,000,000的形式

        # 创建得分图像
        self.score_image = self.font.render(score_str,
                                            True,
                                            self.text_color,
                                            self.settings.bg_color)
        
        # 在屏幕右上角显示得分,距离右边缘20像素，上边缘20像素
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right =self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """"将最高分转换为图像"""
        # 将最高分摄入到最近的10的整数倍
        round_high_score = round(self.stats.high_score, -1) # 第二个参数为-1表示舍入到10位

        # 将数值转换为字符串
        high_score_str = "{:,}".format(round_high_score) # 格式化为1,000,000的形式

        # 创建最高分图像
        self.high_score_image = self.font.render(high_score_str,
                                            True,
                                            self.text_color,
                                            self.settings.bg_color)
        
        # 在屏幕上方正中间显示
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right =self.screen_rect.centerx # 水平居中
        self.high_score_rect.top = self.score_rect.top # 与得分高度保持一致

    def prep_level(self):
        """将等级转换为图像"""
        level_pre_str = str(self.stats.level)
        level_str = f"L {level_pre_str}"
        
        self.level_image = self.font.render(level_str,True,self.text_color,self.settings.bg_color)
        
        # 在得分下方显示
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还余下多少艘飞船"""
        # 创建一个空编组来存储飞船实例c:\Users\Administrator\Downloads\r2d2_87090.ico
        self.ships = Group()

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)

            ship.rect.x = 10 + ship_number * ship.rect.width

            ship.rect.y = 10

            self.ships.add(ship)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
        
    def show_score(self):
        """"在屏幕上显示得分、最高分、等级和剩余飞船"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

