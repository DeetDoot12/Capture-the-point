import socket
from _thread import *
import pickle
from CTP import Game

server="0.0.0.0"
port=5556
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    print(str(e))


try:
    s.listen()
    print("waiting for a connection")
    server_start=True
except:
    print('\nSERVER START FAILED AT s.listen()\nTRY UPDATING IP4 ADDRESS\n')
    server_start=False





#players=[Player(50,50,25,(0,255,0)),Player(500,500,25,(255,0,0))]


displays={}
games={}
connected=set()

def threaded_client(conn,filler):
    global current_players
    conn.send(str.encode("connected"))
    channel=int(conn.recv(2048).decode())
    if not (channel in displays):
        displays[channel]=[1]
        for i in range(0,99):
            displays[channel].append(0)
        p=0
    else:
        for i in range(0,len(displays[channel])):
            if 0==displays[channel][i]:
                p=i
                displays[channel][i]=1
                break
    print(channel,p)
    conn.send(str.encode(str(p)))
    interactable_as_display=conn.recv(2048).decode()=="True"
    if p==0 and channel%10==0 or not (channel//10 in games):
        games[channel//10]=Game()
        games[channel//10].new_game=True
    conn.send(pickle.dumps(games[channel//10]))
    data=pickle.loads(conn.recv(2048))
    games[channel//10]=data
    conn.send(pickle.dumps(games[channel//10]))
    reply=''
    while True:
        try:
            data=pickle.loads(conn.recv(2048))
            if not data:
                print("no data recieved")
                break
            else:
                try:
                    if p==0 and channel%10==0:
                        games[channel//10].team_points=data.team_points
                        games[channel//10].play_game_over_sound=data.play_game_over_sound
                        games[channel//10].MAX_FPS=data.MAX_FPS
                        games[channel//10].TEAM_COUNT=data.TEAM_COUNT
                        games[channel//10].POINTS_NEEDED_FOR_WIN=data.POINTS_NEEDED_FOR_WIN
                        games[channel//10].POINT_FREQUENCY=data.POINT_FREQUENCY
                        games[channel//10].NUMBERS_REQUIRED_FOR_CAPTURE=data.NUMBERS_REQUIRED_FOR_CAPTURE
                        games[channel//10].TIME_LEFT_WHEN_BEEP_STARTS=data.TIME_LEFT_WHEN_BEEP_STARTS
                        games[channel//10].LOCKOUT_DURATION=data.LOCKOUT_DURATION
                        games[channel//10].INACTIVITY_TIME=data.INACTIVITY_TIME
                        games[channel//10].CAPTURE_PROGRESS_DECREASE_RATE=data.CAPTURE_PROGRESS_DECREASE_RATE
                        games[channel//10].MIN_BEEP_FREQUENCY=data.MIN_BEEP_FREQUENCY
                        games[channel//10].MAX_BEEP_FREQUENCY=data.MAX_BEEP_FREQUENCY
                        games[channel//10].CAPTURE_GREEN_FLASH_DURATION=data.CAPTURE_GREEN_FLASH_DURATION
                        games[channel//10].CORRECT_GREEN_FLASH_DURATION=data.CORRECT_GREEN_FLASH_DURATION
                        games[channel//10].NUMBER_SEPERATION=data.NUMBER_SEPERATION
                        games[channel//10].new_game=data.new_game
                        games[channel//10].game_over=data.game_over
                        if data.new_game:
                            games[channel//10]=data

                    if p==0 and not games[channel//10].new_game:
                        games[channel//10].display_number[channel%10]=data.display_number[channel%10]
                        games[channel//10].lockout[channel%10]=data.lockout[channel%10]
                        games[channel//10].team_capturing[channel%10]=data.team_capturing[channel%10]
                        games[channel//10].team_captured[channel%10]=data.team_captured[channel%10]
                        games[channel//10].number_pause[channel%10]=data.number_pause[channel%10]
                        games[channel//10].duration_since_correct[channel%10]=data.duration_since_correct[channel%10]
                        games[channel//10].capture_progress[channel%10]=data.capture_progress[channel%10]
                        games[channel//10].time_since_captured[channel%10]=data.time_since_captured[channel%10]
                        games[channel//10].play_incorrect_sound[channel%10]=data.play_incorrect_sound[channel%10]
                        games[channel//10].play_capture_sound[channel%10]=data.play_capture_sound[channel%10]
                        games[channel//10].play_beep_sound[channel%10]=data.play_beep_sound[channel%10]
                    
                    while interactable_as_display and p>=len(games[channel//10].channel_keys_pressed[channel%10]):
                        games[channel//10].channel_keys_pressed[channel%10].append([])
                    while interactable_as_display and p>=len(data.channel_keys_pressed[channel%10]):
                        data.channel_keys_pressed[channel%10].append([])
                    if p!=0 and interactable_as_display:
                        games[channel//10].channel_keys_pressed[channel%10][p]=data.channel_keys_pressed[channel%10][p]
                    

                    reply=games[channel//10]
                    conn.sendall(pickle.dumps(reply))
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
            break
    print("lost connection to: ", p)
    displays[channel][p]=0
    conn.close()
                    
if server_start:
    while True:
        conn, addr=s.accept()
        print('connected to: ',addr)
        start_new_thread(threaded_client, (conn,0))