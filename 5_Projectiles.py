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
print(clock)

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


    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0 

        # the reason we can call standing here is because of the super (base class) function and inheritance 
        # in this case init is usually the super/base class
        # so we can inherit from the BASE/SUPER class but we cannot inherit from the child classes 
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

def redrawGameWindow():
    
    #background image
    win.blit(bg, (0,0))
    man.draw(win)
    
    #we have to draw the bullet. Bullets is a list of objects
    #here we actually draw the each bullet in the list of objects bullets. The reason we can shift between bullet.x vs bullet.draw is because of inheritance
    for bullet in bullets:
        # print(bullets.__init__.radius)
        print(bullet.x)
        bullet.draw(win)
    
    pygame.display.update() 


# main Loop
#creating an instance of our object/classs
man = player(300, 410, 64, 64)
bullets = []
run = True
while run:
    
    clock.tick(27) 
    
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            run = False 

    # we are looping throught the list of objects. and if its in the screen then it moves a certain velocity. if it is off screen then it gets deleted 
    for bullet in bullets:
        # dont go off the screen 
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        #its off the screen then we delete the bullet
        else:
            # this will find the bullet index in the list and pop (remove it) 
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        
        # This is where we append bullets
        if len(bullets) < 5:
            #this means the bullets are coming forom the middle of the man (as to why we are rounding we dont want a decimal value)
            # 1. so we are creating an instance of the projectile object which is a bullet. 
            # 2. we are maxing it to 5 bullets on the screen
            # 3. we are adding this object/instance into the list called "bullets"
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height //2), 6, (0, 0, 0), facing))


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
            # man.right = False
            # man.left = False
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
