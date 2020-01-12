# -*- coding: utf-8 -*-

try:
    import tkinter as tk
    from tkinter import ttk
    import tkinter.messagebox as messagebox
except ImportError:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox
import datetime
import tkcalendar

class MaterialInStock(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.container)
        
        self.parent = parent
        
        self.materialName = tk.StringVar(self)
        self.materialName.set(self.parent.default)
        self.materialName.trace('w', self.refresh)
        
        materialList = list(self.parent.stock.material.keys())
        self.materialNameList = tk.OptionMenu( self, self.materialName, *materialList )
        label1 = tk.Label( self, text=u'物料名稱')
        label1.grid(row=0,column=0)
        self.materialNameList.grid(row=0,column=1)
        
        self.materialNum = tk.StringVar(self)
        self.materialNum.set('')
        
        tk.Label( self, text=u'物料編碼').grid(row=1,column=0)
        tk.Label( self, textvariable=self.materialNum).grid(row=1,column=1)
        
        label2 = tk.Label( self, text=u'數量')
        self.productAmount = tk.Entry(self)
        label2.grid(row=2,column=0)
        self.productAmount.grid(row=2, column=1)
        self.unit = tk.StringVar()
        tk.Label(self, textvariable=self.unit).grid(row=1, column=2)
        
        self.calendar = tkcalendar.DateEntry(self)
        self.calendar.grid(row=3, columnspan=4)
    
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
    
        button = tk.Button( self, text=u'提交', command=lambda: self.submit() )
        button.grid(row=5, column=0, columnspan=2)
        button2 = tk.Button( self, text=u'返回', command=lambda: self.parent.show_frame("MainPage") )
        button2.grid(row=5, column=2, columnspan=2)
        button3 = tk.Button( self, text=u'新增原料', command=lambda: self.parent.addMaterial() )
        button3.grid(row=0, column=2)
        button3 = tk.Button( self, text=u'刷新', command=lambda: self.refresh() )
        button3.grid(row=1, column=2)
        
    def setProduct(self, product):
        self.productName.set(product)
        
    def refresh(self, *arg):
        productList = sorted(list(self.parent.stock.material.keys()))
        self.materialNameList.destroy()
        self.materialNameList = tk.OptionMenu( self, self.materialName, *productList )
        self.materialNameList.grid(row=0,column=1)
        name = self.materialName.get()
        #print(name)
        if name in self.parent.stock.material:
            self.unit.set(self.parent.stock.material[name][u'單位'])
            self.materialNum.set(self.parent.stock.material[name][u'物料編碼'])
        else:
            self.unit.set('')
            self.materialNum.set('')

    def submit(self):
        try:
            stock = self.parent.stock
            
            name = self.materialName.get()
            assert name != self.parent.default
            amount = int( self.productAmount.get() )
            
            stock.inMaterial( name, amount, self.calendar.get_date() )
        except AssertionError:
            messagebox.showinfo(u'錯誤', u'非法操作')
        except ValueError:
            messagebox.showinfo(u'錯誤', u'數量錯誤')
        else:
            self.parent.stock.saveData()
            self.parent.show_frame("MainPage")
            
