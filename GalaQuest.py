'''
Author: Freeman Zhang
Date: May 30, 2017
Description: This is the code for the main game of GalaQuest
'''

# I - Import and Initialize
import pygame, Sprites, random
pygame.init()
pygame.mixer.init()

def help():
    '''Displays the help page, will return to main menu if the user presses backspace'''
    # D - Display configuration
    screen = pygame.display.set_mode((480, 640))
    pygame.display.set_caption("GalaQuest")
 
    # E - Entities
    background = pygame.Surface((480, 640))
    help = pygame.image.load('Help.png')
    screen.blit(help, (0,0))
    
    allSprites = pygame.sprite.OrderedUpdates()
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)  
    
    # A - Action (broken into ALTER steps)
    
        # A - Assign values to key variabless
    clock = pygame.time.Clock()
    keepGoing = True

        # L - Loop
    while keepGoing:
 
        # T - Timer to set frame rate
        clock.tick(30)
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        
        #Takes the keys that the user presses and moves the player sprite 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]: 
            return 0
            
        # R - Refresh display
        allSprites.clear(screen, background)
        allSprites.update(screen)
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    # exits function, back into main() 
    return 
    
def menu():
    '''Displays the main menu, with two options'''
    # D - Display configuration
    screen = pygame.display.set_mode((480, 640))
    pygame.display.set_caption("GalaQuest")
 
    # E - Entities
    #Loading and playing the background music for the menu
    pygame.mixer.music.load('Intro Screen.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    
    #creates sprites for the background, menu and pointer
    background = pygame.Surface((480, 640))
    menu = Sprites.Menu()  
    pointer = Sprites.Pointer()

    allSprites = pygame.sprite.OrderedUpdates(menu, pointer)
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)  
    
    # A - Action (broken into ALTER steps)
    
        # A - Assign values to key variabless
    clock = pygame.time.Clock()
    keepGoing = True

        # L - Loop
    while keepGoing:
 
        # T - Timer to set frame rate
        clock.tick(30)
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        
        #Takes the keys that the user presses and moves the pointer
        keys = pygame.key.get_pressed()
        #changes the pages 
        if menu.get_page() == 2:
            if keys[pygame.K_UP]: 
                pointer.move_up()
                menu.move_up()
            #will return 2 to go the the help screen
            if keys[pygame.K_SPACE]:
                return 2
            
        if menu.get_page() == 1:
            if keys[pygame.K_DOWN]: 
                pointer.move_down()
                menu.move_down()
            #will return 1 to go to the main game
            if keys[pygame.K_SPACE]:
                return 1
            
        # R - Refresh display
        allSprites.clear(screen, background)
        allSprites.update(screen)
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    # exits function, back into main() 
    return 
        

