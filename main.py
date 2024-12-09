import asyncio
import json
import os
from tkinter import *
from tkinter import ttk
import requests
import pygame as pg
from io import BytesIO
import main_post
import subprocess

game_code = input("Write game code: ")
player_code = input("Write your player code: ")

url = "http://127.0.0.1:8000/get/"
data = {
    "game_code": game_code,
    "player_code": player_code,
    "start": "00",
    "end": "00"
}
response = requests.get(url, json=data)
data_inf = json.loads(response.text)[0]['fields_chess']

def req():
        url = "http://127.0.0.1:8000/post/"
        data = {
            "game_code": game_code,
            "player_code": player_code,
            "start": start.get(),
            "end": end.get()
        }

        response = requests.post(url, json=data)
        label["text"] = response.text

root = Tk()
root.title("ChessPost")
root.geometry("250x200")

start = ttk.Entry()
start.pack(anchor=NW, padx=6, pady=6)
end = ttk.Entry()
end.pack(anchor=NW, padx=6, pady=6)


btn = ttk.Button(text="Request", command=req)
btn.pack(anchor=NW, padx=6, pady=6)

label = ttk.Label()
label.pack(anchor=NW, padx=6, pady=6)




pg.init()
pg.font.init()
pg_font = pg.font.SysFont('Comic Sans MS', 30)

RES = WIDTH, HEIGHT = 600, 600
sc = pg.display.set_mode(RES)
pg.display.set_caption("Chess")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLEDZOLOT = (238, 232, 170)
OHRA = (160, 82, 45)

FPS = 1
size = 75
clock = pg.time.Clock()

FIGURES_PATH = "figures_img"

def load_figures():
    images = {}
    for file in os.listdir(FIGURES_PATH):
        if file.endswith(".png"):
            key = file.split(".")[0]
            image = pg.image.load(os.path.join(FIGURES_PATH, file))
            images[key] = pg.transform.scale(image, (size, size))
    return images

figures_images = load_figures()

def get_figure_key(owner, figure_type):
    owner_code = "0" if owner == "white" else "1"
    type_code = {
        "pawn": "P",
        "rook": "R",
        "knight": "H",
        "bishop": "B",
        "queen": "Q",
        "king": "K",
    }
    return f"{type_code[figure_type]}{owner_code}"

def chess_to_screen(col, row):
    x = (ord(col) - ord('a')) * size
    y = (8 - int(row)) * size
    return x, y


board = pg.Surface((700, 700))
board.fill(WHITE)
for x in range(8):
    for y in range(8):
        color = BLEDZOLOT if (x + y) % 2 == 0 else OHRA
        pg.draw.rect(board, color, [size * x, size * y, size, size])

def draw_figures(surface, data):
    for row, cols in data.items():
        for col, cell in cols.items():
            if cell['figure']:
                x, y = chess_to_screen(col, row)
                figure_key = get_figure_key(cell['owner'], cell['type'])
                if figure_key in figures_images:
                    surface.blit(figures_images[figure_key], (x, y))


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    sc.blit(board, (0, 0))
    url = "http://127.0.0.1:8000/get/"
    data = {
        "game_code": game_code,
        "player_code": player_code,
        "start": "00",
        "end": "00"
    }
    response = requests.get(url, json=data)
    data_inf = json.loads(response.text)[0]['fields_chess']
    draw_figures(sc, data_inf)
    pg.display.flip()


    root.update()
    clock.tick(FPS)



