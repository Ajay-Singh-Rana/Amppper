# h3avren

"""
This module contains all the functions required for the image processing part of the application
"""

# imports
import tkinter as tk
import PIL as pl
import os

if(not os.path.isdir('.temp')):
    os.mkdir('.temp')

# image editing functions
def inv(image):
    temp = pl.ImageOps.invert(image)
    temp.save('.temp/{}')


# image editor window
class ImageEditor(tk.Toplevel):
    def __init__(self,image):
        super().__init__()
        self.title('Image Editor')
        x = int((self.winfo_screenwidth() - 800)/2)
        y = int((self.winfo_screenheight() - 600)/2)
        self.geometry(f'800x600+{x}+{y}')
        self.resizable(False,False)
        self.image = tk.PhotoImage(file = image)

        main_frame = tk.Frame(self)
        main_frame.pack()

        tool_frame = tk.Frame(main_frame,height = 600,width = 100,bg = 'Black')
        tool_frame.grid(row = 0, column = 0,rowspan = 2)

        preview_frame= tk.Frame(main_frame,height = 560,width = 700)
        preview_frame.grid(row = 0, column = 1)

        option_frame= tk.Frame(main_frame,height = 40,width = 700)
        option_frame.grid(row = 1,column = 1)

        # options frame buttons
        undo = tk.Button(option_frame,text = 'Undo')
        undo.grid(row = 0, column = 0,padx = 10)

        save = tk.Button(option_frame,text = 'Save')
        save.grid(row = 0, column = 1,padx = 10)

        discard = tk.Button(option_frame,text = 'Discard')
        discard.grid(row = 0, column = 2,padx = 10)

        redo = tk.Button(option_frame,text = 'Redo')
        redo.grid(row = 0,column = 3,padx = 10)


        # Image editing Buttons
        crop = tk.Button(tool_frame,text = 'Crop',width = 10)
        crop.pack()

        annotate = tk.Button(tool_frame,text = 'Annotate',width = 10)
        annotate.pack()

        # image preview frame
        label = tk.Label(preview_frame,image = self.image,width = 700 ,height = 560)
        label.pack(fill = tk.BOTH,expand = True)