'''
Author: Freeman Zhang
Date: May 30, 2017
Description: This is the code for sprites for GalaQuest
'''

import pygame, random
class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for the paddle which is controlled by the player'''
    def __init__(self, screen):
        '''This initializer takes the player images and puts it on the screen'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Define the image attributes for a black rectangle.
        self.images = [pygame.image.load('Player0.png').convert(), \
                  pygame.image.load('Player1.png').convert()]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.top_boundary = 0
        #Sets the position of where the paddle starts
        self.rect.center = (screen.get_width()/2, screen.get_height() - 100)
        self.__screen = screen
    
    def changex(self, x, screen):
        '''changes the x coordinates of the player sprite'''
        if x:
            self.rect.centerx += 5
        else:
            self.rect.centerx += -5
            
    def changey(self, y, screen):
        '''changes the y coordinates of the player sprite'''
        if y:
            self.rect.centery += 5
        else:
            self.rect.centery += -5
    
    def change_boundary(self):
        '''When the boss comes out, this will prevent the player from colliding 
        with the sprite'''
        self.top_boundary = 230
        
    def get_top(self):
        '''returns coordinates of the top of the sprite'''
        return self.rect.centerx, self.rect.top + 10
    
    def update(self, screen):
        '''Will update the screen to animate it and to prevent it from going offscreen'''
        if self.rect.right >= screen.get_width() - 5:
            self.rect.right = screen.get_width() - 5
        if self.rect.left <= 5:
            self.rect.left = 5
        if self.rect.top <= self.top_boundary:
            self.rect.top = self.top_boundary
        if self.rect.bottom >= screen.get_height() - 30:
            self.rect.bottom = screen.get_height() - 30
        #animates the player sprite    
        if self.image == self.images[0]:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
            
        
    
            
class Background(pygame.sprite.Sprite):
    '''This class defines the sprite for the infinite scrolling background'''
    def __init__(self):
        '''Creates the infinite scrolling background and moves it down'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)        
        
        self.image = pygame.image.load('blue_background.png').convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = 640
        
    def update(self, screen):
        '''Will move the image down, and as the screen reaches the top of the
        image, it is reset'''
        self.rect.bottom += 2
        if self.rect.top == 0:
            self.rect.bottom = screen.get_height()
            
class Good_Bullet(pygame.sprite.Sprite):
    '''This class defines the sprite for the bullet shot by the player'''
    def __init__(self, top):
        '''This will initialize the bullet sprite'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('good_bullet.png').convert()
        self.rect = self.image.get_rect()
        self.appear(top)
        self.move = 10
        self.__hit_boss = 0
        
    def hit_boss(self):
        '''The bullet will react different when it kills the boss, for better animation'''
        self.__hit_boss += 1
        
    def appear(self, top):
        '''This will make the bullet appear'''
        self.rect.center = top
    
    def hide(self):
        '''Will hide the sprite off screen and kill it'''
        self.rect.center = (1000, -200)
        self.move = 0
        self.kill()
        
    def update(self, screen):
        '''Will move the bullet up the screen and kill it when it goes offscreen'''
        self.rect.centery -= self.move
        if self.__hit_boss == 10:
            self.hide()
        if self.rect.bottom < 0:
            self.hide()        

  
