from time import time as timer
from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, p_image, speed, x, y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 640:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 15, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)
score =0
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            

class Bullet(GameSprite):
    def update(self):    
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

      
window = display.set_mode((700,500))
display.set_caption('')
background=transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


clock = time.Clock()
FPS = 60
speed = 10

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)
font3 = font.SysFont('Arial', 36)
win = font1.render('Win!', True, (255,255,0))
lose = font2.render('Lose!', True, (255,0,0))
rel = font3.render('Wait, reload...', True, (255,0,0))


bullets = sprite.Group()
monsters = sprite.Group()
asters = sprite.Group()
player = Player('rocket.png', 8, 350, 400, 80, 100)
for i in range(3):
    ast = Asteroid('asteroid.png', randint(1,2), randint(80, 620), -40, 80, 50) 
    asters.add(ast)
for i in range(5):
    enemy = Enemy('ufo.png',randint(2, 3), randint(80, 620), -40, 80, 50)
    monsters.add(enemy)


rel_time = False
num_fire = 0
finish = False
game = True
while game == True:
    for e in event.get():  
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    player.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if finish == False:
        window.blit(background, (0,0))
        text_lose = font1.render('Пропущенно: ' + str(lost), 1, (255, 255, 255))
        text_score = font1.render('Уничтожено: ' + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        window.blit(text_score, (10, 20))
        monsters.update()
        monsters.draw(window)
        asters.update()
        asters.draw(window)
        bullets.update()
        bullets.draw(window)
        sprite_list = sprite.spritecollide(
            player, monsters, False
        )
        ast_list = sprite.spritecollide(
            player, asters, False
        )
        collides = sprite.groupcollide(
            monsters,bullets, True, True
        )
        for i in collides:
            score += 1
            enemy = Enemy('ufo.png',randint(2, 3), randint(80, 620), -40, 80, 50)
            monsters.add(enemy)
        player.reset()
        player.update()
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                window.blit(rel, (300, 460))
            else:
                num_fire = 0
                rel_time = False
        if score >= 10:
            finish = True
            window.blit(win, (350,250))
        if sprite_list or ast_list or lost >= 3:
            finish = True
            window.blit(lose, (350,250))
    else:
        for i in monsters:
            i.kill()
            del i
        for i in bullets:
            i.kill()
            del i    
    
    display.update()
    clock.tick(FPS)
        













