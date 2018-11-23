import random
from math import exp
import pickle

class neuroNet:

    def __init__(self,xCount,y1Count,y2Count):
        self.x=[]
        self.w1=[]
        self.e1=[]
        self.y1=[]
        self.w2=[]
        self.e2=[]
        self.y2=[]
        self.w3=[]
        self.e3=0
        self.y3=0
        self.z=1
        self.d3=1
        self.d2=[]
        self.d1=[]
        self.w1New=[]
        self.w2New=[]
        self.w3New=[]
        self.xCount=xCount
        self.y1Count=y1Count
        self.y2Count=y2Count
        self.xInit()

    def xInit(self):
        for i in range(0,self.xCount):
            self.x.append(0)
        for i in range(0,self.y1Count):
            self.e1.append(0)
            self.y1.append(0)
            self.d1.append(0)
        for i in range(0,self.y2Count):
            self.e2.append(0)
            self.y2.append(0)
            self.d2.append(0)
        self.w1Init()
        self.w2Init()
        self.w3Init()

    def w1Init(self):
        for i in range(0,(self.xCount*self.y1Count)):
            self.w1.append(random.uniform(-1, 1))
        self.w1New=self.w1[:]

    def w2Init(self):
        for i in range(0,(self.y1Count*self.y2Count)):
            self.w2.append(random.uniform(-1, 1))
        self.w2New=self.w2[:]

    def w3Init(self):
        for i in range(0,self.y2Count):
            self.w3.append(random.uniform(-1, 1))
        self.w3New=self.w3[:]

    def outWindow(self):
        print(self.x)
        print(self.w1)
        print(self.e1)
        print(self.y1)
        print(self.w2)
        print(self.e2)
        print(self.y2)
        print(self.w3)
        print(self.e3)
        print(self.y3)
        print(self.z)
        print(self.d3)
        print(self.d2)
        print(self.d1)
        print(self.w1New)
        print(self.w2New)
        print(self.w3New)
        
    def randomWeights(self):
        for i in range(0,(self.xCount*self.y1Count)):
            self.w1[i]=random.uniform(-1, 1)
        for i in range(0,(self.y1Count*self.y2Count)):
            self.w2[i]=random.uniform(-1, 1)
        for i in range(0,self.y2Count):
            self.w3[i]=random.uniform(-1, 1)

    def calculate(self):
        for i in range(0,self.y1Count):
            self.e1[i]=0
            for j in range(0,self.xCount):
                #сумма перед 1 скрытым слоем
                self.e1[i]=self.e1[i]+self.x[j]*self.w1[self.xCount*i+j]
            #выход 1 скрытого слоя
            self.y1[i]=1/(1+exp(-self.e1[i]))
        for i in range(0,self.y2Count):
            self.e2[i]=0
            for j in range(0,self.y1Count):
                #сумма перед 2 скрытым слоем
                self.e2[i]=self.e2[i]+self.y1[j]*self.w2[self.y1Count*i+j]
            #выход 2 скрытого слоя
            self.y2[i]=1/(1+exp(-self.e2[i]))
        self.e3=0
        for i in range(0,self.y2Count):
            #сумма перед выходом
            self.e3=self.e3+self.y2[i]*self.w3[i]
        #выход
        self.y3=1/(1+exp(-self.e3))
        #ошибка
        self.d3=self.z-self.y3
        #ошибка 2 скрытого слоя
        for i in range(0,self.y2Count):
            self.d2[i]=self.w3[i]*self.d3
        #ошибка 1 скрытого слоя
        for i in range(0,self.y1Count):
            self.d1[i]=0
            for j in range(0,self.y2Count):
                self.d1[i]=self.d1[i]+self.w2[j*self.y1Count+i]*self.d2[j]
        #новые веса между входным и 1 скрытым слоем
        j=0
        for i in range(0,(self.xCount*self.y1Count)):
            self.w1New[i]=self.w1[i]+self.d1[i//self.xCount]*(exp(-self.e1[i//self.xCount])/(1+exp(-self.e1[i//self.xCount]))**2)*self.x[j]
            j=j+1
            if (j==self.xCount):
                j=0
        #новые веса между 1 скрытым слоем и 2 скрытым слоем
        j=0
        for i in range(0,(self.y1Count*self.y2Count)):
            self.w2New[i]=self.w2[i]+self.d2[i//self.y1Count]*(exp(-self.e2[i//self.y1Count])/(1+exp(-self.e2[i//self.y1Count]))**2)*self.y1[j]
            j=j+1
            if (j==self.y1Count):
                j=0
        #новые веса между 2 скрытым слоем и выходом
        for i in range(0,self.y2Count):
            self.w3New[i]=self.w3[i]+self.d3*(exp(-self.e3)/(1+exp(-self.e3))**2)*self.y2[i]
        
    def lesson(self):
        for i in range(1,151):
            self.w1=self.w1New[:]
            self.w2=self.w2New[:]
            self.w3=self.w3New[:]
            self.calculate()
            if (self.z==1):
                if (self.y3>0.95):
                    return i
            elif (self.z==0):
                if (self.y3<0.05):
                    return i
        return 150

    def saveNeuro(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.__dict__, f)

    def loadNeuro(self):
        with open('data.pickle', 'rb') as f:
            self.__dict__ = pickle.load(f)
