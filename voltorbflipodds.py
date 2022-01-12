import math
from tkinter import *
def Calculate(totalsheight, totalswidth, possmatrix):


    #[heightinitvals] is 2 x "height" matrix where 
    #the ith value of the first entry is the number of 0s in the ith row and 
    #the ith value of the second entry is the total of the numbers in the ith row

    #[heightinitvals] is 2 x "width" matrix where 
    #the ith value of the first entry is the number of 0s in the ith column and 
    #the ith value of the second entry is the total of the numbers in the ith column

    #[allpossiblebyrow] is an mxa matrix where a is unknown and the ith entry indicates the raw possible sequences for the ith row of the board
    #[allpossiblebycol] is an nxa matrix where a is unkown and the ith entry indicates the raw possible sequences for the ith column of the board

    #m=len(heightinitvals)
    #n=len(widthinitvals)
    allpossiblebyrow=possmatrix
    allpossiblebycol=transposemat(possmatrix)
    m=len(allpossiblebyrow)
    n=len(allpossiblebycol)
    possiblerowcombs=[[] for i in range(m)]
    possiblecolcombs=[[] for j in range(n)]
    for i in range(m):
        possiblerowcombs[i]=combs(allpossiblebyrow[i]) #creates a matrix of possible combinations for each row based on the possible values for each element in a row
    for i in range(n):
        possiblecolcombs[i]=combs(allpossiblebycol[i])#creates a matrix of possible combinations for each column based on the possible values for each element in a column

    temprowcombs=checktotals(totalsheight, possiblerowcombs) #removes number combinations for each row (represented as tuples) whose totals 
                                                             #do not add up to the total indicated by the game for that row
    tempcolcombs=checktotals(totalswidth, possiblecolcombs) #removes number combinations for each column (represented as tuples) whose totals 
                                                            #do not add up to the total indicated by the game for that column

    rowcombsnoinv=removeinvalid(temprowcombs, tempcolcombs) #removes number combinations for each row that cannot possibly match with any number combinations for a column
    colcombsnoinv=removeinvalid(tempcolcombs, temprowcombs) #removes number combinations for each column that cannot possibly match with any number combinations for a row



    oddslossrow, oddsgoodrow=calcpercentagemat(rowcombsnoinv) #calculates the percentage of combinations that have 0 in the (i,j) entry and the percentage that have 2 or 3 in the (i,j) entry for 
                                                              #oddslossrow and oddsgoodrow respectively
    oddsloss2, oddsgood2=calcpercentagemat(colcombsnoinv)
    oddslosscol=transposemat(oddsloss2)
    oddsgoodcol=transposemat(oddsgood2)
    
    return oddslossrow, oddsgoodrow, oddslosscol, oddsgoodcol

def removeinvalid(possiblecombs1, possiblecombs2):             #removes number combinations for each entry of "possiblecombs1" that cannot possibly match with any number combinations for "possiblecombs2"
                                                               #assuming one argument represents possible combinations for a set of rows and the other argument for a set of columns
                                                               #e.g. if possiblecombs1[0]=[(0,0,1,2,2),(1,0,2,0,2)] but possiblecombs2[0]=[(1,1,1,1,1)], then (0,0,1,2,2) will be removed from 
                                                               #possiblecombs1 since possiblecombs2[0] would indicate that the only possible value for entry (0,0) in the game could be "1", then (0,0,1,2,2) cannot possibly be
                                                               # in possiblecombs1, as that would indicate that entry (0,0) is "0"
    m=len(possiblecombs1)
    n=len(possiblecombs2)
    finalcombs=[[] for i in range(m)]
    for i in range(m):
        for j in range(len(possiblecombs1[i])):
            valid1=True
            for k in range(n):
                valid2=False
                for l in range(len(possiblecombs2[k])):
                    if possiblecombs1[i][j][k]==possiblecombs2[k][l][i]:
                        valid2=True

                valid1=valid1 and valid2
            if valid1:
                finalcombs[i].append(possiblecombs1[i][j])
    return finalcombs


