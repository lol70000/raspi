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
from newsapi import NewsApiClient
import tkinter as tk

window = tk.Tk()
window.attributes("-fullscreen")

widt= 800
heigh= 480

frame = tk.Frame(master=window,width=int(widt),height=int(heigh),bg="red")
frame.pack(fill=tk.BOTH)

btn_ext= tk.Button(text="X",command=window.destroy,bg="red")

label = tk.Label(master=frame,text="Hello World", bg="red")
label.place(x=widt/2, y=heigh/2)

window.mainloop()