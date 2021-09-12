# h3avren

"""
This file contains all the code for the video processing part of the application
"""

import os
import tkinter as tk
import moviepy as mv
from interfaces import CFrame, StandardWindow


# a class to implement the join of two video files
class JoinVideo(CFrame):
    def __init__(self,parent,controller):
        CFrame.__init__(self,parent,controller)
        
        button = tk.Button(self,text = 'Hey see this is working for real..!')
        button.pack()


# this class implements the video tools window
class VideoEditor(StandardWindow):
    def __init__(self,parent,controller):
        StandardWindow.__init__(self,parent,controller)

        for f in (JoinVideo,):
            page_name = f.__name__
            frame = f(parent = self.container,controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0,column = 0,sticky = 'nesw')
        
