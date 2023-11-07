import tkinter as tk
from newsapi import NewsApiClient
import grovepi
import threading
from WorldTimeAPI import service as serv

class FullscreenWindow:
    def __init__(self, root,color,widt,heigt,disp):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.bgcolor = color
        self.fgcolor = "white"
        self.widt= widt
        self.heigh = heigt
        self.buttonfont = ("Helvetica",12)
        self.fontsize = 12
        self.font = ("Helvetica",16)
        news = newsApi()
        butt=button()
        self.list = news.request(disp,4)
        x = threading.Thread(target=self.makeinitialframe())
        y= threading.Thread(target=butt.status())
        x.start()
        y.start()
        if (y ==1):
            self.settingsscreen()


    def makeinitialframe(self):
        self.frame = tk.Frame(master=self.root,bg=self.bgcolor,width=self.widt,height=self.heigh)
        self.frame.pack()
        self.create_destry_button(self.widt-83,0)
        
    def create_destry_button(self,widt,heigh):
        button1 = tk.Button(master=self.frame, text="X",bg="red",fg=self.fgcolor, command=self.root.destroy,font=self.buttonfont)
        button1.configure(highlightbackground=self.bgcolor,highlightcolor=self.fgcolor)
        button1.place(x=widt+45,y=heigh)
        self.add_all_infos(self.list,20,200)

    def add_label(self,text,xx,yy):
        label = tk.Label(master=self.frame,text=str(text),bg=self.bgcolor,fg=self.fgcolor,font=self.font)
        label.place(x=xx,y=yy)

    def add_all_infos(self,list,xx,yy):
        x=0
        y = yy
        abst = self.fontsize
        if(len(list)%2 ==0):
            y+= abst/2
        m=0
        while(len(list)/2>m):
            y+=self.fontsize
            y+=abst
            m+=1
        while(x<len(list)):
            label = tk.Label(master=self.frame,text=str(list[x]),bg=self.bgcolor,fg=self.fgcolor,font=self.font)
            label.place(x=xx,y=y)
            y-=abst
            y-=self.fontsize
            x+=1

    def settingsscreen(self):
        self.frame.destroy()
        self.frame = tk.Frame(master=self.root,bg=self.bgcolor,width=self.widt,height=self.heigh)
        self.frame.pack()
        self.create_destry_button(self.widt-83,0)

class newsApi:
    def __init__(self):
        self.api = NewsApiClient(api_key='50481567b2e445c29cf4451867a2c398')

    def request(self,displaying,numberof):
        topnews = [];
        x=0
        rawnews = self.api.get_top_headlines(language="de",country="ch")
        while x < int(numberof):
            topnews.append(rawnews["articles"][x][str(displaying[0])])
            topnews.append(rawnews["articles"][x][str(displaying[1])])
            x+=1
        return topnews
    
    def request_requirements(self,displaying,numberof,requirements):
        topnews = [];
        x=0
        rawnews = self.api.get_top_headlines(language="de",country="ch",q=requirements[0],category=requirements[1])
        while x < numberof:
            topnews.append(rawnews["articles"][x][str(displaying[0])])
            topnews.append(rawnews["articles"][x][str(displaying[1])])
            x+=1
        return topnews
    

class clock:
    def __init__(self):
        myclient = serv.Client('timezone')
        requests = {"area":"Europe","location":"Zurich"}
        response = myclient.get(**requests)
        datentime = response.datetime
        dateotime = datentime.split('T')
        timeonly = dateotime[1].split('.')
        self.puretime = timeonly[0]
        print(self.puretime)

class button:
    def __init__(self):
        grovepi.set_bus('RPI_1');
        self.buttonPort = 2
        grovepi.pinMode(self.buttonPort, "INPUT")

    def status(self):
        while(grovepi.digitalRead(self.buttonPort)==0):
            self.status()
            print(0)
        return grovepi.digitalRead(buttonPort)