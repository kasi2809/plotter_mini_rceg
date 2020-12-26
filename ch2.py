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
        if ((containerNo < 1 or containerNo > 1000) or (quiery < 1 or query > 1000)):
            raise ValueError
#insert towRobots() here


        testCase -= 1

####################################################################################################






except:
    pass
