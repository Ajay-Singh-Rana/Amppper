# h3avren

"""
This file contains all the code for the video processing part of the application
"""

import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from moviepy.editor import VideoFileClip
from interfaces import CFrame, StandardWindow


# a class to implement the functionality to mute for extract audio 
class Mute(CFrame):
    def __init__(self,parent,controller):
        CFrame.__init__(self,parent,controller)
        
        self.file_label = tk.Label(self,text = '---Empty Selection---',
        padx = 10,pady = 5,bg = '#ee3456')
        self.file_label.grid(row = 0,column = 0,padx = 10,pady = 10)

        self.add = tk.Button(self,text = 'Select File',command = self.browse,
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10)
        self.add.grid(row = 0, column = 1,padx = 10)

        self.mute = tk.Button(self,text= 'Mute',
        command = lambda: self.run_thread(self.mute_file),
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10)
        self.mute.grid(row = 1,columnspan = 2,padx = 10)

        self.status = tk.Label(self,text = 'No process..!',
        width = 20,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.status.grid(row = 2,column = 0,padx = 10,pady = 5)

        self.queue = tk.Label(self,text = 'Queued : 0',
        width = 10,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.queue.grid(row = 2,column = 1,padx = 10,pady = 5)

    def mute_file(self):
        try:
            clip = VideoFileClip(self.filename)
            clip.write_videofile(self.filename,audio = False)
        except:
            messagebox.showerror(title = 'Error',message = 'Error muting video')


class Extract(CFrame):
    def __init__(self,parent,controller):
        CFrame.__init__(self,parent,controller)
        self.save_as = ''
        
        self.file_label = tk.Label(self,text = '---Empty Selection---',
        padx = 10,pady = 5,bg = '#ee3456')
        self.file_label.grid(row = 0,column = 0,padx = 10,pady = 10)

        self.add = tk.Button(self,text = 'Select File',command = self.browse,
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10)
        self.add.grid(row = 0, column = 1,padx = 10)

        self.export_as = ttk.Combobox(self,
        values = ('mp3','flv','ogg','wav','wma','avi'),state = 'readonly')

        self.export_as.grid(row = 1, column = 0,padx = 10,pady = 10)
        self.export_as.current(0)

        self.extract = tk.Button(self,text= 'Extract',
        command = lambda: self.run_thread(self.extract_file),
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10)
        self.extract.grid(row = 1,column = 1,padx = 10)

        self.status = tk.Label(self,text = 'No process..!',
        width = 20,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.status.grid(row = 2,column = 0,padx = 10,pady = 5)

        self.queue = tk.Label(self,text = 'Queued : 0',
        width = 10,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.queue.grid(row = 2,column = 1,padx = 10,pady = 5)

    def extract_file(self):
        self.saveas = filedialog.asksaveasfilename()
        try:
            clip = VideoFileClip(self.filename)
            clip.audio.write_audiofile(self.save_as,audio = False)
        except:
            messagebox.showerror(title = 'Error',message = 'Error converting to audio')



# a class to implement the join of two video files
class JoinVideo(CFrame):
    def __init__(self,parent,controller):
        CFrame.__init__(self,parent,controller)
        self.filename_1,self.filename_2 = None,None

        self.filelabel_1 = tk.Label(self,text = '---Empty Selection---',
        padx = 10,pady = 5,bg = '#ee3456')
        self.filelabel_1.grid(row = 0,column = 0,padx = 10,pady = 10)

        self.add_1 = tk.Button(self,text = 'Select File',command = lambda: self.browse(1),
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10)
        self.add_1.grid(row = 0, column = 1,padx = 10)

        self.filelabel_2 = tk.Label(self,text = '---Empty Selection---',
        padx = 10,pady = 5,bg = '#ee3456')
        self.filelabel_2.grid(row = 0,column = 0,padx = 10,pady = 10)

        self.add_2 = tk.Button(self,text = 'Select File',command = lambda: self.browse(2),
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10)
        self.add_2.grid(row = 0, column = 1,padx = 10)

    def browse(self,num):
        CFrame.browse(self,0)
        if(num == 1):
            self.filename_1 = self.filename
            if(self.filename_1):
                self.filelabel_1.config(text = os.path.split(self.filename_1)[1])

        if(num == 2):
            self.filename_2 = self.filename
            if(self.filename_2):
                self.filelabel_2.config(text = os.path.split(self.filename_1)[1])


# this class implements the video tools window
class VideoEditor(StandardWindow):
    def __init__(self,parent,controller):
        StandardWindow.__init__(self,parent,controller)

        mute = tk.Button(self,text = 'Mute',bg = '#2abc8d',
        activebackground = '#aabc8d',relief = 'flat',width = 5,
        command = lambda: self.show_frame('Mute','Video Tools','Mute'))
        mute.place(x = 30,y = 30)

        extract = tk.Button(self,text = 'Extract',bg = '#2abc8d',
        activebackground = '#aabc8d',relief = 'flat',width = 5,
        command = lambda: self.show_frame('Extract','Video Tools','Extract'))
        extract.place(x = 130,y = 30)

        join_video = tk.Button(self,text = 'Join',bg = '#2abc8d',
        activebackground = '#aabc8d',relief = 'flat',width = 5,
        command = lambda: self.show_frame('JoinVideo','Video Tools','Join'))
        join_video.place(x = 230,y = 30)

        for f in (Mute,Extract,JoinVideo):
            page_name = f.__name__
            frame = f(parent = self.container,controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0,column = 0,sticky = 'nesw')
        