def game():
    '''Controls the main game loop'''
    # D - Display configuration
    screen = pygame.display.set_mode((480, 640))
    pygame.display.set_caption("GalaQuest")
 
    # E - Entities 
    #Loads and plays the main battle music
    pygame.mixer.music.load('Arcade Funk.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2) 
    #Loads in 2 sfx, one for shooting and the other for explosion
    shoot = pygame.mixer.Sound('shoot.wav')
    shoot.set_volume(0.1)
    boom = pygame.mixer.Sound('boom.wav')
    boom.set_volume(0.2)
    
    #Loads in the sprites for the background, player, border, score, health and boss
    background = pygame.Surface((480, 640))
    background2 = Sprites.Background()    
    player = Sprites.Player(screen)
    border = Sprites.Border(screen)
    score = Sprites.Score()
    player_health = Sprites.Player_health(screen)
    boss_ship = Sprites.Boss(screen)
    #Creats sprite groups for health bars, bullets, enemies, powerup and explosions
    health = pygame.sprite.Group(player_health)
    good_bullet_group = pygame.sprite.Group()
    bad_bullet_group = pygame.sprite.Group()
    laser_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    #creates the allsprites group
    allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
    
    #preloads some animations offscreen to prevent lag later on
    explode = Sprites.Explosion((-100, -100))
    explosion_group.add(explode)
    laser = Sprites.Laser((-100, -100))
    laser_group.add(laser)

    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)  
    
    # A - Action (broken into ALTER steps)
    
        # A - Assign values to key variabless
    clock = pygame.time.Clock()
    keepGoing = True
    player_shoot = True
    boss_shoot = True
    enemy_appear = True
    boss_appear = True
    boss_health_appear = False
    change_attack_pattern = True
    boss_laser = True
    player_move = True
    wave_1 = True
    wave_2 = False
    wave_3 = False
    wave_4 = False
    wave_5 = False
    boss_wave = False   
    end_game_counter = 0
    boss_attack_pattern = 1
    attack_pattern_length = 1    
    bonus = 0
    count = 0
    gameover = 0


        # L - Loop
    while keepGoing:
 
        # T - Timer to set frame rate
        clock.tick(30)
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            #if event.type == pygame.KEYDOWN:
        
        #To control the speed at which the player shoots
        if player_shoot:
            start_ticks_shoot = pygame.time.get_ticks()
            player_shoot = False
        #shoots a bullet every 0.3 seconds
        if (pygame.time.get_ticks() - start_ticks_shoot)/100 > 3:
            good_bullet = Sprites.Good_Bullet(player.get_top())    
            good_bullet_group.add(good_bullet)
            allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
            shoot.play()
            player_shoot = True
        
        if wave_1:
            #To control the speed the enemies spawn
            if enemy_appear:
                start_ticks_enemy = pygame.time.get_ticks()
                enemy_appear = False
            #sends an enemy out every 0.5 seconds
            if (pygame.time.get_ticks() - start_ticks_enemy)/100 > 5:
                enemy = Sprites.Enemy((-50, 50), 5, 4)
                enemy_group.add(enemy)
                allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
                enemy_appear = True
                count += 1
                #After 8 enemies, it goes on to the next wave
                if count == 8:
                    count = 0
                    wave_1 = False
                    wave_2 = True
                    x_center = 50
                    
        if wave_2:
            #To control the speed the enemies spawn
            if enemy_appear:
                start_ticks_enemy = pygame.time.get_ticks()
                enemy_appear = False
            #sends an enemy out every 0.5 seconds
            if (pygame.time.get_ticks() - start_ticks_enemy)/100 > 5:
                enemy = Sprites.Enemy((x_center, -200), 0, 8)
                enemy_group.add(enemy)
                allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
                enemy_appear = True
                count += 1
                x_center += 50
                #after 9 enemies, goes on to the next wave
                if count == 9:
                    count = 0
                    wave_2 = False
                    wave_3 = True
                    
        if wave_3:
            #To control the speed the enemies spawn
            if enemy_appear:
                start_ticks_enemy = pygame.time.get_ticks()
                enemy_appear = False
            #sends an enemy out every 0.8 seconds
            if (pygame.time.get_ticks() - start_ticks_enemy)/100 > 8:
                #will spawn 8 enemies
                if count < 8:
                    enemy = Sprites.Enemy((600, 80), -8, 0)
                    enemy_group.add(enemy)
                    allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
                enemy_appear = True
                count += 1
                #After 8 seconds, goes on to the next wave
                if count == 10:
                    count = 0
                    wave_3 = False
                    wave_4 = True
                    x_center = 35
                    y_center = -200
            #changes the movement of the enemies in this group        
            for enemy in enemy_group:
                if enemy.rect.left < 200:
                    enemy.change_move(0, 6)
                    
        if wave_4:
            #To control the speed the enemies spawn
            if enemy_appear:
                start_ticks_enemy = pygame.time.get_ticks()
                enemy_appear = False
            #sends an enemy out every 0.1 seconds
            if (pygame.time.get_ticks() - start_ticks_enemy)/100 > 1:
                #will spawn 9 enemies
                if count < 9:
                    enemy = Sprites.Enemy((x_center, y_center), 0, 4)
                    enemy_group.add(enemy)
                    allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
                enemy_appear = True
                count += 1
                x_center += 51
                y_center += 26
                #Will go to the next wave after 30 counts
                if count == 30:
                    count = 0
                    wave_4 = False
                    wave_5 = True
                    x_center = 35
                    y_center = -300
                    y_change = 100
                    
        if wave_5:
            #To control the speed the enemies spawn
            if enemy_appear:
                start_ticks_enemy = pygame.time.get_ticks()
                enemy_appear = False
            #sends an enemy out every 0.05 seconds
            if (pygame.time.get_ticks() - start_ticks_enemy)/10 > 5:
                #Will spawn 9 enemies
                if count < 9:
                    enemy = Sprites.Enemy((x_center, y_center), 0, 4)
                    enemy_group.add(enemy)
                    allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
                enemy_appear = True
                count += 1
                x_center += 51
                y_center += y_change
                y_change = -y_change
                #After 75 counts, it will go on to the next wave
                if count == 75:
                    count = 0
                    wave_5 = False
                    boss_wave = True        
            
        #To make the boss show up        
        if boss_wave and boss_appear:
            player.change_boundary()
            boss_ship.start_move()
            boss_appear = False
            boss_health_appear = True
            #changes the music to the boss battle music
            pygame.mixer.music.load('Fast Ace.wav')
            pygame.mixer.music.set_volume(0.2)            
            pygame.mixer.music.play(-1)
            
        
        #Creates the boss' health bar and adds it to the health group    
        if boss_ship.check_move() == 0 and boss_health_appear:
            border.boss_health(screen)
            boss_health = Sprites.Boss_Health(screen)
            health.add(boss_health)
            allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
            boss_health_appear = False
            
        #For when the boss shows up
        
        #Changing attack patterns
        if change_attack_pattern:
            start_ticks_change_pattern = pygame.time.get_ticks()
            change_attack_pattern = False
        #Each attack pattern has a different time length
        if (pygame.time.get_ticks() - start_ticks_change_pattern)/1000 > attack_pattern_length:
            if boss_attack_pattern == 1:
                boss_attack_pattern = 2
                attack_pattern_length = 7
            elif boss_attack_pattern == 2:
                boss_attack_pattern = 3
                boss_laser = True
                attack_pattern_length = 5
            else:
                boss_attack_pattern = 1
                attack_pattern_length = 4
            change_attack_pattern = True 

        #Attack pattern 1
        if boss_attack_pattern == 1 and not boss_appear and boss_ship.check_move() == 0:
            if boss_shoot:
                start_ticks_boss_shoot = pygame.time.get_ticks()
                boss_shoot = False
            #Every 0.9 seconds, it will spawn 8 bullets in certain positions
            if (pygame.time.get_ticks() - start_ticks_boss_shoot)/100 > 9:            
                bad_bullet1 = Sprites.Bad_Bullet((boss_ship.rect.centerx+10, boss_ship.rect.bottom - 5))
                bad_bullet2 = Sprites.Bad_Bullet((boss_ship.rect.centerx-10, boss_ship.rect.bottom - 5))
                bad_bullet3 = Sprites.Bad_Bullet((boss_ship.rect.centerx+19, boss_ship.rect.bottom - 5))
                bad_bullet4 = Sprites.Bad_Bullet((boss_ship.rect.centerx-19, boss_ship.rect.bottom - 5))                
                bad_bullet5 = Sprites.Bad_Bullet((screen.get_width() - 66, boss_ship.rect.bottom - 60))
                bad_bullet6 = Sprites.Bad_Bullet((66, boss_ship.rect.bottom - 60))
                bad_bullet7 = Sprites.Bad_Bullet((screen.get_width() - 54, boss_ship.rect.bottom - 60))
                bad_bullet8 = Sprites.Bad_Bullet((54, boss_ship.rect.bottom - 60))                 
                bad_bullet_group.add(bad_bullet1, bad_bullet2, bad_bullet3, bad_bullet4, bad_bullet5, bad_bullet6, bad_bullet7, bad_bullet8)
                #recreating the spritegroup
                allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
                boss_shoot = True
        
        #Attack pattern 2        
        if boss_attack_pattern == 2 and not boss_appear and boss_ship.check_move() == 0:
            if boss_shoot:
                start_ticks_boss_shoot = pygame.time.get_ticks()
                boss_shoot = False
            if (pygame.time.get_ticks() - start_ticks_boss_shoot)/100 > 8:
                #Every 0.8 seconds, it spawns many bullets at slightly different positions
                for y in range(3, 7):
                    for x in range(-3, 4):
                        round_bullet1 = Sprites.Round_Bullet((boss_ship.rect.centerx + random.randrange(-50, 50), boss_ship.rect.bottom + random.randrange(-30, 50)), x*2, y)
                        bad_bullet_group.add(round_bullet1)
                #recreating the spritegroup
                allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
                boss_shoot = True
                
        #Attack Pattern 3
        if boss_attack_pattern == 3 and not boss_appear and boss_ship.check_move() == 0:
            if boss_laser == True:
                #Creates 2 lasers and adds them to the laser group
                laser1 = Sprites.Laser((117, 370))
                laser2 = Sprites.Laser((363, 370))
                laser_group.add(laser1, laser2)
                #recreating the spritegroup
                allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health) 
                boss_laser = False  
        
        #checks for boss and good bullet collision
        if not boss_appear and boss_ship.check_move() == 0:
            if pygame.sprite.spritecollide(boss_ship, good_bullet_group, False):
                for bullet in good_bullet_group:
                    if boss_ship.rect.colliderect(bullet):
                        bullet.hit_boss()
                        boss_health.lose_health(1)
                        #Every quarter of the boss health, it will spawn a powerup
                        if boss_health.get_health() % 500 == 0 and boss_health.get_health()>0:
                            heal = Sprites.Heal((random.randrange(80, 400), boss_ship.rect.bottom))
                            powerups.add(heal)
                #Increasing the bonus score
                bonus += 1
                score.increase_score(bonus - 250)
      
        #Collision between player and bad bullets            
        if pygame.sprite.spritecollide(player, bad_bullet_group, False):
            for bullet in bad_bullet_group:
                if player.rect.colliderect(bullet):
                    #Will check if the bullets hit the top left and right corners of the player sprite
                    if not bullet.rect.collidepoint(player.rect.topleft) and\
                       not bullet.rect.collidepoint(player.rect.topright):
                        #This will hide the sprite offscreen and kill it
                        bullet.hide()
                        bullet.kill()
                        player_health.lose_health(15)
                        #resets the bonus score
                        bonus = 0
         
        #Checks if the boss is dead               
        if not boss_appear and boss_ship.check_move() == 0 and boss_health.get_health() == 0:
            #Explosions spawned within the boss area
            for explode in range(15):
                explosion = Sprites.Explosion((random.randrange(boss_ship.rect.left, boss_ship.rect.right),\
                                               random.randrange(boss_ship.rect.top, boss_ship.rect.bottom)))
                explosion_group.add(explosion)
                boom.play()
            #recreating the sprite group
            allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
            #Kills all projectiles onscreen
            for bullet in bad_bullet_group:
                bullet.kill()
            for laser in laser_group:
                laser.kill()
            for bullet in good_bullet_group:
                bullet.kill()
            end_game_counter += 1
            #changes gameover to 1 and will show a victory screen
            gameover = 1
            
        #Checks if the player is dead    
        if player_health.get_health() == 0: 
            player_move = False
            #explosions spawned within the player area
            for explode in range(1):
                boom.play()
                explosion = Sprites.Explosion((random.randrange(player.rect.left, player.rect.right),\
                                                   random.randrange(player.rect.top, player.rect.bottom)))
                explosion_group.add(explosion)
            #recreating the sprite group
            allSprites = pygame.sprite.OrderedUpdates(background2, good_bullet_group, laser_group, bad_bullet_group, boss_ship, powerups, enemy_group, player, explosion_group, border, score, health)
            for bullet in bad_bullet_group:
                    bullet.kill()
            for laser in laser_group:
                laser.kill()
            for bullet in good_bullet_group:
                bullet.kill()
            end_game_counter += 1 
            #changes gameover to 2 which will display a defeat screen
            gameover = 2
        
        #lets the explosions play for a while, before exitting the loop        
        if end_game_counter == 100:
            keepGoing = False            
                
            
        #collision between player and lasers
        if pygame.sprite.spritecollide(player, laser_group, False):
            for laser in laser_group:
                if player.rect.colliderect(laser) and laser.final_form():                   
                    player_health.lose_health(3)
                    bonus = 0

        #Detects collision between the good bullets and the enemies
        if pygame.sprite.groupcollide(good_bullet_group, enemy_group, False, False):
            for enemy in enemy_group:
                for bullet in good_bullet_group:
                    if bullet.rect.colliderect(enemy):
                        boom.play()
                        #gets the current center before hiding it to be used later
                        center = enemy.get_center()
                        #This will hide the sprite offscreen and kill it
                        enemy.hide()
                        enemy.kill()
                        # 5% chance to spawn a heal
                        if random.randrange(20) == 0:
                            heal = Sprites.Heal(center)
                            powerups.add(heal)
                        explosion = Sprites.Explosion(center)
                        explosion_group.add(explosion)
                        bullet.hide()
                        bullet.kill()
                        #increases the score and bonus
                        score.increase_score(100 + bonus)
                        bonus += 10
                        
        
        #Detects collision between the player and enemies                
        if pygame.sprite.spritecollide(player, enemy_group, False):
            for enemy in enemy_group:
                if enemy.rect.colliderect(player):
                    boom.play()
                    center = enemy.get_center()
                    #This will hide the sprite offscreen and kill it
                    enemy.hide()
                    enemy.kill()
                    #spawns an explosion
                    explosion = Sprites.Explosion(center)
                    explosion_group.add(explosion)                    
                    player_health.lose_health(30)
                    score.increase_score(100)
        
        #Detects collision betwen the player and the powerup            
        if pygame.sprite.spritecollide(player, powerups, False):
            for powerup in powerups:
                if powerup.rect.colliderect(player): 
                    player_health.heal_health()
                    powerup.kill()
        
        #Checks if the enemies fly off the screen without being killed
        #If they are alive, then the score is decreased and bonus is reset
        for enemy in enemy_group:
            if enemy.getx() > 0 and enemy.rect.left > screen.get_width():
                enemy.hide()
                bonus = 0
                score.decrease_score(50)
            if enemy.getx() < 0 and enemy.rect.right < 0:
                enemy.hide()
                bonus = 0
                score.decrease_score(50)
            if enemy.rect.top > screen.get_height():
                enemy.hide()
                bonus = 0
                score.decrease_score(50)
                
        #Takes the keys that the user presses and moves the player sprite
        if player_move:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]: player.changey(0, screen)
            if keys[pygame.K_DOWN]: player.changey(1, screen)
            if keys[pygame.K_RIGHT]: player.changex(1, screen)
            if keys[pygame.K_LEFT]: player.changex(0, screen)
           
        # R - Refresh display
        allSprites.clear(screen, background)
        allSprites.update(screen)
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    #shows a victory screen
    if gameover == 1:
        victory = pygame.image.load('victory.png')
        screen.blit(victory, (-100, 0))
        pygame.display.flip()
    #shows a defeat screen
    if gameover == 2:
        defeat = pygame.image.load('defeat.png')
        screen.blit(defeat, (30, 80))
        pygame.display.flip()        
    
    #delays the game for 2 seconds, before exitting
    pygame.time.delay(2000)    
    # exits function, back into main() 
    return 

def main():
    '''Controls the different game pages'''
    # hide the mouse pointer
    pygame.mouse.set_visible(False)
    
    option = 0
    while option == 0:
        option = menu()
        if option == 1:
            #after the game ends, option will still be 1, so the loop will end
            game()
        if option == 2:
            #help will return 0 so the menu loop will continue
            option = help()
            
    # Unhide the mouse pointer
    pygame.mouse.set_visible(True)
    #quits main        
    pygame.quit()
    
main()