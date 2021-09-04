# h3avren

"""
This is the GUI part of the application. This is where the GUI of the application is defined.
"""

# imports
import tkinter as tk    # importing the tkinter library as this is what we will be using to create the GUI
from tkinter import filedialog

# image editor window
class ImageEditor(tk.Toplevel):
    def __init__(self,image):
        super().__init__()
        self.title('Image Editor')
        x = int((self.winfo_screenwidth() - 800)/2)
        y = int((self.winfo_screenheight() - 600)/2)
        self.geometry(f'800x600+{x}+{y}')
        self.resizable(False,False)
        self.image = tk.PhotoImage(image)

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
        label = tk.Label(preview_frame,image = self.image)
        label.pack()

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
        self.title('Multimedia Editor')
        
        img_button = tk.Button(self,text = 'Image Options',pady = 5,padx = 5,width = 15,command = self.image_options)
        img_button.pack(padx = 5,pady = 5)

        audio_button = tk.Button(self,text = 'Audio Options',pady = 5,padx = 5,width = 15,command = self.audio_options)
        audio_button.pack(padx = 5,pady = 5)

        video_button = tk.Button(self,text = 'Video Options',pady = 5,padx = 5,width = 15,command = self.video_options)
        video_button.pack(padx = 5,pady = 5)
        
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
        
        


    def audio_options(self):
        pass

    def video_options(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()