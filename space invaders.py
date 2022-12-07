import pygame
import os 
import random
import time
from pygame import mixer



pygame.font.init()
width=800
height=700
# spacepos=0

win=pygame.display.set_mode((width,height))
pygame.display.set_caption("space invaders")

Red_space_ship=pygame.image.load(os.path.join("assets","pixel_ship_red_small.png")).convert_alpha()
green_space_ship=pygame.image.load(os.path.join("assets","pixel_ship_green_small.png")).convert_alpha()
blue_space_ship=pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png")).convert_alpha()

yellow_space_ship=pygame.image.load(os.path.join("assets","pixel_ship_yellow.png")).convert_alpha()

#laser
red_laser=pygame.image.load(os.path.join("assets","pixel_laser_red.png")).convert_alpha()
green_laser=pygame.image.load(os.path.join("assets","pixel_laser_green.png")).convert_alpha()
blue_laser=pygame.image.load(os.path.join("assets","pixel_laser_blue.png")).convert_alpha()
yellow_laser=pygame.image.load(os.path.join("assets","pixel_laser_yellow.png")).convert_alpha()

#background
background=pygame.image.load(os.path.join("assets","background-black.png")).convert_alpha()
background=pygame.transform.rotozoom(background,0,2)
class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
        
    def move(self,vel):
        self.y+=vel
    def off_screen(self,height):
        return  not (self.y <height and self.y>=0)
    def collision(self,obj):
        return collide(self,obj)
    

class Ship:
    COOLDOWN=45
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_image=None
        self.laser_image=None
        self.lasers=[]
        self.cool_down_counter=0
    def cooldowm(self):
        if self.cool_down_counter >=self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter>0:
            self.cool_down_counter+=1
    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x,self.y,self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter=1


    def draw(self,window):
       
        win.blit(self.ship_image,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(win)
    def move_laser(self,vel,obj):
        self.cooldowm()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                 obj.health-+10
                 self.lasers.remove(laser)
    def get_width(self):
        return self.ship_image.get_width()
    def get_height(self):
        return self.ship_image.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x,y,health)
        self.ship_image=yellow_space_ship
        self.laser_image=yellow_laser
        self.mask=pygame.mask.from_surface(self.ship_image)
        self.max_health=health
    def move_laser(self,vel,objs):
        self.cooldowm()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:

                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:            
                            self.lasers.remove(laser)
    def draw(self,window):
        super().draw(window)
        self.healthbar(window)
    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y+self.ship_image.get_height()+10,self.ship_image.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y+self.ship_image.get_height()+10,self.ship_image.get_width()*(self.health/self.max_health),10))

class Enemy(Ship):
    Color_map={"red":(Red_space_ship,red_laser),
    "green":(green_space_ship,green_laser),
    "blue":(blue_space_ship,blue_laser)}
    def __init__(self, x, y,color, health=100): 
        super().__init__(x, y, health)
        
        self.ship_image,self.laser_image=self.Color_map[color]
        self.mask=pygame.mask.from_surface(self.ship_image)
    
    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x-10,self.y,self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter=1
    def move(self,vel):
        self.y+=vel

        
def collide(obj1,obj2):
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y))!=None



def main():
    run=True
    laser_val=6
    player=Player(350,630)
    fps=90
    clock=pygame.time.Clock()
    level=0
    lives=5
    player_vel=5
    enime_val=1
    main_font=pygame.font.SysFont("comicsans",40)
    lost_font=pygame.font.SysFont("comicsans",30)
    enmies=[]
    wave_length=5
    lost=False
    lost_count=0
  
    

    

    def redrow_win():
        # win.blit(background,(0,0))
        win.blit(background,(0,0))
        
        # draw text
        lives_label=main_font.render(f"lives : {lives}",1,(0,255,0))
        level_label=main_font.render(f"level : {level}",1,(0,255,0))
       
        win.blit(lives_label,(10,10))
        win.blit(level_label,(width-level_label.get_width()-10,10))
        for enemy in enmies:
            enemy.draw(win)
        player.draw(win)
        if lost==True:
            out_level=level
            lost_label=lost_font.render(f"you lost your ship !! On the level {out_level}",1,(155,255,0))
            win.blit(lost_label,(width/2-lost_label.get_width()/2,350))


        pygame.display.update()
      

    while run:
        clock.tick(fps)
        redrow_win()
        
        if lives <=0 or player.health<=0:
            lost=True
            lost_count+=1
        if lost:
            if lost_count>60*3:      
                run=False
    
            else:
                continue
        if len(enmies)==0:
            level+=1
            wave_length+=5
            for i in range(wave_length):
                enemy =Enemy(random.randrange(50,width-100),random.randrange(-1500,-100),random.choice(["red","blue","green"]))
                enmies.append(enemy)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
        
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x-player_vel>0:
            player.x-=player_vel
        if keys[pygame.K_d] and player.x+player_vel+100<width:
            player.x+=player_vel
        if keys[pygame.K_w] and player.y -player_vel> 0:
            player.y-=player_vel
        if keys[pygame.K_s] and player.y + player_vel+player.get_height()+15<height:
            player.y+=player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        for enemy in enmies:
            enemy.move(enime_val)
            enemy.move_laser(laser_val,player)
            if random.randrange(0,4*60)==1:
                enemy.shoot()
            if collide(enemy,player):
                player.health-=10
                enmies.remove(enemy)
            if enemy.y+enemy.get_height() >height:
                lives-=1
                enmies.remove(enemy)
        player.move_laser(-laser_val,enmies)

def main_menu():
    title_font=pygame.font.SysFont("comicsams",70)
    run=True
    while run:
        win.blit(background,(0,0))
        title_label=title_font.render( "press the mouse button to begin.. ",1,(0,255,0))
        win.blit(title_label,(width/2-title_label.get_width()/2,350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
main_menu()          







