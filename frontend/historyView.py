# -*- coding: utf-8 -*-

try:
    import tkinter as tk
    from tkinter import ttk
    import tkinter.messagebox as messagebox
    from tkinter import font
except ImportError:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox
    import tkFont as font
import tkcalendar
from datetime import datetime
from PIL import Image, ImageGrab

class HistoryView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.container)
        self.columns = [u'ID', u'時間', u'產品名稱', u'圖號', u'產品數量', u'單位', u'公司名稱', u'總價', u'操作']
        self.parent = parent
        self.exportdata = {}
        
        self.tree = exportTreeView( self, self.columns )
        self.tree.pack()
        self.order = ('time', 'asc')
        
        frame = tk.Frame(self)
        button = tk.Button( frame, text=u'新增', command=self.add )
        button.pack(side='left', fill='y')
        button = tk.Button( frame, text=u'刪除', command=self.remove )
        button.pack(side='left', fill='y')
        frame.pack(fill='x')
        
        self.export = exportTreeView( self, self.columns)
        self.export.pack()
        
        frame = tk.Frame(self)
        button = tk.Button( frame, text=u'生成出貨單', command=self.submitexport )
        button.pack(side='left', fill='y')
        button = tk.Button( frame, text=u'返回', command=lambda: self.parent.show_frame("MainPage") )
        button.pack(side='left', fill='y')
        frame.pack(fill='x')
        
        self.refresh()
        
    def refresh(self):
        self.tree.show(self.parent.stock.history, self.parent.stock)
        
        self.export.show(self.exportdata.values(), self.parent.stock)
        
    def add(self):
        for item in self.tree.tree.selection():
            item_text = self.tree.tree.item(item,"values")[0]
            self.exportdata[item_text] = self.parent.stock.historyquery(item_text)
        self.refresh()
    
    def remove(self):
        for item in self.export.tree.selection():
            item_text = self.export.tree.item(item,"values")[0]
            del self.exportdata[item_text]
        self.refresh()
        
    def submitexport(self):
        top = tk.Toplevel()
        
        frame = tk.Frame(top)
        ft = font.Font(family='Fixdsys', size=25)
        tk.Label(frame, text=u'余姚市臻欣塑模廠 (普通合夥)', font=ft).grid(row=0, column=0, columnspan=2)
        
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'地址:').pack(fill='y', side='left')
        self.address = tk.Entry(subframe)
        self.address.insert(0, u'浙江省余姚市羅渡路6號')
        self.address.pack(fill='x', side='left')
        subframe.grid(row=1, column=0)
        
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'Tel:').pack(fill='y', side='left')
        self.telephone = tk.Entry(subframe)
        self.telephone.pack(fill='y', side='left')
        self.telephone.insert(0, u'13805801051')
        subframe.grid(row=1, column=1)
        
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'送貨單號:').pack(fill='y', side='left')
        self.exportNumber = tk.Entry(subframe)
        self.exportNumber.pack(fill='y', side='left')
        subframe.grid(row=2, column=0)
        
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'送貨日期:').pack(fill='y', side='left')
        self.exportDate = tk.Entry(subframe)
        self.exportDate.insert(0, datetime.now().strftime('%m/%d/%Y'))
        self.exportDate.pack(fill='y', side='left')
        subframe.grid(row=2, column=1)
        
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'客戶名稱:').pack(fill='y', side='left')
        self.company = tk.Entry(subframe)
        self.company.pack(fill='y', side='left')
        subframe.grid(row=3, column=0, columnspan=2)
        
        frame.pack(fill='both')
        
        exportView = exportTreeView( top, self.columns )
        exportView.pack()
        exportView.show(self.exportdata.values(), self.parent.stock)
        
        totalPrice = 0
        for d in self.exportdata.values():
            try:
                totalPrice += int(d[u'總價'])
            except:
                pass
        
        tk.Label(top, text=u'合計: {}'.format(totalPrice)).pack(fill='x')
        ft = font.Font(family='Fixdsys', size=8)
        tk.Label(top, text=u'注:煩請貴司收到貨後請回簽送貨單，並於貨到三個工作日內驗收完畢，如有任何問題請書面聯繫並確定', font=ft).pack(fill='x')
        
        frame = tk.Frame(top)
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'收貨人:').pack(fill='y', side='left')
        self.recevier = tk.Entry(subframe)
        self.recevier.pack(fill='y', side='left')
        subframe.grid(row=0, column=0)
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'送貨人:').pack(fill='y', side='left')
        self.sender = tk.Entry(subframe)
        self.sender.insert(0, u'于紅光')
        self.sender.pack(fill='y', side='left')
        subframe.grid(row=0, column=1)
        
        frame.pack(fill='x')
        
        tk.Button(top, text=u'確認', command=self.submitExport).pack(fill='y', side='left')
        tk.Button(top, text=u'取消', command=top.destroy).pack(fill='y', side='left')
        
        self.top = top
        
        top.mainloop()
        
    def submitExport(self):
        '''
        top = tk.Toplevel()
        
        frame = tk.Frame(top)
        ft = font.Font(family='Fixdsys', size=25)
        tk.Label(frame, text=u'余姚市甄欣素模廠 (普通合夥)', font=ft).grid(row=0, column=0, columnspan=2)
        
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'地址:').pack(fill='y', side='left')
        tk.Label(subframe, text=self.address.get()).pack(fill='y', side='left')
        subframe.grid(row=1, column=0)
        
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'Tel:').pack(fill='y', side='left')
        tk.Label(subframe, text=self.telephone.get()).pack(fill='y', side='left')
        subframe.grid(row=1, column=1)
        
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'送貨單號:').pack(fill='y', side='left')
        tk.Label(subframe, text=self.exportNumber.get()).pack(fill='y', side='left')
        subframe.grid(row=2, column=0)
        
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'送貨日期:').pack(fill='y', side='left')
        tk.Label(subframe, text=self.exportDate.get()).pack(fill='y', side='left')
        subframe.grid(row=2, column=1)
        
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'客戶名稱:').pack(fill='y', side='left')
        tk.Label(subframe, text=self.company.get()).pack(fill='y', side='left')
        subframe.grid(row=3, column=0, columnspan=2)
        frame.pack(fill='both')
        exportView = exportTreeView( top, self.columns )
        exportView.pack()
        exportView.show(self.exportdata.values())
        totalPrice = 0
        for d in self.exportdata.values():
            totalPrice += d[u'總價']
        tk.Label(top, text=u'合計: {}'.format(totalPrice)).pack(fill='x')
        ft = font.Font(family='Fixdsys', size=8)
        tk.Label(top, text=u'注:煩請貴司收到貨後請回簽送貨單，並於貨到三個工作日內驗收完畢，如有任何問題請書面聯繫並確定', font=ft).pack(fill='x')
        frame = tk.Frame(top)
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'收貨人:').pack(fill='y', side='left')
        tk.Label(subframe, text=self.recevier.get()).pack(fill='y', side='left')
        subframe.grid(row=0, column=0)
        subframe = tk.Frame(frame)
        tk.Label(subframe, text=u'送貨人:').pack(fill='y', side='left')
        tk.Label(subframe, text=self.sender.get()).pack(fill='y', side='left')
        subframe.grid(row=0, column=1)
        frame.pack(fill='x')
        top.mainloop()
        '''
        x, y = 2*self.top.winfo_x(), 2*self.top.winfo_y()+40
        img = ImageGrab.grab((x, y, x+2*self.top.winfo_reqwidth(), y+2*self.top.winfo_reqheight()-46))
        img.save(u'出貨單.png')
        #top.destroy()
        self.top.destroy()
        
class exportTreeView(object):
    def __init__(self, master, exportColumns):
        frame = tk.Frame( master, width=600, height=200 )
        self.tree = ttk.Treeview( frame, columns=exportColumns, show='headings' )
        self.columns = exportColumns
        for col in self.columns:
            self.tree.column(col, width=100 if col==u'時間' else 50, anchor='center', stretch=True)
            self.tree.heading(col, text=col)
        self.order = u'ID'
        self.desc = False
        
        self.tree.pack()
        frame.pack_propagate(0)
        
        self.pack = frame.pack
        
    def show(self, data, stock):
        self.tree.delete(*self.tree.get_children())
        sorted_data = sorted(data, key=lambda x:x[self.order], reverse=self.desc)
        
        for d in sorted_data:
            v = []
            for col in self.columns:
                if col in [u'單位', u'圖號']:
                    if u'物料' in d[u'操作']:
                        v.append('' if col == u'圖號' else stock.material[d[u'產品名稱']][col])
                    else:
                        v.append(stock.data[d[u'產品名稱']][col])
                else:
                    v.append(d[col])
            self.tree.insert('', 'end', values=v)
           
        