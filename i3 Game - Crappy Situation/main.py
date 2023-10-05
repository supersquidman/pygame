import pygame
import os
import sys

os.chdir(r'C:\Users\4194915\Documents\Code\Python\i3 Game - Crappy Situation\assets')

pygame.init()
win = pygame.display.set_mode((720,480))
pygame.display.set_caption("Crappy Situation")
pygame.display.set_icon(pygame.image.load('poo.png'))

walkRight = [pygame.image.load('R_1.png'), pygame.image.load('R_2.png'), pygame.image.load('R_0.png')]
walkLeft = [pygame.image.load('L_1.png'), pygame.image.load('L_2.png'), pygame.image.load('L_0.png')]
bg = pygame.image.load('bg.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('shot.wav')
hitSound = pygame.mixer.Sound('slush.wav')
music = pygame.mixer.music.load('synth.mp3')
pygame.mixer.music.play(-1)

score = 0

#PLAYER
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, 30, 28)
        self.health = 10
        
    def draw(self,win):
        if self.walkCount + 1 >= 60:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//20], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//20], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x,self.y))
            else:
                win.blit(walkLeft[0], (self.x,self.y))
        self.hitbox = (self.x + 12, self.y, 12, 44)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 270
        self.walkCount = 0
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    

class projectile(object):
    def __init__(self,x,y,radius,color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8*facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('poo.png'), pygame.image.load('poo1.png'), pygame.image.load('poo2.png'), pygame.image.load('poo3.png')]
    walkLeft = [pygame.image.load('poo.png'), pygame.image.load('poo1.png'), pygame.image.load('poo2.png'), pygame.image.load('poo3.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 1
        self.hitbox = (self.x, self.y, 32, 28)
        self.health = 9
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 60:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 20], (self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 20], (self.x,self.y))
                self.walkCount += 1
            self.hitbox = (self.x+10, self.y+10, 15, 15)
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] -20, 50, 10))
            pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] -20, 50 - (5*(9 - self.health)), 10))
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
    

    def move(self):
        if self.vel > 0:
            if self.x + self.vel< self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        pass
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')
        



#MAIN
def gameEnd():
    win.fill((0,0,0))
    text = font.render('Game Over', 1, (0,0,0))
    win.blit(text, (200,240))
    pygame.display.update()

def redrawGameWindow():
    win.blit(bg,(0,0))
    pygame.draw.rect(win,(0,0,0), (140,250,100,20))
    man.draw(win)
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    text2 = font.render('HP: ' + str(man.health), 1, (0,0,0))
    win.blit(text, (600,10))
    win.blit(text2, (10,10))
    badman.draw(win)
    badman2.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

font = pygame.font.SysFont('comicsans', 30, True)
man = player(50,270,20,20)
badman = enemy(150,230,64,64,200)
badman2 = enemy(100,270,64,64,590)
shootLoop = 0
bullets = []

run = True
while run:
    clock.tick(60)

    if badman.visible == True:
        if man.hitbox[1] < badman.hitbox[1] + badman.hitbox[3] and man.hitbox[1] + man.hitbox[3] > badman.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > badman.hitbox[0] and man.hitbox[0] < badman.hitbox[0] + badman.hitbox[2]:
                man.hit()
                score -= 5
                man.health -= 1

    if badman2.visible == True:
        if man.hitbox[1] < badman2.hitbox[1] + badman2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > badman2.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > badman2.hitbox[0] and man.hitbox[0] < badman2.hitbox[0] + badman2.hitbox[2]:
                man.hit()
                score -= 5
                man.health -= 1

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < badman.hitbox[1] + badman.hitbox[3] and bullet.y + bullet.radius > badman.hitbox[1]:
            if bullet.x + bullet.radius > badman.hitbox[0] and bullet.x - bullet.radius < badman.hitbox[0] + badman.hitbox[2] and badman.visible == True:
                hitSound.play()
                badman.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.y - bullet.radius < badman2.hitbox[1] + badman2.hitbox[3] and bullet.y + bullet.radius > badman2.hitbox[1]:
            if bullet.x + bullet.radius > badman2.hitbox[0] and bullet.x - bullet.radius < badman2.hitbox[0] + badman2.hitbox[2] and badman2.visible == True:
                hitSound.play()
                badman2.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
        
        if bullet.x < 720 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets)<5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (102,204,204), facing))
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.vel
        man.left=True
        man.right=False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 720-man.width:
        man.x += man.vel
        man.right=True
        man.left=False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.3 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    if man.health <= 1:
        gameEnd()
    else:
        redrawGameWindow()



pygame.quit()
sys.exit()
