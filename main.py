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

window= tk.Tk()
window.attributes("-fullscreen",True)

widt= 763
heigh= 480

frame = tk.Frame(master=window,width=int(widt),bg="red",height=int(heigh))
frame.pack(fill=tk.BOTH)

btn_ext= tk.Button(master=window,text="X",bg="blue",command=window.destroy)
btn_ext.place(x=widt,y=0)

label = tk.Label(master=frame,text="Hello World", bg="red")
label.place(x=widt/2, y=heigh/2)

window.mainloop()