class Bad_Bullet(pygame.sprite.Sprite):
    '''This class defines the sprite for the bullet shot by the boss'''
    def __init__(self, center):
        '''Initializes the bad bullets'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Bad_bullet.png').convert()
        self.rect = self.image.get_rect()
        self.rect.center = (center)
        self.__dy = 8
    
    def hide(self):
        '''Will hide the sprite in the corner of screen, where it is not visible'''
        self.rect.center = (0, -100)
        self.move = 0
        self.kill()
        
    def update(self, screen):
        '''Will move the bullets down and kills it when it goes offscreen'''
        self.rect.centery += self.__dy
        if self.rect.top > screen.get_height():
            self.hide()      
        
class Round_Bullet(pygame.sprite.Sprite):
    '''This class defines the sprite for the bullet shot by the boss'''
    def __init__(self, center, movex, movey):
        '''Will initialize the bullet, taking in a position for it to spawn and
        the movement of it'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('round_bullet.png').convert()
        self.rect = self.image.get_rect()
        self.rect.center = (center)
        self.__dx = movex
        self.__dy = movey
    
    def hide(self):
        '''Will hide the sprite in the corner of screen, where it is not visible'''
        self.rect.center = (0, -100)
        self.__dx = 0
        self.__dy = 0
        self.kill()
        
    def update(self, screen):
        '''Will move the bullet and kill it offscreen'''
        self.rect.centery += self.__dy
        self.rect.centerx += self.__dx
        if self.rect.top > screen.get_height():
            self.hide()
            
class Score(pygame.sprite.Sprite):
    '''This class defines the sprite for the score keeper'''
    def __init__(self):
        '''Will initialize the score keeper'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)        
        self.__font = pygame.font.SysFont("Arial", 25)
        self.__score = 0
    
    def increase_score(self, amount):
        '''will increase the score by a certain amount'''
        if amount < 0:
            amount = 0
        self.__score += amount
        
    def decrease_score(self, amount):
        '''will decrease the score by a certain amount'''
        self.__score -= amount    
        
    def update(self, screen):
        '''updates the score onscreen'''
        message = "Score: %d" % self.__score
        self.image = self.__font.render(message, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.top = 610
        self.rect.left = 5
        
class Player_health(pygame.sprite.Sprite):
    '''This class defines the sprite for the health bar'''
    def __init__(self, screen):
        '''Will initialize the health bar of the player's health'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)        
        self.__health = 300
        
        self.image = pygame.Surface((self.__health, 20))
        self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.center = (323, screen.get_height()-15)
        
    def lose_health(self, damage):
        '''Will decrease the amount of health the player has'''
        self.__health -= damage
        if self.__health < 0:
            self.__health = 0
            
    def get_health(self):
        '''Return the health of the player'''
        return self.__health
        
    def heal_health(self):
        '''Will increase the health, is called when the player sprite collides
        with a power up sprite. If the health bar is increased to over the max
        health(300), then it is set to 300'''
        self.__health += 60
        if self.__health > 300:
            self.__health = 300
        
    def update(self, screen):
        '''Will change the length of the health bar to indicate a change in
        the amount of health the player has left'''
        self.image = pygame.Surface((self.__health, 20))
        self.image.fill((255, 0, 0))        
        
