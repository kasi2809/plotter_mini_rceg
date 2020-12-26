#Global variable

def twoRobots(containerNo, query):
    robotAPos = robotBPos = 0
    instruction = []
    for i in range(query):
        temp = input().split()
        temp = [int(x) for x in temp]

        #To satisfy the constraints
        for i in temp: 
            if( i < 1 or i > query ):
                raise ValueError
        if (temp[0] == temp[1]):
            raise ValueError

        instruction.append(temp)
     
#disctance covered
    distanceCovered =[]
    
    if(robotAPos_temp == instruction[0][0]):
        robotAPos = instruction[0][1]
        
    elif(robotBPos_temp == instruction[0][0]):
        robotBPos = instruction[0][1]

    

    distanceCovered.append( abs(instruction[0][1] - instruction[0][0]))
    #instruction.pop(0)
    
    if( robotAPos == instruction[1][0]):
        robotAPos = instruction[1][1]
        distanceCovered.append( abs(instruction[1][1] - instruction[1][0]))
    else:   
        robotBPos = instruction[1][1]
        distanceCovered.append( abs(instruction[1][1] - instruction[1][0]))

    for i in range(2, len(instruction)): 
        if ( abs(robotAPos -  instruction[i][0]) > abs(robotBPos -  instruction[i][0])):
            robotBPos = instruction[i][1]
            distanceCovered.append( abs(robotBPos -  instruction[i][0])+ abs(instruction[i][1] - instruction[i][0]))
        else: 
            robotAPos = instruction[i][1]
            distanceCovered.append( abs(robotAPos -  instruction[i][0]+ abs(instruction[i][1] - instruction[i][0])))
    
    robotAPos_temp = robotAPos
    robotBPos_temp = robotBPos

    return sum(distanceCovered)
try:

####################################################################################################
                        #getting input from user 
    testCase=int(input())
    if (tesCase < 1 or testCase > 50):
        raise ValueError

    while(testCase > 0):
        mn = input().split()
        containerNo = int(mn[0])
        query = int(mn[1])
        if ((containerNo < 1 or containerNo > 1000) or (query < 1 or query > 1000)):
            raise ValueError
#insert towRobots() here
        minDis = twoRobots()
        print(minDis)

        
        testCase -= 1

####################################################################################################






except:
    pass
