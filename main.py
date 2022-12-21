#main.py
from pygame import*
#python 3.6 (for home)
from random import*
from math import*
from sys import*
from os import*



#make screen appear in center--
environ["SDL_VIDEO_CENTERED"] = "1"
#images----------------------------------
#background image
backgroundImg = image.load("background_img.png")
backgroundImg = transform.scale(backgroundImg,(800,500))
#key image
keyImg = image.load("key_img.png")
keyImg = transform.scale(keyImg,(50,50))
#door image
doorImg = image.load("door_img.png")
doorImg = transform.scale(doorImg,(50,50))
#wall image
wallImg = image.load("wall_img.png")
wallImg = transform.scale(wallImg,(50,50))
#wallimg2
wallImg2 = image.load("wall2_img.png")
wallImg2 = transform.scale(wallImg2,(50,50))
#heart image (for life)
heartImg = image.load("heart_img.png")
heartImg = transform.scale(heartImg,(30,30))
#spike image (actually a poisonous mushroom)
spikeImg = image.load("spike_img.png")
spikeImg = transform.scale(spikeImg,(50,50))
#mute images
#not muted
muteOffImg = image.load("muteOff_img.png")
muteOffImg = transform.scale(muteOffImg,(30,30))
#is muted
muteOnImg = image.load("muteOn_img.png")
muteOnImg = transform.scale(muteOnImg,(30,30))
#finaly character
peachImg = image.load("peach_img.png")
peachImg = transform.scale(peachImg,(80,100))
bowserImg = image.load("bowser_img.png")
bowserImg = transform.scale(bowserImg,(80,100))

#main character---------not in use atm
def makePictures(name,start,end):
    #makes pictures for mario animation-------------
    pictures = []
    #loop around--- pastes a bunch of imgs in 2d list
    for i in range(start,end+1):
        pictures.append(image.load("%s/%s%03d.png"%(name,name,i)))
    #transforms them so it matches 75x75 img
    for i in range(len(pictures)):
        pictures[i] = transform.scale(pictures[i],(50,50))

    return pictures

#for main images
pics = []
pics.append(makePictures("Mario",19,24)) #left
pics.append(makePictures("Mario",1,6)) #right
#image...
L_UPimg = image.load("Mario/Mario023.png")
L_UPimg = transform.scale(L_UPimg,(50,50))
R_UPimg = image.load("Mario/Mario003.png")
R_UPimg = transform.scale(R_UPimg,(50,50))

#continue...
#[] around because it's a one thing in a 2d list
pics.append([L_UPimg]) #lEFT_UP
pics.append([R_UPimg]) #right up
#main character images end----------------------------



#end of images---------------------------------------



#placements/variables--------------------------------------------

#level start (level 1)
level = 1
#wall variable, hold placement of wear the blocks of walls are
walls = []
walls2 = []
#spike
spike = []
#screen stuff---
res = width,height = 800,500
screen = display.set_mode(res)
#life--
life = 3
#lives rects, 3 at corner, 30 by 30
lives = [Rect(660,10,30,30), Rect(710,10,30,30), Rect(760,10,30,30)]
#music
#repeat indefinetly
musicTime = -1
init()
#loads music
mixer.music.load("main_music.mp3")
#for repetition
mixer.music.play(musicTime)
#if they want to mute it
musicMuted = False
#top left corner, mute button
musicRect = Rect(10,10,30,30)
#placeholder
peachRect = Rect(400,350,80,100)
bowserRect = Rect(500,350,80,100)
#timer
counter,text = 0,"0".rjust(3)
#speed of timer, (goes by seconds)
time.set_timer(USEREVENT,1000)
font = font.SysFont("Consolas",20)
timerRect = Rect(360,10,80,30)
clock = time.Clock()

#object is a placeholder to call out
#level1
#wall
class Wall(object):
    #_init_ creates
    #when called, only need to call a single argument
    def __init__(self, place):
        global walls
        #16 x 10 ... blocks are 50 by 50
        #place changes everytime, self.Rect is a variable
        self = Rect(place[0],place[1],50,50)
        #adds all of them to the walls
        walls.append(self)
#spike
class Spike():
    def __init__(self,place):
        global spike
        #adds spike
        self = Rect(place[0],place[1],50,50)
        spike.append(self)


