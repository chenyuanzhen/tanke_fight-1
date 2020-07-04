"""
    内容: 这是关于游戏内部玩法代码设置
"""

import pygame
import sys
import random
from Tank import Bullet
from Map import Brick, Iron_brick, Prop_tank_speed, Prop_bullet_speed, End_theme

# 道具刷新时间计数器
count = 2000
refresh_time = 2000


# 初始化音乐文件
def music_player():

    # 加载音频文件
    my_music = pygame.mixer.Sound("./music/start.wav")
    # 加载的音量大小
    my_music.set_volume(1)
    my_music.play(1)
    # 加载音频文件
    pygame.mixer.music.load("./music/back.wav")
    # 加载时声音大小
    pygame.mixer.music.set_volume(0.3)
    # 常规播放
    pygame.mixer.music.play(-1)


"""
    检查坦克键位按下函数
    如果上一个键位
    参数 event, tank, ai_settings, screen, bullets
"""


def tank_check_keydown(event, tank, ai_settings, screen, bullets, flag):
    if event.key == tank.key_right:
        tank.moving_right = True
    elif event.key == tank.key_left:
        tank.moving_left = True
    elif event.key == tank.key_up:
        tank.moving_up = True
    elif event.key == tank.key_down:
        tank.moving_down = True
    elif event.key == tank.key_fight:
        fire_bullet(tank, ai_settings, screen, bullets, flag)


# 响应键盘按下
def check_keydown_events(event, tank_1, tank_2, ai_settings, screen, bullets_1, bullets_2):
    # 当为q 则结束程序
    if event.key == pygame.K_q:
        sys.exit()
    # 若事件为玩家1的键位
    if event.key in ai_settings.player_1_key:
        tank_check_keydown(event, tank_1, ai_settings, screen, bullets_1, 1)
    # 若事件为玩家2的键位
    elif event.key in ai_settings.player_2_key:
        tank_check_keydown(event, tank_2, ai_settings, screen, bullets_2, 2)


# 响应键盘松开
def check_keyup_events(event, tank_1, tank_2):
    if event.key == tank_1.key_right:
        tank_1.moving_right = False
    elif event.key == tank_1.key_left:
        tank_1.moving_left = False
    elif event.key == tank_1.key_up:
        tank_1.moving_up = False
    elif event.key == tank_1.key_down:
        tank_1.moving_down = False

    elif event.key == tank_2.key_down:
        tank_2.moving_down = False
    elif event.key == tank_2.key_left:
        tank_2.moving_left = False
    elif event.key == tank_2.key_up:
        tank_2.moving_up = False
    elif event.key == tank_2.key_right:
        tank_2.moving_right = False


"""
    函数名:        check_event
    函数功能:      检查键盘和鼠标的操作
    传入参数:
        @:param  tank_1, tank_2, ai_settings, screen, bullets_1, bullets_2 (这里传入参数不关键)
"""


def check_event(tank_1, tank_2, ai_settings, screen, bullets_1, bullets_2):
    for event in pygame.event.get():
        # 当为上下左右按键按下时，命令坦克上下左右走
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, tank_1, tank_2, ai_settings, screen, bullets_1, bullets_2)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, tank_1, tank_2)
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     mouse_x, mouse_y = pygame.mouse.get_pos()


# 更新画面
def update_screen(ai_setting, screen, tank_1, tank_2, bullets_1, bullets_2, bricks, iron_bricks, prop_0, prop_1,
                  scoreboard):
    scoreboard.prep_score()
    # 每次循环都要重绘制屏幕
    screen.fill(ai_setting.bg_color)
    # 绘制精灵
    for bullet in bullets_1.sprites():
        bullet.draw_bullet()
    for bullet in bullets_2.sprites():
        bullet.draw_bullet()
    for brick in bricks.sprites():
        brick.blitme()
    for i_brick in iron_bricks.sprites():
        i_brick.blitme()
    for prop_0 in prop_0.sprites():
        prop_0.blitme()
    for prop_1 in prop_1.sprites():
        prop_1.blitme()
    # 绘制坦克
    tank_1.blitme()
    tank_2.blitme()
    # 显示分数
    scoreboard.show_score()
    # 让最近绘制屏幕可见
    pygame.display.flip()


