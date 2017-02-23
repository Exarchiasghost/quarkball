#################################
#LIBRARIES(START)
#################################

from __future__ import division
import math
import random
#import numpy

#import sys
#import os
#import datetime

##############
#LIBRARIES(END)
##############




#########################
#GLOBAL VARIABBLES(START)
#########################
itIsTheFirstLine = True     #This variable is about the input line. If the line is the first the variable itIsTheFirstLine is True.
itIsTheFirstLine = True
T=0     #The number of lines with usefull Data. the number of tierations.
result = "Not any result right now" #this is used for the result wich is printed in the end of the code with the default value.
testSum = 0 #This is used to make the mainCheckFunction() bit more interesting but making the function to work as add function.
countForT = 0 #this is the count vairiable that helps to check that the iterations are not more than the predefined T variable.
countForDwnldN = 0
dwnldK = 0
dwnldTArray = []
dwnldDarray = []
spliterFunctionsArray = []

#first line variables.
howManyVideos = 0
howManyEndPoints = 0
howManyRequests = 0
howManyCaches = 0
howManyMBsPerCache = 0

fileForOutput = open('output.txt','w')
fileForInput = open('input.in','r')
#######################
#OGLOBAL VARIABLES(END)
#######################



##########################
#TEMPLATE FUNCTIONS(START)
##########################

#the mainCheckFunction() function is doing the necessary checking before the mainCalculativFunction().
#there is always something to check
def mainCheckFunction(checkFunctionsProperty):
        if checkFunctionsProperty == True:
                return True

#The function mainCalculativFunction() solves the logical problem of the exercise.
#Now it works like a SUM function.       
def mainCalculativFunction(inputProperty):
    global testSum #This is used to make the mainCheckFunction() bit more interesting but making it to work as add function.
    if mainCheckFunction(True):
        testSum = int(inputProperty) + testSum
        return str(testSum) 

#The function firstLineCorrection() changes the itIsTheFirstLine to False and stores the N to the variable T
def firstLineCorrection(inputForNInitiation):
    global itIsTheFirstLine
    global T
    itIsTheFirstLine = False
    T = inputForNInitiation

def SecondLineCorrection():
    global itIsTheSecondLine
    itIsTheSecondLine = False
    
#this is the function that uses the countForT to check up that the iterations are not more than what the T variable defines    
def iterationsCheck(hereGoesTheCountForTParameter):
    if hereGoesTheCountForTParameter >= int(T):
        return True
    
#My first thought was to use "for in" loop but after using it I figured out that the use of Range is the best solution.
#As I know, a loop with range is more efficient than the typical "for in" loop.
#Use this function in case of sorting, or in the case of temparated array. you will not regret it.    
def printFromArray(Arrayname, probablytheTVariable):
    for i in range(int(probablytheTVariable)):
        print(str(Arrayname[i]))

def printFromArray2(Arrayname):
    for i in Arrayname:
        print(str(Arrayname[i]))


        
#fills a two-dimensional array with the value N, (the line from the input).
#it needs to get called for every line from the main iteration, (for every N) 
#it needs to work before the twoDimentionalArrayHandler()
#it works optimaly inside the mainCalculativFunction()       
def spliterFunction(strValueFromN):
    global spliterFunctionsArray
    spliterFunctionsArray.append(strValueFromN.split(' ')) 
    
#this is the best way to handle the second dimention of two dimentional array
#it needs to work after the spliterFunction()
#it works optimaly inside the mainCalculativFunction()
#initialy works as sum function
def twoDimentionalArrayHandler(arrayNameParameter, Iterationsnumber):
    return int(arrayNameParameter[Iterationsnumber][0]) + int(arrayNameParameter[Iterationsnumber][1])