class Border(pygame.sprite.Sprite):
    '''Creates the border around the game that holds the score and health bar'''
    def __init__(self, screen):
        '''Will initialize the borders around the window'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Draws a border
        self.image = pygame.Surface((screen.get_width(), screen.get_height()))
        self.image = self.image.convert()
        #drawing the borders
        pygame.draw.rect(self.image, (160, 160, 160), ((0, 0), (5, screen.get_height())), 0)
        pygame.draw.rect(self.image, (160, 160, 160), ((0, 0), (screen.get_width(), 5)), 0)
        pygame.draw.rect(self.image, (160, 160, 160), ((screen.get_width() - 5, 0), (5, screen.get_height())), 0)
        pygame.draw.rect(self.image, (160, 160, 160), ((0, screen.get_height() - 30), (screen.get_width(), 30)), 0)
        #border for the player's health bar
        pygame.draw.rect(self.image, (1, 0, 0), ((171, screen.get_height()- 27), (303, 23)), 2)
        #making the parts that aren't the border transparent
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0 
        
    def boss_health(self, screen):
        '''Will change the border when the boss comes into screen'''
        pygame.draw.rect(self.image, (160, 160, 160), ((0, 0), (screen.get_width(), 30)), 0)
        pygame.draw.rect(self.image, (1, 0, 0), ((38, 3), (401, 23)), 2)
        pygame.draw.rect(self.image, (100, 0, 0), ((5, 30), (screen.get_width()-11, 200)), 2)
        pygame.draw.rect(self.image, (1, 0, 0), ((140, 5), (1, 22)), 2)
        pygame.draw.rect(self.image, (1, 0, 0), ((240, 5), (1, 22)), 2)
        pygame.draw.rect(self.image, (1, 0, 0), ((340, 5), (1, 22)), 2)        
        
class Enemy(pygame.sprite.Sprite):
    '''This class defines the sprite for enemy ships'''
    def __init__(self, center, x, y):
        '''will initialize the enemies, by taking in a position for it to spawn 
        and the movement'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #loads in 2 images for animation
        self.images = [pygame.image.load('Enemy0.png').convert(), \
                  pygame.image.load('Enemy1.png').convert()]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        #will set the center to the center argument
        self.rect.center = center
        #sets the movements based on the arguments
        self.__dx = x
        self.__dy = y
    
    def getx(self):
        '''returns the movement'''
        return self.__dx
    
    def hide(self):
        '''Will hide the sprite off screen, where it is not visible'''
        self.rect.center = (-200, -200)
        self.__dx = 0
        self.__dy = 0
        self.kill()
        
    def get_center(self):
        '''This method will return the current coordinates for the sprites center'''
        return self.rect.center
    
    def change_move(self, newx, newy):
        '''Will change the movement of the sprite'''
        self.__dx = newx
        self.__dy = newy
        
    def update(self, screen):
        '''Will move the sprite down by the amount indicated by the self.move variable'''
        self.rect.centery += self.__dy
        self.rect.centerx += self.__dx
        
        #will change the image to animate it        
        if self.image == self.images[0]:
            self.image = self.images[1]
        else:
            self.image = self.images[0]        

class Boss(pygame.sprite.Sprite):
    '''This class defines the sprite for the boss'''
    def __init__(self, screen):
        '''initializes the boss'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('bigger_size_boss.png').convert()
        self.rect = self.image.get_rect()
        #hides the boss offscreen
        self.rect.center = (screen.get_width()/2, -100)
        self.__move = 0
        
    def start_move(self):
        '''Starts moving the boss onto the screen'''
        self.__move = 3
        
    def check_move(self):
        '''returns the movement of the boss'''
        return self.__move
    
    def update(self, screen):
        '''Will update the boss sprite'''
        if self.__move > 0:
            self.rect.centery += self.__move
        '''Will stop the movement of the boss sprite after reaching a certain point'''
        if self.rect.top > 33:
            self.__move = 0
            
class Boss_Health(pygame.sprite.Sprite):
    '''This class defines the sprite for the health bar'''
    def __init__(self, screen):
        '''Initializes the boss health'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)        
        self.__health = 2000
        #drawing the health bar
        self.image = pygame.Surface((self.__health/5, 20))
        self.image.fill((255, 0, 0))
        pygame.draw.rect(self.image, (1, 0, 0), ((100, 0), (1, 23)), 2)
        pygame.draw.rect(self.image, (1, 0, 0), ((200, 0), (1, 23)), 2)
        pygame.draw.rect(self.image, (1, 0, 0), ((300, 0), (1, 23)), 2)
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2, 15)  
        
    def lose_health(self, damage):
        '''Will decrease the amount of health the player has'''
        self.__health -= damage
        if self.__health < 0:
            self.__health = 0
    
    def get_health(self):
        '''returns the health'''
        return self.__health
        
    def update(self, screen):
        '''Will change the length of the health bar to indicate a change in
        the amount of health the boss has left'''
        self.image = pygame.Surface((self.__health/5, 20))
        self.image.fill((255, 0, 0))
        pygame.draw.rect(self.image, (1, 0, 0), ((100, 0), (1, 23)), 2)
        pygame.draw.rect(self.image, (1, 0, 0), ((200, 0), (1, 23)), 2)
        pygame.draw.rect(self.image, (1, 0, 0), ((300, 0), (1, 23)), 2)
        
