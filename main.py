from classes import FullscreenWindow,newsApi,clock
from newsapi import NewsApiClient
import threading
import tkinter as tk
import grovepi
import time
import ev
from WorldTimeAPI import service as serv

def initialise_clock():
    clo = clock()

value = 0
def initialise_libs():
    disp=["author","title"]
    req = ["Formel 1","general"]

    root = tk.Tk()
    app = FullscreenWindow(root,"black",800,480,disp)
    root.mainloop()

x = threading.Thread(target=initialise_clock)
y= threading.Thread(target=initialise_libs)
x.start()
y.start()
x.join()
y.join()