def calcpercentagemat(combs):
                                                        #calcpercentagemat takes the possible row/column value combinations, which is what "combs" is, and calculates both the
                                                        #percentage of combinations that have 0 as the (i,j) entry and stores taht value as oddsloss[i][j]. Additionally, it calculates the
                                                        #percentage of possible combinations that have 2 or 3 as the (i,j) entry and stores that value as oddsgood[i][j]
    oddsloss=[[0 for i in range(len(combs[0][0]))]for j in range(len(combs))]
    oddsgood=[[0 for i in range(len(combs[0][0]))]for j in range(len(combs))]

    for i in range(len(combs)):
        for k in range(len(combs[0][0])):
            losses=0
            special=0
            for j in range(len(combs[i])):
                if combs[i][j][k]==0:
                    losses+=1
                elif combs[i][j][k]!=1:
                    special+=1
            oddsloss[i][k]=(((losses/len(combs[i]))*1000)//1)/1000
            oddsgood[i][k]=(((special/len(combs[i]))*1000)//1)/1000
    return oddsloss, oddsgood

def checktotals(totals, combs):                     #simply removes "possible" number combinations for a row or column whose sum of the values do not equal the total indicated by the game board
                                                    #therefore, if a possible combination for row 1 is indicated by (0,1,1,0,1) being in combs, but the total for row 1 indicated by the gameboard is 2,
                                                    #then (0,1,1,0,1) is removed from the matrix returned by checktotals
    retcombs=[[]for i in range(len(combs))]
    for i in range(len(combs)):
        for j in range(len(combs[i])):
            total0=0
            total=0
            for k in range(len(combs[i][j])):
                if combs[i][j][k]==0:
                    total0+=1
                total+=combs[i][j][k]
            if total0==totals[0][i] and total==totals[1][i]:
                retcombs[i].append(combs[i][j])
    return retcombs
            

def combs(combslist):
    #takes in mxn matrix of tuples of possible values for each entry
    #the (i,j) entry of combs list indicates the possible values for the (i,j) square in the game
    if len(combslist)==0:
        return [()]
    else:
        tempret=[]
        for elt in (combslist[0]):
            tempmat=combs(combslist[1:])
            for tup in tempmat:
                tempret.append((elt,)+tup)
        return tempret

def transposemat(matrix):
    tempmat=[[0 for i in range(len(matrix))] for j in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            tempmat[j][i]=matrix[i][j]
    return tempmat



def fullcalculation(totalsheight, totalswidth, possmatrix):
                                                #this can be thought of as the "main" fucntion. It first calls the calculate function which returns the matrices of 
                                                # probabilities based on the possible number combinations by row and by column. It then takes the geometric mean of these matrices and returns it element wise.
                                                #For example, if "oddslossrows" calculates that the probability that entry (0,0) of the game is 25% and "oddslosscols" calculates that the probability that entry
                                                #(0,0) of the game is 10%, then "finallossodds"[0][0]=sqrt(.25*.1)=.158 or 15.8% chance. I (somewhat) arbitrarily chose geometric mean because i felt that this 
                                                #was the best (and simplest) way to combine the results of the two odds matrices while maintaining the integrity of the estimated probability since the raw value of the probability
                                                #doesn't intrinsicly matter, only the value of the probability when compared to the other probabilities in "finallossodds". The same process was used for "finalgoododds".
                                                #Next, form this final matrix of probabilities "finaloddsloss", I simply calculated which entry (i,j) had the smallest value (whilst not being equal to 0, implying we already know the value of that entry to not be 0).
                                                # This entry(i,j) would then be our next best guess. If there were multiple entries in "finallossodds" that had the same smallest probability, a tiebreaker was decided by checking "finalgoododds" and seeing whcih of these 
                                                # "lowest probabiliity entries" had the *highest* probability of being a 2 or a 3 since revealing 2's and 3's help more than revealing a 1. If there was still a tie here, it just randomly returns one of these entries as the next best guess
    oddslossrows, oddsgoodrows, oddslosscols,oddsgoodcols = Calculate(totalsheight, totalswidth, possmatrix)

    finallossodds=[[0 for i in range(len(oddslosscols))]for j in range(len(oddslosscols[0]))]
    finalgoododds=[[0 for i in range(len(oddslosscols))]for j in range(len(oddslosscols[0]))]
    for i in range(len(oddslosscols)):
        for j in range(len(oddslosscols[0])):
            finallossodds[i][j]=int(( math.sqrt(oddslosscols[i][j]*oddslossrows[i][j])*100)//1)
            finalgoododds[i][j]=int((math.sqrt(oddsgoodcols[i][j]*oddsgoodrows[i][j])*100)//1)

    lowest=100
    lowestcoords=[]
    for i in range(len(possmatrix)):    
        for j in range(len(possmatrix[0])):

            if len(possmatrix[i][j])!=1 and finallossodds[i][j]<lowest and oddsgoodrows[i][j]!=0:
                lowest=finallossodds[i][j]
                lowestcoords=[(i,j)]
            elif finallossodds[i][j]==lowest and len(possmatrix[i][j])!=1 and oddsgoodrows[i][j]!=0:
                lowestcoords.append((i,j))
    highest=0
    highestcoords=[]
    for tup in lowestcoords:
        (i,j)=tup
        if finalgoododds[i][j]>highest:
            highest=finalgoododds[i][j]
            highestcoords=[(i,j)]
        elif finalgoododds[i][j]==highest:
            highestcoords.append((i,j))



    #print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in finallossodds]))
    #print("\n")
    #print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in finalgoododds]))
    #print("\n")

    return lowestcoords, highestcoords


#Everything below here need not much explanation. I decided after writing the initial code to include a GUI to make the using of this program easier, especially for people besides myself. 
#it simply adds in 45 possible entry boxes, 25 for the cards in the game to be flipped and 20 for the intial values found on the gameboard indicated the row/column value sums and the number of 0's in each.
#It then returns onscreen the best possible choice for your next card as calculated above in the rest of the program

def addnewentry(canvas, size, x, y):
    myentry=Entry(root)
    canvas.create_window(x,y,height=boxsize, width=boxsize, window=myentry)
    return myentry

def addnewlabel(canvas, size, x, y, inptext):
    mylabel=Label(root, text=inptext)
    canvas.create_window(x,y,height=boxsize, width=boxsize, window=mylabel)
    return

root=Tk()
boxsize=35
h=5
w=5
entryarray=[[None for j in range(w+2)]for i in range(h+2)]

canvas1=Canvas(root, width =15*boxsize, height=15*boxsize)
canvas1.pack()
    

for i in range(h+2):
    for j in range(w+2):
        x=(2+i)*1.5*boxsize-.5*boxsize
        y=(2+j)*1.5*boxsize-.5*boxsize
        if i<=4 or j<=4:
            if i>=5:
                x+=boxsize
            if j>=5: 
                y+=boxsize           
            entryarray[i][j]=addnewentry(canvas1, boxsize, x,y)
        if i==0:
            x2=boxsize
            y2=(2+j)*1.5*boxsize-.5*boxsize
            mytext=str(j+1)
            if j==5:
                mytext="S"
                y2+=boxsize
            elif j==6:
                mytext="V"
                y2+=boxsize
            addnewlabel(canvas1, boxsize, x2, y2, mytext)
        if j==0:
            x2=(2+i)*1.5*boxsize-.5*boxsize
            y2=boxsize
            mytext=str(i+1)
            if i==5:
                mytext="S"
                x2+=boxsize
            elif i==6:
                mytext="V"
                x2+=boxsize
            addnewlabel(canvas1, boxsize, x2, y2, mytext)            
        
for i in range(h+2):
    x2=boxsize
    y2=(2+i)*1.5*boxsize-.5*boxsize
    mytext=str(i+1)
    if i==5:
        y2+=boxsize
        mytext="S"
    elif i==6:
        y2+=boxsize
        mytext="V"
    
def solve():
    pmatrix=[[(0,1,2,3) for j in range(w)]for i in range(h)]
    theight=[[],[]]
    twidth=[[],[]]
    for i in range(h):
        for j in range(w):
            if len(entryarray[i][j].get())!=0:
                pmatrix[j][i]=tuple([int(entryarray[i][j].get())])
                
    tempw1=[]
    tempw2=[]    
    for i in range(h):
        tempw1.append(int(entryarray[i][w+1].get()))
        tempw2.append(int(entryarray[i][w].get()))
    twidth[0]=tuple(tempw1)
    twidth[1]=tuple(tempw2)

    temph1=[]
    temph2=[]
    for j in range(w):
        temph1.append(int(entryarray[h+1][j].get()))
        temph2.append(int(entryarray[h][j].get()))
    theight[0]=tuple(temph1)
    theight[1]=tuple(temph2)

    bestodds, bestoddshigh = fullcalculation(theight, twidth, pmatrix)
    bestchoicesstr="best choices"
    for elt in bestodds:
        bestchoicesstr+="; ("+ str(elt[0]+1) + ", " +str(elt[1]+1)+")"
    besthighstr="tiebreaker; " "("+ str(bestoddshigh[0][0]+1) + ", " +str(bestoddshigh[0][1]+1)+")"       
    label1=Label(root, text=bestchoicesstr)
    canvas1.create_window(11.75*boxsize, 12*boxsize, width= 5*boxsize, window=label1)
    label2=Label(root, text=besthighstr)
    canvas1.create_window(11.75*boxsize, 12.5*boxsize, window=label2)

button1=Button(text="Solve", command=solve)
canvas1.create_window(11.75*boxsize, 11*boxsize, height=boxsize, width=2.5*boxsize, window=button1)
root.mainloop()
