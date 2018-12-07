import pickle

class listNeuroNet:

    def __init__(self):
        self.listNeuro=[]#список нейросетей

    def addNeuro(self,neuro):
        self.listNeuro.append(neuro)#добавление нейросети в список
        
    def saveNeuro(self):
        #сохранение нейросети
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.__dict__, f)

    def loadNeuro(self):
        #загрузка нейросети
        with open('data.pickle', 'rb') as f:
            self.__dict__ = pickle.load(f)