# 检查子弹是否符合条件  flag是表明玩家1 1 or 玩家2 2
def fire_bullet(tank, ai_settings, screen, bullets, flag):
    # 创建一颗子弹，并将其加入到编组bullets中 而且当前子弹数目要小于允许存在的
    if len(bullets) < ai_settings.bullet_allow:
        if flag == 1:
            new_bullet = Bullet(ai_settings, screen, tank, ai_settings.bullet_speed_factor + ai_settings.bullet1_effect)
        elif flag == 2:
            new_bullet = Bullet(ai_settings, screen, tank, ai_settings.bullet_speed_factor + ai_settings.bullet2_effect)
        else:
            new_bullet = Bullet(ai_settings, screen, tank, ai_settings.bullet_speed_factor)
        bullets.add(new_bullet)


# 播放子弹击中声音 默认是坦克击中声音
def play_hit_sound(path="./music/tankhit.wav"):
    tank_hit_sound = pygame.mixer.Sound(path)  # 加载声音
    tank_hit_sound.play()  # 调用play()函数播放


# 负责更新 子弹显示
def update_bullets(bullets_1, bullets_2, tank_1, tank_2, bricks, iron_bricks, ai_setting, scoreboard):
    # 绘制子弹函数
    bullets_1.update()
    bullets_2.update()
    # 检测子弹碰撞是否发生碰撞 子弹若击中会消失 自己的子弹不会被自己击中, 子弹击中砖块也会消失
    if pygame.sprite.spritecollide(tank_1, bullets_2, True):
        bullet_hit(tank_1, ai_setting, scoreboard, 1)
    if pygame.sprite.spritecollide(tank_2, bullets_1, True):
        bullet_hit(tank_2, ai_setting, scoreboard, 2)
    elif pygame.sprite.groupcollide(bullets_1, bricks, True, True):
        play_hit_sound("./music/brick.wav")
    elif pygame.sprite.groupcollide(bullets_2, bricks, True, True):
        play_hit_sound("./music/brick.wav")
    elif pygame.sprite.groupcollide(bullets_1, iron_bricks, True, False):
        play_hit_sound("./music/iron.wav")
    elif pygame.sprite.groupcollide(bullets_2, iron_bricks, True, False):
        play_hit_sound("./music/iron.wav")
    else:
        # 检测子弹是否到达边界, 删除已经消失的子弹
        for bullet in bullets_1.copy():
            if bullet.rect.x < 0 or bullet.rect.x > ai_setting.screen_width or bullet.rect.y < 0 or bullet.rect.y > \
                    ai_setting.screen_height:
                bullets_1.remove(bullet)
        for bullet in bullets_2.copy():
            if bullet.rect.x < 0 or bullet.rect.x > ai_setting.screen_width or bullet.rect.y < 0 or bullet.rect.y > \
                    ai_setting.screen_height:
                bullets_2.remove(bullet)


# 更新坦克位置
def update_tanks(tank, bricks, other_tank, iron_bricks, prop_0, prop_1, ai_setting, screen, flag):
    if pygame.sprite.spritecollide(tank, bricks, False):
        pass
    # 当坦克触碰到坦克加速道具时
    elif pygame.sprite.spritecollide(tank, prop_0, True):
        # 播放道具声音
        play_hit_sound("./music/tankspeed.wav")
        # 实现增益效果
        if tank.speed <= ai_setting.windows_tank_speed_limit:
            tank.speed += ai_setting.tank_speed_effect
    # 当坦克触碰到子弹加速道具时
    elif pygame.sprite.spritecollide(tank, prop_1, True):
        # 播放道具声音
        play_hit_sound("./music/tankspeed.wav")
        # 实现增益效果
        if flag == 1:
            ai_setting.bullet1_effect += ai_setting.bullet_speed_effect
        elif flag == 2:
            ai_setting.bullet2_effect += ai_setting.bullet_speed_effect
    else:
        tank.update_position(bricks, other_tank, iron_bricks)


