import pygame 

#always need to do 
pygame.init()

#Width and Height of the window
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")

x = 50 
y = 50 
width = 40
height = 60 
vel = 5

run = True
while run:
    # kind of like the clock in ms
    pygame.time.delay(100)
    # check for events = user changes. This gets a list of all the events that happen
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            run = False 

    #Returns a sequence of boolean values representing the state of every key on the keyboard. Use the key constant values to index the array. A True value means the that button is pressed.
    # https://www.pygame.org/docs/ref/key.html?highlight=get_pressed#pygame.key.get_pressed
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel 

    # window coordinates
    #0,0        500, 0
    #0, 500     500, 500

    
    # this will fill the screen with black so that we are essentially updating the background then redrawing 
    win.fill((0,0,0))
    #pygame website has all the shapes we want (R, G , B)
    pygame.draw.rect(win, (255, 0, 0 ), (x, y, width, height))
    #need to update in order to draw 
    pygame.display.update() 

pygame.quit()
