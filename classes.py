import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from newsapi import NewsApiClient
import datetime
import grovepi
import threading
import ev
import time
import signal
from WorldTimeAPI import service as serv

class FullscreenWindow:
    def __init__(self, root,color,widt,heigt,disp,mode):
        #here the main attributes are set
        self.root = root
        self.root.option_add("*TCombobox*Listbox.font", "Calibri 16")
        self.root.attributes('-fullscreen', True)
        self.bgcolor = color
        self.fgcolor = "white"
        self.widt= widt
        self.heigh = heigt
        #here the fonts as well as the font sizes are initialised
        self.buttonfont = ("Calibri",12)
        self.fontsize = 12
        self.font = ("Calibri",16)
        #here the news api is initialized for later use
        self.news = newsApi()
        self.disp = disp
        #here it is checked if the new instance of Fullscreen widow will be used for the silence frame or not
        #this is because the funktion wich checks if it is needed is running in another thread and it was easier to make a new window than to make an event
        if mode == "silence":
            self.makesilenceframe()
        else:
            self.makeinitialframe()

    def makesilenceframe(self):
        #here the silence frame is made with the appropriate buttonone to close the window and one to add the silence button wich turns the buzzer off
        self.silframe = tk.Frame(master=self.root,bg=self.bgcolor,width=self.widt,height=self.heigh)
        self.silframe.pack()
        self.create_sil_destry_button(self.widt-95,0)
        self.silence_button()
        
    def create_sil_destry_button(self,widt,heigh):
        #here the exit Button fpr the silence window is made with the function stop_all_action as its command when pressed
        button1 = tk.Button(master=self.silframe, text="Exit",bg="green",fg=self.fgcolor, command=self.stop_all_action,font=self.buttonfont)
        button1.configure(highlightbackground=self.bgcolor,highlightcolor=self.fgcolor)
        button1.place(x=widt+45,y=heigh)
        
    def makeinitialframe(self):
        #here the frame for a non silence window is made it only has the most necesary buttons in it (one to close the application and one to the settings)
        #this is sonce this is the screen that would be shown if it were to be used as a alarmclock
        self.frame = tk.Frame(master=self.root,bg=self.bgcolor,width=self.widt,height=self.heigh)
        self.frame.pack()
        self.create_destry_button(self.widt-83,0)
        self.create_settings_button(self.heigh)
        
    def create_destry_button(self,widt,heigh):
        #the destroy button fpr the nonsilence frame is declared with all the apropriate values
        button1 = tk.Button(master=self.frame, text="X",bg="red",fg=self.fgcolor, command=self.stop_all_action,font=self.buttonfont)
        button1.configure(highlightbackground=self.bgcolor,highlightcolor=self.fgcolor)
        button1.place(x=widt+45,y=heigh)

    def stop_all_action(self):
        #here the buzzing is set to zero so that it dosn't buzz when closing the window and then the window is destroyed
        ev.buzzing=0
        self.root.destroy()
        
    def create_settings_button(self,heir):
        #the button wich leads you to the settings is made and given the appropriate function
        butto = tk.Button(master=self.frame,text="settings",bg="blue",fg=self.fgcolor,command=self.settingsscreen,font=self.buttonfont)
        butto.configure(highlightbackground=self.bgcolor,highlightcolor=self.fgcolor)
        butto.place(x=0,y=0)

    def add_label(self,text,xx,yy):
        #this is the function to add a label with the text of your choice
        label = tk.Label(master=self.frame2,text=str(text),bg=self.bgcolor,fg=self.fgcolor,font=self.font)
        label.place(x=xx,y=yy)

    def silence_button(self):
        #this function is here to add the button wich would turn of the buzzer off when you are beeing woke up hence the text of the button
        self.sil_but = tk.Button(master=self.silframe,text="Let me sleeeeeep!",bg=self.bgcolor,fg=self.fgcolor,font=self.buttonfont,command=self.silence)
        self.sil_but.configure(highlightbackground=self.bgcolor,highlightcolor=self.fgcolor)
        self.sil_but.place(x=340,y=200)
        
    def silence(self):
        #this function gets called by the silence button when pressed it gets the api response of the above mentioned News API and also sets the buzzer to stop buzzing
        #additionaly it calls the function, wich adds all the news wich it has gotten from the api request to the screen, and destroy the silence button.
        ev.buzzing = 0
        self.list = self.news.request(self.disp,4)
        self.add_all_infos(self.list,20,200)
        self.sil_but.destroy()


    def rest_shit(self):
        #In this function the labels and the entry for the hour and the minute are with is corresponding values wich can be chosen from, also a submit button is added
        self.wakeuptimelanel= tk.Label(self.frame2, text="Current wakeup time:"+str(ev.wakeuptime),bg=self.bgcolor,fg=self.fgcolor,font=self.font)
        self.wakeuptimelanel.place(relx=0.5,rely=0.275,anchor="center")

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

    def get_selected_time(self):
        #here the inputs of the abouve entry are being checked and added together in order to create the wanted wake up time
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        time_str = [str(hour),":",str(minute),":00"]
        time = ''.join(time_str)
        print(time)
        self.wake_up_time = time
        ev.wakeuptime=time
        print(self.wake_up_time)
        self.wakeuptimelanel.destroy()
        updatedwakeuptimelanel= tk.Label(self.frame2, text="Current wakeup time:"+str(ev.wakeuptime),bg=self.bgcolor,fg=self.fgcolor,font=self.font)
        updatedwakeuptimelanel.place(relx=0.5,rely=0.275,anchor="center")
        self.add_label("Your Time has been set",300,300)

    def backbutton(self):
        #here the button wich leads you back to the start screen out of the settingsscreen
        back_button = tk.Button(master=self.frame2,text="<--",bg="grey",fg=self.fgcolor,command=self.frame2.destroy,font=self.font)
        back_button.configure(highlightbackground=self.bgcolor,highlightcolor=self.fgcolor)
        back_button.place(x=0,y=0)

    def add_all_infos(self,list,xx,yy):
        #here all the news wich were gotten by the News APi are added to the appropriate screen
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
            #here the length of the sting is checked and if it is so long that it would go out of frame a line break is inserted
            maxlength = 85
            if len(list[x]) > maxlength:
                formattedText = '\n'.join([list[x][i:i+maxlength] for i in range(0, len(list[x]),maxlength)])
                list[x] = formattedText
            label = tk.Label(master=self.silframe,text=str(list[x]),bg=self.bgcolor,fg=self.fgcolor,font=self.font)
            label.place(x=xx,y=y)
            y-=abst
            y-=self.fontsize
            x+=1

    def settingsscreen(self):
        #here the settingsscreen is added with all its buttons
        self.frame2 = tk.Frame(master=self.frame,bg=self.bgcolor,width=self.widt,height=self.heigh)
        self.frame2.pack()
        self.create_destry_button(self.widt-83,0)
        self.backbutton()
        self.rest_shit()
        self.frame2.mainloop()
        

