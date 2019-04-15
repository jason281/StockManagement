# -*- coding: utf-8 -*-

class Company:
    def __init__( self, companyName ):
        self.name = companyName
        self.data = {}
        self.history = []
        
    def add(self, productName, productAmount, totalPrice, time):
        if productName not in self.data:
            self.data[productName] = 0
        self.data[productName] += productAmount
        
        his = {}
        his['Time'] = time
        his['Name'] = productName
        his['Amount'] = productAmount
        his['UnitPrice'] = totalPrice*1.0/productAmount
        his['TotalPrice'] = totalPrice
        self.history.append(his)
    