# 代码功能：外星人入侵游戏
import sys # 用于退出游戏
import pygame
from time import sleep
from settings import Settings # 导入Settings类，用于管理游戏设置
from ship import Ship
from bullet import Bullet # 导入Bullet类
from alien import Alien
from game_stats import GameStats # 导入统计类
from button import Button
from scoreboard import Scoreboard
from rule_display import RuleDisplay  # 导入规则显示类

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 游戏初始化
        pygame.init()                     # 初始化pygame库
        self.clock = pygame.time.Clock()  # 创建一个时钟对象，用于控制游戏帧率
        self.settings = Settings()        # 创建一个settings对象，用于存储游戏设置

        # 创建游戏窗口，并设置窗口标题栏
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # 创建游戏统计信息的实例and记分牌实例
        self.stats = GameStats(self)
        # self.stats.game_active = False # 游戏刚启动时处于非活动状态,已经写到self.stats内部
        self.sb = Scoreboard(self)
        self.rule_display = RuleDisplay(self)  # 创建规则显示实例

        # 创建游戏对象/实例
        self.ship = Ship(self)               # 创建一艘飞船，传递当前游戏实例作为参数，并其赋值给self.ship属性
        self.bullets = pygame.sprite.Group() # 创建一个用于存储子弹的编组
        self.aliens = pygame.sprite.Group()  # 创建一个用于存储外星人的编组
        self._create_fleet()                 # 调用创建外星人舰队的方法

        # 创建Play按钮
        self.play_button = Button(self, "Play")

        # 准备规则显示
        self.rule_display.prep_rules()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()         # 检查事件（调用专门的辅助方法）

            # 仅在游戏处于活动状态时更新
            if self.stats.game_active:
                self.ship.update()           # 更新飞船位置
                self._update_bullets()       # 更新子弹位置（包含碰撞检测）
                self._update_aliens()        # 更新外星人位置（包含边缘检测）
            
            self._update_screen()        # 更新屏幕（始终渲染）
            self.clock.tick(60)          # 设置游戏帧率为60帧每秒
    
    # 输入层

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONUP: # 改成释放鼠标
                mouse_pos = pygame.mouse.get_pos()  # 获取鼠标位置
                self._check_play_button(mouse_pos)  # 检测是否点击了play按钮

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # print("Moving right: True") # 测试代码
            self.ship.moving_right = True # 向右移动飞船
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True # 向左移动飞船
        elif event.key == pygame.K_ESCAPE:
            self.stats.save_high_score()
            sys.exit() # 按ESC键退出游戏
        elif event.key == pygame.K_SPACE:
            self._fire_bullet() # 按空格发射子弹
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """处理鼠标点击事件"""
        # 检测鼠标点击位置是否在Play按钮类
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            # 重置游戏统计信息
            self.stats.reset_stats()
            self.sb.prep_score() #重置分数图像（以用于显示，分数已经在上面重置了）

            # 重置游戏速度
            self.settings.initialize_dynamic_settings()

            # 激活游戏
            self.stats.game_active = True # 开始游戏

            # 清空现有的外星人和子弹
            self.aliens.empty() # 清空外星人
            self.bullets.empty() # 清空子弹

            # 创建新的外形舰队，并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 重置得分、等级显示和飞船数量
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 隐藏规则显示
            self.rule_display.hide_rules()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

            # 调试信息
            # print(f"速度重置：飞船 = {self.settings.ship_speed},"
            #       f"子弹 = {self.settings.alien_speed},"
            #       f"外星人 = {self.settings.alien_speed}")


    # 逻辑层

    def _fire_bullet(self):
        """创建新子弹,并将其加入编组"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self) # 创建一个子弹实例
            self.bullets.add(new_bullet) # 将子弹加入编组

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        # 更新子弹位置
        self.bullets.update()

        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))调试的时候加入这个代码，看后台是否起效果，然后删除掉以防减少游戏速度

        # 调用检测子弹和外星人碰撞的方法
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """检查子弹和外星人的碰撞"""
        # 检查子弹和外星人的碰撞
        collisions = pygame.sprite.groupcollide(
            self.bullets,    # 第一个编组：子弹
            self.aliens,     # 第二个编组：外星人
            True,            # 碰撞后删除子弹
            True             # 碰撞后删除外星人
        )

        # 如果发生碰撞，更新得分
        if collisions:
            # 遍历所有被击中的外星人群组
            for aliens in collisions.values():
                # 计算这批碰撞中的外星人数量乘以分数
                self.stats.score += self.settings.alien_points * len(aliens)
            # 更新分数图像
            self.sb.prep_score()
            # 检测是否创造了最高分并显示
            self.sb.check_high_score()
        
        # 检测外星舰队是否被完全消灭
        if not self.aliens:
            # 清空所有剩余子弹并创建新舰队
            self.bullets.empty() # 清空子弹
            self._create_fleet() # 创建新舰队

            # 提高游戏速度
            self.settings.increase_speed()

            # 提高等级并更新显示
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """"创建一个外形舰队"""
        # 创建一个外星人,再不断添加，直到没有空间添加外星人为止
        # 外星人的间距为外星人的宽度和外星人的高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._creat_alien(current_x, current_y)
                current_x += 2 * alien_width
            # 添加一行外星人后，重置x值并递增y值
            current_x = alien_width
            current_y += 2* alien_height 
    
    def _creat_alien(self, x_position, y_position):
        """创建一个外星人并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """更新外形舰队中所有外星人的位置"""
        # 检测外星人是否到达边缘
        self._check_fleet_edges()

        # 自动调用每个外星人的update方法
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship hit!!!") # 调试用，检测碰撞是否起作用
            self._ship_hit()

        # 检测是否有外星人到达屏幕底部
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """检测是否有外星人到达屏幕边缘"""
        # 遍历所有外星人检查边缘
        for alien in self.aliens.sprites():
            if alien.check_edges():
                # 发现边缘接触，改变方向并退出循环
                self._change_fleet_direction()
                break # 只需要一个外星人触发

    def _change_fleet_direction(self):
        """改变舰队水平移动方向，并向下移动一行"""
        # 所有外星人向下移动
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        # 改变水平移动方向
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """检测是否有外星人到达屏幕下边缘"""
        for alien in self.aliens.sprites():
            # 检测是否到达屏幕底部
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break # 立即退出，不再检查其他外星人

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 将ships_left减1
            self.stats.ships_left -= 1
            
            # 更新飞船速度
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一个新的舰队，并将飞船放到屏幕底部中央
            self._create_fleet()     # 创建新舰队
            self.ship.center_ship()  # 调用ship类的center_ship方
            
            # 暂停
            sleep(0.5)  # 暂停0.5秒
        else:
            # 游戏结束
            self.stats.game_active = False

            # 显示规则（游戏结束，重新开始前）
            self.rule_display.show_rules_display()

            # 显示鼠标光标
            pygame.mouse.set_visible(True)


    # 渲染层

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 先填充背景
        self.screen.fill(self.settings.bg_color)

        # 绘制游戏元素
        for bullet in self.bullets.sprites(): # 遍历绘制所有子弹
            bullet.draw_bullet()
        self.ship.blitme()                    # 调用飞船的blitme方法，绘制飞船前景
        self.aliens.draw(self.screen)         # 绘制外星人（使用精灵组）

        # 显示得分
        self.sb.show_score()

        # 显示规则（在非活动状态时）
        self.rule_display.draw_rules()

        # 如果游戏除非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 最后刷新显示
        pygame.display.flip()


# 本段代码确保只有在直接运行alien_invasion.py文件时才会执行游戏
if __name__ == '__main__':
    ai = AlienInvasion() # 创建游戏实例
    ai.run_game() # 运行游戏
