import pygame
import random
from CTP import Game
from CTPnetwork import Network
import tkinter as tk

def get_screen_resolution_width():
    root = tk.Tk()
    root.withdraw() 
    screen_width = root.winfo_screenwidth()
    root.destroy() # Close the Tkinter instance
    return screen_width
def get_screen_resolution_height():
    root = tk.Tk()
    root.withdraw() 
    screen_height = root.winfo_screenheight()
    root.destroy() # Close the Tkinter instance
    return screen_height


#gameplay (see text below for descriptions)
TEAM_COUNT=2
POINTS_NEEDED_FOR_WIN=240
POINT_FREQUENCY=1
NUMBERS_REQUIRED_FOR_CAPTURE=13
TIME_LEFT_WHEN_BEEP_STARTS=60
LOCKOUT_DURATION=1
INACTIVITY_TIME=5
CAPTURE_PROGRESS_DECREASE_RATE=8
DISPLAY_CHANNEL=0
INTERACTABLE_AS_DISPLAY=True
TERRORIST_MODE=True
ACTIVATES_AFTER=0

"""
TEAM_COUNT=number of teams (max 4)
POINTS_NEEDED_FOR_WIN=number of points for a team to win
POINT_FREQUENCY=number of seconds per point when captured (making this too small can cause the games time to vary duratically)
NUMBERS_REQUIRED_FOR_CAPTURE=how many numbers need to be typed in to capture a point
TIME_LEFT_WHEN_BEEP_STARTS=how many seconds before a team wins that the beeping will start
LOCKOUT_DURATION=how many seconds the keyboard is disabled after an incorrect input
INACTIVITY_TIME=how many seconds after an input will a teams capture progress begin to drop
CAPTURE_PROGRESS_DECREASE_RATE=how many seconds for 1 capture progress to be removed after INACTIVITY_TIME
DISPLAY_CHANNEL=the channel must be a number ending in 0 to be a hostgame then all channels above (up to the next 0) will copy the settings of this host game. 
if the host leaves, then the next person to join the channel becomes the host. a display will not become a host unless it leaves and joins back.
Will be asked what channel to join when pressing play if DISPLAY_CHANNEL is -1.


Example for a 1 point game with 2 non interactable displays and 1 interactable display:
If you want to have a point with a screen facing both ways, and both are interactable aswell as display screens in each teams spawn, then do the following:

Running server:
make sure one of the devices has the server file running. if it wont run then the IP address needs to be updated or you have no internet connection.
To do this open the command prompt app on your computer (idk how for apple) and type in ipconfig and hit enter.
for apple, google how to get ip4 address and get it because idk how.
Copy the numbers next to IP4 ADDRESS and paste them in the server file next to server=. 
also paste it in every devices CTPnetwork.py file next to self.server=
make sure there are no spaces and the ip address is surrounded by these->"
now the server should run and devices on the same internet connection should be able to connect.

The only file that needs to be edited after the server is started is capture the point.py. 
All of the following steps are editing this file.

Creating host game:
create a game with your desired settings. Join channel 0 by setting DISPLAY_CHANNEL=0.
The settings of the first person to join the server automatically gets copied to all other connections.

Creating interactable display:
in the display you want to be interactable make sure INTERACTABLE_AS_DISPLAY=True.
Then set DISPLAY_CHANNEL=0 aswell. run the file. This screen should mirror the host screen but also be interactable (can capture the point using this display)

creating 2 non-interactable displays:
in a display you want to just mirror the point, in the file capture the point.py make sure INTERACTABLE_AS_DISPLAY=False.
Then set DISPLAY_CHANNEL=0 aswell. run the file. This screen should mirror the host screen but not be interactable in any way
do this again in your last device and place near each teams spawn.

Note:
You do not need to re-start every file to restart the game.
You only need to restart the host game then all of the displays will update their settings to copy the host.
they will not lose there interactible or non interactable properties.

If you want more points then do the following:
if you want another point then set DISPLAY_CHANNEL=1. this point will copy the settings of the point in DISPLAY_CHANNEL=0.
The first display to run the game file with DISPLAY_CHANNEL=1 will be the host of that point.
All others that join the same channel will just be displays of the host of the point. they will be interactable if INTERACTABLE_AS_DISPLAY=True.
you can have up to 10 points per game.
DISPLAY_CHANNEL=10 will be run completley seperatley to DISPLAY_CHANNEL=0. it is treated as its own seperate game.
so if you want 3 seperate games run the files with DISPLAY_CHANNEL=0 to 9 for game 1, DISPLAY_CHANNEL=10 to 19 for game 2,  DISPLAY_CHANNEL=20 to 29 for game 3

If you want more displays on one screen then do the following:
in your capture the point.py file scroll down to the visuals section and set SCREEN_WIDTH and SCREEN_HEIGHT to the appropriate values to fit more displays on the screen.
setting both to 0.5 will make the display only take up a quarter of the screen.
do this in capture the point duplicate.py files aswell.
if you have 3 points then use 3 files (capture the point.py,capture the point duplicate.py,capture the point duplicate2.py) and have them join the same DISPLAY_CHANNEL as each point.
for the example above you would need 2 files with DISPLAY_CHANNEL=0 for the first file and DISPLAY_CHANNEL=1 for the second. 
SCREEN_WIDTH=0.5 for both so each only takes up half of the screen.
"""

