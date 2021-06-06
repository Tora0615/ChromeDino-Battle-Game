# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 18:11:10 2021

@author: Arthur
"""

import requests

# 可嘗試壓縮資料
#bz2.compress(str(room['1418']).encode())
#Out[26]: b"BZh91AY&SY\xf9\xca\x92\xb0\x00\x00q\x1f\x80@\x84q\x10\x01\x00\x00\x00\xb3\xe7\xddj \x00\x89\x05QD\xf524\xd1\x84\xc14\x02\xaaj\x86\xc5\x00\x03'\xa4~\xa9`\xae!(\xf0\xa1\xd0\xd0\xdc\xe5\xcb\xd6\x1dO\xb3)C\xb3\xf7u\xe8\x85\x1d:\xc4\x1d\xb7\x16!B\xc6\r\x9e\x08\xfcI\xaa\xadY0\x97\xb2\xe6\x1e\x8a\xa9%\xcf\x84\x93\x11\x19\x16s,J\xab\x9bJ\x1bf\xb6\xa9\xfe.\xe4\x8ap\xa1!\xf3\x95%`"

#bz2.decompress(b).decode()
#Out[25]: "{'a': {'hp': '100', 'mp': '100', 'position_x': 200, 'position_y': 200, 'move_left': 'False', 'move_right': 'False'}, 'b': {'hp': '200', 'mp': '200', 'position_x': 600, 'position_y': 200, 'move_left': 'False', 'move_right': 'False'}}"


def get_uuid():
    url = 'http://10.147.17.133:8000/getnewuuid'
    result = requests.get(url)
    print('Your room_id is ' + result.text)
    return result.text
    
def initroom(needToCreatNewRoom,room_id,username): #needToCreatNewRoom 為 True/False 
    my_data = {'needToCreatNewRoom': str(needToCreatNewRoom), 
               'room_id':room_id, 
               'username':username
               }
    url = 'http://10.147.17.133:8000/initroom'
    result = requests.post(url, data = my_data)
    
    #--- debug only ---
    # print('initnewgame - status : ' + str(result.status_code))
    if(result.status_code==200):
        print(result.text)

def getdata(room_id):
    url = 'http://10.147.17.133:8000/getdata?room={}'.format(str(room_id)) 
    result = requests.get(url)
    #--- debug only ---
    '''
    print('getdata - status : ' + str(result.status_code))
    if(result.status_code==200):
        print(result.text)
    '''
    return result.text

def initgame():
    pass


def updatedata(room_id,player_id,hp,mp,move_left,move_right,shoot,jump,in_air):
    my_data = {'room_id': room_id, 
               'player_id':player_id, 
               'hp':hp,
               'mp':mp,
               #'position_x':position_x,
               #'position_y':position_y
               'move_left':move_left,
               'move_right':move_right,
               'shoot':shoot,
               'jump':jump,
               'in_air':in_air
               }
    url = 'http://10.147.17.133:8000/updatedata'
    result = requests.post(url, data = my_data)
    
    #--- debug only ---
    '''
    print('updatedata - status : ' + str(result.status_code))
    if(result.status_code==200):
        print(result.text)
    '''
    return result.text


# data for test API updatedata
'''
room_id = 'myroom'
player_id = 'player1'
hp = 890
mp = 900 
position_x = 200 
position_y = 10
'''





