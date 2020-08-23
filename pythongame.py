# A test game made by Alex Kotov
# Last Edits 8/23/2020
import pygame
pygame.init()

# Load Basics such as Program Icon, Program Name, etc
programIcon = pygame.image.load('icon.png') # loads icon
pygame.display.set_icon(programIcon) # changes the icon of the window
window = pygame.display.set_mode((900,507)) # creates a window with dimensions of the background
pygame.display.set_caption("Shooter") # renames the window

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), \
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), \
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
# loads in the sprites for the character to walk left

walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), \
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), \
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
# loads in the sprites for the character to walk right

bg2 = pygame.image.load('bg2.jpg') # background
char = pygame.image.load('standing.png') # standing sprite
gun = pygame.image.load('gun.png') # the sprite for the bullet


clock = pygame.time.Clock() # creates a new clock object

# SOUNDS SOUNDS SOUNDS SOUNDS SOUNDS SOUNDS
bulletSound = pygame.mixer.Sound('bullet.wav') # sound of bullet being shot
hitSound = pygame.mixer.Sound('hit.wav') # sound of enemy being hit
explosionSound = pygame.mixer.Sound('explosion.wav') # explosion sound
jumpSound = pygame.mixer.Sound('jump.wav') # jumping sound
music = pygame.mixer.music.load('music.mp3') #music
pygame.mixer.music.play(-1) # plays music in a loop
# SOUNDS SOUNDS SOUNDS SOUNDS SOUNDS SOUNDS

score = 0 # creates a new variable for score

