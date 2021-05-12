import pygame, sys, random    #1
  
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,600))
    screen.blit(floor_surface, (floor_x_pos + 500,600))

def create_pipe():  #13-6
    random_pipe_pos = random.choice(pipe_height) #14-1
    bottom_pipe = pipe_surface.get_rect(midtop = (520, random_pipe_pos)) #14-2
    top_pipe = pipe_surface.get_rect(midbottom = (520, random_pipe_pos - 200)) #14-3
    return bottom_pipe, top_pipe #14-4 returned as tuple (needs tuple unpacking at line 60)

def move_pipes(pipes):  #13-7
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# def draw_pipes(pipes): #13-8
#     for pipe in pipes:
#         screen.blit(pipe_surface, pipe)
def draw_pipes(pipes): #14-6
    for pipe in pipes:
        if pipe.bottom >= 700:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)    


def check_collisions(pipes):  #15 start
    for pipe in pipes:  #15-1
        if bird_rect.colliderect(pipe): #15-2
            return False     #15-3  go check collisions in while loop

    if bird_rect.top <= -100 or bird_rect.bottom >= 600: #15-4  (next create a new variable 'game active')
        return False

    return True 

def rotate_bird(bird): #16-2
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3,1)  #convert to alpha where bird image loaded
    return new_bird

def bird_animation():   #17-10
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
	return new_bird,new_bird_rect          

# def score_display():
#     score_surface = game_font.render(str(int(score)), True, (255,255,255)) #18-3 (True for antialianising)
#     score_rect = score_surface.get_rect(center = (250, 100)) #18-4
#     screen.blit(score_surface, score_rect) #18-5 (next call function in while loop)

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,350))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

def pipe_score_check():
    global score
    global can_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                can_score = False

pygame.init()  #2
screen = pygame.display.set_mode((500, 700)) #canvas size  #x=576, y=700  #3
clock = pygame.time.Clock() #frame rate   #7

game_font = pygame.font.Font('04B_19.ttf', 40) #18-2 (next above function score_display)


bg_surface = pygame.image.load('assets/back_ground.jpg').convert()  #convert for ease of pygame  #8
#pygame.transform.scale2x(bg_surface) scale to 2x
floor_surface = pygame.image.load('assets/floor.png').convert()
floor_x_pos = 0  #9  use it inplace of x


bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha()) #17
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha()) #17-1
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha()) #17-2
bird_frames = [bird_downflap,bird_midflap,bird_upflap] #17-3
bird_index = 0  #17-4
bird_surface = bird_frames[bird_index] #17-5
bird_rect = bird_surface.get_rect(center = (200, 300)) #17-6

BIRDFLAP = pygame.USEREVENT + 1  #17-7
pygame.time.set_timer(BIRDFLAP,200) #17-8  (next in while loop after extend)

# bird_surface = pygame.image.load('assets/bluebird.png').convert_alpha() #10
#bird_surface = pygame.transform.scale2x(bird_surface) #10-1 optional 
# bird_rect = bird_surface.get_rect(center = (200,300)) #10-2

pipe_surface = pygame.image.load('assets/pipe-green.png') #13-1
pipe_surface = pygame.transform.scale2x(pipe_surface) #13-1 optional
pipe_list = []  #13-2
spawn_pipe = pygame.USEREVENT  #13-3
pygame.time.set_timer(spawn_pipe, 1200)  #13-4

pipe_height = [240, 300, 350]   #14 start go above

#Game Variables #11 - 1
gravity = 0.30
bird_movement = 0
game_active = True #15-5

can_score = True
score = 0 #18
high_score = 0 #18-1 (next go up game_font)

while True:     #4
    for event in pygame.event.get():  #6
        if event.type == pygame.QUIT:   
            pygame.quit()
            sys.exit() #to exit file completely

        if event.type == pygame.KEYDOWN:  #12-1
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0    #12-3
                bird_movement -= 10  #12-2

            if event.key == pygame.K_SPACE and game_active == False:    #15-7 (also do game active above)
                game_active = True #15-8
                pipe_list.clear()
                bird_rect.center = (200,300)
                bird_movement = 0
                score = 0


        if event.type == spawn_pipe: #13-5
            # pipe_list.append(create_pipe())  #13-6 (line 8)
            pipe_list.extend(create_pipe()) #14-5  next change draw pipe function to flip pipes

        if event.type == BIRDFLAP: #17-9
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_surface,bird_rect = bird_animation()


    #surface
    screen.blit(bg_surface,(0,0)) #(0,0) => top left       #8
    
    if game_active:  #15-6
        #bird
        bird_movement += gravity     #11-2
        rotated_bird = rotate_bird(bird_surface) #16
        bird_rect.centery += bird_movement  #11-3
        # screen.blit(bird_surface, bird_rect)  #10-3
        screen.blit(rotated_bird, bird_rect)  #16-1
        game_active = check_collisions(pipe_list) #15-5
        
        #pipes
        pipe_list = move_pipes(pipe_list) #13-8 (line 12)
        draw_pipes(pipe_list) #13-9 (line 17)

        pipe_score_check() #updated new for scoring
        score_display('main_game')
        # score_sound_countdown -= 1
        # if score_sound_countdown <= 0:
        #     score_sound.play()
		# 	score_sound_countdown = 100
    else:
        # screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
        

    # floor_x_pos += 1 #move right
    floor_x_pos -= 3 #move left
    # screen.blit(floor_surface, (floor_x_pos,600)) #9  remove after putting in fucntion
    draw_floor()  #10 make function above

    

    #floor
    if floor_x_pos <= -500:  #10
        floor_x_pos = 0

    pygame.display.update()   #5
    clock.tick(90)  #top limit    #7