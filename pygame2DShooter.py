########################################################

# Pygame2DShooter is a 2D Shooter game made in python
# using the module pygame. Currently features such as
# Jumping, Shooting, Enemies, Healthbars and more
# Have been added.

# Libraries Used: pygame

# Pygame2DShooter will automatically start upon running
# The Program.

# Please read Controls.txt for Controls or look at the
# .md file located in the github.

# The Goal of Pygame2DShooter is to Eliminate the Enemy
# Using your gun. Bumping into the Enemy will lead to
# A loss in score.

# please report any issues to the github immediately.

# Pygame2DShooter can be reused or edited in any way.

# Alex Kotov  08/23/2020
# Last Update 010/3/2020

########################################################

import pygame
pygame.init()

# Load Basics such as Program Icon, Program Name, etc
programIcon = pygame.image.load('resources/misc/icon.png') # loads icon
pygame.display.set_icon(programIcon) # changes the icon of the window
window = pygame.display.set_mode((900,507)) # creates a window with dimensions of the background
pygame.display.set_caption("Shooter") # renames the window

# loads in the sprites for the character to walk left
walkRight = [pygame.image.load('resources/man/R1.png'), pygame.image.load('resources/man/R2.png'),
             pygame.image.load('resources/man/R3.png'), pygame.image.load('resources/man/R4.png'),
             pygame.image.load('resources/man/R5.png'), pygame.image.load('resources/man/R6.png'),
             pygame.image.load('resources/man/R7.png'), pygame.image.load('resources/man/R8.png'),
             pygame.image.load('resources/man/R9.png')]

# loads in the sprites for the character to walk right
walkLeft = [pygame.image.load('resources/man/L1.png'), pygame.image.load('resources/man/L2.png'),
            pygame.image.load('resources/man/L3.png'), pygame.image.load('resources/man/L4.png'),
            pygame.image.load('resources/man/L5.png'), pygame.image.load('resources/man/L6.png'),
            pygame.image.load('resources/man/L7.png'), pygame.image.load('resources/man/L8.png'),
            pygame.image.load('resources/man/L9.png')]

# Load in Other Sprites
bg2 = pygame.image.load('resources/misc/bg2.jpg') 
char = pygame.image.load('resources/man/standing.png') 
gun = pygame.image.load('resources/misc/gun.png') 


clock = pygame.time.Clock()

# SOUNDS SOUNDS SOUNDS SOUNDS SOUNDS SOUNDS
bulletSound = pygame.mixer.Sound('resources/audio/bullet.wav') 
hitSound = pygame.mixer.Sound('resources/audio/hit.wav') 
explosionSound = pygame.mixer.Sound('resources/audio/explosion.wav') 
jumpSound = pygame.mixer.Sound('resources/audio/jump.wav') 
music = pygame.mixer.music.load('resources/audio/music.mp3') 
pygame.mixer.music.play(-1) 
# SOUNDS SOUNDS SOUNDS SOUNDS SOUNDS SOUNDS

score = 0 