class Heal(pygame.sprite.Sprite):
    '''This class defines the sprite for my power up, which increases the length
    by a little'''
    def __init__(self, center):
        '''Initializes the heal buff'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('Powerup.png')
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (0,0)
        self.rect.center = center
                  
    def update(self, screen):
        '''Moves the sprite down the screen'''
        self.rect.centery += 5
        #Once the heal is completely off the screen, it will kill itself
        if self.rect.top > screen.get_height():
            self.kill()
            
class Laser(pygame.sprite.Sprite):
    '''This class defines the sprite for my power up, which increases the length
    by a little'''
    def __init__(self, center):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)\
        #loading the images for the laser animation
        self.images = []
        for image_number in range(10):
            self.laser = pygame.image.load('laser/Laser' + str(image_number) +\
                                           '.png')
            self.laser.convert()
            self.images.append(self.laser)
            
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.__center = center
        self.rect.center = self.__center
        self.__laser_number = 0
        self.__initial_laser = 0
        self.__final_laser = 0
    
    def final_form(self):
        '''checks if the laser is in its final form'''
        if self.__laser_number == 9:
            return True
    
    def update(self, screen):
        '''Updates and animates the laser'''
        self.__initial_laser += 1
        #after the laser is in the initial stage for 35 frames, it continues on
        if self.__initial_laser > 35:
            self.image = self.images[self.__laser_number]
            self.rect = self.image.get_rect()
            self.rect.center = self.__center
            self.__laser_number += 1
            if self.__laser_number > 9:
                self.__laser_number = 9
            self.__final_laser += 1
        #after the laser is in its final form for 100 frames, it kills itself
        if self.__final_laser > 100:
            self.kill()
                    
class Explosion(pygame.sprite.Sprite):
    '''This class defines the sprite for my power up, which increases the length
    by a little'''
    def __init__(self, center):
        '''Initializes the explosion sprite, taking in a center for it to spawn at'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #loads in the images for the explosion
        self.images = []
        for image_number in range(8):
            image = pygame.image.load('explosion/explosion' + \
                                str(image_number) + '.png')
            self.images.append(image)
        
        self.image = self.images[0]
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        #sets the center to the center argument
        self.__center = center
        self.rect.center = self.__center
        self.__image_number = 0
    
    def update(self, screen):
        '''Updates and animates the sprite'''
        self.__image_number += 1
        self.image = self.images[self.__image_number]
        self.rect = self.image.get_rect()
        self.rect.center = self.__center
        '''After reaching the final picture, it kills itself'''
        if self.__image_number == 7:
            self.kill()
            
class Pointer(pygame.sprite.Sprite):
    '''This class defines the sprite for the pointer sprite'''
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self) 
        #loads in the images of the pointer sprites
        self.images = [pygame.image.load('Menu_Pointer.png'),\
                       pygame.image.load('Menu_Pointer1.png')]
        self.image = self.images[0]
        self.image = self.image.convert()
        self.rect  = self.image.get_rect()
        self.rect.center = (120, 380)
    
    def move_up(self):
        '''moves the sprite up'''
        self.rect.centery = 380
        
    def move_down(self):
        '''moves the sprite down'''
        self.rect.centery = 480
        
    def update(self, screen):
        '''Updates and animates the sprite'''
        if self.image == self.images[0]:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
            
class Menu(pygame.sprite.Sprite):
    '''This class defines the menu sprite'''
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #loads in 2 different images for different selections
        self.__menu_start = pygame.image.load('Menu_start.png')
        self.__menu_help = pygame.image.load('Menu_help.png')
        self.image = self.__menu_start
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
    
    def get_page(self):
        '''return the current page it is on'''
        if self.image == self.__menu_start:
            return 1
        if self.image == self.__menu_help:
            return 2
        
    def move_up(self):
        '''changes the image to menu start'''
        self.image = self.__menu_start
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        
    def move_down(self):
        '''changes the image to menu help'''
        self.image = self.__menu_help
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0