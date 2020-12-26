# Complete the solve function below.
def solve(points):
    global x,y,z
    x1 = points[0][0]
    y1 = points[0][1]
    z1 = points[0][2]
    ###
    x2 = points[1][0]
    y2 = points[1][1]
    z2 = points[1][2]
    ###
    x3 = points[2][0]
    y3 = points[2][1]
    z3 = points[2][2]
    ###
    x = points[3][0]
    y = points[3][1]
    z = points[3][2]
    ###
    for s in range(0,4):
        for t in range(0,3):
            if points[s][t]<(-1000) or points[s][t]>1000:
                raise ValueError
    ###
    e1 = ((y2-y1)*(z3-z1))-((y3-y1)*(z2-z1))
    e2 = -((z3-z1)*(x2-x1))-((z2-z1)*(x3-x1))
    e3 = ((x2-x1)*(y3-y1))-((x3-x1)*(y2-y1))
    e4 = -((e1*x1)+(e2*y1)+(e3*z1))

    out = e1*x + e2*y + e3*z + e4
    if (out == 0):
        return 'YES'
    else:
        return 'NO'
try:
    T = int(input())
    if T<1 or T>10**4:
        raise ValueError
    for t_itr in range(T):
        points = []
        for _ in range(4):
            points.append(list(map(int, input().rstrip().split())))

        result = solve(points)
        print(result)

except:
    pass
