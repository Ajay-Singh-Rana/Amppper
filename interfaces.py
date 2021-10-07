# h3avren

"""
Here I will define all the classes that are inherited by the other 
modules in order to implement common functionalities
"""

# imports
import os
from tkinter import filedialog
import tkinter as tk
import threading

# a class to browse files and implement the common frame
class CFrame(tk.Frame):
    """
    This class implements the frame 
    that i'll be using in different tool windows
    to display the different functionalities that
    can be used under that tool
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.filename = ''
        self.thread = 0
        self.controller = controller
        self.config(bg = '#2AA2BC')

    def browse(self,present = 1):
        self.filename = filedialog.askopenfilename()
        if(self.filename and present):
            self.label.config(text = os.path.split(self.filename)[1])

    def run_thread(self,target_func):
        self.thread += 1
        thread = threading.Thread(target = target_func)
        thread.start()

# a class to create the common window for all the tools
class StandardWindow(tk.Frame):
    """
    This is the frame that i'll be using
    as a window for different tools and their
    respective functionalities
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.frames = {}
        self.background_img = tk.PhotoImage(file = 'icons/amppper.png')
        im_height,im_width = self.background_img.height(), self.background_img.width()

        self.background = tk.Canvas(self,height = im_height,width = im_width)
        self.background.pack(fill = 'both',expand = True)

        self.background.create_image(0,0,image = self.background_img,anchor = 'nw')

        self.container = tk.Frame(self,width = 300,height = 250)
        self.container.place(x = 155,y = 160)

        button = tk.Button(self.background,text = 'Home',width = 5,
        command = lambda:self.controller.show_frame('MainFrame'),relief = 'flat',
        bg = '#2abc8d',activebackground = '#aabc8d')
        button.place(x = 430,y = 30)
    
    def show_frame(self,page_name,window_title,title):
        frame = self.frames[page_name]
        frame.tkraise()
        self.controller.title(f'Amppper -> {window_title} -> {title}')