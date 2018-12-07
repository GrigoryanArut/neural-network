import random
from math import exp
import pickle

class neuroNet:

    def __init__(self,xCount,y1Count,y2Count,name):
        self.x=[]#входной слой
        self.w1=[]#веса перед первым скрытым
        self.e1=[]#взвешенная сумма в первым скрытым
        self.y1=[]#выход первого скрытого
        self.w2=[]#веса перед вторым скрытым
        self.e2=[]#взвешенная сумма во втором скрытом
        self.y2=[]#выход второго скрытого
        self.w3=[]#веса перед выходом
        self.e3=0#взвешенная сумма в выходе
        self.y3=0#выход нейросети
        self.z=1#эталон
        self.d3=1#ошибка выхода
        self.d2=[]#ошибка второго скрытого
        self.d1=[]#ошибка перовго скрытого
        self.w1New=[]#новые веса перед первым скрытым
        self.w2New=[]#новые веса перед вторым скрытым
        self.w3New=[]#новые веса перед выходом
        self.xCount=xCount#количество входных нейронов
        self.y1Count=y1Count#количество нейронов в первом скрытом слое
        self.y2Count=y2Count#количество нейронов во втором скрытом слое
        self.name=name#буква нейросети
        self.xInit()

    def xInit(self):
    #заполнение нулями всего чего можно при инициализации
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

    #рандомные веса при инициализации 
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
        #вывод нейросети (старая версия)
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
        #рандомные веса (старая версия)
        for i in range(0,(self.xCount*self.y1Count)):
            self.w1[i]=random.uniform(-1, 1)
        for i in range(0,(self.y1Count*self.y2Count)):
            self.w2[i]=random.uniform(-1, 1)
        for i in range(0,self.y2Count):
            self.w3[i]=random.uniform(-1, 1)

    #подсчёт
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
        if (self.z==1):
            if (self.y3>0.9):
                return 0
        elif (self.z==0):
            if (self.y3<0.9):
                return 0
        for i in range(1,1001):
            #замена весов, новыми весами
            self.w1=self.w1New[:]
            self.w2=self.w2New[:]
            self.w3=self.w3New[:]
            self.calculate()
            #проверка на эталон, 90 процентов точность
            if (self.z==1):
                if (self.y3>0.9):
                    return i
            elif (self.z==0):
                if (self.y3<0.9):
                    return i
        return 1000