#Visuals
AUTO_SCREEN_SCALE=True
SCREEN_WIDTH=1
SCREEN_HEIGHT=1
#AUTO_SCREEN_SCALE automatically determines appropriate screen size. This overrides WIDTH AND HEIGHT.
#SCREEN_WIDTH is how much of the width of the screen the display takes up
#SCREEN_HEIGHT is how much of the vertical of the screen the display takes up
WIDTH=1000
HEIGHT=700/1300*WIDTH
MAX_FPS=30
MIN_BEEP_FREQUENCY=MAX_FPS
MAX_BEEP_FREQUENCY=MAX_FPS/20
CAPTURE_GREEN_FLASH_DURATION=MAX_FPS*1
CORRECT_GREEN_FLASH_DURATION=MAX_FPS*0.75
NUMBER_SEPERATION=MAX_FPS/20*0





def get_screen_resolution_width():
    root = tk.Tk()
    root.withdraw() 
    screen_width = root.winfo_screenwidth()
    root.destroy() # Close the Tkinter instance
    return screen_width
def get_screen_resolution_height():
    root = tk.Tk()
    root.withdraw() 
    screen_height = root.winfo_screenheight()
    root.destroy() # Close the Tkinter instance
    return screen_height
if AUTO_SCREEN_SCALE:
    # if get_screen_resolution_width()*700/1300>get_screen_resolution_height():
    #     HEIGHT=int(get_screen_resolution_height()*SCREEN_SIZE)
    #     WIDTH=int(HEIGHT*1300/700)
    # else:
    #     WIDTH=int(get_screen_resolution_width()*SCREEN_SIZE)
    #     HEIGHT=int(WIDTH*700/1300)
    WIDTH=int(get_screen_resolution_width()*(SCREEN_WIDTH-0))
    HEIGHT=int(get_screen_resolution_height()*(SCREEN_HEIGHT-0.05))
    


#No touchy
POINT_FREQUENCY*=MAX_FPS
LOCKOUT_DURATION*=MAX_FPS
INACTIVITY_TIME*=MAX_FPS
ACTIVATES_AFTER*=MAX_FPS
CAPTURE_PROGRESS_DECREASE_RATE*=MAX_FPS
if DISPLAY_CHANNEL==-1:
    DISPLAY_CHANNEL=int(input("join which channel?"))

X=0
Y=1 

pygame.init()
pygame.mixer.init()

SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("CTP")

DISPLAY_NUMBER_FONT=pygame.font.SysFont("bauhaus 93",int(HEIGHT/1.5))
WIN_FONT=pygame.font.SysFont("bauhaus 93",int(HEIGHT/5))

LOCKOUT_SURFACE=pygame.Surface((WIDTH/10,WIDTH/10))
LOCKOUT_SURFACE.set_alpha(150)
LOCKOUT_SURFACE.fill((200,0,0))

#CELEBRATION=pygame.mixer.Sound("FNAF - 6 AM sound.mp3")
try:
    BEEP=pygame.mixer.Sound("Barcode scanner beep sound (sound effect).mp3")
    BOMB_SOUND=pygame.mixer.Sound("Explosion sound effect - bomb sound - boom sound.mp3")
    CAPTURE_SOUND=pygame.mixer.Sound("success - Sound Effect.mp3")
    INCORRECT_SOUND=pygame.mixer.Sound("incorrect sound effect.mp3")
    if not TERRORIST_MODE:
        BOMB_SOUND=pygame.mixer.Sound("FNAF - 6 AM sound.mp3")
        BEEP=pygame.mixer.Sound("Bonk Sound Effect - Mr (mp3cut.net).mp3")
except:
    BEEP=pygame.mixer.Sound("capture the flag/Barcode scanner beep sound (sound effect).mp3")
    BOMB_SOUND=pygame.mixer.Sound("capture the flag/Explosion sound effect - bomb sound - boom sound.mp3")
    CAPTURE_SOUND=pygame.mixer.Sound("capture the flag/success - Sound Effect.mp3")
    INCORRECT_SOUND=pygame.mixer.Sound("capture the flag/incorrect sound effect.mp3")
    if not TERRORIST_MODE:
        BOMB_SOUND=pygame.mixer.Sound("capture the flag/FNAF - 6 AM sound.mp3")
        BEEP=pygame.mixer.Sound("capture the flag/Bonk Sound Effect - Mr (mp3cut.net).mp3")



BAR_GAP=HEIGHT/20

