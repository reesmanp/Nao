'''
Created on Sep 15, 2014

@author: Paul Reesman
'''

from Tkinter import Tk, Label, BOTH
from ttk import Frame, Style
from main import Logic, Splash

class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        
        self.initUI()
        self.centerWindow()
    
    def initUI(self):
        self.parent.title("BoothTool")
        self.pack(fill=BOTH, expand=1)
        style = Style()
        style.configure("TFrame", background="#333")

    def centerWindow(self):
        windowWidth = self.parent.winfo_screenwidth()
        windowHeight = self.parent.winfo_screenheight()
        
        width = .75 * windowWidth
        height = .75 * windowHeight
        x = (windowWidth - width) / 2
        y = (windowHeight - height) / 2
        
        self.parent.geometry("%dx%d+%d+%d" % (width, height, x, y))

def main():
    Splash.splash()
    root = Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()