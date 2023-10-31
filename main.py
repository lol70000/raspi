from classes import FullscreenWindow,newsApi,clock
from newsapi import NewsApiClient
import threading
import tkinter as tk

from WorldTimeAPI import service as serv

clo = clock()

disp=["author","title"]
req = ["Formel 1","general"]
news= newsApi()
requests = news.request(disp,4)
print(requests)

if __name__ == "__main__":
    root = tk.Tk()
    app = FullscreenWindow(root,"black",800,480)
    app.add_all_labels(requests,40,240)
    root.mainloop()