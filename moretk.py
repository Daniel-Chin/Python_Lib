'''
by Daniel
'''
import tkinter as tk
import threading
from PIL import Image, ImageTk

class InputboxThread(threading.Thread):
    def __init__(self, msg, default):
        super(__class__,self).__init__()
        self.msg=msg
        self.default=default
        self.prelock = threading.Lock()
        self.lock=threading.Lock()
        self.prelock.acquire()
        self.start()
        self.prelock.acquire()
        self.lock.acquire()
    
    def run(self):
        with self.lock:
            self.prelock.release()
            
            default = str(self.default)
            confirmed = False
            root = tk.Tk()
            
            def confirm(event):
                nonlocal confirmed, root
                confirmed = True
                root.destroy()
            
            input = tk.StringVar(root)
            entry = tk.Entry(root,textvariable=input, font='Times 20')
            entry.bind('<Return>', confirm)
            input.set(default)
            entry.select_range(0, 'end')
            entry.icursor('end')
            
            label = tk.Label(root, text=self.msg, font='Courier 20') 
            
            label.grid()
            entry.grid(sticky='we')
            root.grid_columnconfigure(0, weight=1)
            entry.focus()
            root.mainloop()
            if confirmed:
                self.input = input.get()
            else:
                self.input = default

def inputbox(msg = '', default = ''):
    return InputboxThread(msg, default).input

class MsgboxThread(threading.Thread):
    def __init__(self, msg):
        super(__class__,self).__init__()
        self.msg=msg
        self.prelock = threading.Lock()
        self.lock=threading.Lock()
        self.prelock.acquire()
        self.start()
        self.prelock.acquire()
        self.lock.acquire()
    
    def run(self):
        with self.lock:
            self.prelock.release()
            root = tk.Tk()
            
            label = tk.Label(root, text=self.msg, font='Times 20') 
            button = tk.Button(root, text='OK', command=root.destroy)
            button.bind('<Return>', lambda event : (root.destroy()))
        
            label.pack()
            button.pack()
            button.focus()
            root.mainloop()

def msgbox(msg = ''):
    MsgboxThread(msg)

class StretchMessage(tk.Message):
    def __init__(self, master, **kw):
        if 'font' not in kw:
            kw['font'] = 'Times 20'
        super(__class__,self).__init__(master, **kw)
        self.bind('<Button-3>', self.displayText)
        master.handlers_to_convey.append(self.stretch)
    
    def stretch(self, event):
        self.config(width=event.width)
    
    def displayText(self,event):
        inputbox('You can copy now',self.cget('text'))
    
    def toughSetText(self, text):
        try:
            super(__class__,self).config(text = text)
        except:
            tempMessage = tk.Message(self.master)
            chunk = ''
            for char in text:
                try:
                    tempMessage.config(text = char)
                    chunk += char
                except:
                    chunk += '?'
            tempMessage.destroy()
            super(__class__,self).config(text = chunk)

class StretchPicture(tk.Frame):
    def __init__(self, master, image_path, keep_ratio = True, **kw):
        super(__class__,self).__init__(master, **kw)
        self.keep_ratio = keep_ratio
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.original = Image.open(image_path)
        self.photoImage = ImageTk.PhotoImage(self.original)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        self.canvas.create_image(0, 0, image=self.photoImage, anchor=tk.NW, tags="IMG")
        self.canvas.grid(row=0, sticky='wens')
        self.bind("<Configure>", self.resize)
        self.config(**kw)
    
    def pack(self):
        super(__class__,self).pack(fill=tk.BOTH, expand=1)
    
    def grid(self, **kw):
        super(__class__,self).grid(sticky='wens', **kw)
    
    def resize(self, event):
        if self.keep_ratio:
            ratio = self.original.size[0]/self.original.size[1]
            frame_ratio = event.width / event.height
            if ratio > frame_ratio:
                # Use width
                size = (event.width, int(event.width / ratio))
            else:
                # Use height
                size = (int(event.height * ratio), event.height)
        else:
            size = (event.width, event.height)
        resized = self.original.resize(size,Image.ANTIALIAS)
        self.photoImage = ImageTk.PhotoImage(resized)
        self.canvas.delete("IMG")
        self.canvas.create_image(int(event.width/2), 
            int(event.height/2), image=self.photoImage, anchor=tk.CENTER, tags="IMG")

class ToughText(tk.Text):
    def __init__(self, master, **kw):
        super(__class__,self).__init__(master, **kw)
    
    def insert(self, index, chars, *args):
        try:
            super(__class__,self).insert(index, chars, *args)
        except:
            if chars is None:
                return
            tempText = tk.Text(self.master)
            chunk = ''
            for char in chars:
                try:
                    tempText.insert(tk.END,char)
                    chunk += char
                except:
                    chunk += '?'
            tempText.destroy()
            super(__class__,self).insert(index, chunk, *args)

def bilingualStringLen(string, fontsize = 18):
    length = 0
    for char in string:
        if len(char.encode()) > 1:
            length+=2.2
        else:
            length+=1
    length = int(length * fontsize / 18)
    return length

def makeStretcherParent(widget):
    widget.handlers_to_convey = []
    def stretchChildren(event):
        for handler in widget.handlers_to_convey:
            handler(event)
    widget.bind('<Configure>', stretchChildren)

if __name__=='__main__':
    msgbox(inputbox('msg','default'))
