# 代码功能：规则显示类
import pygame.font

class RuleDisplay:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # 🆕 英文版规则内容
        self.rules = [
            "Alien Invasion - Quick Guide",
            "=" * 25,
            "CONTROLS:",
            "  left right / A D - Move",
            "  SPACE - Shoot",
            "  ESC - Quit",
            "",
            "KEY RULES:",
            "  • Destroy aliens to score",
            "  • Avoid alien collisions",
            "  • 3 lives total"
        ]
            
        # 🆕 更专业的视觉设计
        self.title_color = (255, 215, 0)  # 金色标题
        self.text_color = (255, 100, 100)  # 浅红色正文
        self.bg_color = (20, 20, 40, 200)  # 半透明深蓝背景
        self.border_color = (255, 0, 0)    # 红色边框
        self.accent_color = (0, 255, 255)  # 青色强调色
        
        self.title_font = pygame.font.SysFont(None, 28, bold=True)
        self.text_font = pygame.font.SysFont(None, 22)
        
        # 🆕 动态计算规则框大小
        self.rule_rect = pygame.Rect(0, 0, 350, 280)
        self.rule_rect.right = self.screen_rect.right - 20
        self.rule_rect.bottom = self.screen_rect.bottom - 20
        
        self.show_rules = True
        self.prep_rules()
    
    def prep_rules(self):
        """准备规则文本图像"""
        self.rule_images = []
        line_height = 22
        current_y = self.rule_rect.top + 15
        
        for i, rule_text in enumerate(self.rules):
            if rule_text.startswith("🚀") or "===" in rule_text:
                # 标题行
                font = self.title_font
                color = self.title_color
            elif rule_text.startswith("•"):
                # 强调行
                font = self.text_font
                color = self.accent_color
            elif rule_text and not rule_text.startswith(" ") and ":" in rule_text:
                # 小标题
                font = self.text_font
                color = self.title_color
            else:
                # 普通文本
                font = self.text_font
                color = self.text_color
            
            rule_image = font.render(rule_text, True, color)
            rule_image_rect = rule_image.get_rect()
            rule_image_rect.left = self.rule_rect.left + 15
            rule_image_rect.top = current_y
            
            self.rule_images.append((rule_image, rule_image_rect))
            current_y += line_height
    
    def draw_rules(self):
        """绘制带特效的规则框"""
        if not self.show_rules:
            return
            
        # 🆕 创建半透明表面
        rule_surface = pygame.Surface((self.rule_rect.width, self.rule_rect.height), pygame.SRCALPHA)
        
        # 🆕 绘制半透明背景
        pygame.draw.rect(rule_surface, self.bg_color, (0, 0, self.rule_rect.width, self.rule_rect.height))
        
        # 🆕 绘制边框
        pygame.draw.rect(rule_surface, self.border_color, (0, 0, self.rule_rect.width, self.rule_rect.height), 3)
        
        # 🆕 绘制内部装饰线
        pygame.draw.line(rule_surface, self.accent_color, (10, 40), (self.rule_rect.width - 10, 40), 2)
        
        # 🆕 将规则表面绘制到屏幕上
        self.screen.blit(rule_surface, self.rule_rect)
        
        # 🆕 绘制规则文本
        for rule_image, rule_rect in self.rule_images:
            self.screen.blit(rule_image, rule_rect)
    
    def hide_rules(self):
        """隐藏规则显示"""
        self.show_rules = False
        # print("📋 规则显示已隐藏") # 测试代码
    
    def show_rules_display(self):
        """显示规则"""
        self.show_rules = True
        self.prep_rules()
        # print("📋 规则显示已开启") # 测试代码
