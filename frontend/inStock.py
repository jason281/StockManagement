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

class InStock(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.container)
        
        self.parent = parent
        
        self.productName = tk.StringVar(self)
        self.productName.set(self.parent.default)
        self.companyName = tk.StringVar(self)
        self.companyName.set(self.parent.default)

        # ==================row0=====================
        label1 = tk.Label( self, text=u'產品名稱')
        label1.grid(row=0,column=0)

        companyList = [self.parent.default] + list(set(self.parent.stock.data.index.get_level_values(0)))
        self.companyNameList = tk.OptionMenu( self, self.companyName, *companyList, command=self.refresh )
        self.companyNameList.bind('<Button-1>', self.refresh)
        self.companyNameList.grid(row=0,column=1)
        
        productList = [self.parent.default]
        self.productNameList = tk.OptionMenu( self, self.productName, *productList, command=self.refresh )
        self.productNameList.bind('<Button-1>', self.refresh)
        self.productNameList.grid(row=0,column=2)

        
        # ==================row1=====================
        label2 = tk.Label( self, text=u'產品數量')
        label2.grid(row=1,column=0)

        self.productAmount = tk.DoubleVar(self)
        self.productAmount.set(0)
        self.productAmount.trace('w', self.refresh_consume)
        tk.Entry(self, textvariable=self.productAmount).grid(row=1, column=1)

        self.unit = tk.StringVar()
        tk.Label(self, textvariable=self.unit).grid(row=1, column=2)
        
        # ==================row2=====================
        self.material_consume = [None]*self.parent.maxMaterial_num
        self.actual_consume = [None]*self.parent.maxMaterial_num
        self.unit_consume = [None]*self.parent.maxMaterial_num
        for i in range(self.parent.maxMaterial_num):
            subframe = tk.Frame(self)
            
            tk.Label(subframe, text=u'消耗物料{}'.format(i+1)).pack(fill='y', side='left')
            
            self.material_consume[i] = tk.StringVar(self)
            self.material_consume[i].set('')
            tk.Label(subframe, textvariable=self.material_consume[i]).pack(fill='y', side='left')
            
            self.actual_consume[i] = tk.DoubleVar(self)
            self.actual_consume[i].set(0)
            tk.Entry(subframe, textvariable=self.actual_consume[i]).pack(fill='y', side='left')
            
            self.unit_consume[i] = tk.StringVar(self)
            self.unit_consume[i].set('')
            tk.Label(subframe, textvariable=self.unit_consume[i]).pack(fill='y', side='left')
            
            subframe.grid(row=i+2, column=0, columnspan=4)
        
        self.calendar = tkcalendar.DateEntry(self)
        self.calendar.grid(row=2+self.parent.maxMaterial_num, columnspan=4)
    
        self.grid_rowconfigure(3+self.parent.maxMaterial_num, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
    
        button = tk.Button( self, text=u'提交', command=lambda: self.submit() )
        button.grid(row=4+self.parent.maxMaterial_num, column=0, columnspan=2)
        button2 = tk.Button( self, text=u'返回', command=lambda: self.parent.show_frame("MainPage") )
        button2.grid(row=4+self.parent.maxMaterial_num, column=2, columnspan=2)
        button3 = tk.Button( self, text=u'新增產品', command=lambda: self.parent.addProduct() )
        button3.grid(row=0, column=3)
        
    def setProduct(self, product):
        self.productName.set(product)
        
    def refresh(self, *arg):
        companyList = [self.parent.default] + list(set(self.parent.stock.data.index.get_level_values(0)))
        self.companyNameList.destroy()
        self.companyNameList = tk.OptionMenu( self, self.companyName, *companyList, command=self.refresh )
        self.companyNameList.grid(row=0,column=1)
        if self.parent.stock.data.index.get_level_values(0).isin([self.companyName.get()]).any():
            productList = sorted(list(self.parent.stock.data.loc[self.companyName.get()].index))
        else:
            productList = [self.parent.default]
        self.productNameList.destroy()
        self.productNameList = tk.OptionMenu( self, self.productName, *productList, command=self.refresh )
        self.productNameList.grid(row=0,column=2)
        name = self.productName.get()
        self.refresh_consume()
        if name in self.parent.stock.data:
            self.unit.set(self.parent.stock.data[name][u'單位'])

    def submit(self):
        try:
            stock = self.parent.stock
            
            name = self.productName.get()
            index = (self.companyName.get(), self.productName.get())
            assert name != self.parent.default
            amount = int( self.productAmount.get() )
            for idx, string in enumerate(self.parent.stock.data.loc[index].iloc[-5:]):
                if string == '':
                    continue
                print('string: ', string)
                mat, _ = string.split(',')
                assert self.parent.stock.material[mat][u'數量'] >= self.actual_consume[idx].get()
            
            stock.inStock( name, self.companyName.get(), amount, self.calendar.get_date() )
            for idx, string in enumerate(self.parent.stock.data.loc[index].iloc[-5:]):
                if string == '':
                    continue
                mat, _ = string.split(',')
                self.parent.stock.material[mat][u'數量'] -= self.actual_consume[idx].get()
                
        except AssertionError:
            messagebox.showinfo(u'錯誤', u'非法操作或物料庫存不足')
        except ValueError:
            messagebox.showinfo(u'錯誤', u'產品數量錯誤')
        else:
            self.parent.stock.saveData()
            self.parent.show_frame("MainPage")
            
    def refresh_consume(self, event=None, *arg):
        try:
            float(self.productAmount.get())
        except tk.TclError:
            return
        if self.productName.get() == self.parent.default or self.productName.get() not in self.parent.stock.data:
            return
        for idx, (mat,consume) in enumerate(self.parent.stock.data[self.productName.get()][u'消耗'].items()):
            self.material_consume[idx].set(mat)
            self.actual_consume[idx].set(float(self.productAmount.get())*float(consume))
            self.unit_consume[idx].set(self.parent.stock.material[mat][u'單位'])
            
