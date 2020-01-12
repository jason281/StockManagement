# -*- coding: utf-8 -*-
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

class StockView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.container)
        columns = [u'名稱', u'數量', u'單位', u'圖號']
        self.columns = columns
        
        frame = tk.Frame( self, width=600, height=200 )
        self.parent = parent
        tree = ttk.Treeview( frame, columns=columns,show='headings' )
        for col in columns:
            tree.column(col, width=100, anchor='center')
            tree.heading(col, text=col)
        
        tree.pack()
        frame.pack_propagate(0)
        frame.pack()
        self.tree = tree
        self.order = u'名稱'
        self.desc=False
        
        frame = tk.Frame( self, width=600, height=200 )
        self.material_col = [u'物料名稱', u'物料編碼', u'數量', u'單位']
        tree = ttk.Treeview( frame, columns=self.material_col,show='headings' )
        for col in self.material_col:
            tree.column(col, width=100, anchor='center')
            tree.heading(col, text=col)
        
        tree.pack()
        frame.pack_propagate(0)
        frame.pack()
        self.material_order = u'物料名稱'
        self.material_desc=False
        self.material_tree = tree
        
        self.show()
        
        button1 = tk.Button( self, text=u'新增', command=self.parent.addProduct )
        button1.pack(side='left', fill='y')
        button2 = tk.Button( self, text=u'刪除', command=self.delete )
        button2.pack(side='left', fill='y')
        button3 = tk.Button( self, text=u'修改', command=self.modify )
        button3.pack(side='left', fill='y')
        button4 = tk.Button( self, text=u'返回', command=lambda: self.parent.show_frame("MainPage") )
        button4.pack(side='left', fill='y')
        
        tree.bind('<Double-1>', self.modify)
        
    def refresh(self):
        self.show()
        
    def show(self):
        self.tree.delete(*self.tree.get_children())
        
        data = self.parent.stock.data
        sorted_data = sorted(data.keys(), key=lambda x:data[x][self.order], reverse=self.desc)
        
        for name in sorted_data:
            d = []
            for col in self.columns:
                d.append(data[name][col])
            self.tree.insert('', 'end', values=d)
            
        self.material_tree.delete(*self.material_tree.get_children())
        data = self.parent.stock.material
        sorted_data = sorted(data.keys(), key=lambda x:data[x][self.material_order], reverse=self.material_desc)
        
        for name in sorted_data:
            d = []
            for col in self.material_col:
                d.append(data[name][col])
            self.material_tree.insert('', 'end', values=d)
        
    def delete(self):
        for item in self.tree.selection():
            item_text = self.tree.item(item,"values")[0]
            self.parent.stock.removeProduct(item_text)
        for item in self.material_tree.selection():
            item_text = self.material_tree.item(item,"values")[0]
            del self.parent.material[item_text]
        self.parent.refresh()
        
    def modify(self, item=None):
        item = self.tree.selection()[0]
        item_text = self.tree.item(item,"values")[0]
        ori_amount = self.tree.item(item,"values")[1]
        
        top = tk.Toplevel()
        
        productList = sorted(list(self.parent.stock.data.keys()))
        self.productName = tk.StringVar(self)
        self.productName.set(item_text)
        productNameList = tk.OptionMenu( top, self.productName, *productList )
        label1 = tk.Label( top, text=u'產品名稱')
        label1.grid(row=0,column=0)
        productNameList.grid(row=0,column=1)
        
        label2 = tk.Label( top, text=u'產品數量')
        amount = tk.Entry(top)
        amount.insert(0, ori_amount)
        label2.grid(row=1, column=0)
        amount.grid(row=1, column=1)
        
        label2 = tk.Label( top, text=u'單位')
        unit = tk.Entry(top)
        unit.insert(0, self.parent.stock.productUnit[name])
        label2.grid(row=2, column=0)
        unit.grid(row=2, column=1)
        
        label2 = tk.Label( top, text=u'圖號')
        sn = tk.Entry(top)
        sn.insert(0, self.parent.stock.productSN[name])
        label2.grid(row=3, column=0)
        sn.grid(row=3, column=1)
        
        button = tk.Button( top, text=u'提交', command=lambda: self.submitModify(item_text, amount.get(), unit.get(), sn.get(), top) )
        button.grid(row=4, column=0)
        button2 = tk.Button( top, text=u'返回', command=top.destroy )
        button2.grid(row=4, column=1)
        
        top.mainloop()
        
    def submitModify(self, ori_name, amount, unit, sn, top):
        try:
            name = self.productName.get()
            amount = int( amount )
            if name != ori_name:
                self.parent.stock.removeProduct(ori_name)
            self.parent.stock.data[name] = {u'名稱':name, u'數量':amount, u'單位':unit, u'圖號':sn}
        except ValueError:
            messagebox.showinfo(u'錯誤', u'產品數量錯誤')
        else:
            top.destroy()
            self.parent.refresh()