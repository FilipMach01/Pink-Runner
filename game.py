import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks()/100) - start_time
    score_surf = test_font.render(f"Score: {current_time}",False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement (obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_index,player_surf

    if player_rect.bottom < 300:
        player_surf = player_jump     
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0       
        player_surf = player_walk[int(player_index)]


pygame.init()
# surfs
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("PINK RUNNER")
clock = pygame.time.Clock()
test_font = pygame.font.Font("graphic/Pixeltype.ttf",50)
game_active = False
start_time = 0
score = 0
if_not_pouse = True

test_surf = pygame.image.load('graphic/Sky.png').convert()
ground_surf = pygame.image.load('graphic/Ground.png').convert()


snail_frame_1 = pygame.image.load('graphic/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphic/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphic/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphic/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obtacle_rect_list = []

player_walk_1 = pygame.image.load('graphic/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphic/player_walk_2.png').convert_alpha()
player_walk =[player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphic/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_walk_1.get_rect(midbottom = (80,300))
player_gravity = 0

# intro screen
player_stand = pygame.image.load('graphic/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
palyer_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render("Pink Runner",None, (64,64,64))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render("Press space to srart",None, (64,64,64))
game_message_rect = game_message.get_rect(center = (400,330))

game_pouse_message = test_font.render("Press space to continue",None, (64,64,64))
game_pouse_message_rect = game_pouse_message.get_rect(center = (400,200))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom >= 300:               
                        player_gravity = -20
                        if_not_pouse = True
                                   

                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if_not_pouse = False
                    player_rect.midbottom = (80,300)
                    screen.blit(game_pouse_message,game_pouse_message_rect)
 
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True     
                start_time = int(pygame.time.get_ticks()/100)         
        if game_active:
            if event.type == obstacle_timer :
                if randint(0,2):
                    obtacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obtacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),210)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        if if_not_pouse == True:
    # render
            screen.blit(test_surf,(0,0))
            screen.blit(ground_surf,(0,300))
            # pygame.draw.rect(screen,"Pink",score_rect)
            # pygame.draw.rect(screen,"Pink",score_rect,10)
            
            # screen.blit(score_surf,score_rect)
            score = display_score()
            # obstacle movement
            obtacle_rect_list = obstacle_movement(obtacle_rect_list)
            
            # collision
            game_active = collisions(player_rect,obtacle_rect_list)
            # Player -----------------------
            player_gravity += 0.95
            player_rect.y += player_gravity 
            
        
            
            if player_rect.bottom >= 300:
                player_rect.bottom = 300
            player_animation()
            screen.blit(player_surf, player_rect)

            # collisions

            
    
    else:
        screen.fill((110, 83, 173))
        screen.blit(player_stand,palyer_stand_rect)
        obtacle_rect_list.clear()

        player_rect.midbottom = (80,300)
        

        score_message = test_font.render(f'Your score: {score}',False,(64,64,64))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)
        
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    
    
    
    pygame.display.update()
    clock.tick(60)
