# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 21:21:55 2021

@author: Arthur
"""
import os
import time

import web_api
    

    
temp = input('輸入數字加入或是創立房間(0加入 1創立) : ') 
if temp == '0':
    needToCreatNewRoom = False
    room_id = str(input('輸入房間id : '))
else:
    needToCreatNewRoom = True
    room_id = web_api.get_uuid()
    
username = input('輸入用戶名稱 : ') 
web_api.initroom(needToCreatNewRoom,room_id,username)

initdata = eval(web_api.getdata(room_id))


print('等待玩家加入',end = '')
while len(initdata) != 2:
    time.sleep(1)
    print('.',end = '')
    initdata = eval(web_api.getdata(room_id))
print('\n玩家已到齊 ! ')


player_id = player_name = username
temp = list(initdata.keys())
temp.remove(username)
enemy_name = temp[0]
    





print('遊戲初始化中...')

import pygame

pygame.init()

#define game variables
GRAVITY = 0.75

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('dino - ' + str(player_id)) #視窗文字

#load images
#bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define player action variables
moving_left = False
moving_right = False
shoot = False

#define colours
BG = (255,255,255)

def draw_bg():
    screen.fill(BG)



class Soldier(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, scale, speed):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		#self.ammo = ammo
		#self.start_ammo = ammo
		self.shoot_cooldown = 0
		#self.grenades = grenades
		self.health = 100
		self.max_health = self.health
		self.direction = 1
		self.vel_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		
		#load all images for the players
		animation_types = ['Idle', 'Run', 'Jump', 'Death']
		for animation in animation_types:
			#reset temporary list of images
			temp_list = []
			#count number of files in the folder
			num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)

		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


	def update(self):
		self.update_animation()
		self.check_alive()
		#update cooldown
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1


	def move(self, moving_left, moving_right):
		#reset movement variables
		dx = 0
		dy = 0

		#assign movement variables if moving left or right
		if moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		#jump
		if self.jump == True and self.in_air == False:
			self.vel_y = -11
			self.jump = False
			self.in_air = True

		#apply gravity
		self.vel_y += GRAVITY
		if self.vel_y > 10:
			self.vel_y
		dy += self.vel_y

		#check collision with floor
		if self.rect.bottom + dy > 300:
			dy = 300 - self.rect.bottom
			self.in_air = False

		#update rectangle position
		self.rect.x += dx
		self.rect.y += dy


	def shoot(self):
		if self.shoot_cooldown == 0 : #and self.ammo > 0:  #TODO ammo to mp
			self.shoot_cooldown = 20
			bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
			bullet_group.add(bullet)
			#reduce ammo
			#self.ammo -= 1


	def update_animation(self):
		#update animation
		ANIMATION_COOLDOWN = 100
		#update image depending on current frame
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out the reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0



	def update_action(self, new_action):
		#check if the new action is different to the previous one
		if new_action != self.action:
			self.action = new_action
			#update the animation settings
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()



	def check_alive(self):
		if self.health <= 0:
			self.health = 0
			self.speed = 0
			self.alive = False
			self.update_action(3)


	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self):
		#move bullet
		self.rect.x += (self.direction * self.speed)
		#check if bullet has gone off screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()

		#check collision with characters
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				player.health -= 5
				self.kill()
		if pygame.sprite.spritecollide(enemy, bullet_group, False):
			if enemy.alive:
				enemy.health -= 5
				self.kill()

#create sprite groups
bullet_group = pygame.sprite.Group()

#player = Soldier('player', 200, 200, 3, 5)
#enemy = Soldier('enemy', 400, 200, 3, 5)

if needToCreatNewRoom == True: #true -> 自己 = player -> 綠色那隻
    player = Soldier('player', 
                     int(initdata[player_name]['position_x']), 
                     int(initdata[player_name]['position_y']), 
                     3, 
                     5)
    enemy = Soldier('enemy', 
                    int(initdata[enemy_name]['position_x']), 
                    int(initdata[enemy_name]['position_y']), 
                    3, 
                    5)
else:
    player = Soldier('player', 
                     int(initdata[enemy_name]['position_x']), 
                     int(initdata[enemy_name]['position_y']), 
                     3, 
                     5)
    enemy = Soldier('enemy', 
                    int(initdata[player_name]['position_x']), 
                    int(initdata[player_name]['position_y']), 
                    3, 
                    5)




print('遊戲已啟動 ! ')

run = True
while run:
    
    clock.tick(FPS)

    draw_bg()

    player.update()
    player.draw()
    enemy.update()
    enemy.draw()

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)
    
    #--- new ---
    
    
    # 分目前誰是player1、2
    if needToCreatNewRoom == True:
        # 這是player (User01/room creater)
        hp = 100  #上傳要改
        mp = 100 
        
        if player.alive:
            if shoot:
                player.shoot()
            if player.in_air:
                player.update_action(2)#2: jump
            elif moving_left or moving_right:
                player.update_action(1)#1: run
            else:
                player.update_action(0)#0: idle
                
            # 自己移動
            player.move(moving_left, moving_right)
            # 上傳移動資料並隨後下載 #TODO API 更改上傳薪資料
        
        now_data = eval(web_api.updatedata(room_id,player_id,hp,mp,moving_left,moving_right))
            
        if enemy.alive:
            if shoot:
                enemy.shoot()
            if enemy.in_air:
                enemy.update_action(2)#2: jump
            elif eval(now_data[enemy_name]['move_left']) or eval(now_data[enemy_name]['move_right']):
                enemy.update_action(1)#1: run
            else:
                enemy.update_action(0)#0: idle
            # 根據下載資料移動對方
            enemy.move(eval(now_data[enemy_name]['move_left']),eval(now_data[enemy_name]['move_right']))
        
    else:
        # 這是enemy (User02/add)
        hp = 200 
        mp = 200 
        
        if enemy.alive:
            if shoot:
                enemy.shoot()
            if enemy.in_air:
                enemy.update_action(2)#2: jump
            elif moving_left or moving_right:
                enemy.update_action(1)#1: run
            else:
                enemy.update_action(0)#0: idle
                
            enemy.move(moving_left, moving_right)
            
        now_data = eval(web_api.updatedata(room_id,player_id,hp,mp,moving_left,moving_right))
            
        if player.alive:
            if shoot:
                player.shoot()
            if player.in_air:
                player.update_action(2)#2: jump
            elif eval(now_data[enemy_name]['move_left']) or eval(now_data[enemy_name]['move_right']):
                player.update_action(1)#1: run
            else:
                player.update_action(0)#0: idle
                
            player.move(eval(now_data[enemy_name]['move_left']),eval(now_data[enemy_name]['move_right']))
        
    
    #--- new ---
    
    
    	#update player actions
    
        
    
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
                
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_w and enemy.alive:
                enemy.jump = True
                
            if event.key == pygame.K_ESCAPE:
                run = False

        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            




    pygame.display.update()

pygame.quit()


#TODO 刪除 Room
print('遊戲結束。')