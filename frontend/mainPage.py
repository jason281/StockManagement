# -*- coding: utf-8 -*-

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

class MainPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.container)
        
        self.parent = parent
        button1 = tk.Button(self, text=u'材料入庫', command=lambda: self.parent.show_frame("MaterialInStock"))
        button2 = tk.Button(self, text=u'入庫', command=lambda: self.parent.show_frame("InStock"))
        button3 = tk.Button(self, text=u'銷庫', command=lambda: self.parent.show_frame("OutStock"))
        button4 = tk.Button(self, text=u'現有庫存', command=lambda: self.parent.show_frame("StockView"))
        button5 = tk.Button(self, text=u'歷史紀錄', command=lambda: self.parent.show_frame("HistoryView"))
        
        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack()
        
    def refresh(self):
        pass