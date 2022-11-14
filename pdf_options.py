# h3avren

import time
from tkinter import messagebox,filedialog
import tkinter as tk
import PyPDF2
from interfaces import CFrame,StandardWindow
import os

# pdf to text
class PDF2TEXT(CFrame):
    def __init__(self,parent,controller):
        CFrame.__init__(self,parent,controller)
       
        self.label = tk.Label(self,text = '---Empty Selection---',
        padx = 10,pady = 5,bg = '#ee3456')
        self.label.grid(row = 0,column = 0,padx = 10,pady = 20)

        self.add = tk.Button(self,text = 'Select File',command = self.browse,
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10)
        self.add.grid(row = 0, column = 1,padx = 10,pady = 20)

        self.extract = tk.Button(self,text = 'Extract',
        command = lambda: self.run_thread(self.extract_text),
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10)
        self.extract.grid(row = 1,columnspan = 2,padx = 10,pady = 15)

        self.status = tk.Label(self,text = 'No process..!',
        width = 20,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.status.grid(row = 2,column = 0,padx = 10,pady = 15)

        self.queue = tk.Label(self,text = 'Queued : 0',
        width = 10,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.queue.grid(row = 2,column = 1,padx = 10,pady = 15)

    def run_thread(self,target_func):
        CFrame.run_thread(self,target_func)
        if(self.thread >= 2):
            self.extract.config(state = tk.DISABLED)

    def extract_text(self):
        if(self.filename):
            try:
                self.status.config(text = 'Processing...',bg = '#2a8d12')
                self.queue.config(text = f'Queued : {self.thread}',bg = '#2a8d12')
                temp = self.filename
                self.filename = ''
                self.label.config(text = '---Empty Selection---')
                os.system(f'pdf2txt.py {temp} -o {os.path.basename(temp[:-3])}txt')
                self.status.config(text = 'Success..!',bg = '#2a8d12')
            except:
                self.status.config(text = 'Failed..!',bg = '#ee3456')       
            
            
            self.thread -= 1
            if(self.thread < 2):
                self.extract.config(state = tk.NORMAL)
            self.queue.config(text = f'Queued : {self.thread}')
            if(self.thread == 0):
                time.sleep(1)
                self.queue.config(bg = '#ae34d9')
                self.status.config(text = 'No Process..!',bg = '#ae34d9')
        else:
            messagebox.showerror(title = 'File Error',message = 'Select a File First..!')

# joining two pdfs
class JoinPDF(CFrame):
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

        self.join = tk.Button(self,text = 'Join',
        command = lambda: self.run_thread(self.join_pdf),
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10)
        self.join.grid(row = 2,columnspan = 2)

        self.status = tk.Label(self,text = 'No process..!',
        width = 20,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.status.grid(row = 3,column = 0,padx = 10,pady = 10)

        self.queue = tk.Label(self,text = 'Queued : 0',
        width = 10,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.queue.grid(row = 3,column = 1,padx = 10,pady = 10)

    def browse(self,num):
            CFrame.browse(self,0)
            if(num == 1):
                self.filename_1 = self.filename
                if(self.filename_1):
                    self.file_label_1.config(text = os.path.split(self.filename_1)[1])
            else:
                self.filename_2 = self.filename
                if(self.filename_2):
                    self.file_label_2.config(text = os.path.split(self.filename_2)[1])

    def join_pdf(self):
        if(self.filename_1 and self.filename_2):
            save_as = filedialog.asksaveasfilename(defaultextension = '.pdf',filetypes = (('.pdf files','*.pdf'),))
            if(save_as):
                try:
                    file_list = [self.filename_1,self.filename_2]
                    self.status.config(text = 'Processing...',bg = '#2a8d12')
                    self.queue.config(text = f'Queued : {self.thread}',bg = '#2a8d12')
                    self.filename_1 = ''
                    self.file_label_1.config(text = '---Empty Selection---')
                    self.filename_2 = ''
                    self.file_label_2.config(text = '---Empty Selection---')
                    pdf = PyPDF2.PdfFileMerger()
                    for file in file_list:
                        pdf.append(file)
                    with open(save_as,'wb') as output_file:
                        pdf.write(output_file)
                    self.status.config(text = 'Success..!',bg = '#2a8d12')
                    save_as = ''
                except:
                    self.label.config(text = 'Failed..!',bg = '#ee3456')
            else:
                messagebox.showerror(title = 'Error..!',message = 'Give a name for the output file..!')
        else:
            messagebox.showerror(title = 'Error..!',message = 'Select the files to join..!')
        
        self.thread -= 1
        self.queue.config(text = f'Queued : {self.thread}')
        if(self.thread == 0):
            time.sleep(1)
            self.queue.config(bg = '#ae34d9')
            self.status.config(text = 'No Process..!',bg = '#ae34d9')


# pdf page split feature
class SplitPage(CFrame):
    def __init__(self,parent,controller):
        CFrame.__init__(self,parent,controller)
        
        self.label = tk.Label(self,text = '---Empty Selection---',
        padx = 10,pady = 5,bg = '#ee3456')
        self.label.grid(row = 0,column = 0,padx = 10,pady = 20)

        self.add = tk.Button(self,text = 'Select File',command = self.browse,
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',width = 10)
        self.add.grid(row = 0, column = 1,padx = 10,pady = 20)

        self.numPages = tk.Label(self,bg = '#2AA2BC')
        self.numPages.grid(row = 1,column = 0,padx = 10,pady = 5)

        self.textLabel = tk.Label(self.numPages,text = 'Set of Pages : ',
        bg = '#2AA2BC')
        self.textLabel.grid(row = 0,column = 0)

        self.entry = tk.Entry(self.numPages,relief = 'sunken',
        selectbackground = '#aa348c',width = 3)
        self.entry.insert(0,'1')
        self.entry.grid(row = 0,column = 1)

        self.split = tk.Button(self,text = 'Split',
        command = lambda: self.run_thread(self.split_pages),
        bg = '#2abc8d',relief = 'flat',activebackground = '#aabc8d',
        width = 10)
        self.split.grid(row = 1,column = 1,padx = 10,pady = 15)

        self.status = tk.Label(self,text = 'No process..!',
        width = 20,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.status.grid(row = 2,column = 0,padx = 10,pady = 15)

        self.queue = tk.Label(self,text = 'Queued : 0',
        width = 10,pady = 5,bg = '#ae34d9',fg = 'White',relief = 'sunken')
        self.queue.grid(row = 2,column = 1,padx = 10,pady = 15)


    def split_pages(self):
        if(self.filename):
            destination_directory = filedialog.askdirectory()
            if(destination_directory):
                try:
                    input_ = PyPDF2.PdfFileReader(self.filename)
                    self.status.config(text = 'Processing...',bg = '#2a8d12')
                    self.queue.config(text = f'Queued : {self.thread}',bg = '#2a8d12')
                    self.filename = ''
                    self.label.config(text = '---Empty Selection---')
                    skip = self.entry.get()
                    if(skip == ''):
                        skip = 1
                    else:
                        skip = int(self.entry.get())
                    
                    total= input_.numPages + 1
                    if(skip == 1):
                        for i in range(0,total):
                            writer = PyPDF2.PdfFileWriter()
                            page = input_.getPage(i)
                            writer.addPage(page)
                            with open(f'{destination_directory}/page_{i}.pdf','wb') as file:
                                writer.write(file)
                    else:
                        for i in range(0,total,skip):
                            writer = PyPDF2.PdfFileWriter()
                            start = i
                            for j in range(i,i + skip):
                                page = input_.getPage(j)
                                writer.addPage(page)
                                if(j == total):
                                    break
                            with open(f'{destination_directory}/pages_{start}_to_{start+skip}.pdf','wb') as file:
                                writer.write(file)
                    
                    self.status.config(text = 'Success..!',bg = '#2a8d12')
                except:
                    self.status.config(text = 'Failed..!',bg = '#ee3456')
            else:
                messagebox.showerror(title = 'Error..!',message = 'Select a directory to save the output files in..!')
        else:
            messagebox.showerror(title = 'Error..!',message = 'Select the files to join..!')
        
        self.thread -= 1
        self.queue.config(text = f'Queued : {self.thread}')
        if(self.thread == 0):
            time.sleep(1)
            self.queue.config(bg = '#ae34d9')
            self.status.config(text = 'No Process..!',bg = '#ae34d9')


# this class implements the PDF tools window
class PDFOptions(StandardWindow):
    def __init__(self,parent,controller):
        StandardWindow.__init__(self,parent,controller)

        extract = tk.Button(self,text = 'PDF2Text',bg = '#2abc8d',
        activebackground = '#aabc8d',relief = 'flat',width = 8,
        command = lambda: self.show_frame('PDF2TEXT','PDF Tools','Extract Text'))
        extract.place(x = 30,y = 30)

        join_pdf = tk.Button(self,text = 'Join',bg = '#2abc8d',
        activebackground = '#aabc8d',relief = 'flat',width = 5,
        command = lambda: self.show_frame('JoinPDF','PDF Tools','Join PDF'))
        join_pdf.place(x = 140,y = 30)

        split = tk.Button(self,text = 'Split',bg = '#2abc8d',
        activebackground = '#aabc8d',relief = 'flat',width = 5,
        command = lambda: self.show_frame('SplitPage','Video Tools','Split Pages'))
        split.place(x = 230,y = 30)

        for f in (SplitPage,JoinPDF,PDF2TEXT):
            page_name = f.__name__
            frame = f(parent = self.container,controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0,column = 0,sticky = 'nesw')