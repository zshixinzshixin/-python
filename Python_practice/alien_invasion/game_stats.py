# 代码功能：游戏统计类
import json
import os

class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats() # 初始化时调用重置方法，可重复重置

        # 游戏启动时处于非活动状态
        self.game_active = False

        # 最高分不应被重置，在__init__（）中初始化
        # self.high_score = 0
        self.high_score = self._load_high_score()
    

    def reset_stats(self):
            """初始化在游戏运行期间可能变化的统计信息"""
            self.ships_left = self.settings.ship_limit # 飞船数量
            self.score = 0
            self.level = 1

    def _load_high_score(self):
        """从文件加载最高分"""
        try:
            # 尝试打开最高分文件
            with open('high_score.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # 文件不存在时返回0
            return 0
        except json.JSONDecodeError:
            # 文件被损毁返回0
            print("最高分文件已经受损,重置为0")
            return 0
        
    def save_high_score(self):
        """保存最高分到文件"""
        try:
            with open('high_score.json', 'w') as f:
                json.dump(self.high_score, f)
            print(f"最高分已保存")
        except Exception as e:
            print(f"保存失败")