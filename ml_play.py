"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm
import math
import random as rd
p1test=100
def ml_loop(side: str):

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    check=False
    p1 =False
    
    p2 =False
    person=False
    dead=True
    Pdirect=rd.randint(0,1)
    def move_to(player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+20  > pred : return 2 # goes left
            elif scene_info["platform_1P"][0]+20 <pred : return 1 # goes right
            else : return 0 # NONE
        else :
            if scene_info["platform_2P"][0]+20  > pred : return 2 # goes left
            elif scene_info["platform_2P"][0]+20 <pred : return 1 # goes right
            else : return 0 # NONE
    def cut_the_ball():
        tmp=rd.randint(0,2)
        if tmp==2: return 2 # goes left
        elif tmp==1: return 1 # goes right
        else : return 1 # NONE


    def ml_loop_for_1P(): 
        if scene_info["ball_speed"][1] > 0 : # 球正在向下 # ball goes down
            abs_speedX=abs(scene_info["ball_speed"][0])  #將speed設為正
            now_direct=0
            yseg = math.ceil((scene_info["platform_1P"][1]-scene_info["ball"][1]-5 ) / scene_info["ball_speed"][1])  # 幾個frame以後會需要接  # x means how many frames before catch the ball
            if scene_info["ball_speed"][0]>0:  #球往右邊跑，等等由左邊開始計算
                xseg = math.ceil((195-scene_info["ball"][0])/abs_speedX) 
                now_direct=1
            else:                               #球往左邊跑，等等由右邊開始計算
                xseg = math.ceil(scene_info["ball"][0]/abs_speedX)   # 目前的xreg
                now_direct=0
            x_range_seg=math.ceil(195/abs_speedX)  #現在速度的xrangeseg
            last_reg=abs(int(yseg-xseg)%int(x_range_seg) )#最後的reg
            bound = abs(int((yseg-xseg)//x_range_seg +now_direct)%2)
            
            pred =abs(195*bound-last_reg*abs_speedX)
            if yseg<xseg:
                pred=scene_info["ball"][0]+yseg*scene_info["ball_speed"][0]
            # print(scene_info["ball_speed"],pred,now_direct,yseg,xseg,last_reg,x_range_seg,bound,scene_info["ball"],scene_info["platform_2P"],scene_info["platform_1P"])  
            if scene_info["ball"][1]+scene_info["ball_speed"][1]>=415 :
                # print(scene_info["frame"],scene_info["blocker"],scene_info["ball_speed"],scene_info["ball"],scene_info["platform_1P"],scene_info["platform_2P"])          
                return cut_the_ball()          
            else: 
                
                return move_to(player = '1P',pred = pred)
        else : # 球正在向上 # ball goes up
            # if scene_info["ball"][1]==415:
            #     # print(scene_info["frame"],scene_info["blocker"],scene_info["ball_speed"],scene_info["ball"],scene_info["platform_1P"],scene_info["platform_2P"])          
            # global p1test
            # if scene_info["ball"][1]==415:
            #     if scene_info["ball_speed"][0]>0:
            #         p1test=195-scene_info["ball"][0]/2 
            #     else:
            #         p1test=scene_info["ball"][0]/2
            return move_to(player = '1P',pred = 100)
            


    def ml_loop_for_2P():  # as same as 1P
        if scene_info["ball_speed"][1] < 0 : 
            abs_speedX=abs(scene_info["ball_speed"][0])  #將speed設為正
            now_direct=0
            yseg = math.ceil((scene_info["platform_2P"][1]+30-scene_info["ball"][1] ) / scene_info["ball_speed"][1])  # 幾個frame以後會需要接  # x means how many frames before catch the ball
            if scene_info["ball_speed"][0]>0:  #球往右邊跑，等等由左邊開始計算
                xseg = math.ceil((195-scene_info["ball"][0])/abs_speedX) 
                now_direct=1
            else:                               #球往左邊跑，等等由右邊開始計算
                xseg = math.ceil(scene_info["ball"][0]/abs_speedX)   # 目前的xreg
                now_direct=0
            x_range_seg=math.ceil(195/abs_speedX)  #現在速度的xrangeseg
            last_reg=abs(int(yseg-xseg)%int(x_range_seg) )#最後的reg
            bound = abs(int((yseg-xseg)//x_range_seg +now_direct)%2)
            
            pred =abs(195*bound-last_reg*abs_speedX)
            if yseg<xseg:
                pred=scene_info["ball"][0]+yseg*scene_info["ball_speed"][0]
            # print(pred,now_direct,yseg,xseg,last_reg,x_range_seg,bound,scene_info["ball"])    
            if scene_info["ball"][1]-scene_info["ball_speed"][1]<=80 :
                print(scene_info["frame"],scene_info["ball_speed"],scene_info["ball"],scene_info["platform_1P"],scene_info["platform_2P"])          
                return cut_the_ball()          
            else: return move_to(player = '2P',pred = pred)
        else : 

            return move_to(player = '2P',pred = 100)
            
    start_frame=rd.randint(0,20)
    print(start_frame,"ooooooooo")
    test=0
    # 2. Inform the game process that ml process is ready
    comm.ml_ready()
    
    # 3. Start an endless loop
    while True:
        
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()
        # print(scene_info["blocker"])
        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False
            if dead==True:
                start_frame=rd.randint(0,20)
                dead=False
                print(start_frame,"pppppppppp")
            Pdirect=rd.randint(0,1)
            person=True
            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue
        # 3.4 Send the instruction for this frame to the game process
        if not ball_served and scene_info["frame"]>=start_frame:
            direct=rd.randint(0,1)
            if direct==0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            else:
                comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_RIGHT"})
            ball_served = True
            continue
        elif scene_info["frame"]<start_frame:
            person=True
            if scene_info["ball"][1]>150:
                preson=True
            else:
                preson=False
            if person==True and side=="1P" or person==False and side=="2P":          
                if Pdirect==0:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                else:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
        else:
            dead=True
            if side == "1P":
                command = ml_loop_for_1P()
            else:
                command = ml_loop_for_2P()

            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            