class newsApi:
    #here the NeWS API is initialised with the api key
    def __init__(self):
        self.api = NewsApiClient(api_key='50481567b2e445c29cf4451867a2c398')

    def request(self,displaying,numberof):
        #here the api gets its request and sorts it so that only the author and the titel are gotten
        topnews = []
        x=0
        #here it is declared from wich country and in wich language we would like the headlines
        rawnews = self.api.get_top_headlines(language="de",country="ch")
        #after the answer has been received the request is broken up and only the title and the author are added into the list
        #this is also only done for the number of articles wanted
        while x < int(numberof):
            topnews.append(rawnews["articles"][x][str(displaying[0])])
            topnews.append(rawnews["articles"][x][str(displaying[1])])
            x+=1
        return topnews
    

class clock:
    def __init__(self):
        #here the clock api is initialised and the buzzer is also called to prepare for wakeup at the requested time
        self.myclient = serv.Client('timezone')
        self.requests = {"area":"Europe","location":"Zurich"}
        self.buz= buzzer()
        #here the here the ckecking function is started and the final time is set to "00:00" so that even if the programm 
        #is not able to get a time the program will not just stop
        self.checking()
        self.finaltime = "00:00"

    def getresponse(self):
        #here the systemtime is taken and formatted
        currenttime = datetime.datetime.now()
        formatettime = currenttime.strftime("%H:%M:%S")
        self.finaltime=formatettime
        #here the time would have been gotten from an api but because it didnt have a time.sleep and the fair use policy sais no more than 1 request per minute
        #my raspberry pi has now been blocked by the api
        """
        try:
            response = self.myclient.get(**self.requests)
            datentime = response.datetime
            dateotime = datentime.split('T')
            timeonly = dateotime[1].split('.')
            puretime = timeonly[0]
            purertime = puretime.pop()
            self.finaltime = ''.join(purertime)
        except:
            print("JSON DECODE EROR")
            self.finaltime= "00:00"
        """

    def checking(self):
        #this function is constantly running and checking if the desired wakeup time has been reached
        print("hello im here")
        print(ev.wakeuptime)
        self.getresponse()
        print(self.finaltime)
        while ev.wakeuptime!= self.finaltime:
            print(self.finaltime)
            print(ev.wakeuptime)
            print("working..")
            self.getresponse()
            time.sleep(0.2)
            if ev.wakeuptime == self.finaltime:
                self.preparing()

    def preparing(self):
        #this function is there to start the prozess of threading
        print("got it...")
        ev.buzzing = 1
        print (ev.buzzing)
        self.threading()

    def threading(self):
        # this function is here to start the buzzing and also to make the window where you can silence the buzzer and where the news will be displayed
        one = threading.Thread(target=self.wakeup)
        two = threading.Thread(target=self.makesilencewindow)
        one.start()
        two.start()
        one.join()
        two.join()

    def makesilencewindow(self):
        #this is the function to lauch another instance of tkinter and make another window wich will then be the silence window
        root2 = tk.Tk()
        disp=["author","title"]
        app2 = FullscreenWindow(root2,"black",800,480,disp,"silence")
        root2.mainloop()
    
    def wakeup(self):
        #this function is running while the buzzer buzes and restarts the ckecking prozess when stoped
        while ev.buzzing == 1:
            self.buz.buzing()
            print("buz")
            time.sleep(0.1)
            self.buz.stop_buzzing()
            print("no buz")
            time.sleep(0.1)
        self.checking()

class buzzer:
    #here the buzzer is initialised
    def __init__(self):
        self.buz_port = 8
        grovepi.pinMode(self.buz_port,"OUTPUT")

    def buzing(self):
        #the buzzer is set to buz
        grovepi.digitalWrite(self.buz_port,1)

    def stop_buzzing(self):
        #the buzer is set to stop buzzing
        grovepi.digitalWrite(self.buz_port,0)

class Gracefullkiller:
    #this class is there to stop the buzzer to stop buzzing when the programm is stopped while still buzzing
    killnow = False
    def __init__(self):
        signal.signal(signal.SIGINT,self.exitgracefully)
        signal.signal(signal.SIGTERM, self.exitgracefully)

    def exitgracefully(self, *args):
        buz=buzzer()
        buz.stop_buzzing()
        self.killnow = True