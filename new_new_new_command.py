import openpyxl
from neuroNet import neuroNet

def fileRead(neuro,nomer):
    #считывание с файла
    fontSize=8
    with open('test'+nomer+'.txt', 'r') as text_file:
        i=0
        for line in text_file:
            for j in range(0,fontSize):
                neuro.x[i]=int(line[j])
                i=i+1
                
    neuro.calculate()
    print(neuro.y3)
    
def letterCopy(neuro,r,c):
    #открытие книги EXCEL
    try:
        wb = openpyxl.load_workbook(filename = 'в.xlsx')
        #print('excel file open')
    except Exception as e:
        print('not found excel file')
        return -1
    
    #открытие страницы
    try:
        sheet1 = wb['Буквы']
        #print('found sheet Буквы')
    except Exception as e:
        print('not found sheet Буквы')
        return -1
    
    #копирование буквы
    cEnd=c+8;
    for i in range(0,neuro.xCount):
        neuro.x[i]=sheet1.cell(row=int(r),column=int(c)).value
        c=c+1
        if (c==cEnd):
            c=c-8
            r=r+1
            
    neuro.calculate()
            
def teaching(neuro):
    #обучение по условию
    iterLesson=0
    excLesson=0
    r=1
    c=1
    i=1

    while (excLesson<10):
        letterCopy(neuro,r,c)
        iterLesson=neuro.lesson()
        if (iterLesson==1):
            excLesson=excLesson+1
        else:
            excLesson=0
        
        c=c+9

        if (c>64):
            c=1
            r=10
            neuro.z=0

        if ((r==10)and(c>55)):
            c=1
            r=1
            neuro.z=1

def main():
    neuro = neuroNet(64,15,5)

    while True:
        menu=input("""
Введите команду:
rw - randomWeights
t - teaching
fr - fileRead
o - outWindow
sn - saveNeuro
ln - loadNeuro
ex - exit
""")
        if (menu=='rw'):
            neuro.randomWeights()
            print()
            print('rw done')
        if (menu=='t'):
            teaching(neuro)
            print()
            print('t done')
        if (menu=='o'):
            neuro.outWindow()
        if (menu=='fr'):
            nomer=input("""
Введите цифру
""")
            fileRead(neuro,nomer)
            print()
            print('fr done')
        if (menu=='sn'):
            neuro.saveNeuro()
            print()
            print('sn done')
        if (menu=='ln'):
            neuro.loadNeuro()
            print()
            print('ln done')
        if (menu=='ex'):
            break

if __name__ == "__main__":
    main()
