# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 17:51:40 2021

@author: Arthur
"""

from flask import Flask, request 
#from fastapi import FastAPI, requests as request
#import uvicorn

import shortuuid
shortuuid.set_alphabet("123456789")

'''
# demo data type
room = {'myroom':
        {'player1':{
            'hp':1000,
            'mp':1000,
            'position_x':200,
            'position_y':200,
            'move_left':False,
            'move_right':False,
            'shoot':False
            },
         'player2':{
             'hp':1000,
             'mp':1000,
             'position_x':400,
             'position_y':200,
             'move_left':False,
             'move_right':False,
             'shoot':False
             }
         }
        }
'''

uuid_list = []
room = {}

app = Flask(__name__)
#app = FastAPI()

@app.route('/', methods=['GET'])
def main():
    #room_id = request.args.get('room')
    #return room[room_id]
    return 'Exist room : {} '.format(str(list(room.keys()))) #list(room.keys()) -> ['myroom', 'myroom2']


@app.route('/getnewuuid', methods=['GET'])
def getnewuuid():
    new_uuid = shortuuid.uuid()[0:4]
    if new_uuid not in uuid_list:
        uuid_list.append(new_uuid)
        return new_uuid

@app.route('/initroom', methods=['POST'])
def initroom():
    #---- get form post method ----
    needToCreatNewRoom = request.values['needToCreatNewRoom']
    room_id = request.values['room_id']
    player_id = request.values['username']
    #---- get form post method ----
    
    if needToCreatNewRoom == 'True' or needToCreatNewRoom == 'true':
        room[room_id] = {}
        position_x = 200
        position_y = 200
    else:
        if player_id in room[room_id]:
            return 'You can\'t use same name'
        else:
            position_x = 600
            position_y = 200
        

    
    hp = 1000
    mp = 1000
    
    room[room_id][player_id] = {}
    room[room_id][player_id]['hp'] = hp
    room[room_id][player_id]['mp'] = mp
    room[room_id][player_id]['position_x'] = position_x
    room[room_id][player_id]['position_y'] = position_y
    room[room_id][player_id]['move_left'] = 'False'
    room[room_id][player_id]['move_right'] = 'False'
    room[room_id][player_id]['shoot'] = 'False'
    room[room_id][player_id]['jump'] = 'False'
    room[room_id][player_id]['in_air'] = 'True'
    
    
    if needToCreatNewRoom == 'True' or needToCreatNewRoom == 'true':
        return 'room created'
    else:
        return 'room joined'
        
    
@app.route('/getdata', methods=['GET'])
def getdata():
    room_id = request.args.get('room')
    return room[room_id]

@app.route('/updatedata', methods=['POST'])
def updatedata():
    #---- get form post method ----
    room_id = request.values['room_id']
    player_id = request.values['player_id']
    hp = request.values['hp']
    mp = request.values['mp']
    #position_x = request.values['position_x']
    #position_y = request.values['position_y']
    move_left = request.values['move_left']
    move_right = request.values['move_right']
    shoot = request.values['shoot']
    jump = request.values['jump']
    in_air = request.values['in_air']
    #---- get form post method ----

    #---- debug only ----
    temp = []
    temp.append(room_id)
    temp.append(player_id)
    temp.append(hp)
    temp.append(mp)
    #temp.append(position_x)
    #temp.append(position_y)
    temp.append(move_left)
    temp.append(move_right)
    print('--> '+ str(temp))
    #---- debug only ----
    
    #---- update data ----
    room[room_id][player_id]['hp'] = hp
    room[room_id][player_id]['mp'] = mp
    #room[room_id][player_id]['position_x'] = position_x
    #room[room_id][player_id]['position_y'] = position_y
    room[room_id][player_id]['move_left'] = move_left
    room[room_id][player_id]['move_right'] = move_right
    room[room_id][player_id]['shoot'] = shoot
    room[room_id][player_id]['jump'] = jump
    room[room_id][player_id]['in_air'] = in_air
    #---- update data ----
    
    #return 'ok'
    # 必須要有return -> 不然會有 500 err : The view function did not return a valid response. The return type must be a string, dict, tuple, Response instance, or WSGI callable, but it was a int.
    return room[room_id] #可以在return post status 的同時回傳資料 

if __name__ == '__main__':
     #app.run(host='127.0.0.1', port=8000)
     app.run(host='10.147.17.133', port=8000) #flask
     