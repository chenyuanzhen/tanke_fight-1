import pygame
from os import path


def main_menu(ai_setting, screen):
    # 加载游戏初始界面背景图片.
    title = pygame.image.load(path.join(path.join(path.dirname(__file__), 'picture'), "main.png"))
    # 加载初始音乐
    begin_music = pygame.mixer.Sound("./music/begin.wav")
    # 加载的音量大小
    begin_music.set_volume(1)
    begin_music.play(1)
    # 改变图像大小
    title = pygame.transform.scale(title, (ai_setting.screen_width, ai_setting.screen_height))
    screen.blit(title, (0, 0))
    pygame.display.update()
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                # 初始音乐停止
                begin_music.stop()
                break
        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            pass
