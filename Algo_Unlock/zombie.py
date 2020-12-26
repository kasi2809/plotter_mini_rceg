
z=[]
days=0
try:
    # Main function
    if __name__ == '__main__':
        # take the T (test_cases) input
        array_size=int(input())
        if array_size<1 or array_size>10**5:
            raise ValueError
        instring = input()
        z= instring.split(" ")
        if (len(z) != array_size):
            raise ValueError
        for i in range(array_size):
            z[i]=int(z[i])
            if(z[i]<0 or z[i]>10**9):
                 raise ValueError

        while True:
            temp_index=[]
            temp_z=[]
            if len(z)>=2:
                for index in range(1,len(z),2):
                    if z[index]>z[index-1]:
                        temp_index.append(index)
            if len(temp_index)==0:
                break
            else:
                for k in range(len(z)):
                    if k not in temp_index:
                        temp_z.append(z[k])
                z=temp_z[0:len(temp_z)]
                days+=1

        print(days)
except:
    pass