#16 by 10, each W and character space is 50 by 50 block
#W = wall
#D = door (exit)
#K = Key (to get to exit)
#[space] = area avaiable to walk
#levels-----------------------
#level1
level1 = [
"WWWWWWWWWWWWWWWW",
"W      W       W",
"W G    W      KW",
"WWWWW  W     WWW",
"W      WWW     W",
"W      W       W",
"W      W     WWW",
"W      WWWW    W",
"WWWW         DWW",
"WWWWWWWWWWWWWWWW",
]

#defining each row and column
x,y = 0,0 #will be defined to show spot
#defining level1--start off
for row in level1:
    for column in row:
        if column == "W":
            Wall((x,y)) #it adds the placement to a list called walls
        elif column == "D":
            #door placement
            doorRect = Rect(x,y,50,50) #if it is
        elif column =="K":
            keyRect = Rect(x,y,50,50) #makes a key spot
        x += 50 #adds 50 each time to move on to next chracter in row
    #if the row changes, then it resets the x value and it moves to next row in y value
    y+=50
    x = 0
#to draw the blocks
def drawBlock(door,key,doorImg,keyImg,walls,wallImg,wallImg2,level,backgroundImg,peachImg,peach,bowserImg,bowser):
    global item
    #set incase background image doesn't work
    screen.fill(0)
    #background image
    screen.blit(backgroundImg,(0,0))
    #door appears when key is caught
    if item =="key":
        screen.blit(doorImg,(door[0],door[1]))
    #key disappears when key is obtained
    elif item !="key":
        screen.blit(keyImg,(key[0],key[1]))

    for w in walls:
        if level%2 == 0:
            screen.blit(wallImg2,(w[0],w[1]))
        else:
            screen.blit(wallImg,(w[0],w[1]))
    for s in spike:
        screen.blit(spikeImg,(s[0],s[1]))
    #if reached last level
    if level == 5:
        screen.blit(peachImg,(peach[0],peach[1]))
        screen.blit(bowserImg,(bowser[0],bowser[1]))

#S = spike (lose life if touch)
#G = where mario starts
#level2
level2 = [
"WWWWWWWWWWWWWWWW",
"W GW           W",
"W WW  W        W",
"W     W  W  W  W",
"WW    WD       W",
"W   WWWWWWW    W",
"WS         W   W",
"WWWW          WW",
"WK     SWW    SW",
"WWWWWWWWWWWWWWWW",
]
level3 = [
"WWWWWWWWWWWWWWWW",
"WG             W",
"WW             W",
"W  W  W  W  W  W",
"W  WSSWSSWSSW  W",
"WSSWWWWWWWWWW  W",
"WWW            W",
"W      K       W",
"WD  S    S  S  W",
"WWWWWWWWWWWWWWWW",
]
level4 = [
"WWWWWWWWWWWWWWWW",
"W G     WD     W",
"WWWWWW  W      W",
"W      WWWW    W",
"W       W     WW",
"WK S    WS     W",
"WWWWWWW WWW    W",
"W             WW",
"W  S S    WW   W",
"WWWWWWWWWWWWWWWW",
]
#level 5 is a congrats level
level5 = [
"WWWWWWWWWWWWWWWW",
"W SSSKS S SDS  W",
"W  S  SSS  S   W",
"W  S  S S S S  W",
"W              W",
"W              W",
"W              W",
"W              W",
"W G            W",
"WWWWWWWWWWWWWWWW",
]

#to move to next level (start after level1
levels = [level1,level2,level3,level4,level5]
def createLevel(level):
    #resets walls and spike and fills it with new level's stuff
    global walls,guy,item,doorRect,keyRect,spike
    walls = []
    spike = []
    x2,y2 = 0,0
    for row in level:
        for column in row:
            #does same as level1 stuff
            if column =="W":
                Wall((x2,y2))
            elif column =="D":
                doorRect = Rect(x2,y2,50,50)
            elif column =="K":
                keyRect = Rect(x2,y2,50,50)
            #added spikes
            elif column =="S":
                #adds it
                Spike((x2,y2))
            #starting position of mario (G = guy)
            elif column == "G":
                #sets position
                guy.x = x2
                guy.y = y2

            x2 +=50
        y2+=50
        x2 = 0
    #resets item
    item = ""

