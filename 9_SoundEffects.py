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

# load a sound effect
bulletSound = pygame.mixer.Sound('assets/Game_bullet.mp3')
hitSound = pygame.mixer.Sound('assets/Game_hit.mp3')
# bulletSound.play() = play souind effect

# load music
music = pygame.mixer.music.load('assets/music.mp3')
# -1 means repeat song when its over
pygame.mixer.music.play(-1)

score = 0 

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
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
    
    # triggers when player collides with goblin
    def hit(self):
        self.x = 60
        self.y = 410
        # his image is stationary 
        self.walkCount = 0 
        font1 = pygame.font.SysFont('comincsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (screenWidth/2 - text.get_width()/2, screenLength/2 - text.get_height()/2))
        pygame.display.update()
        #pause for user to see the update 
        # this time delay also gets affected by ur computer processor the better the faster
        i = 0 
        while i < 300:
            # in ms so 10 ms * 300 
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

    
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
        self.originalhealth = 10
        self.health = 10
        self.visible = True 
    
    def draw(self, win):
        self.move()

        if self.visible:
            #we have 11 enemy images
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount// 3 ], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            # red bar - shown first which gets overlapped by the green bar
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            # green bar - we are subtracting the green bar width everytime he gets hit because. this happens in the Width parameter
            pygame.draw.rect(win, (0, 128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/self.originalhealth) * (self.originalhealth - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)                  
            # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

        

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

        # if he gets hit then he loses health 
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False 
        print('hit')
        # pass

def redrawGameWindow():
    
    #background image
    win.blit(bg, (0,0))
    # ready to render some text an make it a surface that we can blit onto a window
    text = font.render('Score: '+ str(score), 1, (0,0,0))
    win.blit(text, (390, 10))
    man.draw(win)
    goblin.draw(win)
    
    for bullet in bullets:
        # print(bullets.__init__.radius)
        # print(bullet.x)
        bullet.draw(win)
    
    pygame.display.update() 


# main Loop
#creating an instance of our object/classs

# font, size, bold, italics
font = pygame.font.SysFont('comicsans', 30, True)

man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
onebullet = 0 
bullets = []
run = True
while run:
    
    clock.tick(27) 


    # if character collides with goblin 
    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0]  < goblin.hitbox[0] + goblin.hitbox[2]:
            man.hit()
            score -= 5 
            

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
                hitSound.play()
                goblin.hit()
                score += 1 
                #deletde the bullet
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
        bulletSound.play()
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