def main_draw(game,team_count,points_needed_for_win,numbers_required_for_capture,capture_green_flash_duration,correct_green_flash_duration,activates_after):
    if game.team_captured[DISPLAY_CHANNEL%10]==None:
        SCREEN.fill((255,255,255))
    elif game.team_captured[DISPLAY_CHANNEL%10]==0:
        SCREEN.fill((255,150,0))
    elif game.team_captured[DISPLAY_CHANNEL%10]==1:
        SCREEN.fill((100,100,255))
    elif game.team_captured[DISPLAY_CHANNEL%10]==2:
        SCREEN.fill((100,255,100))
    elif game.team_captured[DISPLAY_CHANNEL%10]==3:
        SCREEN.fill((255,0,255))
    

    # if game.team_capturing!=None:
    #     if game.team_capturing==-1:
    #         color=(255,255,255)
    #     if game.team_capturing==0:
    #         color=(255,150,0)
    #     if game.team_capturing==1:
    #         color=(100,100,250)
    #     if game.team_capturing==2:
    #         color=(100,255,100)
    #     if game.team_capturing==3:
    #         color=(255,0,255)
    #     pygame.draw.rect(SCREEN,color,pygame.Rect(0,0,int(WIDTH*game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing]/NUMBERS_REQUIRED_FOR_CAPTURE),HEIGHT))
    # else:
    captures=[]
    for i in range(0,len(game.capture_progress[DISPLAY_CHANNEL%10])):
        if game.capture_progress[DISPLAY_CHANNEL%10][i]>0:
            captures.append([None,0])
            j=0
            while captures[j][1]>game.capture_progress[DISPLAY_CHANNEL%10][i] and j<len(captures):
                j+=1
            temp=[i,game.capture_progress[DISPLAY_CHANNEL%10][i]]
            temp2=[None,0]
            while j<len(captures):
                if j+1<len(captures):
                    temp2=[captures[j][0],captures[j][1]]
                captures[j]=[temp[0],temp[1]]
                if j+1<len(captures):
                    temp=[temp2[0],temp2[1]]
                j+=1
    for i in range(0,len(captures)):
        if captures[i][0]==game.team_capturing[DISPLAY_CHANNEL%10]:
            captures.append([captures[i][0],captures[i][1]])
            captures.remove(captures[i])
            break

    colors=[(255,150,0),(100,100,250),(100,255,100),(255,0,255),(255,255,255)]
    for i in captures:
        if i[0]>=team_count:
            i[0]=-1
        pygame.draw.rect(SCREEN,colors[i[0]],pygame.Rect(0,0,int(WIDTH*i[1]/numbers_required_for_capture),HEIGHT))

    if game.time_since_captured[DISPLAY_CHANNEL%10]<capture_green_flash_duration:
        pygame.draw.rect(SCREEN,(int((game.time_since_captured[DISPLAY_CHANNEL%10]/capture_green_flash_duration/2+0.5)*220),220,int((game.time_since_captured[DISPLAY_CHANNEL%10]/capture_green_flash_duration/2+0.5)*220)),pygame.Rect(BAR_GAP*2/3,BAR_GAP*2/3,int(BAR_GAP*2/3+(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count+BAR_GAP*2/3)),10)
        pygame.draw.rect(SCREEN,(200,100,0),pygame.Rect(BAR_GAP,BAR_GAP,int(game.team_points[0]/points_needed_for_win*(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count)))
        if team_count>1:
            pygame.draw.rect(SCREEN,(int((game.time_since_captured[DISPLAY_CHANNEL%10]/capture_green_flash_duration/2+0.5)*220),220,int((game.time_since_captured[DISPLAY_CHANNEL%10]/capture_green_flash_duration/2+0.5)*220)),pygame.Rect(BAR_GAP*2/3,BAR_GAP*2+(HEIGHT-BAR_GAP*(team_count+1))/team_count-BAR_GAP/3,int(BAR_GAP*2/3+(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count+BAR_GAP*2/3)),10)
            pygame.draw.rect(SCREEN,(0,0,200),pygame.Rect(BAR_GAP,BAR_GAP*2+(HEIGHT-BAR_GAP*(team_count+1))/team_count,int(game.team_points[1]/points_needed_for_win*(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count)))
            if team_count>2:
                pygame.draw.rect(SCREEN,(int((game.time_since_captured[DISPLAY_CHANNEL%10]/capture_green_flash_duration/2+0.5)*220),220,int((game.time_since_captured[DISPLAY_CHANNEL%10]/capture_green_flash_duration/2+0.5)*220)),pygame.Rect(BAR_GAP*2/3,BAR_GAP*3+(HEIGHT-BAR_GAP*(team_count+1))/team_count*2-BAR_GAP/3,int(BAR_GAP*2/3+(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count+BAR_GAP*2/3)),10)
                pygame.draw.rect(SCREEN,(0,100,0),pygame.Rect(BAR_GAP,BAR_GAP*3+(HEIGHT-BAR_GAP*(team_count+1))/team_count*2,int(game.team_points[2]/points_needed_for_win*(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count)))
                if team_count>3:
                    pygame.draw.rect(SCREEN,(int((game.time_since_captured[DISPLAY_CHANNEL%10]/capture_green_flash_duration/2+0.5)*220),220,int((game.time_since_captured[DISPLAY_CHANNEL%10]/capture_green_flash_duration/2+0.5)*220)),pygame.Rect(BAR_GAP*2/3,BAR_GAP*4+(HEIGHT-BAR_GAP*(team_count+1))/team_count*3-BAR_GAP/3,int(BAR_GAP*2/3+(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count+BAR_GAP*2/3)),10)
                    pygame.draw.rect(SCREEN,(125,0,125),pygame.Rect(BAR_GAP,BAR_GAP*4+(HEIGHT-BAR_GAP*(team_count+1))/team_count*3,int(game.team_points[3]/points_needed_for_win*(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count)))
    else:
        pygame.draw.rect(SCREEN,(220,220,220),pygame.Rect(BAR_GAP*2/3,BAR_GAP*2/3,int(BAR_GAP*2/3+(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count+BAR_GAP*2/3)),10)
        pygame.draw.rect(SCREEN,(200,100,0),pygame.Rect(BAR_GAP,BAR_GAP,int(game.team_points[0]/points_needed_for_win*(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count)))
        if team_count>1:
            pygame.draw.rect(SCREEN,(220,220,220),pygame.Rect(BAR_GAP*2/3,BAR_GAP*2+(HEIGHT-BAR_GAP*(team_count+1))/team_count-BAR_GAP/3,int(BAR_GAP*2/3+(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count+BAR_GAP*2/3)),10)
            pygame.draw.rect(SCREEN,(0,0,200),pygame.Rect(BAR_GAP,BAR_GAP*2+(HEIGHT-BAR_GAP*(team_count+1))/team_count,int(game.team_points[1]/points_needed_for_win*(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count)))
            if team_count>2:
                pygame.draw.rect(SCREEN,(220,220,220),pygame.Rect(BAR_GAP*2/3,BAR_GAP*3+(HEIGHT-BAR_GAP*(team_count+1))/team_count*2-BAR_GAP/3,int(BAR_GAP*2/3+(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count+BAR_GAP*2/3)),10)
                pygame.draw.rect(SCREEN,(0,100,0),pygame.Rect(BAR_GAP,BAR_GAP*3+(HEIGHT-BAR_GAP*(team_count+1))/team_count*2,int(game.team_points[2]/points_needed_for_win*(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count)))
                if team_count>3:
                    pygame.draw.rect(SCREEN,(220,220,220),pygame.Rect(BAR_GAP*2/3,BAR_GAP*4+(HEIGHT-BAR_GAP*(team_count+1))/team_count*3-BAR_GAP/3,int(BAR_GAP*2/3+(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count+BAR_GAP*2/3)),10)
                    pygame.draw.rect(SCREEN,(125,0,125),pygame.Rect(BAR_GAP,BAR_GAP*4+(HEIGHT-BAR_GAP*(team_count+1))/team_count*3,int(game.team_points[3]/points_needed_for_win*(WIDTH-BAR_GAP*2)),int((HEIGHT-BAR_GAP*(team_count+1))/team_count)))
    

    if game.number_pause[DISPLAY_CHANNEL%10]==0 and game.team_capturing[DISPLAY_CHANNEL%10]!=None and game.team_capturing[DISPLAY_CHANNEL%10]!=game.team_captured[DISPLAY_CHANNEL%10]:
        if game.duration_since_correct[DISPLAY_CHANNEL%10]<correct_green_flash_duration:
            display_number_text=DISPLAY_NUMBER_FONT.render(str(game.display_number[DISPLAY_CHANNEL%10]),True,(0,255-int(game.duration_since_correct[DISPLAY_CHANNEL%10]/correct_green_flash_duration*255),0),None)
        else:
            display_number_text=DISPLAY_NUMBER_FONT.render(str(game.display_number[DISPLAY_CHANNEL%10]),True,(0,0,0),None)
        if game.lockout[DISPLAY_CHANNEL%10]!=0:
            display_number_text=DISPLAY_NUMBER_FONT.render(str(game.display_number[DISPLAY_CHANNEL%10]),True,(255,0,0),None)
        SCREEN.blit(display_number_text,pygame.Rect(WIDTH/2-display_number_text.get_width()/2,HEIGHT/2-display_number_text.get_height()/2,1,1))
    
    

    for i in range(0,len(game.team_points)):
        if game.team_points[i]==points_needed_for_win:
            if i==0:
                win_text=WIN_FONT.render("ORANGE WINS!",True,(0,0,0),None)
            elif i==1:
                 win_text=WIN_FONT.render("BLUE WINS!",True,(0,0,0),None)
            elif i==2:
                 win_text=WIN_FONT.render("GREEN WINS!",True,(0,0,0),None)
            elif i==3:
                 win_text=WIN_FONT.render("PINK WINS!",True,(0,0,0),None)
            SCREEN.blit(win_text,pygame.Rect(WIDTH/2-win_text.get_width()/2,HEIGHT/2-win_text.get_height()/2,1,1))

    
    if activates_after>0:
        SCREEN.fill((0,0,0))
        display_number_text=DISPLAY_NUMBER_FONT.render(str(int(activates_after/MAX_FPS)),True,(255,255,255),None)
        SCREEN.blit(display_number_text,pygame.Rect(WIDTH/2-display_number_text.get_width()/2,HEIGHT/2-display_number_text.get_height()/2,1,1))
    elif activates_after==0:
        pygame.mixer.Sound.play(CELEBRATION)

    pygame.display.update()



def main():
    game=None
    connected=False
    try:
        n=Network()
        print("Channel:",DISPLAY_CHANNEL)
        p=int(n.str_send0(str(DISPLAY_CHANNEL)))
        print("Player:",p)
        game=n.str_send1(str(INTERACTABLE_AS_DISPLAY))
        print("connected to server")
    except Exception as e:
        print("could not connect to server")
    if game==None:
        game=Game()
        p=0
    else:
        connected=True
    
    activates_after=ACTIVATES_AFTER
    running=True
    inactivity_time=0
    point_addition_timer=0
    capture_progress_decrease_timer=[]
    beep_timer=0
    time_since_game_over=0
    played_game_over_sound=False
    # incorrect_sound_timer=0 were just using the lockout timer
    played_capture_sound=False
    played_incorrect_sound=False
    played_beep_sound=False
    capture_sound_timer=0
    beep_sound_timer=0
    game_over_sound_timer=0
    max_fps=MAX_FPS
    team_count=TEAM_COUNT
    points_needed_for_win=POINTS_NEEDED_FOR_WIN
    point_frequency=POINT_FREQUENCY
    numbers_required_for_capture=NUMBERS_REQUIRED_FOR_CAPTURE
    time_left_when_beep_starts=TIME_LEFT_WHEN_BEEP_STARTS
    lockout_duration=LOCKOUT_DURATION
    inactivity_time_global=INACTIVITY_TIME
    capture_progress_decrease_rate=CAPTURE_PROGRESS_DECREASE_RATE
    min_beep_frequency=MIN_BEEP_FREQUENCY
    max_beep_frequency=MAX_BEEP_FREQUENCY
    capture_green_flash_duration=CAPTURE_GREEN_FLASH_DURATION
    correct_green_flash_duration=CORRECT_GREEN_FLASH_DURATION
    number_seperation=NUMBER_SEPERATION
    new_game_reset_timer=MAX_FPS/2
    updated_settings=False
    temp69=MAX_FPS
    if DISPLAY_CHANNEL%10==0 and p==0:
        game.game_over=False
        game.MAX_FPS=MAX_FPS
        game.TEAM_COUNT=TEAM_COUNT
        game.POINTS_NEEDED_FOR_WIN=POINTS_NEEDED_FOR_WIN
        game.POINT_FREQUENCY=POINT_FREQUENCY
        game.NUMBERS_REQUIRED_FOR_CAPTURE=NUMBERS_REQUIRED_FOR_CAPTURE
        game.TIME_LEFT_WHEN_BEEP_STARTS=TIME_LEFT_WHEN_BEEP_STARTS
        game.LOCKOUT_DURATION=LOCKOUT_DURATION
        game.INACTIVITY_TIME=INACTIVITY_TIME
        game.CAPTURE_PROGRESS_DECREASE_RATE=CAPTURE_PROGRESS_DECREASE_RATE
        game.MIN_BEEP_FREQUENCY=MIN_BEEP_FREQUENCY
        game.MAX_BEEP_FREQUENCY=MAX_BEEP_FREQUENCY
        game.CAPTURE_GREEN_FLASH_DURATION=CAPTURE_GREEN_FLASH_DURATION
        game.CORRECT_GREEN_FLASH_DURATION=CORRECT_GREEN_FLASH_DURATION
        game.NUMBER_SEPERATION=NUMBER_SEPERATION
        game.display_number=[random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10)]
        game.lockout=[0,0,0,0,0,0,0,0,0,0]
        game.team_capturing=[None,None,None,None,None,None,None,None,None,None]
        game.team_captured=[None,None,None,None,None,None,None,None,None,None]
        game.number_pause=[0,0,0,0,0,0,0,0,0,0]
        game.duration_since_correct=[100000,100000,100000,100000,100000,100000,100000,100000,100000,100000]
        game.time_since_captured=[100000,100000,100000,100000,100000,100000,100000,100000,100000,100000]
        game.play_incorrect_sound=[False,False,False,False,False,False,False,False,False,False]
        game.play_capture_sound=[False,False,False,False,False,False,False,False,False,False]
        game.play_beep_sound=[False,False,False,False,False,False,False,False,False,False]
        game.play_game_over_sound=False
        game.team_points=[]
        game.capture_progress=[[],[],[],[],[],[],[],[],[],[]]
        for i in range(0,TEAM_COUNT):
            game.team_points.append(0)
            capture_progress_decrease_timer.append(0)
        capture_progress_decrease_timer.append(0)
        for k in range(0,10):
            for i in range(0,TEAM_COUNT):
                game.capture_progress[k].append(0)
            game.capture_progress[k].append(0)
        

    while (running):
        if temp69>0:
            temp69-=1
        else:
            temp69=MAX_FPS
            print(game.game_over)
        if not (DISPLAY_CHANNEL%10==0 and p==0):
            max_fps=game.MAX_FPS
            team_count=game.TEAM_COUNT
            points_needed_for_win=game.POINTS_NEEDED_FOR_WIN
            point_frequency=game.POINT_FREQUENCY
            numbers_required_for_capture=game.NUMBERS_REQUIRED_FOR_CAPTURE
            time_left_when_beep_starts=game.TIME_LEFT_WHEN_BEEP_STARTS
            lockout_duration=game.LOCKOUT_DURATION
            inactivity_time_global=game.INACTIVITY_TIME
            capture_progress_decrease_rate=game.CAPTURE_PROGRESS_DECREASE_RATE
            min_beep_frequency=game.MIN_BEEP_FREQUENCY
            max_beep_frequency=game.MAX_BEEP_FREQUENCY
            capture_green_flash_duration=game.CAPTURE_GREEN_FLASH_DURATION
            correct_green_flash_duration=game.CORRECT_GREEN_FLASH_DURATION
            number_seperation=game.NUMBER_SEPERATION
        else:
            if game.new_game:
                if new_game_reset_timer>0:
                    new_game_reset_timer-=1
                else:
                    game.new_game=False
        if (not updated_settings or game.new_game) and not (DISPLAY_CHANNEL%10==0 and p==0):
            capture_progress_decrease_timer=[]
            for i in range(0,TEAM_COUNT):
                capture_progress_decrease_timer.append(0)
            capture_progress_decrease_timer.append(0)
            inactivity_time=0
            point_addition_timer=0
            beep_timer=0
            time_since_game_over=0
            played_game_over_sound=False
            # incorrect_sound_timer=0 were just using the lockout timer
            played_capture_sound=False
            played_incorrect_sound=False
            played_beep_sound=False
            capture_sound_timer=0
            beep_sound_timer=0
            game_over_sound_timer=0
            updated_settings=True

        

        clock=pygame.time.Clock()
        clock.tick(max_fps)
        mouse_position=pygame.mouse.get_pos()
        mouse_buttons=pygame.mouse.get_pressed(3)
        keys=pygame.key.get_pressed()
        if p==0:
            for i in range(0,len(game.capture_progress[DISPLAY_CHANNEL%10])):
                if game.capture_progress[DISPLAY_CHANNEL%10][i]>0 and not (game.team_capturing[DISPLAY_CHANNEL%10]==i or (game.team_capturing[DISPLAY_CHANNEL%10]==-1 and i==len(game.capture_progress[DISPLAY_CHANNEL%10])-1)) :
                    if capture_progress_decrease_timer[i]>0:
                        capture_progress_decrease_timer[i]-=1
                        if capture_progress_decrease_timer[i]<0:
                            capture_progress_decrease_timer[i]=0
                    else:
                        game.capture_progress[DISPLAY_CHANNEL%10][i]-=1
                        capture_progress_decrease_timer[i]=capture_progress_decrease_rate
        if p==0:            
            for i in range(0,len(game.team_points)):
                if (points_needed_for_win-game.team_points[i])*point_frequency/max_fps<=time_left_when_beep_starts and i==game.team_captured[DISPLAY_CHANNEL%10] and not game.game_over:
                    if beep_timer<=0:
                        beep_timer=max_beep_frequency  +  (points_needed_for_win-game.team_points[i])*point_frequency/max_fps /time_left_when_beep_starts  *  (min_beep_frequency-max_beep_frequency)
                        pygame.mixer.Sound.play(BEEP)
                        beep_sound_timer=2
                        game.play_beep_sound[DISPLAY_CHANNEL%10]=True
                        played_beep_sound=True
                    else:
                        beep_timer-=1
                        if beep_timer<0:
                            beep_timer=0
        if p==0:
            if game.lockout[DISPLAY_CHANNEL%10]>0:
                game.lockout[DISPLAY_CHANNEL%10]-=1
                if game.lockout[DISPLAY_CHANNEL%10]<=0:
                    game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                    game.lockout[DISPLAY_CHANNEL%10]=0
            
            if game.number_pause[DISPLAY_CHANNEL%10]>0:
                game.number_pause[DISPLAY_CHANNEL%10]-=1
                if game.number_pause[DISPLAY_CHANNEL%10]<0:
                    game.number_pause[DISPLAY_CHANNEL%10]=0
            if inactivity_time<inactivity_time_global:
                inactivity_time+=1
            else:
                game.team_capturing[DISPLAY_CHANNEL%10]=None
            if activates_after>-1:
                activates_after-=1
                if -1<activates_after<0:
                    activates_after=0
            game.duration_since_correct[DISPLAY_CHANNEL%10]+=1
            game.time_since_captured[DISPLAY_CHANNEL%10]+=1
        if game.game_over:
            time_since_game_over+=1

        #point giving and game ending
        if p==0 and DISPLAY_CHANNEL%10==0:
            for i in game.team_captured:
                if i!=None and not game.game_over:
                    if point_addition_timer>0:
                        point_addition_timer-=1
                    else:
                        point_addition_timer=point_frequency
                        game.team_points[i]+=1
                        if game.team_points[i]>=points_needed_for_win:
                            game.game_over=True
                            pygame.mixer.Sound.play(BOMB_SOUND)
                            game.play_game_over_sound=True
                            game_over_sound_timer=max_fps
        keys_pressed=[]
        for i in game.channel_keys_pressed[DISPLAY_CHANNEL%10]:
            for j in i:
                keys_pressed.append(j)
        events=pygame.event.get()
        for event in range(0,len(events)+1):
            if ((event!=len(events) and events[event].type==pygame.KEYDOWN) or len(keys_pressed)>0) and not game.game_over and (p==0 or INTERACTABLE_AS_DISPLAY) and activates_after==-1:
                try:
                    key=events[event].key
                except Exception as e:
                    key=None
                if p==0:
                    if key==pygame.K_o or "o" in keys_pressed:

                        inactivity_time=0
                        game.team_capturing[DISPLAY_CHANNEL%10]=0
                        if "o" in keys_pressed:
                            keys_pressed.remove("o")
                    elif (key==pygame.K_t or key==pygame.K_b or "t" in keys_pressed or "b" in keys_pressed) and team_count>1:
                        game.team_capturing[DISPLAY_CHANNEL%10]=1
                        inactivity_time=0
                        if "t" in keys_pressed:
                            keys_pressed.remove("t")
                        if "b" in keys_pressed:
                            keys_pressed.remove("b")
                    elif (key==pygame.K_g or "g" in keys_pressed) and team_count>2:
                        game.team_capturing[DISPLAY_CHANNEL%10]=2
                        inactivity_time=0
                        if "g" in keys_pressed:
                            keys_pressed.remove("g")
                    elif (key==pygame.K_p or "p" in keys_pressed) and team_count>3:
                        game.team_capturing[DISPLAY_CHANNEL%10]=3
                        inactivity_time=0
                        if "p" in keys_pressed:
                            keys_pressed.remove("p")
                    elif key==pygame.K_d or "d" in keys_pressed:
                        game.team_capturing[DISPLAY_CHANNEL%10]=-1
                        inactivity_time=0
                        if "d" in keys_pressed:
                            keys_pressed.remove("d")
                else:
                    if key==pygame.K_o:
                        if not "o" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("o")
                    else:
                        if "o" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("o")
                    if key==pygame.K_t or key==pygame.K_b:
                        if not "b" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("b")
                    else:
                        if "b" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("b")
                    if key==pygame.K_g:
                        if not "g" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("g")
                    else:
                        if "g" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("g")
                    if key==pygame.K_p:
                        if not "p" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("p")
                    else:
                        if "p" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("p")
                    if key==pygame.K_d:
                        if not "d" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("d")
                    else:
                        if "d" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("d")
                    if key==pygame.K_0:
                        if not "0" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("0")
                    else:
                        if "0" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("0")
                    if key==pygame.K_1:
                        if not "1" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("1")
                    else:
                        if "1" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("1")
                    if key==pygame.K_2:
                        if not "2" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("2")
                    else:
                        if "2" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("2")
                    if key==pygame.K_3:
                        if not "3" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("3")
                    else:
                        if "3" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("3")
                    if key==pygame.K_4:
                        if not "4" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("4")
                    else:
                        if "4" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("4")
                    if key==pygame.K_5:
                        if not"5" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("5")
                    else:
                        if "5" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("5")
                    if key==pygame.K_6:
                        if not "6" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("6")
                    else:
                        if "6" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("6")
                    if key==pygame.K_7:
                        if not "7" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("7")
                    else:
                        if "7" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("7")
                    if key==pygame.K_8:
                        if not "8" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("8")
                    else:
                        if "8" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("8")
                    if key==pygame.K_9:
                        if not "9" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].append("9")
                    else:
                        if "9" in game.channel_keys_pressed[DISPLAY_CHANNEL%10][p]:
                            game.channel_keys_pressed[DISPLAY_CHANNEL%10][p].remove("9")
                if game.team_capturing[DISPLAY_CHANNEL%10]!=None and game.lockout[DISPLAY_CHANNEL%10]==0 and game.number_pause[DISPLAY_CHANNEL%10]==0 and game.team_capturing[DISPLAY_CHANNEL%10]!=game.team_captured[DISPLAY_CHANNEL%10] and p==0:
                    if key==pygame.K_0 or "0" in keys_pressed:
                        if game.display_number[DISPLAY_CHANNEL%10]==0:
                            game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]+=1
                            game.number_pause[DISPLAY_CHANNEL%10]=number_seperation
                            game.duration_since_correct[DISPLAY_CHANNEL%10]=0
                            game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                        else:
                            game.lockout[DISPLAY_CHANNEL%10]=lockout_duration
                            pygame.mixer.Sound.play(INCORRECT_SOUND)
                            game.play_incorrect_sound[DISPLAY_CHANNEL%10]=True
                            played_incorrect_sound=True
                        inactivity_time=0
                        if "0" in keys_pressed:
                            keys_pressed.remove("0")
                    elif key==pygame.K_1 or "1" in keys_pressed:
                        if game.display_number[DISPLAY_CHANNEL%10]==1:
                            game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]+=1
                            game.number_pause[DISPLAY_CHANNEL%10]=number_seperation
                            game.duration_since_correct[DISPLAY_CHANNEL%10]=0
                            game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                        else:
                            game.lockout[DISPLAY_CHANNEL%10]=lockout_duration
                            pygame.mixer.Sound.play(INCORRECT_SOUND)
                            game.play_incorrect_sound[DISPLAY_CHANNEL%10]=True
                            played_incorrect_sound=True
                        inactivity_time=0
                        if "1" in keys_pressed:
                            keys_pressed.remove("1")
                    elif key==pygame.K_2 or "2" in keys_pressed:
                        if game.display_number[DISPLAY_CHANNEL%10]==2:
                            game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]+=1
                            game.number_pause[DISPLAY_CHANNEL%10]=number_seperation
                            game.duration_since_correct[DISPLAY_CHANNEL%10]=0
                            game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                        else:
                            game.lockout[DISPLAY_CHANNEL%10]=lockout_duration
                            pygame.mixer.Sound.play(INCORRECT_SOUND)
                            game.play_incorrect_sound[DISPLAY_CHANNEL%10]=True
                            played_incorrect_sound=True
                        inactivity_time=0
                        if "2" in keys_pressed:
                            keys_pressed.remove("2")
                    elif key==pygame.K_3 or "3" in keys_pressed:
                        if game.display_number[DISPLAY_CHANNEL%10]==3:
                            game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]+=1
                            game.number_pause[DISPLAY_CHANNEL%10]=number_seperation
                            game.duration_since_correct[DISPLAY_CHANNEL%10]=0
                            game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                        else:
                            game.lockout[DISPLAY_CHANNEL%10]=lockout_duration
                            pygame.mixer.Sound.play(INCORRECT_SOUND)
                            game.play_incorrect_sound[DISPLAY_CHANNEL%10]=True
                            played_incorrect_sound=True
                        inactivity_time=0
                        if "3" in keys_pressed:
                            keys_pressed.remove("3")
                    elif key==pygame.K_4 or "4" in keys_pressed:
                        if game.display_number[DISPLAY_CHANNEL%10]==4:
                            game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]+=1
                            game.number_pause[DISPLAY_CHANNEL%10]=number_seperation
                            game.duration_since_correct[DISPLAY_CHANNEL%10]=0
                            game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                        else:
                            game.lockout[DISPLAY_CHANNEL%10]=lockout_duration
                            pygame.mixer.Sound.play(INCORRECT_SOUND)
                            game.play_incorrect_sound[DISPLAY_CHANNEL%10]=True
                            played_incorrect_sound=True
                        inactivity_time=0
                        if "4" in keys_pressed:
                            keys_pressed.remove("4")
                    elif key==pygame.K_5 or "5" in keys_pressed:
                        if game.display_number[DISPLAY_CHANNEL%10]==5:
                            game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]+=1
                            game.number_pause[DISPLAY_CHANNEL%10]=number_seperation
                            game.duration_since_correct[DISPLAY_CHANNEL%10]=0
                            game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                        else:
                            game.lockout[DISPLAY_CHANNEL%10]=lockout_duration
                            pygame.mixer.Sound.play(INCORRECT_SOUND)
                            game.play_incorrect_sound[DISPLAY_CHANNEL%10]=True
                            played_incorrect_sound=True
                        inactivity_time=0
                        if "5" in keys_pressed:
                            keys_pressed.remove("5")
                    elif key==pygame.K_6 or "6" in keys_pressed:
                        if game.display_number[DISPLAY_CHANNEL%10]==6:
                            game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]+=1
                            game.number_pause[DISPLAY_CHANNEL%10]=number_seperation
                            game.duration_since_correct[DISPLAY_CHANNEL%10]=0
                            game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                        else:
                            game.lockout[DISPLAY_CHANNEL%10]=lockout_duration
                            pygame.mixer.Sound.play(INCORRECT_SOUND)
                            game.play_incorrect_sound[DISPLAY_CHANNEL%10]=True
                            played_incorrect_sound=True
                        inactivity_time=0
                        if "6" in keys_pressed:
                            keys_pressed.remove("6")
                    elif key==pygame.K_7 or "7" in keys_pressed:
                        if game.display_number[DISPLAY_CHANNEL%10]==7:
                            game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]+=1
                            game.number_pause[DISPLAY_CHANNEL%10]=number_seperation
                            game.duration_since_correct[DISPLAY_CHANNEL%10]=0
                            game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                        else:
                            game.lockout[DISPLAY_CHANNEL%10]=lockout_duration
                            pygame.mixer.Sound.play(INCORRECT_SOUND)
                            game.play_incorrect_sound[DISPLAY_CHANNEL%10]=True
                            played_incorrect_sound=True
                        inactivity_time=0
                        if "7" in keys_pressed:
                            keys_pressed.remove("7")
                    elif key==pygame.K_8 or "8" in keys_pressed:
                        if game.display_number[DISPLAY_CHANNEL%10]==8:
                            game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]+=1
                            game.number_pause[DISPLAY_CHANNEL%10]=number_seperation
                            game.duration_since_correct[DISPLAY_CHANNEL%10]=0
                            game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                        else:
                            game.lockout[DISPLAY_CHANNEL%10]=lockout_duration
                            pygame.mixer.Sound.play(INCORRECT_SOUND)
                            game.play_incorrect_sound[DISPLAY_CHANNEL%10]=True
                            played_incorrect_sound=True
                        inactivity_time=0
                        if "8" in keys_pressed:
                            keys_pressed.remove("8")
                    elif key==pygame.K_9 or "9" in keys_pressed:
                        if game.display_number[DISPLAY_CHANNEL%10]==9:
                            game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]+=1
                            game.number_pause[DISPLAY_CHANNEL%10]=number_seperation
                            game.duration_since_correct[DISPLAY_CHANNEL%10]=0
                            game.display_number[DISPLAY_CHANNEL%10]=random.randrange(0,10)
                        else:
                            game.lockout[DISPLAY_CHANNEL%10]=lockout_duration
                            pygame.mixer.Sound.play(INCORRECT_SOUND)
                            game.play_incorrect_sound[DISPLAY_CHANNEL%10]=True
                            played_incorrect_sound=True
                        inactivity_time=0
                        if "9" in keys_pressed:
                            keys_pressed.remove("9")
                    if game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]==numbers_required_for_capture:
                        game.capture_progress[DISPLAY_CHANNEL%10][game.team_capturing[DISPLAY_CHANNEL%10]]=0
                        game.time_since_captured[DISPLAY_CHANNEL%10]=0
                        pygame.mixer.Sound.play(CAPTURE_SOUND)
                        game.play_capture_sound[DISPLAY_CHANNEL%10]=True
                        played_capture_sound=True
                        capture_sound_timer=max_fps/2
                        if game.team_capturing[DISPLAY_CHANNEL%10]!=-1:
                            game.team_captured[DISPLAY_CHANNEL%10]=game.team_capturing[DISPLAY_CHANNEL%10]
                        else:
                            game.team_captured[DISPLAY_CHANNEL%10]=None
                        game.team_capturing[DISPLAY_CHANNEL%10]=None
            if event!=len(events) and events[event].type==pygame.QUIT:
                pygame.quit()
                pygame.mixer.quit()
                running=False
        if p==0:
            if beep_sound_timer>0:
                beep_sound_timer-=1
                if beep_sound_timer<0:
                    beep_sound_timer=0
            if game.play_beep_sound[DISPLAY_CHANNEL%10] and beep_sound_timer==0:
                game.play_beep_sound[DISPLAY_CHANNEL%10]=False
            if capture_sound_timer>0:
                capture_sound_timer-=1
                if capture_sound_timer<0:
                    capture_sound_timer=0
            if game.play_incorrect_sound[DISPLAY_CHANNEL%10] and game.lockout[DISPLAY_CHANNEL%10]==0 and played_incorrect_sound:
                game.play_incorrect_sound[DISPLAY_CHANNEL%10]=False
                played_incorrect_sound=False
            if game.play_capture_sound[DISPLAY_CHANNEL%10] and capture_sound_timer==0 and played_capture_sound:
                game.play_capture_sound[DISPLAY_CHANNEL%10]=False
                played_capture_sound=False
        else:
            if game.play_incorrect_sound[DISPLAY_CHANNEL%10] and not played_incorrect_sound:
                played_incorrect_sound=True
                pygame.mixer.Sound.play(INCORRECT_SOUND)
            if game.play_capture_sound[DISPLAY_CHANNEL%10] and not played_capture_sound:
                played_capture_sound=True
                pygame.mixer.Sound.play(CAPTURE_SOUND)
            if game.play_beep_sound[DISPLAY_CHANNEL%10] and not played_beep_sound:
                played_beep_sound=True
                pygame.mixer.Sound.play(BEEP)
            if not game.play_incorrect_sound[DISPLAY_CHANNEL%10]:
                played_incorrect_sound=False
            if not game.play_capture_sound[DISPLAY_CHANNEL%10]:
                played_capture_sound=False
            if not game.play_beep_sound[DISPLAY_CHANNEL%10]:
                played_beep_sound=False
            
        if p==0 and DISPLAY_CHANNEL%10==0:
            if game_over_sound_timer>0:
                game_over_sound_timer-=1
                if game_over_sound_timer<0:
                    game_over_sound_timer=0
            if game.play_game_over_sound and game_over_sound_timer==0:
                game.play_game_over_sound=False
        else:
            if game.play_game_over_sound and not played_game_over_sound:
                played_game_over_sound=True
                pygame.mixer.Sound.play(BOMB_SOUND)
            if not game.play_game_over_sound:
                played_game_over_sound=False

            
        if connected:
            try:
                temp=n.send(game)
                if temp!=None:
                    game=temp
                else:
                    connected=False
                    print("Disconected from server")

            except Exception as e:
                print("could not recieve game data. Disconecting")
                connected=False
           
        if running:
            main_draw(game,team_count,points_needed_for_win,numbers_required_for_capture,capture_green_flash_duration,correct_green_flash_duration,activates_after)



main()
