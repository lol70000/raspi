"""
This is my api key for the news api:
50481567b2e445c29cf4451867a2c398
"""


"""
from test import pie

raspipie = pie()
raspipie.printing("hello")
"""
"newsapi = NewsApiClient(api_key='50481567b2e445c29cf4451867a2c398')"
from classes import FullscreenWindow,newsApi
from newsapi import NewsApiClient
import threading

import tkinter as tk

req=["author","title"]
news= newsApi()
requests = news.request(req,"4")
print(requests)

if __name__ == "__main__":
    root = tk.Tk()
    app = FullscreenWindow(root,"white",800,480)
    app.add_label(requests[1],150,240)
    root.mainloop()