def firstLineSpliter(inputFromN):
    global howManyVideos, howManyEndPoints, howManyRequests, howManyCaches, howManyMBsPerCache
    firtstLine = inputFromN.split()
    howManyVideos = firtstLine[0]
    howManyEndPoints = firtstLine[1]
    howManyRequests = firtstLine[2]
    howManyCaches = firtstLine[3]
    howManyMBsPerCache = firtstLine[4]


def secondLineSpliter(inputFromN):
    videoArray = inputFromN.split()


def endPointHandler(inputFromN):
    global countForDwnldN, latency, i = 0
    endpointvalues = ""
    endpointvalues = inputFromN.split()
    if countForDwnldN == 0:
        i = i + 1
        endpointvalues[0] = latency
        countForDwnldN = endpointvalues[1]
        endPointArray[i].append(latency)
    else:
        endPointArray[i].append(endpointvalues)
        countForDwnldN = countForDwnldN - 1


def insideCaseCalculation(dwnldNparam, dwnldKparam):
    print(int(dwnldNparam) + int(dwnldKparam))

##########################
#TEMPLATE FUNCTIONS(END)
##########################
        
        
#################################
#OBJECT ORIENTED FUNCTIONS(START)
#################################
#stuff that help objects to do stuff.
#Those function are meant to be only inside the mainCalculativFunction()


#Helper function to calculate distance between 2 points
def distance(p1, q1, p2, q2):
    return math.sqrt((p1-q1)**2 + (p2-q2)**2)

#################################
#OBJECT ORIENTED FUNCTIONS(END)
#################################


###############
#CLASSES(START)
###############
#Here are all the classes.


#############
#CLASSES(END)
#############

class Object:
    def __init__(self):
        print("I am an object and i just been constructed")
        
class Cote(object):
    def __init__(self):
        print("I am an cote and i just been constructed")
        
class Chicken(Cote):
    def __init__(self):
        print("Winner! Winner! Chicken dinner!")
        
class Egg(Cote):
    def __init__(self):
        print("Hello sir! I am an egg and the answer for everything is 42")


#######################
#MAIN() FUNCTION(START)
#######################
    
#The main iteration, (AKA the main loop), now is the main() function. 
#The separation of code to functions blocks keeps the template simple and clear.    
def main():
    global countForT
    for N in fileForInput:
        print("itIsTheFirstLine now is " + str(itIsTheFirstLine))
        fileForOutput.write("itIsTheFirstLine now is " + str(itIsTheFirstLine))
        #print("itIsTheFirstLine now is " + str(itIsTheFirstLine) end='\n' file=f)
        if itIsTheFirstLine == True:
            firstLineCorrection(N)
            firstLineSpliter(N)
        elif itIsTheSecondLine = True:
            secondLineCorrection()
            secondLineSpliter(N)
        else:
            result = mainCalculativFunction(N)
            countForT += 1
            print("the T which represent the number of lines with input data, now is " + str(T)) 
            fileForOutput.write("the T which represent the number of lines with input data, now is " + str(T))       
            if iterationsCheck(countForT):
                #here add code when the answer comes in the end as a final result.
                printFromArray2(howManyVideos)
                printFromArray2(howManyEndPoints)
                printFromArray2(howManyRequests)
                printFromArray2(howManyCaches)
                printFromArray2(howManyMBsPerCache)
                printFromArray2(endPointArray)
                print("the result of the main calculative fuction know as mainCalculativFunction() now is " + result)
                fileForOutput.write("the result of the main calculative fuction know as mainCalculativFunction() now is " + result)
            else:
                #Here add code if there are many answers that are coming separately with every iteration.
                #here is the best location for the printFromArray()function.
                print ("the N now which is the value of the last input now is " + str(N))
                fileForOutput.write("the N now which is the value of the last input now is " + str(N))
                
if __name__ == "__main__": main()

#####################
#MAIN() FUNCTION(END)
#####################



#Optimal print example
#print("Case #", str(unregisteredcase), ": ", number_string2, " ",sep="", end='\n', file=f)


fileForInput.close()
fileForOutput.close()
print("That's all folks!")