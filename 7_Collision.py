import pygame 

#always need to do 
pygame.init()


screenWidth = 500 
screenLength = 480
win = pygame.display.set_mode((screenWidth, screenLength))
pygame.display.set_caption("First Game")

# load images - with two list (left and right)
walkRight = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'), pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
walkLeft = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'), pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'), pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg = pygame.image.load('assets/bg.jpg')
char = pygame.image.load('assets/standing.png')


# clock speed
clock = pygame.time.Clock()
# print(clock)

#this could be used for multiple players now
class player(object):

    def __init__(self, x, y, width, height) -> None:
        super().__init__()
        self.x = x 
        self.y = y
        self.height = height 
        self.width = width 
        self.vel = 5 
        self.isJump = False 
        self.jumpCount = 10 
        self.left = False 
        self.right = False 
        self.walkCount = 0 
        self.standing = True
        # 4 things inside a tuple = rectangle in pygame 
        # we slot this in the draw.rect function
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)


    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0 

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
                # print(self.walkCount)
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        #we have to redraw the hitbox so it moves with the character 
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)              
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
                # win.blit(char, (self.x,self.y))
    
class projectile(object):
    def __init__(self, x, y, radius, color, facing) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        #testing super/base inheritance
        # self.tester = 1
        
    
    def draw(self, win):
        # print(self.tester)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    
    #load enemy images 
    walkRight = [pygame.image.load('assets/R1E.png'), pygame.image.load('assets/R2E.png'), pygame.image.load('assets/R3E.png'), pygame.image.load('assets/R4E.png'), pygame.image.load('assets/R5E.png'), pygame.image.load('assets/R6E.png'), pygame.image.load('assets/R7E.png'), pygame.image.load('assets/R8E.png'), pygame.image.load('assets/R9E.png'), pygame.image.load('assets/R10E.png'), pygame.image.load('assets/R11E.png')]
    walkLeft = [pygame.image.load('assets/L1E.png'), pygame.image.load('assets/L2E.png'), pygame.image.load('assets/L3E.png'), pygame.image.load('assets/L4E.png'), pygame.image.load('assets/L5E.png'), pygame.image.load('assets/L6E.png'), pygame.image.load('assets/L7E.png'), pygame.image.load('assets/L8E.png'), pygame.image.load('assets/L9E.png'), pygame.image.load('assets/L10E.png'), pygame.image.load('assets/L11E.png')]

    def __init__(self, x, y, width, height, end) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end 
        # starting and ending 
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        # start, end, width, height for rectangle parameters 
        self.hitbox = (self.x + 17, self.y + 2, 31, 57) 
    
    def draw(self, win):
        self.move()

        #we have 11 enemy images
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount// 3 ], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)                  
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

        

    def move(self):
        #going right
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * - 1
                self.walkCount = 0 
        #going left
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * - 1
                self.walkCount = 0 

    def hit(self):
        print('hit')
        # pass

def redrawGameWindow():
    
    #background image
    win.blit(bg, (0,0))
    man.draw(win)
    goblin.draw(win)
    
    for bullet in bullets:
        # print(bullets.__init__.radius)
        # print(bullet.x)
        bullet.draw(win)
    
    pygame.display.update() 


# main Loop
#creating an instance of our object/classs
man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
onebullet = 0 
bullets = []
run = True
while run:
    
    clock.tick(27) 

    # this onebullet is basically adding a cooldown in timer. so we dont just spam the bullets
    # if onebullet is greater than 1 when it user hits space, then one bullets gets added to 2 and goes through it again until its greater than 4. itll reset to 0 then it can go through
    # spacebar again. The longer the number to reset the longer the cooldonw  
    if onebullet > 0:
        onebullet += 1
    if onebullet > 3:
        onebullet = 0
    
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            run = False 

    # we are looping throught the list of objects. and if its in the screen then it moves a certain velocity. if it is off screen then it gets deleted 
    for bullet in bullets:
        
        # if the bullet is in between the y rectangle of the hitbox
        # above bottom rectangle and below the top of the recatngle 
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            # bullet right side of the left side of the box and bullet in the right side of the left side of the box
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                bullets.pop(bullets.index(bullet))

        # dont go off the screen 
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        #its off the screen then we delete the bullet
        else:
            # this will find the bullet index in the list and pop (remove it) 
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and onebullet == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        
        # This is where we append bullets
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height //2), 6, (0, 0, 0), facing))
        
        onebullet = 1

    if keys[pygame.K_LEFT] and man.x > man.vel: 
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screenWidth - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0 
    
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True 
            man.walkCount = 0 
    else:
        if man.jumpCount >= -10: 
            neg = 1
            if man.jumpCount < 0:
                neg = -1 
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    

    # print(man.right)
    redrawGameWindow()

    
    


pygame.quit()