# 检测当子弹击中坦克时
def bullet_hit(tank, ai_setting, scoreboard, flag):
    play_hit_sound()
    # 被击中减分
    if flag == 1:
        scoreboard.score_1 -= 1
    elif flag == 2:
        scoreboard.score_2 -= 1

    tank.reset(ai_setting)


# 生成砖块
def gen_brick(bricks, ai_settings, screen):
    list_x = (150, 150, 150, 150,
              210, 210, 210, 210, 210,
              270, 270,
              330, 330, 330, 330, 330,
              450, 450, 450, 450, 450, 450,
              510, 510,
              570, 570, 570, 570, 570, 570,
              690, 690, 690, 690, 690,
              750, 750,
              810, 810, 810, 810, 810,
              870, 870, 870, 870,
              )  # 1~4最外一圈 ,5~8倒数第二圈， 9~13倒数第一圈
    list_y = (240, 360, 480, 600,
              120, 180, 420, 660, 720,
              300, 540,
              120, 180, 240, 420, 600,
              120, 180, 300, 540, 660, 720,
              360, 480,
              120, 180, 300, 540, 660, 720,
              240, 420, 600, 660, 720,
              300, 540,
              120, 180, 420, 660, 720,
              240, 360, 480, 600,
              )
    for counter in range(0, ai_settings.brick_num):
        new_brick = Brick(ai_settings, screen, [list_x[counter], list_y[counter]])
        bricks.add(new_brick)


# 生成铁块
def gen_Ibrick(iron_bricks, ai_settings, screen):
    list_x = (30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
              990, 990, 990, 990, 990, 990, 990, 990, 990, 990, 990, 990, 990,
              30, 90, 150, 210, 270, 330, 390, 450, 510, 570, 630, 690, 750, 810, 870, 930, 990,
              30, 90, 150, 210, 270, 330, 390, 450, 510, 570, 630, 690, 750, 810, 870, 930, 990,

              150, 150, 150, 150, 150,
              870, 870, 870, 870, 870,
              150, 270, 390, 510, 630, 750, 870,
              150, 270, 390, 510, 630, 750, 870,

              330, 330, 330, 330, 330,
              390, 390,
              510, 510,
              630, 630,
              690, 690, 690, 690, 690,

              510,
              )  # 1~4最外一圈 ,5~8倒数第二圈， 9~13倒数第一圈  14最中间
    list_y = (60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780,
              60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780,
              60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60,
              780, 780, 780, 780, 780, 780, 780, 780, 780, 780, 780, 780, 780, 780, 780, 780, 780,

              180, 300, 420, 540, 660,
              180, 300, 420, 540, 660,
              180, 180, 180, 180, 180, 180, 180,
              660, 660, 660, 660, 660, 660, 660,

              300, 360, 480, 540, 660,
              300, 540,
              300, 540,
              300, 540,
              180, 300, 360, 480, 540,

              420,
              )
    for counter in range(0, ai_settings.iron_brick_num):
        new_brick = Iron_brick(ai_settings, screen, [list_x[counter], list_y[counter]])
        iron_bricks.add(new_brick)


# 随机生成道具
def gen_prop(prop_0, prop_1, ai_setting, screen):
    global count
    count += 1
    pos = ai_setting.prop_pos
    random.shuffle(pos)
    if len(prop_1) < ai_setting.prop_num and count > refresh_time:
        new_prop1 = Prop_bullet_speed(ai_setting, screen, pos[0])
        prop_1.add(new_prop1)

    # 判断生成道具是否符合条件
    if len(prop_0) < ai_setting.prop_num and count > refresh_time:
        new_prop0 = Prop_tank_speed(ai_setting, screen, pos[5])
        prop_0.add(new_prop0)

    if len(prop_0) != 0 or len(prop_1) != 0:
        count = 0


def show_end_theme(screen, ai_setting, end_theme, flag):
    # 绘制屏幕
    screen.fill(ai_setting.bg_color)
    # 写入内容
    end_theme.write_content(flag)
    # 显示结束画面
    end_theme.show()
    record = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    ai_setting.initizlize_dynamic_settings()
                    record = 1
                    break
                elif event.key == pygame.K_2:
                    sys.exit()

        if record == 1:
            break
