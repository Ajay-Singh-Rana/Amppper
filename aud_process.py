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

class Logo(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.background = tk.PhotoImage(file='icons/amppper.png')
        canvas = tk.Canvas(self,height = self.background.height(),width = self.background.width())
        canvas.pack(fill='both',expand = True)
        canvas.create_image((0,0),image = self.background,anchor = 'nw')

class ChangeFormat(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        formats = ttk.Combobox(self,values = ('.mp3','.flv','.ogg','.wav','.wma','.avi'))
        formats.pack()


class JoinAudio(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        filename_1 ,filename_2 = '',''

        file_label_1 = tk.Label(self,text = '---Empty Selection---',width = 15)
        file_label_1.grid(row = 0,column = 0,padx= 10,pady = 10)

        add_1 = tk.Button(self,text = 'Select File',command = lambda:browse_file(filename_1))
        add_1.grid(row = 0,column = 1,padx = 10,pady = 10)

        file_label_2 = tk.Label(self,text = '---Empty Selection---',width = 15)
        file_label_2.grid(row = 1,column = 0,padx = 10,pady =10)

        add_2 = tk.Button(self,text='Select File')
        add_2.grid(row = 1,column = 1,padx = 10,pady =10)

        export_as = ttk.Combobox(self,values = ('.mp3','.flv','.ogg','.wav','.wma','.avi'))
        export_as.grid(row = 2, column = 0,padx = 10,pady = 10)

        export_as.current(0)
    
    def browse_file(filename):
        filename = filedialog.askopenfilename()
        if(filename):
            file_label_1.config(text = filename)




def join_audio(filename_1,filename_2,export_as,ext):
    audio_1 = AudioSegment.from_file(file_name_1,os.path.splitext(filename_1)[1][1:])
    audio_2 = AudioSegment.from_file(file_name_2,os.path.splitext(filename_2)[1][1:])
    final = audio_1 + audio_2
    final.export(f'{export_as}.{ext}',format = ext)


def change_format(file_name,to):
    pass

class AudioEditor(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry('610x450')
        self.title('Audio Tools')
        self.resizable(False,False)
        self.frames = {}

        container = tk.Frame(self)
        container.pack(expand = True,side = 'bottom',fill = 'both')

        button = tk.Button(self,text = 'Change Format',width = 15,command = lambda:self.show_frame('ChangeFormat'))
        button.pack(padx=10)

        audio_join = tk.Button(self,text = 'Join Audio',width = 15,command = lambda:self.show_frame('JoinAudio'))
        audio_join.pack(padx=10)
        
        for f in (ChangeFormat,JoinAudio,Logo):
            page_name = f.__name__
            frame = f(parent = container,controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0,column = 0,sticky = 'nesw')
    
    def show_frame(self,page_name):
        frame = self.frames[page_name]
        frame.tkraise()