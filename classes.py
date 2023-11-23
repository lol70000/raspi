import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from newsapi import NewsApiClient
import grovepi
import threading
import ev
import time
from WorldTimeAPI import service as serv

global wake_up_time
wake_up_time = 0
class FullscreenWindow:
    def __init__(self, root,color,widt,heigt,disp):
        self.root = root
        self.root.option_add("*TCombobox*Listbox.font", "Calibri 16")
        "self.root.attributes('-fullscreen', True)"
        self.bgcolor = color
        self.fgcolor = "white"
        self.widt= widt
        self.heigh = heigt
        self.buttonfont = ("Calibri",12)
        self.fontsize = 12
        self.font = ("Calibri",16)
        self.news = newsApi()
        self.disp = disp
        self.makeinitialframe()
        if ev.buzzing==1 :
            self.silence_button()
        
    def makeinitialframe(self):
        self.frame = tk.Frame(master=self.root,bg=self.bgcolor,width=self.widt,height=self.heigh)
        self.frame.pack()
        self.create_destry_button(self.widt-83,0)
        self.create_settings_button(self.heigh)
        
    def create_destry_button(self,widt,heigh):
        button1 = tk.Button(master=self.frame, text="X",bg="red",fg=self.fgcolor, command=self.root.destroy,font=self.buttonfont)
        button1.configure(highlightbackground=self.bgcolor,highlightcolor=self.fgcolor)
        button1.place(x=widt+45,y=heigh)
        
        
    def create_settings_button(self,heir):
        butto = tk.Button(master=self.frame,text="settings",bg="blue",fg=self.fgcolor,command=self.settingsscreen,font=self.buttonfont)
        butto.configure(highlightbackground=self.bgcolor,highlightcolor=self.fgcolor)
        butto.place(x=0,y=0)

    def add_label(self,text,xx,yy):
        label = tk.Label(master=self.frame,text=str(text),bg=self.bgcolor,fg=self.fgcolor,font=self.font)
        label.place(x=xx,y=yy)

    def get_selected_time(self):
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        time_str = [str(hour),":",str(minute)]
        time = ''.join(time_str)
        print(time)
        self.wake_up_time = time
        ev.wakeuptime=time
        print(self.wake_up_time)
        self.frame.destroy

    def silence_button(self):
        self.sil_but = tk.Button(master=self.frame,text="Let me sleeeeeep!",bg=self.bgcolor,fg=self.fgcolor,font=self.buttonfont,command=self.silence)
        self.sil_but.configure(highlightbackground=self.bgcolor,highlightcolor=self.fgcolor)
        self.sil_but.place(x=200,y=200)
        self.list = self.news.request(self.disp,4)
        self.add_all_infos(self.list,20,200)

    def silence(self):
        ev.buzzing = 0
        self.sil_but.destroy

    def rest_shit(self):
        hour_label = tk.Label(self.frame2, text="Hour:",bg=self.bgcolor,fg=self.fgcolor,font=self.font)
        hour_label.place(relx=0.5,rely=0.35,anchor="center")
        self.hour_var = tk.StringVar()
        hour_entry = ttk.Combobox(self.frame2, textvariable=self.hour_var, values=[str(i).zfill(2) for i in range(24)],font=self.font)
        hour_entry.place(relx=0.5,rely=0.425,anchor="center")
        hour_entry.set("00")

        minute_label = tk.Label(self.frame2, text="Minute:",bg=self.bgcolor,fg=self.fgcolor,font=self.font)
        minute_label.place(relx=0.5,rely=0.5,anchor="center")
        self.minute_var = tk.StringVar()
        minute_entry = ttk.Combobox(self.frame2, textvariable=self.minute_var, values=[str(i).zfill(2) for i in range(60)],font=self.font)
        minute_entry.place(relx=0.5,rely=0.575,anchor="center")
        minute_entry.set("00")

        submit_button = tk.Button(self.frame2, text="Submit", command=self.get_selected_time,bg="orange",fg=self.fgcolor,font=self.font)
        submit_button.place(relx=0.5,rely=0.65,anchor="center")

    def backbutton(self):
        back_button = tk.Button(master=self.frame2,text="<--",bg="grey",fg=self.fgcolor,command=self.frame2.destroy,font=self.font)
        back_button.configure(highlightbackground=self.bgcolor,highlightcolor=self.fgcolor)
        back_button.place(x=0,y=0)

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
        self.frame2 = tk.Frame(master=self.frame,bg=self.bgcolor,width=self.widt,height=self.heigh)
        self.frame2.pack()
        self.create_destry_button(self.widt-83,0)
        self.backbutton()
        self.rest_shit()
        self.frame2.mainloop()
        

class newsApi:
    def __init__(self):
        self.api = NewsApiClient(api_key='50481567b2e445c29cf4451867a2c398')

    def request(self,displaying,numberof):
        topnews = []
        x=0
        rawnews = self.api.get_top_headlines(language="de",country="ch")
        while x < int(numberof):
            topnews.append(rawnews["articles"][x][str(displaying[0])])
            topnews.append(rawnews["articles"][x][str(displaying[1])])
            x+=1
        return topnews
    
    def request_requirements(self,displaying,numberof,requirements):
        topnews = []
        x=0
        rawnews = self.api.get_top_headlines(language="de",country="ch",q=requirements[0],category=requirements[1])
        while x < numberof:
            topnews.append(rawnews["articles"][x][str(displaying[0])])
            topnews.append(rawnews["articles"][x][str(displaying[1])])
            x+=1
        return topnews
    

class clock:
    def __init__(self):
        self.myclient = serv.Client('timezone')
        self.requests = {"area":"Europe","location":"Zurich"}
        self.buz= buzzer()
        self.checking()

    def getresponse(self):
        response = self.myclient.get(**self.requests)
        datentime = response.datetime
        dateotime = datentime.split('T')
        timeonly = dateotime[1].split('.')
        puretime = timeonly[0]
        purertime = puretime.split(':')
        purertime.pop()
        purertime.insert(1,":")
        self.finaltime = ''.join(purertime)

    def checking(self):
        print("hello im here")
        self.getresponse()
        while ev.wakeuptime!= self.finaltime:
            print(self.finaltime)
            print(ev.wakeuptime)
            print("working..")
            self.getresponse()
            if ev.wakeuptime == self.finaltime:
                break
        print("got it...")
        ev.buzzing = 1
        print (ev.buzzing)
        self.wakeup()
    
    def wakeup(self):
        while ev.buzzing == 1:
            self.buz.buzing()
            print("buz")
            time.sleep(3)
            self.buz.stop_buzzing()
            print("no buz")
            time.sleep(3)

class buzzer:
    def __init__(self):
        self.buz_port = 8
        grovepi.pinMode(self.buz_port,"OUTPUT")

    def buzing(self):
        grovepi.digitalWrite(self.buz_port,1)

    def stop_buzzing(self):
        grovepi.digitalWrite(self.buz_port,0)