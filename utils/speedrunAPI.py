import json, requests, sqlite3 as sql
import os

#angler 5wknq6vw, Bathtub (vide): xd0ezz49

conn = sql.connect(os.path.join(os.path.dirname(__file__), 'speedruncom.sqlite'))


base = 'https://www.speedrun.com/api/v1'
JCid = 'w6jl8w2d' #https://www.speedrun.com/api/v1/games?name=Jumpcraft

def req(url):
    return requests.get(f'{base}{url}').json()

def levels():
    return req('/games/w6jl8w2d/levels')

def lvlID(level):
    return conn.execute('SELECT id FROM levels WHERE name = ?', (level.title(),)).fetchone()[0]

def difficulty(level):
    return conn.execute('SELECT difficulty FROM levels WHERE name = ?', (level.title(),)).fetchone()[0]

def leaderboard(level):
    id = lvlID(level)
    return req(f'/levels/{id}/records')

def username(id):
    return req(f'/users/{id}')['data']['names']['international']

def link(level):
    id = lvlID(level)
    return req(f'/levels/{id}')['data']['weblink']
