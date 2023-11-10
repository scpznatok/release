import pygame, time,json
from pygame import image, transform, sprite, font, time, mixer 
import pygame.time as ticks
from random import randint

pygame.init()
mixer.init() 
font.init() 

window_width = 800
window_height = 1000 
window = pygame.display.set_mode((window_width, window_height)) 
pygame.display.set_caption("Spaceship war") 
logo1 = image.load("images/logo.png")
pygame.display.set_icon(logo1)



menu_background = transform.scale(image.load("images/menu_background.png"), (window_width, window_height))
menu_background_learn = transform.scale(image.load("images/menu_background_learn.png"), (window_width, window_height))
menu_learn = transform.scale(image.load("images/learn_m.png"), (window_width, window_height))
lose_menu = transform.scale(image.load("images/menu_lose.png"), (800,800))
menu_logo = transform.scale(image.load("images/logo.png"), (400, 400))
settings_background = transform.scale(image.load("images/settings.png"), (window_width, window_height))
loading_background = transform.scale(image.load("images/loading_background.png"), (window_height, window_height))

start_img = image.load("images/buttons/start_button.png")
start_img_hover = image.load("images/buttons/start_button_hover.png")
settings_img = image.load("images/buttons/settings_button.png")
settings_img_hover = image.load("images/buttons/settings_button_hover.png")
exit_img = image.load("images/buttons/exit_button.png")
exit_img_hover = image.load("images/buttons/exit_button_hover.png")
back_img = transform.scale(image.load("images/buttons/back_button.png"), (360, 85)) 
back_img_hover = transform.scale(image.load("images/buttons/back_button_hover.png"), (360, 85)) 
off_img = transform.scale(image.load("images/buttons/off_button.png"), (100, 100))
off_img_hover = transform.scale(image.load("images/buttons/off_button_hover.png"), (100, 100))
on_img = transform.scale(image.load("images/buttons/on_button.png"), (100, 100)) 
on_img_hover = transform.scale(image.load("images/buttons/on_button_hover.png"), (100, 100))
restart_img = transform.scale(image.load("images/buttons/restart_button.png"), (200, 55)) 
restart_img_hover = transform.scale(image.load("images/buttons/restart_button_hover.png"), (200, 55)) 
menu_img = transform.scale(image.load("images/buttons/menu_button.png"), (200, 55)) 
menu_img_hover = transform.scale(image.load("images/buttons/menu_button_hover.png"), (200, 55)) 
learn_img = image.load("images/buttons/learn_button.png")
learn_img_hover = image.load("images/buttons/learn_button_hover.png")

explosin_fx = pygame.mixer.Sound('sound/exp.wav')
explosin_fx.set_volume(0.05)
shoot_fx = pygame.mixer.Sound('sound/shoot.wav')
shoot_fx.set_volume(0.1)
powerUP = pygame.mixer.Sound('sound/powerUp.wav')
powerUP.set_volume(0.1)
click_fx = pygame.mixer.Sound('sound/click.wav')
click_fx.set_volume(0.1)


with open('data/music.json') as file:
    data = json.load(file)
with open('data/learn.json') as file:
    learn = json.load(file)
    print(learn)

mixer.music.load('sound/bg.ogg') 
pygame.mixer.music.set_volume(0.01) 
if data == "True": 
    mixer.music.play()
    music_bg_data = True
else:            
    music_bg_data = False



main = True
game = False
menu = False
settings = False
loading =True
lose = False
last_fuel=0

class Button():
    def __init__(self, x, y, image, image_hover):
        self.image_original = image
        self.image_hover = image_hover
        self.rect = self.image_original.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False 
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
                click_fx.play()
            self.image = self.image_hover
        else:
            self.image = self.image_original 

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        window.blit(self.image, self.rect)

        return action

