"""
    内容: 这是关于游戏中所有数据初始化
         包括玩家双方坦克 初始的速度 子弹速度 屏幕的高宽

"""
import pygame


class Settings:
    # 初始化游戏设置
    def __init__(self):
        self.screen_width = 1020
        self.screen_height = 780
        # 背景RGB配色
        self.bg_color = (54, 54, 54)
        # 坦克大小
        self.tank_size_width = 50
        self.tank_size_height = 50
        # window版本坦克速度
        self.windows_tank_speed = 0.7
        self.windows_bullet_speed = 2.5

        self.windows_tank_speed_limit = 2.0

        # 坦克初始速度 window调整 < 1 ,  window执行一个周期时间太短
        self.tank_speed_factor = self.windows_tank_speed

        # 定义坦克玩家1的键位
        self.player_1_key = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SPACE]
        self.player_2_key = [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_j]
        # 存储坦克1初始位置 记得要算上坦克的长宽 第一位是坦克的x坐标 第二位是坦克的y坐标
        self.tank_1_pos = [40 + self.tank_size_width, self.screen_height / 2 + self.tank_size_height - 60]
        self.tank_2_pos = [self.screen_width - self.tank_size_width - 40,
                           self.screen_height / 2 + self.tank_size_height - 60]

        # 子弹数据初始设置
        self.bullet_speed_factor = self.windows_bullet_speed
        # 记录双方子弹增益效果
        self.bullet1_effect = 0
        self.bullet2_effect = 0
        # 道具坦克速度的增益效果
        self.tank_speed_effect = 0.1
        # 道具子弹速度的增益效果
        self.bullet_speed_effect = 0.15

        # 子弹的长宽
        self.bullet_width = 7
        self.bullet_height = 7
        # 子弹颜色
        self.bullet_color = (255, 0,  0)
        # 子弹射击速度限制
        self.bullet_allow = 3
        # 初始声明值
        self.ori_armor = 3

        # 砖块大小
        self.brick_size_x = self.tank_size_width
        self.brick_size_y = self.tank_size_height
        # 道具大小
        self.prop_size_x = self.tank_size_width
        self.prop_size_y = self.tank_size_height
        # 铁块数目
        self.iron_brick_num = 101
        # 砖块数目
        self.brick_num = 46
        # 道具数量
        self.prop_num = 1
        # 道具位置 以下坐标是可能刷新位置
        self.prop_pos = [[380, 330], [460, 330], [560, 330], [640, 330],
                         [380, 390], [460, 390], [560, 390], [640, 390],
                         [380, 460], [460, 460], [560, 460], [640, 460]]

        # # 动态化初始
        # self.initizlize_dynamic_settings()

    # 初始化随着游戏进行变化的值
    def initizlize_dynamic_settings(self):
        # 子弹数据重新设置
        self.bullet_speed_factor = self.windows_bullet_speed

        # 刷新双方子弹增益效果
        self.bullet1_effect = 0
        self.bullet2_effect = 0

        # 坦克重新初始化速度     window调整 < 1 ,  window执行一个周期时间太短
        self.tank_speed_factor = self.windows_tank_speed
        # 子弹速度设置
        self.bullet_speed_factor = self.windows_bullet_speed

