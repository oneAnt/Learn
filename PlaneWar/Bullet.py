import pygame


class Bullet(object):
    """
    子弹类
    属性：显示窗口、位置、图片
    方法：显示、移动
    """
    def __init__(self, screen, x, y, identity):
        self.screen = screen
        self.x = x
        self.y = y
        self.identity = identity
        self.speed = 5
        self.bullet_img = None
        self.bullet_rct = None
        self.judge()

    def judge(self):
        if self.identity == "player":
            self.speed = 5
            self.bullet_img = pygame.image.load("./img/bullet.png")
            self.x += 39
            self.y -= 15
        elif self.identity == "enemy":
            self.speed = 10
            self.bullet_img = pygame.image.load("./img/bullet1.png")
            self.x += 21
            self.y += 35
        self.bullet_rct = self.bullet_img.get_rect(center=(self.x, self.y))

    def display(self):
        self.screen.blit(self.bullet_img, (self.x, self.y))
        self.bullet_rct.topleft = (self.x, self.y)
    
    def move(self):
        if self.identity == "player":
            self.y -= self.speed
        elif self.identity == "enemy":
            self.y += self.speed
    
    def check(self, rct):
        # 检查子弹是否击中敌人或玩家
        if self.bullet_rct.colliderect(rct):
            return True
        return False
