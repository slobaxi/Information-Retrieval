import re
import nltk
from nltk.corpus import stopwords

#run to instal lib
#nltk.download()

stopWords = set(stopwords.words('english'))

def loadFiels(fileNames):
    list = []
    for fileName in fileNames:
        text = ""
        with open(fileName) as f:
            textRead = f.readlines()
        text = ""
        for s in textRead:
            text += s
        text = re.sub("[^0-9a-zA-Z]", " ", text)
        text = text.lower()
        list.append(text)
    return list    

def createInvertedIndex(fileNames):
    textList =loadFiels(fileNames)

    dic = {}
    i=0

    for text in textList:
        i += 1
        text = text.split(" ") 
        j = 0
        for word in text:
            if word in stopWords:
                continue
            j += 1
            if word in dic:
                if i not in dic[word]:
                    dic[word].append([i,j])         
            else:
                dic[word] = [[i,j]]

    return [dic,len(fileNames)]


def andInvertdIndex(invertedIndex : dict, stringList, max):     
    andList = set()

    for i in range (1,max+1):
        andList.add(i)

    for word in stringList:
        if(word in invertedIndex):
            array = invertedIndex[word]
            setHelper = set()
            for tuple in array:
                setHelper.add(tuple[0])
            andList = andList & setHelper
        else:
            return []        

    return andList 

def orInvertedIndex(invertedIndex,stringList):
    orList = set()
    for word in stringList:
        if(word in invertedIndex):
            array = invertedIndex[word]
            for tuple in array:
                orList.add(tuple[0])

    return orList            

#print(createInvertedIndex(["bridge.txt","bridge history.txt","bridge gameplay.txt","bridge auction.txt"]))                            

invrtIndex = createInvertedIndex(["bridge.txt","bridge history.txt","bridge gameplay.txt","bridge auction.txt"])

inputNum = input("Enter 1 for and, 2 for or, 3 for exit: ")
print(" ")


while True:
    inputStrings = input("enter input words separted with space: ")
    inputStrings = inputStrings.split(" ")
    if inputNum == "1":
       print(andInvertdIndex(invrtIndex[0],inputStrings,invrtIndex[1]))
    elif inputNum == "2":
        orInvertedIndex(invrtIndex[0],inputStrings)    
    else:
        break
    inputNum = input("Enter 1 for and, 2 for or, 3 for exit:") 
