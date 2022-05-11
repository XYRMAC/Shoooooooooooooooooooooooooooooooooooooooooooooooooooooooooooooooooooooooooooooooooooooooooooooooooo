#Создай собственный Шутер!
from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, -15, 20, 15)
        bullets.add(bullet)

score = 0
lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0 
            lost = lost + 1

win_height = 500
win_width = 700

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

font.init()
font2 = font.SysFont("Arial", 36)

font3 = font.SysFont("Arial", 36)
ship = Player("rocket.png", 5, 400, 5, 50, 50)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), 0, randint(1, 5), 80, 50)
    monsters.add(monster)
bullets = sprite.Group()

sprite_list = sprite.groupcollide(monsters, bullets, True, True)

gun = mixer.Sound("fire.ogg")

run = True
clock = time.Clock()
FPS = 60
finish = False
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                gun.play()
                ship.fire()
            
    if not finish:
        window.blit(background,(0,0))

        ship.update()

        monsters.update()

        bullets.update()
        
        ship.reset()

        monsters.draw(window)

        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, randint(1, 5), 80, 50)
            monsters.add(monster)

        if lost >= 3:
            finish = True
            lose = font2.render("Вы проиграли. Не грустите", 1, (225, 15, 25))
            window.blit(lose, (200, 200))


        if score >= 10:
            finish = True
            win = font2.render("Вы выйграли! Вы молодцы", 1, (255, 156, 25))
            window.blit(win, (200, 200))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_lose = font3.render("Убито: " + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (10, 80))


    display.update()
    clock.tick(FPS)

