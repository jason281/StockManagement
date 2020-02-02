# -*- coding: utf-8 -*-

import datetime
import os
import pandas as pd
from .company import Company

kMaterialFileName = "material.csv"
kHistoryFileName = "history.csv"
kProductFileName = "Product.csv"

class Stock:
    def __init__(self):
        self.material = {'':{u'物料名稱':'', u'物料編碼':'', u'數量':0, u'單位':''}}
        self.data = pd.DataFrame(columns=[u'名稱', u'公司', u'數量', u'單位', u'圖號', u'消耗1', u'消耗2', u'消耗3', u'消耗4', u'消耗5']).set_index([u'公司', u'名稱'])
        self.history = []
        self.historymap = {}
        self.history_count = 0
        self.companies = {'':None}

    def loadData(self):
        if os.path.exists(kMaterialFileName):
            self.material = pd.read_csv(kMaterialFileName, encoding = 'utf-8', index_col = 0).to_dict(orient='index')
        if os.path.exists(kProductFileName):
            self.data = pd.read_csv(kProductFileName, encoding = 'utf-8', index_col = (0,1))
            self.data = self.data.fillna('')
        if os.path.exists(kHistoryFileName):
            self.history = pd.read_csv(kHistoryFileName, encoding = 'utf-8', index_col = 0).fillna('').to_dict(orient='records')
            self.history_count = self.history[-1]['ID']
            for idx in range(len(self.history)):
                self.historymap[str(self.history[idx]['ID'])] = idx

    def saveData(self):
        pd.DataFrame(list(self.material.values()), index=self.material.keys()).to_csv(kMaterialFileName, encoding = 'utf_8_sig')
        self.data.to_csv(kProductFileName, encoding = 'utf_8_sig')
        pd.DataFrame(self.history).to_csv(kHistoryFileName, encoding = 'utf_8_sig')
        #pd.DataFrame(self.companies)
    
    def inStock( self, productName, companyName, productAmount, time = datetime.datetime.now() ):
        if (companyName, productName) not in self.data:
            self.data.loc[companyName, productName] = [0, '', '', '', '', '', '', '']
            #{u'數量':0, u'單位':'', u'圖號':'', u'消耗1':'', u'消耗2':'', u'消耗3':'' u'消耗4':'', u'消耗5':''}
        self.data.loc[(companyName, productName), u'數量'] += productAmount
        
        self.historymap[str(self.history_count+1)] = self.history_count
        self.history_count += 1
        self.history.append({'ID':self.history_count, u'時間':time, u'操作':u'入庫', u'產品名稱':productName, u'產品數量':productAmount, u'公司名稱':companyName, u'總價':''})
        
    def outStock( self, productName, productAmount, companyName, totalPrice, time = datetime.datetime.now() ):
        # Stop illegal operation
        assert self.data.index.isin([(companyName, productName)]).any()
        assert self.data.loc[(companyName, productName)][u'數量'] > productAmount
        
        if companyName not in self.companies:
            self.companies[companyName] = Company(companyName)
            
        comp = self.companies[companyName]
        comp.add(productName, productAmount, totalPrice, time)
        
        self.data.loc[(companyName, productName), u'數量'] -= productAmount
        
        self.historymap[str(self.history_count+1)] = self.history_count
        self.history_count += 1
        self.history.append({'ID': self.history_count, u'時間':time, u'操作':u'銷庫', u'產品名稱':productName, u'產品數量':productAmount, u'公司名稱':companyName, u'總價':totalPrice})
        
    def addCompany(self, companyName):
        self.companies[companyName] = Company(companyName)
        
    def historyquery(self, id):
        #print(self.historymap)
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
        
