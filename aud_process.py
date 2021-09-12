# h3avren

"""
This file contains all the functions that will 
be used for audio processing in the main application
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
from interfaces import CFrame,StandardWindow


# frame for trimming an audio file
class Trim(CFrame):
    def __init__(self,parent,controller):
        CFrame.__init__(self,parent,controller)

        self.label = tk.Label(self,text = '---Empty Selection---',
        width = 20,pady = 5,bg = '#ee3456')
        self.label.grid(row = 0,column = 0,padx = 10,pady = 11)

        self.add = tk.Button(self,text = 'Select File',bg = '#2abc8d',
        relief = 'flat',activebackground = '#aabc8d',width = 10,
        command = self.browse)
        self.add.grid(row = 0,column = 1,padx = 10,pady = 12)

        self.display_length = tk.Label(self,text = 'Duration: 00:00',
        bg = '#aa89ca',relief = 'sunken',pady = 5,padx = 5)
        self.display_length.grid(row = 1,column = 0,columnspan = 2,padx = 10,pady = 5)

        self.from_label = tk.Label(self,bg = '#2AA2BC')
        self.from_label.grid(row = 2,column = 0,padx = 10,pady = 5)

        self.from_ = tk.Label(self.from_label,bg = '#2AA2BC',text = 'From:')
        self.from_.grid(row = 0,column = 0)

        self.from_spin = tk.Spinbox(self.from_label,relief = 'sunken',
        selectbackground = '#aa348c',state = 'disable',width = 6)
        self.from_spin.grid(row = 0,column = 1)

        self.to_label = tk.Label(self,bg = '#2AA2BC')
        self.to_label.grid(row = 2,column = 1,padx = 10,pady = 5)

        self.to = tk.Label(self.to_label,bg = '#2AA2BC',text = 'To:')
        self.to.grid(row = 0,column = 0)

        self.to_spin = tk.Spinbox(self.to_label,relief = 'sunken',
        selectbackground = '#aa348c',state = 'disable',width = 6)
        self.to_spin.grid(row = 0,column = 1)

        trim = tk.Button(self,text = 'Trim',width = 10,
        relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d',
        command = self.run_thread)
        trim.grid(row = 4,column = 0,columnspan = 2,padx = 10,pady = 5)

        self.status = tk.Label(self,text = 'No process..!',
        width = 20,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.status.grid(row = 5,column = 0,padx = 10,pady = 5)

        self.queue = tk.Label(self,text = 'Queued : 0',
        width = 10,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.queue.grid(row = 5,column = 1,padx = 10,pady = 5)

    
    def run_thread(self):
        thread = threading.Thread(target = self.trim)
        self.thread += 1
        thread.start()
    
    def browse(self):
        CFrame.browse(self)
        self.label.update()
        if(self.filename):
            try:
                self.audio = AudioSegment.from_file(self.filename)
                duration = self.audio.duration_seconds
                self.display_length.config(text = 'Duration : {:.2f} secs'.format(duration))
                self.from_spin.config(state = 'normal',to = duration,from_ = 0,)
                self.to_spin.config(state = 'normal',to = duration,from_ = 0)
            except:
                self.label.config(text = '---Empty Selection---')
                messagebox.showerror(title = 'Error',message = 'Incompatible file format..!')

    def trim(self):
        if(self.filename):
            ext = os.path.splitext(self.filename)[1]
            filename = filedialog.asksaveasfilename(defaultextension = ext,filetypes = ((f'{ext} files',f'*{ext}'),))
            if(filename):
                try:
                    format_ = {'mp3':'mp3','flv':'flv','ogg':'ogg','wav':'wav','wma':'wma',
                            'avi':'avi','aac':'adts','m4a':'mp4','flac':'flac','opus':'opus','au':'au',
                            'aiff':'aiff','webm':'webm'}
                    try:
                        start = int(float(self.from_spin.get()) * 1000)
                        end = int(float(self.to_spin.get()) * 1000)
                        if(start > end):
                            raise
                        
                        self.status.config(text = 'Processing...',bg = '#2a8d12')
                        self.queue.config(text = f'Queued: {self.thread}',bg = '#2a8d12')
                        self.label.config(text = '---Empty Selection---')
                        self.to_spin.delete(0,'end')
                        self.from_spin.delete(0,'end')
                        self.filename = ''
                        to_be_saved = self.audio[start : end]
                        to_be_saved.export(filename,format = format_[ext[1:]])
                        self.status.config(text = 'Success..!',bg = '#2a8d12')
                    except:
                        messagebox.showerror(title = 'Error...',
                        message = 'Enter the correct values for the To and From..!')
                except:
                    self.status.config(text = 'Failed..!',bg = '#ee3456')
                    messagebox.showerror(title = 'Error...',message = 'Incompatible file..!')
            self.label.config(text = '---Empty Selection---')
            self.display_length.config(text = 'Duration: 00:00')
            self.to_spin.delete(0,'end')
            self.from_spin.delete(0,'end')
        else:
                messagebox.showerror(title = 'Error...',message = 'Select a file to Trim..!')
        
        self.thread -= 1
        self.queue.config(text = f'Queued: {self.thread}',bg = '#2a8d12')
        if(self.thread == 0):
            time.sleep(1)
            self.queue.config(bg = '#ae34d9')
            self.status.config(text = 'No process..!',bg = '#ae34d9')


# frame for changing audio formats
class ChangeFormat(CFrame):
    def __init__(self,parent,controller):
        CFrame.__init__(self,parent,controller)

        self.label = tk.Label(self,text = '---Empty Selection---',
        width = 20,pady = 5,bg = '#ee3456')
        self.label.grid(row = 0,column = 0,padx = 10,pady = 20)

        add = tk.Button(self,text = 'Select File',width = 10,
        relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d',
        command = self.browse)
        add.grid(row = 0,column = 1,padx = 10,pady = 20)

        self.formats = ttk.Combobox(self,state = 'readonly',
        values = ('mp3','flv','ogg','wav','wma','avi','aac','m4a',
        'flac','opus','au','aiff','webm'))
        self.formats.grid(row = 1,column = 0,padx = 10,pady = 20)

        self.formats.current(0)

        convert = tk.Button(self,text = 'Convert',width = 10,
        relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d',
        command = self.run_thread)
        convert.grid(row = 1,column = 1,padx = 10,pady = 20)

        self.status = tk.Label(self,text = 'No process..!',
        width = 20,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.status.grid(row = 2,column = 0,padx = 10,pady = 20)

        self.queue = tk.Label(self,text = 'Queued : 0',
        width = 10,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.queue.grid(row = 2,column = 1,padx = 10,pady = 20)
    
    def run_thread(self):
        self.thread += 1
        thread = threading.Thread(target = self.convert)
        thread.start()
    
    def convert(self):
        if(self.filename):
            ext = self.formats.get()
            filename = filedialog.asksaveasfilename(
                defaultextension = f'.{ext}',filetypes = ((f'.{ext} files',f'*.{ext}'),))
            if(filename):
                try:
                    format_ = {'mp3':'mp3','flv':'flv','ogg':'ogg','wav':'wav','wma':'wma',
                    'avi':'avi','aac':'adts','m4a':'mp4','flac':'flac','opus':'opus','au':'au',
                    'aiff':'aiff','webm':'webm'}
                    self.status.config(text = 'Processing...',bg = '#2a8d12')
                    self.queue.config(text = f'Queued: {self.thread}',bg = '#2a8d12')
                    self.label.config(text = '---Empty Selection---')
                    self.formats.current(0)
                    audio = AudioSegment.from_file(self.filename)
                    self.filename = ''
                    audio.export(filename,format = format_[ext])
                    self.status.config(text = 'Success..!',bg = '#2a8d12')
                except:
                    self.status.config(text = 'Failed..!',bg = '#ee3456')
                    messagebox.showerror(title = 'Error...',message = 'Incompatible file..!')
        else:
            messagebox.showerror(title = 'Error...',message = 'Select a file to convert..!')
        
        self.thread -= 1
        self.queue.config(text = f'Queued: {self.thread}',bg = '#2a8d12')
        if(self.thread == 0):
            time.sleep(1)
            self.queue.config(bg = '#ae34d9')
            self.status.config(text = 'No process..!',bg = '#ae34d9')


# frame for joining audio files
class JoinAudio(CFrame):
    def __init__(self,parent,controller):
        CFrame.__init__(self,parent,controller)
        self.filename_1 ,self.filename_2 = None,None

        self.file_label_1 = tk.Label(self,text = '---Empty Selection---',
        bg = '#ee3456',pady = 5,width = 20)
        self.file_label_1.grid(row = 0,column = 0,padx= 10,pady = 10)

        add_1 = tk.Button(self,text = 'Select File',
        command = lambda:self.browse(1),relief = 'flat',
        bg = '#2abc8d',activebackground = '#aabc8d')

        add_1.grid(row = 0,column = 1,padx = 10,pady = 10)

        self.file_label_2 = tk.Label(self,text = '---Empty Selection---',
        bg = '#ee3456',pady = 5,width = 20)
        self.file_label_2.grid(row = 1,column = 0,padx = 10,pady =10)

        add_2 = tk.Button(self,text='Select File',relief = 'flat',
        bg = '#2abc8d',activebackground = '#aabc8d',
        command = lambda:self.browse(2))

        add_2.grid(row = 1,column = 1,padx = 10,pady =10)

        self.export_as = ttk.Combobox(self,
        values = ('mp3','flv','ogg','wav','wma','avi','aac',
        'm4a','flac','opus','au','aiff','webm'),state = 'readonly')

        self.export_as.grid(row = 2, column = 0,padx = 10,pady = 10)
        self.export_as.current(0)

        join_ = tk.Button(self,text='Join',relief = 'flat',bg = '#2abc8d',
        activebackground = '#aabc8d',command = self.run_thread)

        join_.grid(row = 2,column = 1,padx = 10,pady = 10)

        self.label = tk.Label(self,text = 'No processs..!',width = 20,
        pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')

        self.label.grid(row = 3,column = 0)

        self.queue = tk.Label(self,text = 'Queued : 0',width = 10,
        pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')

        self.queue.grid(row = 3,column = 1,padx = 10,pady = 10)
    
    def browse(self,num):
        CFrame.browse(self)
        if(num == 1):
            self.filename_1 = self.filename
        else:
            self.filename_2 = self.filename
        self.set_labels()
    
    def set_labels(self):
        if(self.filename_1):
            self.file_label_1.config(text = os.path.split(self.filename_1)[1])
        
        if(self.filename_2):
            self.file_label_2.config(text = os.path.split(self.filename_2)[1])

    def run_thread(self):
        self.thread += 1
        thread = threading.Thread(target = self.join_audio)
        thread.start()

    def join_audio(self):
        if(self.filename_1 and self.filename_2):
            ext = self.export_as.get()
            format_ = {'mp3':'mp3','flv':'flv','ogg':'ogg','wav':'wav','wma':'wma',
            'avi':'avi','aac':'adts','m4a':'mp4','flac':'flac','opus':'opus','au':'au',
            'aiff':'aiff','webm':'webm'}
            filename = filedialog.asksaveasfilename(
                defaultextension = f'.{ext}',filetypes = ((f'.{ext} files',f'*.{ext}'),))
            if(filename):
                try:
                    self.label.config(text = 'Processing...',bg = '#2a8d12')
                    self.queue.config(text = f'Queued : {self.thread}',bg = '#2a8d12')
                    audio_1 = AudioSegment.from_file(self.filename_1)
                    self.filename_1 = ''
                    self.file_label_1.config(text = '---Empty Selection---')
                    audio_2 = AudioSegment.from_file(self.filename_2)
                    self.filename_2 = ''
                    self.file_label_2.config(text = '---Empty Selection---')
                    final = audio_1 + audio_2
                    final.export(filename,format = format_[ext])
                    self.label.config(text = 'Success..!',bg = '#2a8d12')
                except:
                    self.file_label_1.config(text = '---Empty Selection---')
                    self.file_label_2.config(text = '---Empty Selection---')
                    self.label.config(text = 'Failed..!',bg = '#ee3456')
                    messagebox.showerror(title = 'Error',message = 'Incompatible file format')

        else:
            messagebox.showerror(title = 'Error..!',message = 'Select the files to join..!')
        
        self.thread -= 1
        self.queue.config(text = f'Queued : {self.thread}')
        if(self.thread == 0):
            time.sleep(1)
            self.queue.config(bg = '#ae34d9')
            self.label.config(text = 'No Process..!',bg = '#ae34d9')


# main frame for the audio editor
class AudioEditor(StandardWindow):
    def __init__(self,parent,controller):
        StandardWindow.__init__(self,parent,controller)

        trim = tk.Button(self.background,text = 'Trim',width= 5,
        command = lambda:self.show_frame('Trim','Trim'),relief = 'flat',
        bg = '#2abc8d',activebackground = '#aabc8d')
        trim.place(x = 30,y = 30)

        button = tk.Button(self.background,text = 'Convert',width = 5,
        command = lambda:self.show_frame('ChangeFormat','Convert'),relief = 'flat',
        bg = '#2abc8d',activebackground = '#aabc8d')
        button.place(x = 130,y = 30)

        audio_join = tk.Button(self.background,text = 'Join',width = 5,
        command = lambda:self.show_frame('JoinAudio','Join Audio'),relief = 'flat',
        bg = '#2abc8d',activebackground = '#aabc8d')
        audio_join.place(x = 230,y = 30)

        for f in (JoinAudio,ChangeFormat,Trim):
            page_name = f.__name__
            frame = f(parent = self.container,controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0,column = 0,sticky = 'nesw')
    
    def show_frame(self,page_name,title):
        frame = self.frames[page_name]
        frame.tkraise()
        self.controller.title(f'Amppper -> Audio Tools -> {title}')