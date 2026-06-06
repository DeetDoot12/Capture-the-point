import random

class Game:
    def __init__(self):
        self.display_number=[random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10),random.randrange(0,10)]
        self.lockout=[0,0,0,0,0,0,0,0,0,0]
        self.team_capturing=[None,None,None,None,None,None,None,None,None,None]
        self.team_captured=[None,None,None,None,None,None,None,None,None,None]
        self.team_points=[0,0,0,0,0,0]
        self.number_pause=[0,0,0,0,0,0,0,0,0,0]
        self.duration_since_correct=[100000,100000,100000,100000,100000,100000,100000,100000,100000,100000]
        self.capture_progress=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        self.time_since_captured=[100000,100000,100000,100000,100000,100000,100000,100000,100000,100000]
        self.play_incorrect_sound=[False,False,False,False,False,False,False,False,False,False]
        self.play_capture_sound=[False,False,False,False,False,False,False,False,False,False]
        self.play_beep_sound=[False,False,False,False,False,False,False,False,False,False]
        self.play_game_over_sound=False
        self.channel_keys_pressed=[[],[],[],[],[],[],[],[],[],[]]
        # for i in range(0,len(self.)):
        #     for j in range(0,10):
        #         self.channel_keys_pressed[i].append([])


        self.new_game=False
        self.game_over=False


        self.MAX_FPS=30
        self.TEAM_COUNT=1
        self.POINTS_NEEDED_FOR_WIN=1000000
        self.POINT_FREQUENCY=1*self.MAX_FPS
        self.NUMBERS_REQUIRED_FOR_CAPTURE=30000
        self.TIME_LEFT_WHEN_BEEP_STARTS=0
        self.LOCKOUT_DURATION=1*self.MAX_FPS
        self.INACTIVITY_TIME=5*self.MAX_FPS
        self.CAPTURE_PROGRESS_DECREASE_RATE=8*self.MAX_FPS
        self.MIN_BEEP_FREQUENCY=self.MAX_FPS
        self.MAX_BEEP_FREQUENCY=self.MAX_FPS/20
        self.CAPTURE_GREEN_FLASH_DURATION=self.MAX_FPS*1
        self.CORRECT_GREEN_FLASH_DURATION=self.MAX_FPS*0.75
        self.NUMBER_SEPERATION=self.MAX_FPS/20*0