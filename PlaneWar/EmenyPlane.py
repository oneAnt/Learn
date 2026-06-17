import pygame
from Bullet import Bullet


class EmenyPlane(object):
    """
    敌人飞机类
    属性：显示窗口、位置、图片
    方法：显示、移动
    """
    def __init__(self, screen):
        self.screen = screen
        self.x = 0
        self.y = 10
        self.speed = 5
        self.bullets = []
        self.enemy_img = pygame.image.load("./img/enemy-1.gif")
        self.enemy_rct = self.enemy_img.get_rect()

    def display(self):
        self.screen.blit(self.enemy_img, (self.x, self.y))
        # 更新碰撞矩形位置
        self.enemy_rct.topleft = (self.x, self.y)
        for bullet in self.bullets:
            bullet.display()
            bullet.move()
            if bullet.y >= 600:
                self.bullets.remove(bullet)

    def move(self):
        self.x += self.speed
        if self.x >= 245:
            self.speed = -self.speed
        elif self.x <= 0:
            self.speed = -self.speed

    def fire(self):
        bullet = Bullet(self.screen, self.x, self.y, "enemy")
        self.bullets.append(bullet)
        print("敌人发射子弹")

    def check(self, player_rct):
        # 检查子弹是否击中玩家
        for bullet in self.bullets:
            if bullet.check(player_rct):
                print("子弹击中玩家")
                return True
        return False