class player(object): # creates a class for the player
    
    def __init__(self, x, y, width, height):
        self.x = x # x variable of player
        self.y = y # y variable of player
        self.width = width # the width of sprite
        self.height = height # height of sprite
        self.vel = 5 # velocity of player
        self.isJump = False # is player jumping
        self.jumpCount = 10 # used for jumping
        self.left = False # used to check if character facing left
        self.right = False # used to check if character facing right
        self.walkCount = 0 # sees what frame sprite is on, default = 0
        self.standing = True # original state
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # hitbox of sprite
        
    def draw(self,window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0 # resets sprite once 27 frames have passed
            
        if not(self.standing):  
            if self.left:
                window.blit(walkLeft[self.walkCount//3], (round(self.x),round(self.y)))
                self.walkCount+=1 # goes through walkleft animation
                
            elif self.right:
                window.blit(walkRight[self.walkCount//3], (round(self.x),round(self.y)))
                self.walkCount+=1 # goes through walkright animation
        else:
            if self.right: # resets walkright frame
                window.blit(walkRight[0], (round(self.x), round(self.y)))
                
            else: # resets walkkeft frame
                window.blit(walkLeft[0], (round(self.x), round(self.y)))
                
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # hitbox
        '''pygame.draw.rect(window, (255, 0, 0), self.hitbox,2)''' # optional for hitboxes

    def hit(self): # the function that describes what happens after a hit
        self.isJump = False # fixes a bug where jumping on an enemy would spawn the player in the ground
        self.jumpCount = 10 # reset jumpcounter
        self.x = 40 # spawn player back
        self.y = 412 # to original point
        self.walkCount = 0 # reset walk count
        
        font2 = pygame.font.SysFont('Arial', 75, True)
        text = font2.render("You lost 10 points", 1, (255,0,0))
        window.blit(text,(160, 200))
        pygame.display.update()
        # text to tell the user what happened
        
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        # allows user to quit during hit
                          
class projectile(object): # creates a class for the projectile
    
    def __init__(self, x, y, radius, facing):
        self.x=x # x val of bullet
        self.y=y # y val of bullet
        self.facing = facing # checks which way bullet is facing
        self.vel = 8 * facing # velocity
        self.radius = 5 # size of bullet

    def draw(self,window): # draws bullet
        window.blit(gun, (self.x-10,self.y-30))

class enemy(object): # creates a class for the enemy
    
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), \
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), \
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), \
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    # loads in the sprites needed for the enemy to walk right
    
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), \
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), \
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), \
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    # loads in the sprites needed for the enemy to walk left
    
    explosion = [pygame.image.load('exp1.png'), pygame.image.load('exp2.png'), pygame.image.load('exp3.png'), \
                 pygame.image.load('exp4.png'), pygame.image.load('exp5.png'), pygame.image.load('exp6.png'), \
                 pygame.image.load('exp7.png'), pygame.image.load('exp8.png'), pygame.image.load('exp9.png'), \
                 pygame.image.load('exp10.png'), pygame.image.load('exp11.png'), pygame.image.load('exp12.png')]
    # loads in the sprites need for the explosion after the enemy's death
    
    def __init__(self, x, y, width, height, end):
        self.x = x # x val of enemy, original start point
        self.y = y # y val of enemy
        self.width = width # width of sprite
        self.height = height # height of sprite
        self.end = end # where does the path end
        self.path = [self.x, self.end] # represents where we start and where we end
        self.walkCount = 0 # original walkcount
        self.vel = 3 # velocity of enemy
        self.hitbox = (self.x + 17, self.y + 2, 31, 57) # hitbox
        self.health = 10 # health of enemy
        self.visible = True # checks if enemy alive
        self.newvarx = 0 # newvars of x when enemy dies
        self.newvary = 0 # newvars of y when enemy dies
        self.count = 0 # count var
        
    def draw(self,window):
        self.move()
        
        if self.visible: # reset animation
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0: # animation of walking right
                window.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
                
            else:
                window.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1 # animation of walking left

            ''' healthbar of enemy '''    
            pygame.draw.rect(window,(0,0,0), (self.hitbox[0]-1, self.hitbox[1] - 16, 52, 12)) # black healthbar
            pygame.draw.rect(window,(255,0,0), (self.hitbox[0], self.hitbox[1] - 15, 50, 10)) # red healthbar
            pygame.draw.rect(window,(0,100,0), (self.hitbox[0], self.hitbox[1] - 15, 50 - (5* (10-self.health)), 10)) # green healthbar

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            '''pygame.draw.rect(window, (255,0,0), self.hitbox,2)''' # optional for hitboxes
            
        else: # explosion
            if self.count <= 35:
                if self.count < 3:
                    explosionSound.play() # plays explosion sound
                window.blit(self.explosion[self.count //3], (self.newvarx, self.newvary))
                self.walkCount+=1 # plays explosion animation
                self.count +=1
                
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel # moves enemy right
            else:
                self.vel = self.vel * -1
                self.walkCount = 0 # change direction
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel # moves enemy left
            else:
                self.vel = self.vel * -1
                self.walkCount = 0 # change direction
                
    def hit(self):
        if self.health > 1:   
            self.health -=1
            #lowers health by 1
            
        else:
            self.visible = False # makes character invisible
            self.newvarx = self.x # sets newvarx and
            self.newvary = self.y # newvary characters

# default jump settings
isJump = False 
jumpCount = 10

def GameWindow():
    window.blit(bg2, (0,0)) # puts background on screen
    text = font.render('Score: ' + str(score), 1, (255,255,255)) # show score
    window.blit(text, (10,10)) # show score
    man.draw(window) # Draw main char
    goblin.draw(window) # draw enemy
    for bullet in bullets: # draws bullets
        bullet.draw(window)
    pygame.display.update() # updates the display
    

#mainloop
font = pygame.font.SysFont('Arial', 30, True) # default Font
man = player(40, 412, 64, 64) # creates the player
goblin = enemy( 300, 412, 64,64, 700) # names enemy and creates it
shoottime = 0 # a variable used for shooting delay
bullets = [] # list of bullets
run = True # default to start program

while run == True:
    clock.tick(27) # framerate
    if goblin.visible == True: # checks for a hit between player and enemy
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit() # plays hit animation
                score-=10 # lower score
                
    '''these 4 lines of code delay shots'''      
    if shoottime > 0:
        shoottime +=1
    if shoottime > 10:
        shoottime = 0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False # closes program

    for bullet in bullets: # checks if bullet hits goblin
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius < goblin.hitbox[0] + goblin.hitbox [2] and bullet.x + bullet.radius > goblin.hitbox[0]:
                if goblin.visible == True: # only hits when visible
                    
                    hitSound.play() # plays hit sound
                    goblin.hit() # runs hit function
                    score+=25 # adds to score
                    bullets.pop(bullets.index(bullet)) # deletes bullet
                    
        if bullet.x < 880 and bullet.x > 0:
            bullet.x += bullet.vel # moves bullet
        else:
            bullets.pop(bullets.index(bullet))
    keys = pygame.key.get_pressed() # defualt key func

    if keys[pygame.K_SPACE] and shoottime == 0:
        if man.left: # changes facing to -1 so
            facing = -1 # bullets travel left
        else:
            facing = 1 # changes right
            
        if len(bullets) < 5: # only shoots if bullets less than 5
            bulletSound.play() # plays bullet sound
            bullets.append(projectile(round((man.x+10) + facing*20), round(man.y+man.height //2), 5 , facing)) # shoots bullet
        shoottime = 1 # reset shoottime
        
    # moves left when left arrow pressed
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x-=5
        man.left=True
        man.right=False
        man.standing = False

    # moves right when right arrow pressed 
    elif keys[pygame.K_RIGHT] and man.x < 831:
        man.x+=5
        man.left=False
        man.right=True
        man.standing = False

    # stands original pos
    else:
        man.standing = True
        man.walkCount = 0

    ''' jumps when not in a jump already '''
    if not(man.isJump):
        if keys[pygame.K_UP]:
            jumpSound.play() # plays jump sound
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            negative = 1 # upward motion in jump
            if man.jumpCount < 0:
                negative = -1 # downfall of jump
            man.y -= (man.jumpCount ** 2)* 0.35 * negative # a power of 2 for a parabola
            man.jumpCount -= 1 # lowers jumpcount
            
        else:
            man.isJump = False # ends jump
            man.jumpCount = 10 # reset original jumpcount
            
    GameWindow()
pygame.quit() # quits program
