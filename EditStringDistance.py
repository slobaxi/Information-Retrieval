from pydoc import doc
from turtle import xcor
import numpy as np
import re
from scipy.stats import kendalltau
import math

def  editStringDistanceHelper(s1,s2,dp,x,y):
    if(x > len(s1)):
        return dp[len(s1)][len(s2)]

    for i in range (1,len(s2)+1):
        if(s1[x-1] == s2[i-1]):
            dp[x][i] = dp[x-1][i-1]
        else:
            dp[x][i] = min(dp[x-1][i-1],dp[x][i-1],dp[x-1][i])+1

    return int(editStringDistanceHelper(s1,s2,dp,x+1,y))    

def editStringDistance(s1 : str, s2 : str):
    dp = np.zeros([len(s1)+1,len(s2)+1])
    for i in range (len(s1)+1):
        dp[i][0] = i
    for i in range (len(s2)+1):
        dp[0][i] = i    
    return editStringDistanceHelper(s1,s2,dp,1,1)



def setStringDistanceJaccard(s1 : str, s2 : str):
    set1, set2 = set(s1), set(s2)
    return len(set1 & set2) / len(set1 | set2)

def tfidf(term: str, fileNames, document):
    list = []
    doc = ""
    if document not in fileNames:
        return

    for fileName in fileNames:
        text = ""
        with open(fileName) as f:
            textRead = f.readlines()
        text = ""
        for s in textRead:
            text +=s
        list.append(text)
        if(fileName == document):
            doc = text    

    idf = 0
    df = 0

    doc = doc.split(" ")
    for word in doc:
        if word == term:
            df=+1

    occurance = 0
    length = 0
    for text in list:
        length += len(text)
        splitedText = text.split(" ")
        for word in splitedText:
            if word == term:
                occurance += 1
                break
    idf = math.log(len(fileNames)/occurance,10)

    return idf * df

print(tfidf("clockwise",["bridge auction.txt","bridge.txt","bridge gameplay.txt"],"bridge gameplay.txt"))
print(tfidf("bridge",["bridge auction.txt","bridge.txt","bridge gameplay.txt"],"bridge gameplay.txt"))

def test(fileName : str):
    text = ""
    with open(fileName) as f:
        textRead = f.readlines()
    text = ""
    for s in textRead:
        text +=s   
    text = text.split(" ")

    editDistance = []
    setDistance = []
    
    for s1 in text:
        for s2 in text:          
            edit = editStringDistance(s1,s2)
            editDistance.append(edit == 0 and 1 or 1/edit)  
            setDistance.append(setStringDistanceJaccard(s1,s2))

    return kendalltau(editDistance,setDistance)

    

# print(test("bridge.txt"))   
