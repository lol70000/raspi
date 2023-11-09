from classes import FullscreenWindow,newsApi,clock
from newsapi import NewsApiClient
import threading
import tkinter as tk
import grovepi
import time
"from events import Events"
from WorldTimeAPI import service as serv

def initialise_libs():
    clo = clock()

    disp=["author","title"]
    req = ["Formel 1","general"]

    root = tk.Tk()
    app = FullscreenWindow(root,"black",800,480,disp)
    root.mainloop()

initialise_libs()