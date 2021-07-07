import pygame 

#always need to do 
pygame.init()


screenWidth = 500 
win = pygame.display.set_mode((screenWidth, 500))
pygame.display.set_caption("First Game")

x = 50 
y = 425 
width = 40
height = 60 
vel = 5

isJump = False
jumpCount = 10 

run = True
while run:
    
    pygame.time.delay(100)
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            run = False 


    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > vel: 
        x -= vel
    if keys[pygame.K_RIGHT] and x < screenWidth - width - vel:
        x += vel
    

    # This is how we jump 
    if not(isJump):
        if keys[pygame.K_UP] and y > vel:
            y -= vel
        if keys[pygame.K_DOWN] and y < 500 - height - vel:
            y += vel 
        if keys[pygame.K_SPACE]:
            # a jump is like a parobola in this module at the apex = 0 accelration. 
            isJump = True 
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
  

    
    
    win.fill((0,0,0))
    pygame.draw.rect(win, (255, 0, 0 ), (x, y, width, height))
    pygame.display.update() 

pygame.quit()
