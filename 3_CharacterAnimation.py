import pygame 

#always need to do 
pygame.init()


screenWidth = 500 
win = pygame.display.set_mode((screenWidth, 480))
pygame.display.set_caption("First Game")

# load images - with two list (left and right)
walkRight = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'), pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
walkLeft = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'), pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'), pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg = pygame.image.load('assets/bg.jpg')
char = pygame.image.load('assets/standing.png')


# clock speed
clock = pygame.time.Clock()
print(clock)

x = 50 
y = 425 
width = 64
height = 64 
vel = 5
isJump = False
jumpCount = 10 
left = False
right = False
walkCount = 0 


def redrawGameWindow():
    #need this to be seen outside
    global walkCount
    # win.fill((0,0,0))

    #background image
    win.blit(bg, (0,0))
    
    # because 27 frames per second 
    if walkCount + 1 >= 27:
        walkCount = 0 

    # image of person 
    if left:
        # In Python, the “//” operator works as a floor division for integer and float arguments
        # blit(source, dest, area=None, special_flags=0) -> Rect
        # Draws a source Surface onto this Surface. The draw can be positioned with the dest argument.
        # we are flooring 3 since 
        win.blit(walkLeft[walkCount//3], (x,y))
        
        walkCount += 1
        print(walkCount)
    elif right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    else:
        win.blit(char, (x,y))
    
    pygame.display.update() 


# main Loop
run = True
while run:
    
    # frame rate = how many frames/images u see per second. 
    # pygame.time.delay(100)
    # here we are setting our FPS to 27

    # tick(framerate=0) -> milliseconds
    # This method should be called once per frame. It will compute how many milliseconds have passed since the previous call.
    # this controls the runtime speed of a game. it will never run more than x frames per second. the higher the X the faster frames are being shown per second than the faster the movement
    clock.tick(50) 
    
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            run = False 


    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > vel: 
        x -= vel
        left = True
        right - False
    elif keys[pygame.K_RIGHT] and x < screenWidth - width - vel:
        x += vel
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0 

    
    if not(isJump):
        #no more up and down movement just jumping 
        # if keys[pygame.K_UP] and y > vel:
        #     y -= vel
        # if keys[pygame.K_DOWN] and y < 500 - height - vel:
        #     y += vel 
        if keys[pygame.K_SPACE]:
            isJump = True 
            right = False
            left = False
            walkCount = 0 
    else:
        if jumpCount >= -10: 
            neg = 1
            if jumpCount < 0:
                neg = -1 
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    
    redrawGameWindow()

    
    


pygame.quit()
