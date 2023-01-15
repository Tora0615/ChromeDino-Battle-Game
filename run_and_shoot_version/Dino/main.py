import pygame
import os
import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.dino_shoot = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    #看輸入啥做對應動作
    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_shoot:
            self.shoot()

        if self.step_index >= 10:
            self.step_index = 0
        
        #跳
        if userInput[pygame.K_w] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        #蹲
        elif userInput[pygame.K_s] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        #射擊
        elif userInput[pygame.K_j] and self.dino_shoot != True:
            self.dino_shoot = True
        # 在平地回復預設
        elif not (self.dino_jump or userInput[pygame.K_s]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
            self.dino_shoot = False 
        #在天空中射擊回復預設
        else:
            self.dino_shoot = False  #
        

    def duck(self):
        self.image = self.duck_img[self.step_index // 5] #//表整數除法
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        
    def shoot(self):
        bullet = Bullet(self.dino_rect.x + (0.6 * self.dino_rect.size[0] * 1), self.dino_rect.centery, 1)
        bullet_group.add(bullet)



# 背景的雲
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))



# 障礙物基本Class
class Obstacle():
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)



# 以下三個繼承Obstacle 並更改內容
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle, pygame.sprite.Sprite): #多重繼承 pygame.sprite
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self) # pygame.sprite init (必須)
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 270
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1
        
    def update(self):
        super().update()
        if pygame.sprite.spritecollide(self, bullet_group, False):  #子彈與鳥碰撞檢測
            #print('here') OK (有進來)
            self.kill()
            obstacles.pop() #必要
            # --------------------
            # 你可能已經用 self.kill() 殺死了他，但在你的 update() 方法中重新設置了他，而沒有在你的代碼中註意到它。當您首先在代碼中使用 self.kill() 而不使用 return 時，通常會發生這種情況。如果你的代碼的其餘部分有一個部分在某些條件下重新設置他（並且確實適用），你的他將永遠不會死
        


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = pygame.image.load('Assets/Other/bullet.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self):
		#move bullet
		self.rect.x += (self.direction * self.speed)
		#check if bullet has gone off screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()



death_count = 0
#create sprite groups
bullet_group = pygame.sprite.Group()


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    
    
    
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
        
    
    

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        
        player.update(userInput)
        player.draw(SCREEN)
        #pygame.draw.rect(SCREEN,(0,0,0),player.dino_rect, 1) #繪製碰撞框

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        
        for obstacle in obstacles:
            # 先更新位置 -> 再繪製物件、碰撞框，才不會有看起來沒撞到但判定撞到的bug、以及碰撞框歪掉
            obstacle.update()  #更新位置
            obstacle.draw(SCREEN)  #繪出物件
            #pygame.draw.rect(SCREEN,(0,0,0),obstacle.rect, 1)  #繪製碰撞框
            # 撞到東西死亡，結束這個迴圈的while loop，就會回到menu的loop
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                global death_count
                death_count += 1
                obstacles = []
                global bullet_group
                bullet_group = pygame.sprite.Group()
                run = False 

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        bullet_group.update()
        bullet_group.draw(SCREEN)
    
        clock.tick(30)
        pygame.display.update()


def menu():
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        #看是不是最開始那局，畫面不同
        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #收到退出，結束loop
                run = False
            if event.type == pygame.KEYDOWN: #收到按下任何按紐，開始
                main()


menu()
pygame.quit() #結束pygame視窗