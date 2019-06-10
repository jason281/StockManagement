# -*- coding: utf-8 -*-

try:
    import tkinter as tk
    from tkinter import ttk
    import tkinter.messagebox as messagebox
except ImportError:
    import Tkinter as tk
    from Tkinter import ttk
    import tkMessageBox as messagebox
from .config import *
import datetime
import tkcalendar

class OutStock(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.container)
        
        self.parent = parent
        
        self.productName = tk.StringVar(self)
        self.productName.set(self.parent.default)
        
        productList = list(self.parent.stock.data.keys())
        self.productNameList = tk.OptionMenu( self, self.productName, *productList )
        label1 = tk.Label( self, text=u'產品名稱')
        label1.grid(row=0,column=0)
        self.productNameList.grid(row=0,column=1, columnspan=2)
        
        label2 = tk.Label( self, text=u'產品數量')
        self.productAmount = tk.Entry( self )
        label2.grid(row=1,column=0)
        self.productAmount.grid(row=1, column=1, columnspan=2)
        
        self.companyName = tk.StringVar(self)
        self.companyName.set(self.parent.default)
        
        companyList = list(self.parent.stock.companies.keys())
        self.companyNameList = tk.OptionMenu( self, self.companyName, *companyList )
        label3 = tk.Label( self, text=u'公司名稱')
        label3.grid(row=2,column=0)
        self.companyNameList.grid(row=2,column=1, columnspan=2)
        
        label4 = tk.Label( self, text=u'產品單價')
        self.unitPrice = tk.DoubleVar(self)
        self.unitPrice.trace('w', self.cal_total)
        label4.grid(row=3,column=0)
        tk.Entry( self, textvariable=self.unitPrice ).grid(row=3, column=1, columnspan=2)
        
        label5 = tk.Label( self, text=u'產品總價')
        self.totalPrice = tk.DoubleVar(self)
        self.totalPrice.trace('w', self.cal_unit)
        label5.grid(row=4,column=0)
        tk.Entry( self, textvariable=self.totalPrice ).grid(row=4, column=1, columnspan=2)
        
        self.calendar = tkcalendar.DateEntry(self)
        self.calendar.grid(row=5, columnspan=4)
        
        self.grid_rowconfigure( 6, weight=1 )
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        button = tk.Button( self, text=u'提交', command=lambda: self.submit() )
        button.grid(row=7, column=0, columnspan=2)
        button2 = tk.Button( self, text=u'返回', command=lambda: self.parent.show_frame("MainPage") )
        button2.grid(row=7, column=2, columnspan=2)
        button3 = tk.Button( self, text=u'新增產品', command=lambda: self.parent.addProduct() )
        button3.grid(row=0, column=4)
        button4 = tk.Button( self, text=u'新增公司', command=lambda: self.parent.addCompany() )
        button4.grid(row=2, column=4)
        
    def setProduct(self, product):
        self.productName.set(product)
    def setCompany(self, company):
        self.companyName.set(company)
        
    def refresh(self):
        productList = sorted(list(self.parent.stock.data.keys()))
        self.productNameList.destroy()
        self.productNameList = tk.OptionMenu( self, self.productName, *productList )
        self.productNameList.grid(row=0,column=1)
        
        companyList = sorted(list(self.parent.stock.companies.keys()))
        self.companyNameList.destroy()
        self.companyNameList = tk.OptionMenu( self, self.companyName, *companyList )
        self.companyNameList.grid(row=2,column=1)

    def submit(self):
        try:
            
            stock = self.parent.stock
            
            name = self.productName.get()
            if name == self.parent.default:
                messagebox.showinfo(u'錯誤', u'請選擇產品名稱')
                return
            amount = int( self.productAmount.get() )
            company = self.companyName.get()
            if company == self.parent.default:
                messagebox.showinfo(u'錯誤', u'請選擇公司名稱')
                return
            price = float( self.totalPrice.get() )
            
            stock.outStock( name, amount, company, price, self.calendar.get_date() )
        except AssertionError:
            messagebox.showinfo(u'錯誤', u'庫存不足')
        except ValueError:
            messagebox.showinfo(u'錯誤', u'產品數量或價格錯誤')
        else:
            self.parent.show_frame("MainPage")
            
    def cal_total(self, *arg):
        print(float(self.unitPrice.get())*int( self.productAmount.get() ))
        self.totalPrice.set(str(float(self.unitPrice.get())*int( self.productAmount.get() )))
        
    def cal_unit(self, *arg):
        self.unitPrice.set(str(float(self.totalPrice.get())/int( self.productAmount.get() ) ))
            
    