"""
    内容: 地图类

"""
import pygame
from pygame.sprite import Sprite


class Brick(Sprite):

    def __init__(self, ai_setting, screen, pos):
        super(Brick, self).__init__()
        # 初始化砖块并设置初始大小
        self.screen = screen
        self.ai_setting = ai_setting
        # 加载z砖块图像并获取其外接矩形   \为转移符
        self.image = pygame.image.load("./picture/brick.jpeg")
        # 改变图像大小
        self.image = pygame.transform.scale(self.image, (ai_setting.brick_size_x, ai_setting.brick_size_y))
        # 获得方位
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 砖块位置 方法是centerx代表坦克中心的x坐标，将其调整事先放置好的x坐标
        self.rect.centerx = pos[0]
        self.rect.bottom = pos[1]

    # 在指定位置绘制坦克
    def blitme(self):
        self.screen.blit(self.image, self.rect)


"""
    铁块类

"""


class Iron_brick(Brick):
    def __init__(self, ai_setting, screen, pos):
        super(Iron_brick, self).__init__(ai_setting, screen, pos)
        # 加载砖块图像并获取其外接矩形   \为转移符
        self.image = pygame.image.load("./picture/iron.jpeg")
        self.image = pygame.transform.scale(self.image, (ai_setting.brick_size_x, ai_setting.brick_size_y))


"""坦克加速道具类"""


class Prop_tank_speed(Sprite):
    def __init__(self, ai_setting, screen, pos):
        super(Prop_tank_speed, self).__init__()
        # 初始化道具并设置初始大小
        self.screen = screen
        self.ai_setting = ai_setting
        # 加载道具图像并获取其外接矩形   \为转移符
        self.image = pygame.image.load("./picture/tankspeed.jpeg")
        # 改变图像大小
        self.image = pygame.transform.scale(self.image, (ai_setting.prop_size_x, ai_setting.prop_size_y))
        # 获得方位
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 增益效果数值
        self.add_speed = 0.5
        # 道具位置 方法是centerx代表坦克中心的x坐标，将其调整事先放置好的x坐标
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

    #
    # # 增益效果函数 坦克速度加快
    # def add_effect(self, tank):
    #     tank.speed += self.add_speed

    # 在指定位置绘制道具
    def blitme(self):
        self.screen.blit(self.image, self.rect)


"""
    子弹加速道具
    继承坦克加速道具
"""


class Prop_bullet_speed(Brick):
    def __init__(self, ai_setting, screen, pos):
        super(Prop_bullet_speed, self).__init__(ai_setting, screen, pos)
        # 加载道具图像并获取其外接矩形   \为转移符
        self.image = pygame.image.load("./picture/bulletspeed.jpeg")
        self.image = pygame.transform.scale(self.image, (ai_setting.brick_size_x, ai_setting.brick_size_y))
        # 道具位置 方法是centerx代表坦克中心的x坐标，将其调整事先放置好的x坐标
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        # 增益效果值
        self.add_speed = 0.5


class Scoreboard:
    def __init__(self, ai_setting, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_setting = ai_setting
        # 设置字体颜色
        self.text_color = (30, 30, 30)
        # 字体类型
        self.font = pygame.font.SysFont(None, 48)
        # 初始化装甲值
        self.score_2 = self.score_1 = ai_setting.ori_armor
        # 准备初始得分画面
        self.prep_score()

    def prep_score(self):
        # 将得分转换为一幅渲染图像
        score_str_1 = str(self.score_1)
        score_str_2 = str(self.score_2)
        # 将分数文字渲染为图片
        self.score_image_1 = self.font.render(score_str_1, True, self.text_color, self.ai_setting.bg_color)
        self.score_image_2 = self.font.render(score_str_2, True, self.text_color, self.ai_setting.bg_color)
        self.score_rect_1 = self.score_image_1.get_rect()
        self.score_rect_2 = self.score_image_2.get_rect()
        # 调整计分板方位
        self.score_rect_1.right = self.screen_rect.left + 20
        self.score_rect_1.top = 20
        self.score_rect_2.left = self.screen_rect.right - 20
        self.score_rect_2.top = 20

    # 展示分数
    def show_score(self):
        self.screen.blit(self.score_image_1, self.score_rect_1)
        self.screen.blit(self.score_image_2, self.score_rect_2)


class End_theme:
    def __init__(self, screen, ai_setting):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_setting = ai_setting
        # 设置字体颜色
        self.text_color = (30, 30, 30)
        # 字体类型
        self.font = pygame.font.SysFont('SimHei', 48)

    def write_content(self, flag):
        # 字体内容
        self.content = "player {} win, press 1 restart, press 2 exit".format(flag)
        self.image = self.font.render(self.content, True, self.text_color, self.ai_setting.bg_color)
        # 获得图片方位
        self.image_rect = self.image.get_rect()
        # 把位置放置在中间
        self.image_rect.centerx = self.screen_rect.centerx
        self.image_rect.centery = self.screen_rect.centery

    # 显示画面
    def show(self):
        self.screen.blit(self.image, self.image_rect)
        # 让最近绘制屏幕可见
        pygame.display.flip()
