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
import time

class Browse:
    def __init__(self):
        self.filename = ''
        self.thread = 0

    def browse(self):
        self.filename = filedialog.askopenfilename()
        if(self.filename):
            self.label.config(text = os.path.split(self.filename)[1])

# frame for trimming an audio file
class Trim(tk.Frame,Browse):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        Browse.__init__(self)
        self.controller = controller
        self.config(bg = '#2AA2BC')

        self.label = tk.Label(self,text = '---Empty Selection---',width = 20,pady = 5,bg = '#ee3456')
        self.label.grid(row = 0,column = 0,padx = 10,pady = 10)

        self.add = tk.Button(self,text = 'Select File',bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10,command = self.browse)
        self.add.grid(row = 0,column = 1,padx = 10,pady = 10)

        #self.status = tk.Label(self,text = 'No Process..!',width = 20,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')



# frame for changing audio formats
class ChangeFormat(tk.Frame,Browse):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        Browse.__init__(self)
        self.controller = controller
        self.config(bg = '#2AA2BC')

        self.label = tk.Label(self,text = '---Empty Selection---',width = 20,pady = 5,bg = '#ee3456')
        self.label.grid(row = 0,column = 0,padx = 10,pady = 20)

        add = tk.Button(self,text = 'Select File',width = 10,relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d',command = self.browse)
        add.grid(row = 0,column = 1,padx = 10,pady = 20)

        self.formats = ttk.Combobox(self,state = 'readonly',values = ('mp3','flv','ogg','wav','wma','avi','aac','m4a','flac','opus','au','aiff','webm'))
        self.formats.grid(row = 1,column = 0,padx = 10,pady = 20)

        self.formats.current(0)

        convert = tk.Button(self,text = 'Convert',width = 10,relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d',command = self.run_thread)
        convert.grid(row = 1,column = 1,padx = 10,pady = 20)

        self.status = tk.Label(self,text = 'No process..!',width = 20,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.status.grid(row = 2,column = 0,padx = 10,pady = 20)

        self.queue = tk.Label(self,text = 'Queued : 0',width = 10,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.queue.grid(row = 2,column = 1,padx = 10,pady = 20)
    
    def run_thread(self):
        self.thread += 1
        thread = threading.Thread(target = self.convert)
        thread.start()
    
    def convert(self):
        if(self.filename):
            ext = self.formats.get()
            filename = filedialog.asksaveasfilename(defaultextension = f'.{ext}',filetypes = ((f'.{ext} files',f'*.{ext}'),))
            if(filename):
                try:
                    format_ = {'mp3':'mp3','flv':'flv','ogg':'ogg','wav':'wav','wma':'wma','avi':'avi','aac':'adts','m4a':'mp4','flac':'flac','opus':'opus','au':'au','aiff':'aiff','webm':'webm'}
                    self.status.config(text = 'Processing...',bg = '#2a8d12')
                    self.queue.config(text = f'Queued: {self.thread}',bg = '#2a8d12')
                    self.label.config(text = '---Empty Selection---')
                    self.formats.current(0)
                    audio = AudioSegment.from_file(self.filename)
                    audio.export(filename,format = format_[ext])
                    self.status.config(text = 'Success..!',bg = '#2a8d12')
                except:
                    self.status.config(text = 'Failed..!',bg = '#ee3456')
        else:
            messagebox.showerror(title = 'Error...',message = 'Select a file to convert..!')
        
        self.thread -= 1
        self.queue.config(text = f'Queued: {self.thread}',bg = '#2a8d12')
        if(self.thread == 0):
            time.sleep(1)
            self.queue.config(bg = '#ae34d9')
            self.status.config(text = 'No process..!',bg = '#ae34d9')


# frame for joining audio files
class JoinAudio(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.filename_1 ,self.filename_2 = None,None
        self.config(bg = '#2AA2BC')
        self.thread_count = 0

        self.file_label_1 = tk.Label(self,text = '---Empty Selection---',bg = '#ee3456',pady = 5,width = 20)
        self.file_label_1.grid(row = 0,column = 0,padx= 10,pady = 10)

        add_1 = tk.Button(self,text = 'Select File',command = lambda:self.browse_file(1),relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d')
        add_1.grid(row = 0,column = 1,padx = 10,pady = 10)

        self.file_label_2 = tk.Label(self,text = '---Empty Selection---',bg = '#ee3456',pady = 5,width = 20)
        self.file_label_2.grid(row = 1,column = 0,padx = 10,pady =10)

        add_2 = tk.Button(self,text='Select File',relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d',command = lambda:self.browse_file(2))
        add_2.grid(row = 1,column = 1,padx = 10,pady =10)

        self.export_as = ttk.Combobox(self,values = ('mp3','flv','ogg','wav','wma','avi','aac','m4a','flac','opus','au','aiff','webm'),state = 'readonly')
        self.export_as.grid(row = 2, column = 0,padx = 10,pady = 10)

        self.export_as.current(0)

        join_ = tk.Button(self,text='Join',relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d',command = self.run_thread)
        join_.grid(row = 2,column = 1,padx = 10,pady = 10)

        self.label = tk.Label(self,text = 'No processs..!',width = 20,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.label.grid(row = 3,column = 0)

        self.queue = tk.Label(self,text = 'Queued : 0',width = 10,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
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
            filename = filedialog.asksaveasfilename(defaultextension = f'.{ext}',filetypes = ((f'.{ext} files',f'*.{ext}'),))
            if(filename):
                try:
                    self.label.config(text = 'Processing...',bg = '#2a8d12')
                    self.queue.config(text = f'Queued : {self.thread_count}',bg = '#2a8d12')
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
            messagebox.showerror(title = 'Error..!',message = 'Select the files to join..!')
        
        self.thread_count -= 1
        self.queue.config(text = f'Queued : {self.thread_count}')
        if(self.thread == 0):
            time.sleep(1)
            self.queue.config(bg = '#ae34d9')
            self.label.config(text = 'No Process..!',bg = '#ae34d9')


# main frame for the audio editor
class AudioEditor(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
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


        for f in (JoinAudio,ChangeFormat,Trim):
            page_name = f.__name__
            frame = f(parent = container,controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0,column = 0,sticky = 'nesw')
    
    def show_frame(self,page_name):
        frame = self.frames[page_name]
        frame.tkraise()