#end of placements/variables--------------------------------------
















#functions------------------------

#draw map function-----------------
#not in use!! just temp
def drawMap(walls,door,key,level,backgroundImg):
    #door and key are rects
    #walls is a 2Dlist of rects
    #this draws the map, must be put below running
    screen.fill((255,255,255))
    #for background
    screen.blit(backgroundImg,(0,0))
    for wall in walls:
        #draws a blackish wall 50 by 50 at the placement
        draw.rect(screen,(10,10,10),wall)
    draw.rect(screen,(255, 0, 0),door)
    #change colour later
    draw.rect(screen,(255, 255, 255),key)

#end of draw walls function----------









#character functions---------------------------------------------------------
#music functions----------
def musicControl(musicRect,clickDown,mouseplace):
    #if not muted
    global musicMuted
    if clickDown and musicRect.collidepoint(mouseplace) and not musicMuted:
        musicMuted = True
        #mutes it
        mixer.music.set_volume(0)
    elif clickDown and musicRect.collidepoint(mouseplace) and musicMuted:
        musicMuted = False
        #if muted, unmutes it
        mixer.music.set_volume(100)
#draws the music
def drawMusic(musicRect,muteOffImg,muteOnImg):
    #if not muted, then show the non muted image,
    if not musicMuted:
        screen.blit(muteOffImg,(musicRect[0],musicRect[1]))
    elif musicMuted:
        screen.blit(muteOnImg,(musicRect[0],musicRect[1]))
    #in case image not loading, shows blank rectangle
    else:
        draw.rect(screen,0,musicRect)

#end of music functions----


#move guy function-----------
def moveGuy(keys,guy):
    #left = -, right= +, up = -
    #vx,vy = velocity of x,y
    #guy."" is a variable within guy, a created variable by function
    #guy is the product
    if keys[K_LEFT]:
        guy.vx = -3
    elif keys[K_RIGHT]:
        guy.vx = 3
    else:
        #not moving
        guy.vx = 0
    #jump-
    if keys[K_UP] and not guy.isJump:
        guy.isJump = True
        #jump up 5
        guy.vy = -5

class Player():
    #creates own object with __init__
    #"self" is similar to the guy object; but can only be used in Player()
    #below: like a blueprint (design)
    #self."" = product

    def __init__(self,x,y,vx,vy):
        #this function just redeclares it, so it can be used below in thguy.losee class
        self.vx = vx
        self.vy = vy
        self.x = x
        self.y = y
        self.isJump = False
        self.invFrames = 0 #if guy just got hit, he gets invincibility for a bit
    #gets rect object
    def getRect(self):
        #placement of where the guy is, slightly smaller, so can fit through gaps
        return Rect(self.x,self.y,48,48)
        self.lose = False
    #actually moves guy and includes if it bumps wall
    def moveReal(self,door,key,spike):
        global walls,item,level,life
        #moves it for x value
        self.x += self.vx
        #gets the square where the guy is, calls out function and turns it to a variable
        guyRect = self.getRect()
        #if guy hits wall
        for w in walls:
            if w.colliderect(guyRect):
                #goes the opposite direction, so it reverses and comes out of wall
                self.x -= self.vx
                #stops
                self.vx = 0
                break


        #for hitting spike with x
        for s in spike:
            if s.colliderect(guyRect) and self.invFrames == 0:
                life -= 1
                #invincibility time
                self.invFrames = 100
                print(life)
                self.x -=self.vx
                #stops
                self.vx = 0
                break
        #moves for y value
        self.y += self.vy
        #gets back to origin
        guyRect = self.getRect()

        #if hits wall
        for w in walls:
            if w.colliderect(guyRect):
                #goes in opposite direction, comes just out of wall
                self.y -= self.vy
                #if velocity is there
                if self.vy >= 0:
                    #makes it so it's unable to fly
                    #once it hits wall it stops jumping
                    guy.isJump = False
                #stops jumping speed
                self.vy = 0
                break


        #if hits door
        if door.colliderect(guyRect) and item == "key":
            #level -> level#
            print("Congrats on completing level",level)
            #adds one for next level
            level += 1
            #calls out function levels -> list, level-1 -> number in list 0-> level1, 1 -> level2
            createLevel(levels[level-1])
        #if hits key
        elif key.colliderect(guyRect) and item !="key":
            item = "key"

        #if hits a spike

        #from y spike
        for s in spike:
            if s.colliderect(guyRect) and self.invFrames == 0:
                #lose a life
                life -= 1
                self.invFrames = 100
                print(life)
                #stop going below and go back to original spot
                self.y -= self.vy
                #stops velocity
                self.vy = 0


