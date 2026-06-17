import pygame
import random
import time
from Player import Player
from EmenyPlane import EmenyPlane


if __name__ == "__main__":
    # 创建屏幕
    screen = pygame.display.set_mode((300, 600))
    background = pygame.image.load("./img/background.png")
    # 设置窗口标题
    pygame.display.set_caption("飞机大战")
    # 创建玩家
    player = Player(screen)
    enemy = EmenyPlane(screen)
    while True:
        # 绘制背景
        screen.blit(background, (0, 0))
        # 绘制玩家
        player.display()
        # 绘制敌人
        enemy.display()
        enemy.move()
        # 敌人开火
        if random.randint(0, 20) == 1:
            enemy.fire()
        if enemy.check(player.player_rct):
            print("敌人子弹击中玩家，游戏结束")
            break
        if player.check(enemy.enemy_rct):
            print("玩家子弹击中敌人，游戏结束")
            break
        # 更新显示
        pygame.display.update()
        time.sleep(0.1)
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move("left")
                elif event.key == pygame.K_RIGHT:
                    player.move("right")
                elif event.key == pygame.K_SPACE:
                    player.fire()
