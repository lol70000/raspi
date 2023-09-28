import tkinter as tk
from newsapi import NewsApiClient

class FullscreenWindow:
    def __init__(self, root,color,widt,heigt):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.frame = tk.Frame(master=root,bg=color,width=widt,height=heigt)
        self.frame.pack()
        self.create_destry_button(widt-83,0)

    def create_destry_button(self,widt,heigh):
        button1 = tk.Button(master=self.frame, text="Button 1", command=self.root.destroy)
        button1.place(x=widt,y=heigh)

    def add_label(self,text,xx,yy):
        label = tk.Label(master=self.frame,text=str(text))
        label.place(x=xx,y=yy)

class newsApi:
    def __init__(self):
        self.api = NewsApiClient(api_key='50481567b2e445c29cf4451867a2c398')

    def request(self,requirements,numberof):
        topnews = [];
        x=0
        rawnews = self.api.get_top_headlines(language="de",country="ch")
        while x < int(numberof):
            topnews.append(rawnews["articles"][x][str(requirements[0])])
            topnews.append(rawnews["articles"][x][str(requirements[1])])
            x+=1
        return topnews
        """print(topnews)"""