class Player(sprite.Sprite):
    def __init__(self, player_x, player_y, player_speed):
        
        super().__init__()
        self.player_image = transform.scale(image.load("images/player/spaceship.png"), (280, 300))
        self.anim_img = []
        self.min_rect = 5
        self.max_rect = 510
        self.min_rect_y = 500
        self.max_rect_y = 750
        self.anim =1
        self.index=0
        self.ammo = 10
        self.last_shot_time = 0 
        self.reset_time = 0
        self.shoot_delay = 400
        self.health = 100
        self.current_time = ticks.get_ticks() 
        self.image = self.player_image
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.fuel = 1600
        # for num in range(1, 6):
        #     imgs = transform.scale(image.load(f'images/player/plane_{num}.png'), (180, 200))
        #     self.anim_img.append(imgs)

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        global lose, lose_text
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.rect.x > self.min_rect:
            self.rect.x -= self.speed-4
        if keys[pygame.K_d] and self.rect.x < self.max_rect: 
            self.rect.x += self.speed-4
        if keys[pygame.K_w] and self.rect.y > self.min_rect_y:
            self.rect.y -= self.speed-5
        if keys[pygame.K_s] and self.rect.y < self.max_rect_y:
            self.rect.y += self.speed-6.5
        # if self.anim ==1:
        #     self.index+=1
        #     if self.index >=0:
        #         self.image = self.anim_img[0]
        #     if self.index >=8:
        #         self.image = self.anim_img[1]
        #     if self.index >=16:
        #         self.image = self.anim_img[2]
        #     if self.index >=24:
        #         self.image = self.anim_img[3]
        #     if self.index >=32:
        #         self.image = self.anim_img[4]
        #     if self.index >=40:
        #         self.index = 0
        
        if self.health <= 0 and not lose: 
            self.kill()
            lose = True
            lose_text = "Схоже що вас знищили"
        self.fuel -= 1
        if self.fuel <= 0:
            self.kill()
            lose = True
            lose_text = "У вас закінчився заряд"


    def shoot(self):
        self.current_time = ticks.get_ticks() 
        if self.current_time - self.last_shot_time >= self.shoot_delay:
            if self.ammo > 0:
                self.ammo -= 1
                self.last_shot_time = self.current_time
                bullet = Bullet(player.rect.x + 135, player.rect.y-24,1)
                bullet_group.add(bullet)
                if not lose:
                    shoot_fx.play()
                
                

class Enemy(sprite.Sprite):
    def __init__(self, enemy_x, enemy_y, enemy_speed,enemy_type,direction):
        
        super().__init__()
        self.enemy_image = transform.scale(image.load(f"images/enemies/enemy_{enemy_type}.png"), (280, 300))
        self.enemy_broken_image = transform.scale(image.load(f"images/enemies/broken/enemy_{enemy_type}.png"), (280, 300))
        self.anim_img = []
        self.anim =1
        self.index=0
        self.direction = direction
        self.current_time = ticks.get_ticks() 
        self.image = self.enemy_image
        self.speed = enemy_speed
        self.rect = self.image.get_rect()
        self.rect.x = enemy_x
        self.rect.y = enemy_y
        self.image = self.enemy_image
        self.last_shot_time = ticks.get_ticks()
        if enemy_type == 1:
            self.hp = 150
            self.shoot_delay = 1500
        elif enemy_type == 2:
            self.shoot_delay = 1000
            self.hp = 80
        elif enemy_type == 3:
            self.shoot_delay = 2000
            self.hp = 200
        # for num in range(1, 6):
        #     imgs = transform.scale(image.load(f'images/player/plane_{num}.png'), (180, 200))
        #     self.anim_img.append(imgs)


    def update(self):
        global enemy_skipped
        if self.hp <=50:
            self.image = self.enemy_broken_image
        self.rect.y += self.speed
        if self.hp <= 0:
            self.kill()
        if self.rect.y >= 1000:
            self.kill()
            enemy_skipped +=1
        hit_player = pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask)
        if hit_player:
            player.health -= 30
            explosion = Explosion(self.rect.x, self.rect.y+100, 200,200)
            explosion_group.add(explosion)
            explosin_fx.play()
            self.kill()
        self.current_time = ticks.get_ticks() 
        if self.current_time - self.last_shot_time >= self.shoot_delay:
            self.shoot()
            self.last_shot_time = self.current_time
        self.rect.x +=self.direction
        if self.rect.x >= 520 or self.rect.x <= 0:
            self.direction = self.direction * -1
            
    def shoot(self):
        bullet = Bullet(self.rect.x + 137, self.rect.y + 300, 2)
        bullet_group.add(bullet)
            
            

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_cor, y_cor, bullet_type):
        
        super().__init__()
        self.image = transform.scale(image.load("images/player/bullet.png"),(10,25)).convert_alpha()
        self.image_r = transform.rotate(self.image,180)
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = x_cor
        self.rect.y = y_cor
        self.bullet_type = bullet_type

    def update(self):
        if self.bullet_type == 1:
            hit_enemies = pygame.sprite.spritecollide(self, enemy_group, False, pygame.sprite.collide_mask)
            for enemy in hit_enemies:
                self.kill()
                enemy.hp -= 50
                if enemy.hp >= 1:
                    explosion = Explosion(self.rect.x, self.rect.y-80, 100, 100)
                    explosion_group.add(explosion)
                    explosin_fx.play()
                elif enemy.hp <=0:
                    explosion = Explosion(self.rect.x-100, self.rect.y-200, 200,200)
                    explosion_group.add(explosion)
                    explosin_fx.play()
                    if randint(1,100) <= 20:
                        buff = Buff(self.rect.x - 100, self.rect.y - 200, randint(1,3))
                        buff_group.add(buff)
            self.rect.y -= 4

                        
                    


        elif self.bullet_type == 2:
            self.image = self.image_r
            self.rect.y += 4
        if self.rect.y < -10 or self.rect.y >= 1010:
            self.kill()
        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            explosion = Explosion(self.rect.x-100, self.rect.y-100, 200,200)
            explosion_group.add(explosion)
            explosin_fx.play()
            player.health -=20
            self.kill()
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self, exp_x, exp_y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 5):
            img = transform.scale(image.load(f"images/explosion/exp{num}.png"), (width, height))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = exp_x
        self.rect.y = exp_y
        self.counter = 0

    def update(self):
        explosion_speed = 4
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


