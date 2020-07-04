"""
    内容:坦克类
"""
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
"""
    @:param ai_setting  设置类
    @:param screen      屏幕类
    @:param key_pos     键位数组 wsad 对应 上下左右
    @:param pos         初始位置列表 [0] 为 x, [1] 为 y
"""


class Tank:

    def __init__(self, ai_setting, screen, key_pos, image, pos):
        # 初始化坦克并设置初始位置
        self.screen = screen
        self.ai_setting = ai_setting
        # 加载坦克图像并获取其外接矩形   \为转移符    pygame.image.load("./picture/tank.jpeg")
        self.image = image
        # 改变图像大小
        self.image = pygame.transform.scale(self.image, (ai_setting.tank_size_width, ai_setting.tank_size_height))
        # 存储坦克上下左右的图片
        self.image_right = pygame.transform.rotate(self.image, -90)
        self.image_down = pygame.transform.rotate(self.image_right, -90)
        self.image_left = pygame.transform.rotate(self.image_down, -90)
        self.image_up = pygame.transform.rotate(self.image_left, -90)
        # 获得方位
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 保存初始的位置
        self.save_ori_pos = pos
        # 将每艘新坦克放在屏幕底部中央 方法是centerx代表坦克中心的x坐标，将其调整事先放置好的x坐标
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        # 坦克移速传值
        self.speed = ai_setting.tank_speed_factor
        # 将坦克属性center中存储为小数值
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)
        # 坦克子弹的发射位置和方向 0 为上, 1 为 右, 2 为 下, 3 为 左
        self.rect_fight = self.rect.top
        self.rect_fight_dir = 0
        # 声明移动标志 False为停止，True为移动
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        # 定义坦克键位 键位存储在设置中 上下左右 0,1,2,3,4
        self.key_up = key_pos[0]
        self.key_down = key_pos[1]
        self.key_right = key_pos[2]
        self.key_left = key_pos[3]
        self.key_fight = key_pos[4]
        self.bullet = Group()

    # 坦克重置函数
    def reset(self, ai_setting):
        # 将每艘新坦克放在屏幕底部中央 方法是centerx代表坦克中心的x坐标，将其调整事先放置好的x坐标
        self.rect.centerx = self.save_ori_pos[0]
        self.rect.centery = self.save_ori_pos[1]
        # 将坦克属性center中存储为小数值
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)
        # 坦克移速传值
        self.speed = ai_setting.tank_speed_factor

    # 负责更新坦克位置并防止坦克飞出界面
    def update_position(self, bricks, tank, iron_bricks):
        save_last_x = self.center_x
        save_last_y = self.center_y
        if self.moving_left and self.rect.left > 0:
            self.image = self.image_left
            self.rect_fight_dir = 3
            self.center_x -= self.speed
            self.rect_fight = self.rect.left

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.speed
            self.rect_fight = self.rect.right
            self.image = self.image_right
            self.rect_fight_dir = 1

        if self.moving_up and self.rect.top > 0:
            self.center_y -= self.speed
            self.rect_fight = self.rect.top
            self.image = self.image_up
            self.rect_fight_dir = 0

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center_y += self.speed
            self.rect_fight = self.rect.bottom
            self.image = self.image_down
            self.rect_fight_dir = 2

        # 根据self.center更新rect对象
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

        if pygame.sprite.spritecollide(self, bricks, False) or pygame.sprite.collide_rect(self, tank) or \
                pygame.sprite.spritecollide(self, iron_bricks, False):
            # print("centerx:{}, centery{}".format(save_last_x, save_last_y))
            self.rect.centerx = save_last_x
            self.rect.centery = save_last_y
            self.center_x = save_last_x
            self.center_y = save_last_y

    # 在指定位置绘制坦克
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    # 重置坦克位置
    def center_tank(self):
        # 将每艘新坦克放在屏幕底部中央 方法是centerx代表飞船中心的x坐标，将其调整事先放置好的x坐标
        self.center_x = self.screen_rect.centerx
        self.center_y = self.screen_rect.bottom


"""
    子弹类
    @:param ai_setting    设置
    @:param screen        屏幕
    @:param tank          由哪一辆坦克发出

"""


# 子弹类
class Bullet(Sprite):
    def __init__(self, ai_setting, screen, tank, speed):
        super(Bullet, self).__init__()

        self.screen = screen
        # 在（0，0）处创建一个表示子弹的矩形，再设置正确位置
        self.rect = pygame.Rect(0, 0, ai_setting.bullet_width,
                                ai_setting.bullet_height)
        self.rect.centerx = tank.rect.centerx
        self.rect.centery = tank.rect.centery
        # 射击的方向
        self.rect_fight_dir = tank.rect_fight_dir
        # 用小数表示子弹位置
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.color = ai_setting.bullet_color
        self.speed_factor = speed

    # 向上移动子弹
    def update(self):
        # 0 为上, 1 为 右, 2 为 下, 3 为 左
        if self.rect_fight_dir == 0:
            self.y -= self.speed_factor
            self.rect.y = self.y
        elif self.rect_fight_dir == 1:
            self.x += self.speed_factor
            self.rect.x = self.x
        elif self.rect_fight_dir == 2:
            self.y += self.speed_factor
            self.rect.y = self.y
        elif self.rect_fight_dir == 3:
            self.x -= self.speed_factor
            self.rect.x = self.x

    # 绘制子弹函数
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
