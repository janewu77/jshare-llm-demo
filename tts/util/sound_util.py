import pygame


def play_sound(file_path):
    # 初始化pygame
    pygame.init()

    # 加载MP3文件
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)

    # 播放音乐
    pygame.mixer.music.play()

    # 保持播放状态，直到音乐播放完毕
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