class Buff(pygame.sprite.Sprite):
    def __init__(self, x, y, buff_type):
        super().__init__()
        self.buff_type = buff_type
        self.image = transform.scale(image.load(f"images/buffs/buff_{buff_type}.png"), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global ttime, third_collected
        self.rect.y += 3
        players = pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask)
        
        for player in players:
            if self.buff_type == 1:
                player.ammo = 20
            elif self.buff_type == 2:
                player.health = 100
            elif self.buff_type == 3: 
                player.shoot_delay = 250
                ttime = ticks.get_ticks()
                third_collected = True
            powerUP.play()
            self.kill()
        if self.rect.y >= 1000:
            self.kill()
        if self.buff_type == 0:
            if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
                player.fuel = 1600
                self.kill()         

            
class HealthBar():
    def __init__(self, x, y, h, w, health, type, fuel):
        self.image = image.load(f"images/healthbar{type}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x-63
        self.rect.y = y-14
        self.health = health
        self.max_hp = health
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.type = type
        self.fuel = fuel
        self.max_fuel = fuel
    def update(self, surface, health, fuel):
        if self.type == 1:
            self.health = health
            r = self.health / self.max_hp
            pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
            pygame.draw.rect(surface, "green", (self.x, self.y, self.w * r, self.h))
            window.blit(self.image, (self.rect.x, self.rect.y))
        elif self.type == 2:
            self.fuel = fuel
            r = self.fuel / self.max_fuel
            pygame.draw.rect(surface, "pink", (self.x, self.y, self.w, self.h))
            pygame.draw.rect(surface, "purple", (self.x, self.y, self.w * r, self.h))
            window.blit(self.image, (self.rect.x, self.rect.y))


def reset_game():
    global game, lose, player, enemy_group, bullet_group, explosion_group, buff_group, player_group, last_fuel, enemy_skipped
    game = True
    lose = False
    enemy_group.empty()
    bullet_group.empty()
    explosion_group.empty()
    buff_group.empty()
    player_group.empty()
    player = Player(50, 600, 7)
    player_group.add(player)
    enemy_skipped = 0
    last_fuel = 0





class Background():
    def __init__(self, bg_x, bg_y):
        self.img = image.load("images/bg.png")
        self.rect = self.img.get_rect()
        self.rect.x = bg_x
        self.rect.y = bg_y

    
    def reset(self):
        window.blit(self.img, (self.rect.x, self.rect.y))
    
    def update(self):
        if self.rect.y >= 1000:
            self.rect.y = -1000
        self.rect.y += 1
        

text = font.Font("fonts/segoeprb.ttf", 25)
text1 = font.Font("fonts/segoeprb.ttf", 45)


player = Player(50, 600, 7)
player_group = pygame.sprite.Group()
player_group.add(player)
healthbar = HealthBar(70,30, 20, 200, 100,1,None)
fuelbar = HealthBar(61,95, 20, 200, None,2,1600)


bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
buff_group = pygame.sprite.Group()
fuel_group = pygame.sprite.Group()


bg1 = Background(0,0)
bg2 = Background(0,-1000)


start_button = Button(300, 583, start_img, start_img_hover) 
settings_button = Button(300, 662, settings_img, settings_img_hover) 
exit_button = Button(297, 740, exit_img, exit_img_hover)
back_button = Button(220, 700, back_img, back_img_hover)
on_button = Button(375,500, on_img, on_img_hover)
off_button = Button(375,500, off_img, off_img_hover)
restart_button = Button(115,790, restart_img, restart_img_hover)
menu_button = Button(485,790, menu_img, menu_img_hover)
learn_button = Button(190,895, learn_img, learn_img_hover)


third_collected = False
ttime = 0
enemy_skipped = 0
lose_text = None

clock = pygame.time.Clock()
FPS = 60




while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False
        if game:
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot()
    if loading:
        window.blit(loading_background, (-0, 0)) 
        loading = False
        menu = True
        
    if menu: 
        if learn == "False":
            if start_button.draw():
                menu = False
                game = True
            if settings_button.draw():
                menu = False
                settings = True
                game = False
            can_click_exit = True
            
            if exit_button.draw() and can_click_exit == True: 
                main = False

            window.blit(menu_background, (0, 0)) 
            start_button.draw() 
            settings_button.draw()
            exit_button.draw()
        elif learn == "True":
            if learn_button.draw():
                learn = "False"
                with open('data/learn.json', 'w') as file:
                    json.dump("False", file)
            window.blit(menu_background_learn, (0, 0)) 
            window.blit(menu_learn, (0, 0)) 
            learn_button.draw()
    
    if settings:
        
        window.blit(settings_background, (0, 0))
        if back_button.draw():
            menu = True
            settings = False
            game = False
            can_click_exit = False
            pygame.time.delay(100)
        if music_bg_data:
            if on_button.draw():
                pygame.time.delay(100)
                mixer.music.stop()
                music_bg_data = False
                with open('data/music.json', 'w') as file:
                    json.dump("False", file)
        else:    
            if off_button.draw():
                pygame.time.delay(100)
                mixer.music.play()
                music_bg_data = True
                with open('data/music.json', 'w') as file:
                    json.dump("True", file)
    if game:
        if not lose:
            bg1.reset()
            bg2.reset()
            bg1.update()
            bg2.update()
            player_group.draw(window)
            player_group.update()
            bullet_group.draw(window)
            bullet_group.update()
            enemy_group.draw(window)
            enemy_group.update()
            explosion_group.draw(window)
            explosion_group.update()
            buff_group.draw(window)
            buff_group.update()
            healthbar.update(window, player.health,player.fuel)
            fuelbar.update(window, player.health,player.fuel)
            current_time = ticks.get_ticks()
            if player.ammo == 0:
                player.reset_time = ticks.get_ticks()
                player.ammo = -1
            if  player.ammo == -1 and ticks.get_ticks()-player.reset_time >=3000:
                    player.ammo = 10

            if player.ammo >0:
                press_btn_txt1 = text.render(str("ammo: "), True, (0, 0, 0), (255, 255, 255))
                window.blit(press_btn_txt1, (20, 600))
                press_btn_txt = text.render(str(player.ammo), True, (0, 0, 0), (255, 255, 255))
                window.blit(press_btn_txt, (110, 600))
            elif player.ammo <0:
                press_btn_txt1 = text.render(str("ammo: "), True, (0, 0, 0), (255, 255, 255))
                window.blit(press_btn_txt1, (20, 600))
                press_btn_txt = text.render(str("reloading"), True, (0, 0, 0), (255, 255, 255))
                window.blit(press_btn_txt, (110, 600))
            if len(enemy_group) <1:
                enemy_type = randint(1,100)
                if enemy_type>=61:
                    enemy_type = 3
                elif enemy_type>=30 and enemy_type<=60:
                    enemy_type = 2
                else:
                    enemy_type = 1
                direction_rand = randint(1,2)
                if direction_rand ==2:
                    direction_rand = -1
                enemy = Enemy(randint(5, 519), -300, 2.22, enemy_type,direction_rand)
                enemy_group.add(enemy)
            if current_time - ttime >= 10000 and third_collected:
                player.shoot_delay = 400
                third_collected = False
                
            if ticks.get_ticks() - last_fuel >= 12000:
                buff = Buff(randint(50, window_width-50), -50, 0)
                buff_group.add(buff)
                last_fuel = ticks.get_ticks()
            if enemy_skipped >= 3:
                lose = True
                lose_text = "Ви пропустили 3 ворогів"
        
        else:
            window.blit(lose_menu, (0, 100))
            if restart_button.draw():
                reset_game()
                
                
            if menu_button.draw():
                reset_game() 
                menu = True
                game = False
                
            press_btn_txt1 = text1.render(lose_text, True, (255, 255, 255))
            window.blit(press_btn_txt1, (105, 165))

    
    
    pygame.display.update()
    clock.tick(FPS)