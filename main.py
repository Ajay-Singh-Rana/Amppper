# h3avren

"""
This is the GUI part of the application. This is where the GUI of the application is defined.
"""

# imports
import tkinter as tk    # importing the tkinter library as this is what we will be using to create the GUI
from tkinter import filedialog
from img_process import ImageEditor
from aud_process import AudioEditor

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
        self.background = tk.PhotoImage(file = 'icons/amppper.png')
        im_height,im_width = self.background.height(), self.background.width()
        self.geometry(f'{im_width}x{im_height}')
        self.resizable(False,False)
        
        background = tk.Canvas(self,height = im_height,width = im_width)
        background.pack(fill = 'both',expand = True)

        background.create_image(0,0,image = self.background,anchor = 'nw')

        img_button = tk.Button(background,text = 'Image Options',pady = 5,padx = 5,width = 15,command = self.image_options,relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d')
        img_button.place(x = 420, y = 170)

        audio_button = tk.Button(background,text = 'Audio Options',pady = 5,padx = 5,width = 15,command = AudioEditor,relief = 'flat',bg = '#2abc8d',activebackground = '#aabc8d')
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

if __name__ == "__main__":
    app = App()
    app.mainloop()