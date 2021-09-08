# h3avren

"""
This is the GUI part of the application. This is where the GUI of the application is defined.
"""

# imports
import tkinter as tk    # importing the tkinter library as this is what we will be using to create the GUI
from tkinter import filedialog
from img_process import ImageEditor
from aud_process import AudioEditor
import os

if(not os.path.isdir('Amppper')):
    os.mkdir('Amppper')

class MainFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title('Amppper')

        self.background = tk.PhotoImage(file = 'icons/amppper.png')
        im_height,im_width = self.background.height(), self.background.width()

        background = tk.Canvas(self,height = im_height,width = im_width)
        background.pack(fill = 'both',expand = True)

        background.create_image(0,0,image = self.background,anchor = 'nw')

        img_button = tk.Button(background,text = 'Image Options',pady = 5,padx = 5,width = 15,command = self.image_options,relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d')
        img_button.place(x = 420, y = 170)

        audio_button = tk.Button(background,text = 'Audio Options',pady = 5,padx = 5,width = 15,command = lambda:self.controller.show_frame('AudioEditor','Audio Tools -> Trim'),relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d')
        audio_button.place(x = 420, y = 210)

        video_button = tk.Button(background,text = 'Video Options',pady = 5,padx = 5,width = 15,command = self.video_options,relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d')
        video_button.place(x = 420, y = 250)

    def image_options(self):
        popup = tk.Toplevel()
        
        def img_select():
            file_name = filedialog.askopenfilename()
            popup.destroy()

            if(file_name):
                ImageEditor(file_name)

        create = tk.Button(popup,text = 'Create an Image',padx = 5,pady = 5,width = 15)
        create.pack(padx = 5,pady = 5)

        edit = tk.Button(popup,text = 'Edit an Image',padx = 5,pady = 5,width = 15,command = img_select)
        edit.pack(padx = 5,pady = 5)
        
 
    def video_options(self):
        pass

# main window 
class App(tk.Tk):
    """
    This class defines the main window of the GUI and all it's content widgets.
    """

    def __init__(self) -> None:
        super().__init__()
        # x = int((self.winfo_screenwidth() - 800)/2)
        # y = int((self.winfo_screenheight() - 600)/2)
        # self.geometry(f'800x600+{x}+{y}')
        self.title('Amppper')
        self.geometry('610x390')
        self.resizable(False,False)
        self.frames = {}
        #self.wm_attributes('-transparentcolor','#a1a1a1')

        background = tk.Frame(self)
        background.pack(fill = 'both',expand = True)

        for f in (AudioEditor,MainFrame):
            page_name = f.__name__
            frame = f(parent = background,controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0,column = 0,sticky = 'nesw')
        
    def show_frame(self,name,title = ''):
        frame = self.frames[name]
        frame.tkraise()
        if(title):
            self.title(f'Amppper -> {title}')
        else:
            self.title('Amppper')

if __name__ == "__main__":
    app = App()
    app.mainloop()