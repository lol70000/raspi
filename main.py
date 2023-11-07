from classes import FullscreenWindow,newsApi,clock,button
from newsapi import NewsApiClient
import threading
import tkinter as tk
import grovepi
from WorldTimeAPI import service as serv

run = True

clo = clock()

disp=["author","title"]
req = ["Formel 1","general"]

root = tk.Tk()
app = FullscreenWindow(root,"black",800,480,disp)
root.mainloop()
