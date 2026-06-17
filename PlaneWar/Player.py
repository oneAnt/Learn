import pygame
from Bullet import Bullet

class Player(object):
    """
    玩家类
    属性：显示窗口、位置、图片、子弹列表
    方法：显示、移动、发射子弹
    """
    def __init__(self, screen):
        self.screen = screen
        self.x = 100
        self.y = 450
        self.bullet_img = "./img/bullet.png"
        self.player_img = pygame.image.load("./img/hero.gif")
        self.player_rct = self.player_img.get_rect()
        self.bullets = []
        self.speed = 10

    def display(self):
        self.screen.blit(self.player_img, (self.x, self.y))
        # 更新碰撞矩形位置
        self.player_rct.topleft = (self.x, self.y)
        for bullet in self.bullets:
            bullet.display()
            bullet.move()
            if bullet.y <= 0:
                self.bullets.remove(bullet)

    def move(self, direction):
        if self.x >= 200 and direction == "right":
            self.x = 200
            print("玩家向右移动到最右侧")
        elif self.x <= 0 and direction == "left":
            self.x = 0
            print("玩家向左移动到最左侧")
        elif direction == "left":
            self.x -= self.speed
            print("玩家向左移动")
        elif direction == "right":
            self.x += self.speed
            print("玩家向右移动")

    def fire(self):
        bullet = Bullet(self.screen, self.x, self.y,"player")
        self.bullets.append(bullet)
        print("玩家发射子弹")

    def check(self, enemy_rct):
        # 检查子弹是否击中敌人
        for bullet in self.bullets:
            if bullet.check(enemy_rct):
                print("子弹击中敌人")
                return True
        return False
