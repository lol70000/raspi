import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from newsapi import NewsApiClient
import grovepi
import threading
from WorldTimeAPI import service as serv

class FullscreenWindow:
    def __init__(self, root,color,widt,heigt,disp):
        self.root = root
        self.root.option_add("*TCombobox*Listbox.font", "Calibri 16")
        self.root.attributes('-fullscreen', True)
        self.bgcolor = color
        self.fgcolor = "white"
        self.widt= widt
        self.heigh = heigt
        self.buttonfont = ("Calibri",12)
        self.fontsize = 12
        self.font = ("Calibri",16)
        news = newsApi()
        self.list = news.request(disp,4)
        self.makeinitialframe()

    def makeinitialframe(self):
        self.frame = tk.Frame(master=self.root,bg=self.bgcolor,width=self.widt,height=self.heigh)
        self.frame.pack()
        self.create_destry_button(self.widt-83,0)
        self.add_all_infos(self.list,20,200)
        
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
        time_str = hour,":",minute
        outputstr= "You selected the time: ",str(time_str)
        messagebox.showinfo("Selected Time", outputstr)

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
        self.create_settings_button(self.heigh)

    def settingsscreen(self):
        self.frame2 = tk.Frame(master=self.frame,bg=self.bgcolor,width=self.widt,height=self.heigh)
        self.frame2.pack()
        self.create_destry_button(self.widt-83,0)
        self.backbutton()
        self.rest_shit()
        self.root.mainloop()

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
"""
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

"""