class player(object): 
    
    def __init__(self, x, y, width, height):
        
        # Declare player Variables
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.vel = 5 
        self.isJump = False 
        self.jumpCount = 10 
        self.left = False 
        self.right = False 
        self.walkCount = 0 
        self.standing = True 
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) 
        
    def draw(self,window):
        # Draw Sprite
        if self.walkCount + 1 >= 27:
            self.walkCount = 0 #
            
        if not(self.standing):  
            if self.left:
                window.blit(walkLeft[self.walkCount//3], (round(self.x),round(self.y)))
                self.walkCount+=1 
                
            elif self.right:
                window.blit(walkRight[self.walkCount//3], (round(self.x),round(self.y)))
                self.walkCount+=1
                
        # Reset Frames
        else:
            if self.right: 
                window.blit(walkRight[0], (round(self.x), round(self.y)))
                
            else: 
                window.blit(walkLeft[0], (round(self.x), round(self.y)))
                
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # hitbox
        '''pygame.draw.rect(window, (255, 0, 0), self.hitbox,2)''' # optional for hitboxes

    def hit(self):
        
        # Declare our hit variables
        self.isJump = False 
        self.jumpCount = 10 
        self.x = 40 
        self.y = 412 
        self.walkCount = 0

        # text to tell the user what happened
        font2 = pygame.font.SysFont('Arial', 75, True)
        text = font2.render("You lost 10 points", 1, (255,0,0))
        window.blit(text,(160, 200))
        pygame.display.update()
        

        # allows user to quit during hit
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        
                          
class projectile(object): 
    
    def __init__(self, x, y, radius, facing):
        # Declare Projectile Variables
        self.x=x 
        self.y=y 
        self.facing = facing 
        self.vel = 8 * facing 
        self.radius = 5 

    # Draw Bullet
    def draw(self,window):
        window.blit(gun, (self.x-10,self.y-30))

class enemy(object):

        # loads in the sprites needed for the enemy to walk right
    walkRight = [pygame.image.load('resources/enemy/R1E.png'), pygame.image.load('resources/enemy/R2E.png'),
                 pygame.image.load('resources/enemy/R3E.png'), pygame.image.load('resources/enemy/R4E.png'),
                 pygame.image.load('resources/enemy/R5E.png'), pygame.image.load('resources/enemy/R6E.png'),
                 pygame.image.load('resources/enemy/R7E.png'), pygame.image.load('resources/enemy/R8E.png'),
                 pygame.image.load('resources/enemy/R9E.png'), pygame.image.load('resources/enemy/R10E.png'),
                 pygame.image.load('resources/enemy/R11E.png')]

    # loads in the sprites needed for the enemy to walk left
    walkLeft = [pygame.image.load('resources/enemy/L1E.png'), pygame.image.load('resources/enemy/L2E.png'),
                pygame.image.load('resources/enemy/L3E.png'), pygame.image.load('resources/enemy/L4E.png'),
                pygame.image.load('resources/enemy/L5E.png'), pygame.image.load('resources/enemy/L6E.png'),
                pygame.image.load('resources/enemy/L7E.png'), pygame.image.load('resources/enemy/L8E.png'),
                pygame.image.load('resources/enemy/L9E.png'), pygame.image.load('resources/enemy/L10E.png'), pygame.image.load('resources/enemy/L11E.png')]

    # loads in the sprites need for the explosion after the enemy's death
    explosion = [pygame.image.load('resources/explosion/exp1.png'), pygame.image.load('resources/explosion/exp2.png'),
                 pygame.image.load('resources/explosion/exp3.png'), pygame.image.load('resources/explosion/exp4.png'),
                 pygame.image.load('resources/explosion/exp5.png'), pygame.image.load('resources/explosion/exp6.png'),
                 pygame.image.load('resources/explosion/exp7.png'), pygame.image.load('resources/explosion/exp8.png'),
                 pygame.image.load('resources/explosion/exp9.png'), pygame.image.load('resources/explosion/exp10.png'),
                 pygame.image.load('resources/explosion/exp11.png'), pygame.image.load('resources/explosion/exp12.png')]
    
    
    def __init__(self, x, y, width, height, end):

        # Declare our variables
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.end = end # Used for endpath
        self.path = [self.x, self.end] 
        self.walkCount = 0 
        self.vel = 3 
        self.hitbox = (self.x + 17, self.y + 2, 31, 57) 
        self.health = 10 
        self.visible = True 
        self.newvarx = 0 
        self.newvary = 0 
        self.count = 0 
        
    def draw(self,window):
        self.move()

        # Draw the character
        if self.visible: 
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0: 
                window.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
                
            else:
                window.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1 

            ''' healthbar of enemy '''    
            pygame.draw.rect(window,(0,0,0), (self.hitbox[0]-1, self.hitbox[1] - 16, 52, 12)) 
            pygame.draw.rect(window,(255,0,0), (self.hitbox[0], self.hitbox[1] - 15, 50, 10)) 
            pygame.draw.rect(window,(0,100,0), (self.hitbox[0], self.hitbox[1] - 15, 50 - (5* (10-self.health)), 10)) 

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            '''pygame.draw.rect(window, (255,0,0), self.hitbox,2)''' # optional

        # explosion 
        else: 
            if self.count <= 35:
                if self.count < 3:
                    explosionSound.play() 
                window.blit(self.explosion[self.count //3], (self.newvarx, self.newvary))
                self.walkCount+=1 
                self.count +=1
                
    def move(self):
        # Move the Character Sprite
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
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
                
    #lowers health by 1   
    def hit(self):
        if self.health > 1:   
            self.health -=1
            
        else:
            self.visible = False 
            self.newvarx = self.x 
            self.newvary = self.y 

# default jump settings
isJump = False 
jumpCount = 10

def GameWindow():
    # Draw the Window and everything on the window
    window.blit(bg2, (0,0)) 
    text = font.render('Score: ' + str(score), 1, (255,255,255)) 
    window.blit(text, (10,10)) 
    man.draw(window) 
    goblin.draw(window) 
    for bullet in bullets: 
        bullet.draw(window)
    pygame.display.update() 
    
# Declare some Game Variables
score = 0 
font = pygame.font.SysFont('Arial', 30, True) 
man = player(40, 412, 64, 64) 
goblin = enemy( 300, 412, 64,64, 700) 
shoottime = 0 # a variable used for shooting delay
bullets = [] 
run = True

# mainloop
while run == True:
    clock.tick(27)
    # Check for Hit Between Player and Enemy
    if goblin.visible == True: 
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit() 
                score-=10 
                
    '''these 4 lines of code delay shots'''      
    if shoottime > 0:
        shoottime +=1
    if shoottime > 10:
        shoottime = 0

    # Alows user to quit Program.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 

    # Check if a bullet hits a goblin.
    for bullet in bullets: 
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius +2 < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.radius +26 > goblin.hitbox[0]:
                if goblin.visible == True: 

                    # Play Animations/Sounds/Functions
                    hitSound.play() 
                    goblin.hit() 
                    score+=25 
                    bullets.pop(bullets.index(bullet)) 

        # Move bullet if in screen
        if bullet.x < 880 and bullet.x > 0:
            bullet.x += bullet.vel 
        else:
            bullets.pop(bullets.index(bullet))
            
    # Declare keys
    keys = pygame.key.get_pressed()

    # Shooting Mechanics
    if keys[pygame.K_SPACE] and shoottime == 0:
        # Direction facing
        if man.left: 
            facing = -1 
        else:
            facing = 1 

        # Shoot Bullet
        if len(bullets) < 5: 
            bulletSound.play() 
            bullets.append(projectile(round((man.x+10) + facing*20), round(man.y+man.height //2), 5 , facing)) # shoots bullet
        shoottime = 1 
        
    # moves left when left arrow or 'a' key pressed
    if keys[pygame.K_LEFT] and man.x > man.vel -20 or keys[pygame.K_a] and man.x > man.vel -20:
        man.x-=5
        man.left=True
        man.right=False
        man.standing = False

    # moves right when right arrow or 'd' key pressed 
    elif keys[pygame.K_RIGHT] and man.x < 831 or keys[pygame.K_d] and man.x < 851:
        man.x+=5
        man.left=False
        man.right=True
        man.standing = False

    # stands in original position
    else:
        man.standing = True
        man.walkCount = 0

    # Jumps when up arrow or 'w' key pressed
    if not(man.isJump):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            jumpSound.play()
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            negative = 1 
            if man.jumpCount < 0:
                negative = -1 
            man.y -= (man.jumpCount ** 2)* 0.35 * negative 
            man.jumpCount -= 1 
            
        else:
            man.isJump = False 
            man.jumpCount = 10 
            
    GameWindow()
pygame.quit() # quits program
