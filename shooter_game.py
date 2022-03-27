from pygame import *
from random import randint

font.init()
text = font.Font(None, 60)
win = text.render('Mission completed!', True, (250, 250, 250))
lose = text.render('Zombies ate your BRAINS!', True, (250, 180, 180))

score = 0
goal = 200
wasted = 0
max_wasted = 1

class GamiesSparitiy(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.hp = 300
        self.garg_hp = 600

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Gamer(GamiesSparitiy):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x	-=	self.speed
        if keys[K_RIGHT] and self.rect.x < window_width - 80:
            self.rect.x	+=	self.speed
    
    def shoot(self):
        bullet = Shot('pea.png', self.rect.centerx, self.rect.top, 50, 50, -8)
        shots.add(bullet)

class Enemy(GamiesSparitiy):
    def update(self):
        self.rect.y += self.speed
        global wasted
        if self.rect.y > window_height:
            self.rect.x = randint(100, window_width - 100)
            self.rect.y = 0
            wasted = wasted + 1
    
    
class Shot(GamiesSparitiy):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class EnemyShot(GamiesSparitiy):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > window_height:
            self.rect.x = randint(100, window_width - 60)
            self.rect.y = 0
            enemyshots.add(enemybullet)

window_width = 700
window_height = 1000
display.set_caption('Plants vs Zombies: Call of Duty edition')
window = display.set_mode((window_width, window_height))
back = transform.scale(image.load('back.jpg'), (700, 1000))

hero = Gamer('peashooter.png', 5, 800, 70, 120, 15)

aliens = sprite.Group()
for i in range(5, 7):
    alien = Enemy('zombie.png', randint(100, window_width - 80), -60, 100, 200, randint(2, 4))
    aliens.add(alien)

superaliens = sprite.Group()
for i in range(1, 2):
    superalien = Enemy('footballer.png', randint(100, window_width - 80), -300, 200, 200, randint(3, 5))

gargs = sprite.Group()
for i in range(1, 2):
    garg = Enemy('garg.png', randint(100, window_width - 80), -300, 350, 350, 1)

imps = sprite.Group()
for i in range(1, 2):
    imp = Enemy('imp.png', randint(100, window_width - 80), 50, 80, 100, 2)

bosses = sprite.Group()
for i in range(1, 2):
    boss = Enemy('BOSS.png', 1, -2300, 700, 2400, 0.1)

boss_health = 3500

shots = sprite.Group()

enemyshots = sprite.Group()
for i in range(3, 4):
    enemybullet = EnemyShot('enemypea.png', randint(100, window_width - 65), -60, 400, 400, 5)


mixer.init()
mixer.music.load("supermusic.mp3")
mixer.music.play()
mixer.music.set_volume(0.6)

window.blit(back,(0, 0))
speed = 10
clock = time.Clock()
FPS = 80
game = True
finish = False

while game is True: 
    clock.tick(FPS)
    
    for ev in event.get(): 
        if ev.type == QUIT: 
            game = False 
        elif ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                hero.shoot()
            
    if finish != True:
        window.blit(back,(0, 0)) 

        score_num = text.render('Score:' + str(score), 1, (250, 250, 250))
        window.blit(score_num, (10, 40))

        hero.update()
        aliens.update()
        superaliens.update()
        gargs.update()
        imps.update()
        bosses.update()
        shots.update()
        enemyshots.update()


        hero.reset()
        aliens.draw(window)
        superaliens.draw(window)
        gargs.draw(window)
        imps.draw(window)
        bosses.draw(window)
        shots.draw(window)
        enemyshots.draw(window)

        collides = sprite.groupcollide(aliens, shots, True, True)
        for c in collides:
            score = score + 2
            alien = Enemy('zombie.png', randint(80, window_width - 80), -60, 100, 200, randint(2, 4))
            aliens.add(alien)
        

        superale_ns = superaliens.sprites() 
        allshots = shots.sprites() 
        for sprt in superale_ns: 
            for shot in allshots: 
                if sprite.collide_circle(sprt, shot): 
                    sprt.hp -= 100 
                    shots.remove(shot) 

                    if sprt.hp < 100: 
                        superaliens.remove(sprt)
                        score = score + 4
                        superalien = Enemy('footballer.png', randint(100, window_width - 80), -300, 200, 200, randint(3, 5))
                        superaliens.add(superalien)
        
        garg_s = gargs.sprites() 
        alshots = shots.sprites() 
        for sprt in garg_s: 
            for shot in alshots: 
                if sprite.collide_circle(sprt, shot): 
                    sprt.garg_hp -= 100 
                    shots.remove(shot) 

                    if sprt.garg_hp < 100: 
                        gargs.remove(sprt)
                        score = score + 6
                        garg = Enemy('garg.png', randint(100, window_width - 80), -300, 350, 350, 1)
                        gargs.add(garg)
                        imps.add(imp)
        
        collides = sprite.groupcollide(imps, shots, True, True)
            
        collides = sprite.groupcollide(bosses, shots, False, True)
        for c in collides:
            boss_health = boss_health - 100

        collides = sprite.groupcollide(aliens, bosses, True, False)

        collides = sprite.groupcollide(superaliens, bosses, True, False)

        collides = sprite.groupcollide(imps, bosses, True, False)

        collides = sprite.groupcollide(gargs, bosses, True, False)

        if sprite.spritecollide(hero, aliens, False) or wasted >= max_wasted:
            finish = True
            window.blit(lose, (100, 400))

        if sprite.spritecollide(hero, superaliens, False):
            finish = True
            window.blit(lose, (100, 400))

        if sprite.spritecollide(hero, gargs, False):
            finish = True
            window.blit(lose, (100, 400))

        if sprite.spritecollide(hero, imps, False):
            finish = True
            window.blit(lose, (100, 400))

        if sprite.spritecollide(hero, bosses, False):
            finish = True
            window.blit(lose, (100, 400))

        if sprite.spritecollide(hero, enemyshots, False):
            finish = True
            window.blit(lose, (100, 400))

        if score >= goal:
            bosses.add(boss)
            boss_num = text.render('Boss health:' + str(boss_health), 1, (250, 250, 250))
            window.blit(boss_num, (10, 80))
            enemyshots.add(enemybullet)

        if score == 20:
            superaliens.add(superalien)

        if score >= 100:
            gargs.add(garg)
  
        if boss_health <= 0:
            finish = True
            window.blit(win, (180, 400))


    display.update()
