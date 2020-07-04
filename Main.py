"""
    内容: 游戏主程序

"""
import Strate_screen as sc
import pygame
from pygame.sprite import Group
from Setting import Settings
from Tank import Tank
from Map import Scoreboard, End_theme
import Game_Funciton as gf
from os import path
import Map as map


def run_game():
    # 进行 pygame 设置和屏幕初始化
    pygame.init()
    pygame.mixer.init()
    
    # 键盘检测的重复检测 比如一直按着某个键也会重复读取该键的操作 未开启:一直按着w 只会检测一次 按下w的操作.  而开启后 一直按着w 会检测到 很多次 按下w的操作
    # pygame.key.set_repeat(1, 10)
    ai_setting = Settings()
    # 屏幕初始化
    screen = pygame.display.set_mode(
        (ai_setting.screen_width, ai_setting.screen_height))
    # 标题名字设置
    pygame.display.set_caption("tank_fight")
    # 开始动画
    sc.main_menu(ai_setting, screen)
    # 音乐初始化
    gf.music_player()
    end_theme = End_theme(screen, ai_setting)
    # 创建两个坦克
    tank_1 = Tank(ai_setting, screen, ai_setting.player_1_key, pygame.image.load("./picture/tank.jpeg"),
                  ai_setting.tank_1_pos)
    tank_2 = Tank(ai_setting, screen, ai_setting.player_2_key, pygame.image.load("./picture/tank2.jpeg"),
                  ai_setting.tank_2_pos)
    scoreboard = Scoreboard(ai_setting, screen)
    bricks = Group()
    iron_bricks = Group()
    # 坦克加速道具
    prop_tank = Group()
    prop_bullet = Group()
    gf.gen_brick(bricks, ai_setting, screen)
    gf.gen_Ibrick(iron_bricks, ai_setting, screen)

    # 进入游戏主循环
    while True:
        # 刷新道具
        gf.gen_prop(prop_tank, prop_bullet, ai_setting, screen)
        # 监视键盘和鼠标事件
        gf.check_event(tank_1, tank_2, ai_setting, screen, tank_1.bullet, tank_2.bullet)
        # 更新坦克的位置设置
        gf.update_tanks(tank_1, bricks, tank_2, iron_bricks, prop_tank, prop_bullet, ai_setting, screen, 1)
        gf.update_tanks(tank_2, bricks, tank_1, iron_bricks, prop_tank, prop_bullet, ai_setting, screen, 2)
        # 更新子弹的位置设置
        gf.update_bullets(tank_1.bullet, tank_2.bullet, tank_1, tank_2, bricks, iron_bricks, ai_setting, scoreboard)
        # 负责屏幕显示
        gf.update_screen(ai_setting, screen, tank_1, tank_2, tank_1.bullet, tank_2.bullet, bricks, iron_bricks,
                         prop_tank, prop_bullet, scoreboard)
        if scoreboard.score_1 <= 0:
            gf.show_end_theme(screen, ai_setting, end_theme, 2)
            scoreboard.score_1 = scoreboard.score_2 = 3
            tank_1.reset(ai_setting)
            tank_2.reset(ai_setting)
            gf.gen_brick(bricks, ai_setting, screen)

        elif scoreboard.score_2 <= 0:
            gf.show_end_theme(screen, ai_setting, end_theme, 1)
            scoreboard.score_1 = scoreboard.score_2 = 3
            tank_1.reset(ai_setting)
            tank_2.reset(ai_setting)
            gf.gen_brick(bricks, ai_setting, screen)


run_game()
