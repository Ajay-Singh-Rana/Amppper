# h3avren

"""
This file contains all the functions that will be used for audio processing in the main application
"""

# imports
from pydub import AudioSegment
import tkinter as tk
import os
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import threading

class ChangeFormat(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.config(bg = '#2AA2BC')

        formats = ttk.Combobox(self,state = 'readonly',values = ('.mp3','.flv','.ogg','.wav','.wma','.avi','.aac','.m4a','flac','opus','au','aiff','webm'))
        formats.pack(padx = 10,pady = 20)

        formats.current(0)

class JoinAudio(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.filename_1 ,self.filename_2 = None,None
        self.config(bg = '#2AA2BC')
        self.thread_count = 0

        self.file_label_1 = tk.Label(self,text = '---Empty Selection---',width = 20)
        self.file_label_1.grid(row = 0,column = 0,padx= 10,pady = 10)

        add_1 = tk.Button(self,text = 'Select File',command = lambda:self.browse_file(1),relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d')
        add_1.grid(row = 0,column = 1,padx = 10,pady = 10)

        self.file_label_2 = tk.Label(self,text = '---Empty Selection---',width = 20)
        self.file_label_2.grid(row = 1,column = 0,padx = 10,pady =10)

        add_2 = tk.Button(self,text='Select File',relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d',command = lambda:self.browse_file(2))
        add_2.grid(row = 1,column = 1,padx = 10,pady =10)

        self.export_as = ttk.Combobox(self,values = ('mp3','flv','ogg','wav','wma','avi','aac','m4a','flac','opus','au','aiff','webm'),state = 'readonly')
        self.export_as.grid(row = 2, column = 0,padx = 10,pady = 10)

        self.export_as.current(0)

        join_ = tk.Button(self,text='Join',relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d',command = self.run_thread)
        join_.grid(row = 2,column = 1,padx = 10,pady = 10)

        self.label = tk.Label(self,text = 'No processs...',width = 20,bg = '#2a8d12',fg = 'White',relief = 'sunken')
        self.label.grid(row = 3,column = 0)

        self.queue = tk.Label(self,text = 'Queued : 0',width = 10,bg = '#2a8d12',fg = 'White',relief = 'sunken')
        self.queue.grid(row = 3,column = 1,padx = 10,pady = 10)
    
    def browse_file(self,num):
        filename = filedialog.askopenfilename()
        if(num == 1):
            self.filename_1 = filename
        else:
            self.filename_2 = filename
        self.set_labels()
    
    def set_labels(self):
        if(self.filename_1):
            self.file_label_1.config(text = os.path.split(self.filename_1)[1])
        
        if(self.filename_2):
            self.file_label_2.config(text = os.path.split(self.filename_2)[1])

    def run_thread(self):
        self.thread_count += 1
        thread = threading.Thread(target = self.join_audio)
        thread.start()

    def join_audio(self):
        if(self.filename_1 and self.filename_2):
            ext = self.export_as.get()
            format_ = {'mp3':'mp3','flv':'flv','ogg':'ogg','wav':'wav','wma':'wma','avi':'avi','aac':'adts','m4a':'mp4','flac':'flac','opus':'opus','au':'au','aiff':'aiff','webm':'webm'}
            filename = filedialog.asksaveasfilename(defaultextension = f'.{ext}')
            if(filename):
                try:
                    self.label.config(text = 'Processing...',bg = '#2a8d12')
                    self.queue.config(text = f'Queued : {self.thread_count}')
                    audio_1 = AudioSegment.from_file(self.filename_1,format_[os.path.splitext(self.filename_1)[1][1:]])
                    self.filename_1 = ''
                    self.file_label_1.config(text = '---Empty Selection---')
                    audio_2 = AudioSegment.from_file(self.filename_2,format_[os.path.splitext(self.filename_2)[1][1:]])
                    self.filename_2 = ''
                    self.file_label_2.config(text = '---Empty Selection---')
                    final = audio_1 + audio_2
                    final.export(filename,format = format_[ext])
                    self.label.config(text = 'Success..!',bg = '#2a8d12')
                except:
                    self.label.config(text = 'Failed..!',bg = '#ee3456')

        else:
            messagebox.showerror(title = 'Error..!',message = 'Select the files first..!')
        
        self.thread_count -= 1
        self.queue.config(text = f'Queued : {self.thread_count}')


def change_format(file_name,to):
    pass

class AudioEditor(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        #self.geometry('610x450')
        #self.title('Amppper Audio Tools')
        #self.resizable(False,False)
        self.frames = {}
        self.background = tk.PhotoImage(file = 'icons/amppper.png')
        im_height,im_width = self.background.height(), self.background.width()

        background = tk.Canvas(self,height = im_height,width = im_width)
        background.pack(fill = 'both',expand = True)

        background.create_image(0,0,image = self.background,anchor = 'nw')

        container = tk.Frame(self,width = 300,height = 250)
        container.place(x = 155,y = 160)

        button = tk.Button(background,text = 'Convert',width = 5,command = lambda:self.show_frame('ChangeFormat'),relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d')
        button.place(x = 30,y = 30)

        audio_join = tk.Button(background,text = 'Join',width = 5,command = lambda:self.show_frame('JoinAudio'),relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d')
        audio_join.place(x = 130,y = 30)
        
        button = tk.Button(background,text = 'Home',width = 5,command = lambda:self.controller.show_frame('MainFrame'),relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d')
        button.place(x = 230,y = 30)


        for f in (ChangeFormat,JoinAudio):
            page_name = f.__name__
            frame = f(parent = container,controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0,column = 0,sticky = 'nesw')
    
    def show_frame(self,page_name):
        frame = self.frames[page_name]
        frame.tkraise()