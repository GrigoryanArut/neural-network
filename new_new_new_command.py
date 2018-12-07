import openpyxl
from neuroNet import neuroNet
from listNeuroNet import listNeuroNet

def fileRead(net,nomer):
    #считывание с файла
    fontSize=8 #размер шрифта 8*8
    with open('test'+nomer+'.txt', 'r') as text_file: #открываем файл
        iStroka=0 #номер строки
        kol=0 #количество букв в этой строке
        predKol=0 #количество букв в прошлой строке
        listLetter=[] #список букв
        listEnter=[] #список, где начинать новую строку
        for line in text_file: #читаем файл по строкам
            iStroka=iStroka+1
            if (iStroka%fontSize==1): #если номер строки 1,9,17..., то это начало новой строчки
                lengthStroka=len(line)-1 #-1 потому что знак перехода на новую строку
                predKol=kol
                kol=kol+(lengthStroka//fontSize)#lengthStroka//fontSize - сколько букв в строке
                if (predKol!=0):
                    listEnter.append(predKol)#добавление номера, когда нужно делать переход строки
                for z in range(predKol,kol):
                    listLetter.append([])#добавляет пустые списки для новых слов
            for z in range(predKol,kol):
                letterLine=[]
                for j in range(z*fontSize-predKol*fontSize,z*fontSize+fontSize-predKol*fontSize):
                    letterLine.append(int(line[j]))#считывает строку для одной буквы
                listLetter[z].extend(letterLine)#добавление в букву новую строчку цифр

    z=0
    k=0
    for i in listLetter:
        listVer={}#создание словаря, где ключ буква, а значение это выход нейросети
        for j in net.listNeuro:
            #перебор нейросетей для одной буквы
            j.x=i[:]
            j.calculate()
            listVer[j.name]=j.y3
        maximum = max(listVer, key=listVer.get)#нахождение максимума по словарю
        print(maximum, end='')
        z=z+1
        #перенос строки в выводе
        if ((len(listEnter)>0)and(z==listEnter[k])):
            if (k<len(listEnter)-1):
                k=k+1
            print()
    
def letterCopy(neuro,c,letter):
    #открытие книги EXCEL
    try:
        wb = openpyxl.load_workbook(filename = (letter+'.xlsx'))
    except Exception as e:
        print('not found excel file')
        return -1
    
    #открытие страницы
    try:
        sheet1 = wb['Лист1']
    except Exception as e:
        print('not found sheet Лист1')
        return -1
    
    #копирование буквы
    cEnd=c+8
    r=1
    for i in range(0,neuro.xCount):
        neuro.x[i]=sheet1.cell(row=int(r),column=int(c)).value
        c=c+1
        if (c==cEnd):
            c=c-8
            r=r+1
            
    neuro.calculate()
            
def teaching(neuro,listTeaching,lenAlphabet,kolLetterTeaching):
    #обучение по условию
    iterLesson=0
    excLesson=0
    #print(neuro.name)

    while (excLesson<lenAlphabet*kolLetterTeaching):#обучается пока не найдет все буквы с первого раза
        excLesson=0
        for i in listTeaching:
            if (i==neuro.name):
                neuro.z=1
            else:
                neuro.z=0
            for c in range(1,1+9*kolLetterTeaching,9):
                letterCopy(neuro,c,i)
                iterLesson=neuro.lesson()
                if (iterLesson==1):
                    excLesson=excLesson+1

def main():
    #создание списка нейросетей
    net = listNeuroNet()
    #список букв в алфавите
    listTeaching=['А','Г','И','К','Л','М','О','П','Р','Т','У','Ф','Х','Ц','Ч','Ш','Ъ','Ь','1','7']
    #создание нейросети и добавление их в список
    lenAlphabet=len(listTeaching)#длина алфавита
    kolLetterTeaching=9#сколько примеров каждой буквы
    for i in range(0,lenAlphabet):
        neuro = neuroNet(64,16,4,listTeaching[i])
        net.addNeuro(neuro)
        
    while True:
        menu=input("""
Введите команду:
t - teaching
fr - fileRead
sn - saveNeuro
ln - loadNeuro
ex - exit
""")

        if (menu=='t'):
            for i in net.listNeuro:
                teaching(i,listTeaching,lenAlphabet,kolLetterTeaching)
            print()
            print('t done')
        if (menu=='fr'):
            nomer=input("""
Введите цифру
""")
            fileRead(net,nomer)
            print()
            print('fr done')
        if (menu=='sn'):
            net.saveNeuro()
            print()
            print('sn done')
        if (menu=='ln'):
            net.loadNeuro()
            print()
            print('ln done')
        if (menu=='ex'):
            break

if __name__ == "__main__":
    main()
