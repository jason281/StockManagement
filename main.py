# -*- coding: utf-8 -*-

import Tkinter as tk
import ttk
from backend.stock import Stock
import frontend
import os
import pickle, numbers, tkcalendar

class Application( tk.Tk ):
    def __init__(self, path='data.pickle'):
        tk.Tk.__init__(self)
        
        self.maxMaterial_num = 5
        
        self.path = path
        if os.path.exists(path):
            self.stock = pickle.load(open(path, 'rb'))
        else:
            self.stock = Stock()
        
        self.default = u'--請選擇--' 
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.frames = {}
        self.frames['MainPage'] = frontend.MainPage(parent=self)
        self.frames['MaterialInStock'] = frontend.MaterialInStock(parent=self)
        self.frames['InStock'] = frontend.InStock(parent=self)
        self.frames['OutStock'] = frontend.OutStock(parent=self)
        self.frames['HistoryView'] = frontend.HistoryView(parent=self)
        self.frames['StockView'] = frontend.StockView(parent=self)
        
        for key in self.frames:
            self.frames[key].grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("MainPage")
        
        
    def show_frame(self, pageName):
        self.refresh()
        frame = self.frames[pageName]
        if pageName in ['StockView', 'HistoryView']:
            frame.refresh()
        frame.tkraise()
        pickle.dump(self.stock, open(self.path, 'wb'))
        
    def refresh(self):
        for pageName in self.frames:
            frame = self.frames[pageName]
            frame.refresh()
            
    def addProduct(self):
        top = tk.Toplevel()
        
        label = tk.Label( top, text=u'產品名稱')
        name = tk.Entry(top)
        label.grid(row=0, column=0)
        name.grid(row=0, column=1)
        name.focus()
        
        label = tk.Label( top, text=u'單位')
        unit = tk.Entry(top)
        label.grid(row=1, column=0)
        unit.grid(row=1, column=1)
        
        label = tk.Label( top, text=u'圖號')
        scriptNumber = tk.Entry(top)
        label.grid(row=2, column=0)
        scriptNumber.grid(row=2, column=1)
        
        
        self.material_var = [None]*self.maxMaterial_num
        self.portion_var = [None]*self.maxMaterial_num
        materialList = sorted(list(self.stock.material.keys()))
        for i in range(self.maxMaterial_num):
            label = tk.Label( top, text=u'消耗物料{}'.format(i+1) )
            self.material_var[i] = tk.StringVar(self)
            self.material_var[i].set(self.default)
            menu = tk.OptionMenu( top, self.material_var[i], *materialList )
            self.portion_var[i] = tk.DoubleVar(self)
            self.portion_var[i].set(0)
            
            label.grid(row=i+3, column=0)
            menu.grid(row=i+3,column=1)
            tk.Entry(top, textvariable=self.portion_var[i]).grid(row=i+3, column=2)
        
        self.addProductWindow = top
        self.addProductName = name
        self.addProductUnit = unit
        self.addProductSN = scriptNumber
        
        button = tk.Button( top, text=u'提交', command=self.submitProduct )
        button.grid(row=3+self.maxMaterial_num, column=0)
        button2 = tk.Button( top, text=u'返回', command=top.destroy )
        button2.grid(row=3+self.maxMaterial_num, column=1)
        
        top.bind('<Return>', self.submitProduct )
        top.mainloop()
        
    def submitProduct(self, event=None):
        name = self.addProductName.get()
        top = self.addProductWindow
        
        if name in self.stock.data:
            messagebox.showinfo(u'錯誤', u'該產品已存在')
        else:
            self.stock.data[name] = {u'名稱':name, u'數量':0, u'單位':self.addProductUnit.get(), u'圖號':self.addProductSN.get(), u'消耗':{self.material_var[i].get():self.portion_var[i].get() for i in range(self.maxMaterial_num) if self.material_var[i].get() != self.default}}
            if '' in self.stock.data:
                self.stock.removeProduct('')
            self.frames['InStock'].setProduct(name)
            self.frames['OutStock'].setProduct(name)
            self.refresh()
            top.destroy()
        pickle.dump(self.stock, open(self.path, 'wb'))
            
    def addCompany(self):
        top = tk.Toplevel()
        
        label = tk.Label( top, text=u'公司名稱')
        name = tk.Entry(top)
        label.grid(row=0, column=0)
        name.grid(row=0, column=1)
        name.focus()
        
        self.addCompanyWindow = top
        self.addCompanyName = name
        
        button = tk.Button( top, text=u'提交', command=self.submitCompany )
        button.grid(row=2, column=0)
        button2 = tk.Button( top, text=u'返回', command=top.destroy )
        button2.grid(row=2, column=1)
        
        top.bind('<Return>', self.submitCompany )
        
        top.mainloop()
        
    def submitCompany(self, event=None):
        name = self.addCompanyName.get()
        top = self.addCompanyWindow
        
        if name in self.stock.companies:
            messagebox.showinfo(u'錯誤', u'該公司已存在')
        else:
            self.stock.addCompany(name)
            if '' in self.stock.companies:
                self.stock.companies.pop('', None)
            self.refresh()
            self.frames['OutStock'].setCompany(name)
            top.destroy()
        pickle.dump(self.stock, open(self.path, 'wb'))
    def addMaterial(self):
        top = tk.Toplevel()
        
        label = tk.Label( top, text=u'物料名稱')
        name = tk.Entry(top)
        label.grid(row=0, column=0)
        name.grid(row=0, column=1)
        name.focus()
        
        label = tk.Label( top, text=u'物料編碼')
        scriptNumber = tk.Entry(top)
        label.grid(row=1, column=0)
        scriptNumber.grid(row=1, column=1)
        
        label = tk.Label( top, text=u'單位')
        unit = tk.Entry(top)
        label.grid(row=2, column=0)
        unit.grid(row=2, column=1)
        
        self.addMaterialWindow = top
        self.addMaterialName = name
        self.addMaterialUnit = unit
        self.addMaterialSN = scriptNumber
        
        button = tk.Button( top, text=u'提交', command=self.submitMaterial )
        button.grid(row=3, column=0)
        button2 = tk.Button( top, text=u'返回', command=top.destroy )
        button2.grid(row=3, column=1)
        
        top.bind('<Return>', self.submitProduct )
        top.mainloop()
        
    def submitMaterial(self, event=None):
        name = self.addMaterialName.get()
        top = self.addMaterialWindow
        
        if name in self.stock.material:
            messagebox.showinfo(u'錯誤', u'該原料已存在')
        else:
            self.stock.material[name] = {u'物料名稱':name, u'物料編碼':self.addMaterialSN.get(), u'數量':0, u'單位':self.addMaterialUnit.get()}
            if '' in self.stock.material:
                self.stock.material.pop('', None)
            #self.frames['InStock'].setProduct(name)
            #self.frames['OutStock'].setProduct(name)
            self.refresh()
            top.destroy()
        pickle.dump(self.stock, open(self.path, 'wb'))
        

app = Application()        
app.mainloop()