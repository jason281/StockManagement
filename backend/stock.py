# -*- coding: utf-8 -*-

import datetime
import os
import pandas as pd
from .company import Company

class Stock:
    def __init__(self):
        self.material = {'':{u'物料名稱':'', u'物料編碼':'', u'數量':0, u'單位':''}}
        self.data = {'':{u'名稱':'', u'數量':0, u'單位':'', u'圖號':'', u'消耗':{}}}
        self.history = []
        self.historymap = {}
        self.history_count = 0
        self.companies = {'':None}
    
    def inStock( self, productName, productAmount, time = datetime.datetime.now() ):
        if productName not in self.data:
            self.data[productName] = {u'名稱':productName, u'數量':0, u'單位':'', u'圖號':'', u'消耗':[]}
        self.data[productName][u'數量'] += productAmount
        
        self.historymap[str(self.history_count+1)] = self.history_count
        self.history_count += 1
        self.history.append({'ID':self.history_count, u'時間':time, u'操作':u'入庫', u'產品名稱':productName, u'產品數量':productAmount, u'公司名稱':'', u'總價':''})
        
    def outStock( self, productName, productAmount, companyName, totalPrice, time = datetime.datetime.now() ):
        # Stop illegal operation
        assert productName in self.data and self.data[productName] > productAmount
        
        if companyName not in self.companies:
            self.companies[companyName] = Company(companyName)
            
        comp = self.companies[companyName]
        comp.add(productName, productAmount, totalPrice, time)
        
        self.data[productName][u'數量'] -= productAmount
        
        self.historymap[str(self.history_count+1)] = self.history_count
        self.history_count += 1
        self.history.append({'ID': self.history_count, u'時間':time, u'操作':u'銷庫', u'產品名稱':productName, u'產品數量':productAmount, u'公司名稱':companyName, u'總價':totalPrice})
        
    def addCompany(self, companyName):
        self.companies[companyName] = Company(companyName)
        
    def historyquery(self, id):
        return self.history[self.historymap[id]]
    
    def removeProduct(self, productName):
        if productName in self.data:
            self.data.pop(productName)
            
    def inMaterial(self, name, amount, date):
        if name not in self.material:
            self.material[name] = {u'物料名稱':name, u'物料編碼':'', u'數量':0, u'單位':''}
        self.material[name][u'數量'] += amount
        
        self.historymap[str(self.history_count+1)] = self.history_count
        self.history_count += 1
        self.history.append({'ID':self.history_count, u'時間':date, u'操作':u'物料入庫', u'產品名稱':name, u'產品數量':amount, u'公司名稱':'', u'總價':''})
        