#print it out
def drawGuy(guy,guyPic):
    #placement on pic is the center bottom point
    screen.blit(guyPic,(guy.x,guy.y))


#draws lives
def drawLives(lives,heartImg,life):
    if life ==3:
        for lif in lives:
            screen.blit(heartImg,(lif[0],lif[1]))
    #if 2 lives
    elif life ==2:
        #counts so when it hits 2, it stops, so it only draws 2 of the hearts
        count =0
        for ii in lives:
            count +=1
            if count <=2:
                screen.blit(heartImg,(ii[0],ii[1]))
    #same thing with 1 life
    elif life ==1:
        count = 0
        for i in lives:
            count+=1
            if count <=1:
                screen.blit(heartImg,(i[0],i[1]))
    #if life hits 0, it is put in loop so it can reset

#timer
def timerPlay(timerRect,text,clock,level,TimeOn):
    draw.rect(screen,(0),timerRect)
    if TimeOn == True:
        screen.blit(font.render(text,True,(255,255,255)),(timerRect[0],timerRect[1]))
        clock.tick(60)
    elif level == 5:
        #prints out paused
        screen.blit(font.render(text,False,(255,255,255)),(timerRect[0],timerRect[1]))
        TimeOn = False


#end of functions----------------

#------------------------------------------------------------------------------------
#function variables-
#main character placement, 0,1= x,y = placement; 2,3 = vx,vy = speed
guy = Player(100,50,0,0)
item = ""
TimeOn = False
MenuOpen = True
running = True
while running:
    clickDown = False
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYUP:
            #when key that is pressed
            keyUP = True
        if e.type == KEYDOWN:
            keyDown = True
            #when key is released
        if e.type == MOUSEBUTTONDOWN:
            clickDown = True
            #for music
        if e.type == USEREVENT and TimeOn == True:
            #for timer, add 1 each time
            counter +=1
            text = str(counter).rjust(3)
        #---------------------
    #always updates, rect of main---
    guyRect = guy.getRect()
    # --------------------------------------------------
    #for timer to stop when hits level 5
    if level < 5:
        TimeOn = True
    else:
        #pause time
        countStop = counter
        textSave = str(countStop).rjust(3)
        print (textSave)
        TimeOn = False
    #mouses (not used much)
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()

    #Caption at the top---
    display.set_caption("MarioRun2! Get to the door!")
    #if menu is not open
    if MenuOpen == True:
        #the keys that get pressed
        keys = key.get_pressed()

        #call out function; keys = keyboard keys, not key in game
        moveGuy(keys,guy)

        #gravity
        guy.vy += 0.1
        #moves the guy
        guy.moveReal(doorRect,keyRect,spike)
        #draws map
        #drawMap(walls,doorRect,keyRect,level)
        #draws blocks besides the character
        drawBlock(doorRect,keyRect,doorImg,keyImg,walls,wallImg,wallImg2,level,backgroundImg,peachImg,peachRect,bowserImg,bowserRect)
        #draws the character
        drawGuy(guy,pics[2][0])
        #draw life
        drawLives(lives,heartImg,life)
        #music-
        musicControl(musicRect,clickDown,(mx,my))
        drawMusic(musicRect,muteOffImg,muteOnImg)
        #decreases invincibility frames
        guy.invFrames -= 1
        if guy.invFrames < 0:
            guy.invFrames = 0 #makes sure it does not go below zero
        #timer
        timerPlay(timerRect,text,clock,level,TimeOn)

        time.wait(1)
    # --------------------------------------------------
    

    display.flip()
    #if life hits 0;
    if life <= 0:
        life = 3
        level = 1
        createLevel(levels[level-1])

quit()
