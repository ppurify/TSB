import numpy as np
# import Environment

# Job1 = Environment.Job(1,0,'In',[3,6],[1,2],0)
# Job2 = Environment.Job(1,1,'Out',[1,4],[3,5],0)
# Job3 = Environment.Job(1,2,'In',[3,6],[1,3],0)
# Job4 = Environment.Job(1,3,'Out',[1,7],[3,5],0)
# Job5 = Environment.Job(2,0,'In',[3,6],[2,2],0)
# Job6 = Environment.Job(2,1,'In',[3,5],[2,5],0)
# Job7 = Environment.Job(2,2,'Out',[2,3],[3,6],0)
# Job8 = Environment.Job(2,3,'In',[3,5],[2,7],0)
#
# Job_Row1 =np.array([Job1, Job2, Job3, Job4])
# Job_Row2 =np.array([Job5, Job6, Job7, Job8])
#
# Job_Set = np.array([Job_Row1, Job_Row2])

k = np.zeros((2, 2, 2, 2, 2))
i = 0
for a in range(2):
    for b in range(2):
        for c in range(2):
            for d in range(2):
                for e in range(2):
                    k[a][b][c][d][e] = i
                    i += 1
np.set_printoptions(threshold=np.inf, linewidth = np.inf)
print(k)
print(k[1][1][1][1][0])
print(k[1][0][0][0][1])

w = np.array([[[1,2,3],[4,5,6],[7,8,9]],[[1,2,3],[4,5,6],[7,8,9]],[[1,2,3],[4,5,6],[7,8,9]]])


print(w[1][1])

# b = np.array([[2,3]])
# c = np.concatenate((a,b), axis=0)
# d = np.array([[2,3]])


