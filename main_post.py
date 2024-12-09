import json
import os
import asyncio
import requests
import pygame as pg
from io import BytesIO
from tkinter import *
from tkinter import ttk

async def run(game_code, player_code):
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

    root.mainloop()

