class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""
    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200 # 屏幕宽度
        self.screen_height = 800 # 屏幕高度
        self.bg_color = (230, 230, 230) # 背景色

        # 飞船设置
        self.ship_limit = 3 # 飞船数量限制


        # 子弹设置
        self.bullet_width = 10
        self.bullet_height = 20
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # 外星舰队设置
        self.fleet_drop_speed = 50 # 到达边缘时，外星人下移的速度


        # 游戏节奏加快就分数提升速度
        self.speedup_scale = 1.1 # 增长比例
        self.score_scale = 1.5

        # 初始化动态设置
        self.initialize_dynamic_settings() # 调用动态设置初始化

    def initialize_dynamic_settings(self):
        """"初始化游戏进行而变化的设置"""
        self.ship_speed = 5 # 飞船移动速度
        self.bullet_speed = 3 # 子弹速度
        self.alien_speed = 1.0 # 外星人水平移动速度

        self.fleet_direction = 1 # 1表示向右移，-1表示向左移
        
        self.alien_points = 50 # 计分设置

    def increase_speed(self):
        """提高速度设置和外星人分数"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

        # 调试信息 显示新的外星人分数
        # print(self.alien_points)