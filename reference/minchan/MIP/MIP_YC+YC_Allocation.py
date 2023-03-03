import ortools
from ortools.linear_solver import pywraplp
import numpy as np
import Environment
import random

# 랜덤 인스턴스 만들 시 주의사항 : Assumption (or Feasible Condition)
# 1. YT의 숫자는 전체 Job의 숫자보다 많아야함
# 2. 모든 YC은 하나 이상의 Job을 할당받아야 함 --> 각 block에 할당된 Job >= 각 block의 YC 수

#1. Make Instance
# 1) Grid World
   # Grid
maximumColumn = 8
maximumRow = 10

   # Block & Berth Location
numberOfBlock = random.randrange(2, 3)
Block_Location_Set = np.array([])
maximum_Column_Set_YC = np.array([])
for i in range(numberOfBlock):
    # block 위치 --> Row는 [1, numberOfBlock] , Column은 [10, 15]
    # Block_Location_Set의 Column은 Block의 가로 너비를 의미함
    block_location = np.array([[i+1, random.randrange(5, maximumColumn)]])
    maximum_Column_Set_YC = np.append(maximum_Column_Set_YC, block_location[0][1])
    if i == 0:
        Block_Location_Set = block_location
    else:
        Block_Location_Set = np.concatenate((Block_Location_Set, block_location),axis=0)

numberOfBerth = random.randrange(2, 5)
Berth_Location_Set = np.array([])
# Row of berth = 0
for i in range(numberOfBerth):
    berth_location = np.array([[0, random.randrange(0, numberOfBerth)]])
    if i == 0:
        Berth_Location_Set = berth_location
    else:
        Berth_Location_Set = np.concatenate((Berth_Location_Set, berth_location),axis=0)

# 2) Component + Parameter
# 일부 Parameter는 미리 구해놓지 않고 바로 MIP 식에서 구할예정
   # Job
totalNumberOfJob = 8
maximumDueOrRelreasedDate = 1
     # MIP에 활용될 Job Set들
Job_Set = np.array([],dtype=object)
Job_b_Set = np.empty((numberOfBlock),dtype=object)
Job_In_Set = np.array([],dtype=object)
Job_Out_Set = np.array([],dtype=object)
Job_b_In_Set = np.empty((numberOfBlock),dtype=object)
Job_b_Out_Set = np.empty((numberOfBlock),dtype=object)

# + Job_Out_0_Set, Job_Out_N_Set

for i in range(totalNumberOfJob):
    block = random.randrange(1, numberOfBlock+1)
    index = i
    type = random.choice(["In","Out"])
    origin = np.array([10000,10000])
    destination = np.array([10000,10000])

    if type == "In":
        origin = random.choice(Berth_Location_Set)
        destination = np.array([block, random.randrange(0, Block_Location_Set[block-1][1]) + 1])
        date = random.randrange(0, maximumDueOrRelreasedDate)

    elif type == "Out":
        origin = np.array([block, random.randrange(0, Block_Location_Set[block-1][1]) + 1])
        destination = random.choice(Berth_Location_Set)
        date = random.randrange(0, maximumDueOrRelreasedDate)
    else:
        print('Error: Job type이 In이나 Out이 아닌 경우가 있습니다.')

    Job = Environment.Job(block,index,type, origin, destination, date)

    Job_Set = np.append(Job_Set, Job)
    if Job.type == "In":
        Job_In_Set = np.append(Job_In_Set, Job)

        if Job_b_In_Set[block-1] is None:
            Job_b_In_Set[block-1] = np.array([Job],dtype=object)
        else:
            Job_b_In_Set[block-1] = np.append(Job_b_In_Set[block-1], Job)
    else:
        Job_Out_Set = np.append(Job_Out_Set, Job)
        if Job_b_Out_Set[block-1] is None:
            Job_b_Out_Set[block-1] = np.array([Job],dtype=object)
        else:
            Job_b_Out_Set[block-1] = np.append(Job_b_Out_Set[block-1], Job)

    if Job_b_Set[block-1] is None:
        Job_b_Set[block-1] = np.array([Job],dtype=object)
    else:
        Job_b_Set[block-1] = np.append(Job_b_Set[block-1], Job)

    # YT
numberOfYT = totalNumberOfJob + 2
movingTimePerUnit_YT = 1
YT_Set = np.array([], dtype=object)
for i in range(numberOfYT):
    initial_Row = random.randrange(0, maximumRow)
    initial_Column = random.randrange(0, maximumColumn)
    initial_Location = np.array([initial_Row,initial_Column])
    YardTruck = Environment.YT(i, initial_Location, movingTimePerUnit_YT)
    YT_Set = np.append(YT_Set, YardTruck)

    # YC
YC_b_Number_Set = np.array([])
safetyDistance_YC = 2
processingTime_YC = 10
movingTimePerUnit_YC = 1
for i in range(numberOfBlock):
    maximumColumn_block = Block_Location_Set[i][1]
#    YC_b_Number = round(maximumColumn_block / safetyDistance_YC - 2)
    YC_b_Number_Set = np.append(YC_b_Number_Set, random.randrange(2, 4))

# Print job info
print('-------------------Job Information----------------')
for b in range(numberOfBlock):
    if Job_b_Set[b] is None:
        print('block', b + 1, '의 Job은 없습니다.')
    else:
        print('block', b + 1, 'Information')
        for i in (Job_b_Set[b]):
            tyt_j = movingTimePerUnit_YT * (abs(i.origin[0] - i.destination[0]) + abs(i.origin[1] - i.destination[1]))
            print(i.index, i.type, i.origin, i.destination, i.releasedDate, i.dueDate, tyt_j)

# print YT info
print('-------------------YT Information----------------')
for t in YT_Set:
    print(t.index, 'initial location : ', t.initial_location)

print('-------------------YC Information----------------')
print('# of YC for each block')
print(YC_b_Number_Set)
print('width of block')
print(maximum_Column_Set_YC)

## MIP Code
# 3) Define variable + Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
# infinity = solver.infinity()
infinity = 10000

    # C_j : Completion Time of Job j ∈ J
    # syc_j : time point in which YC starts operation for job j ∈ J
    # x_b_ij : If job j is processed after job i by YC in same block b, then 1 Else, 0
    # y_b_ijk : If job j is immediately processed after job i by YC_b_k, then 1 Else, 0
    # z_jt : If YT t is assigned for transportation of job j, then 1

C_j_Set = np.array([], dtype=object)
for i in range(Job_Set.size):
    C_j = solver.NumVar(0.0, infinity, 'C_'+ str(i))
    C_j_Set = np.append(C_j_Set, C_j)

syc_j_Set =np.array([], dtype=object)
for i in range(Job_Set.size):
    syc_j = solver.NumVar(0.0, infinity, 'syc_'+str(i))
    syc_j_Set = np.append(syc_j_Set, syc_j)

x_b_ij_Set = np.empty((numberOfBlock), dtype=object)
for b in range(numberOfBlock):
    if Job_b_Set[b] is not None:
        numberOfJob = Job_b_Set[b].size
        x_b_ij = np.empty((numberOfJob, numberOfJob), dtype=object)
        for i in range(numberOfJob):
            for j in range(i):
                if i != j:
                    x_b_ij[i][j] = solver.IntVar(0, 1, 'x_'+str(b)+'_'+str(i)+str(j))
                    x_b_ij[j][i] = solver.IntVar(0, 1, 'x_'+str(b)+'_'+str(j)+str(i))
        x_b_ij_Set[b] = x_b_ij
    else:
        x_b_ij_Set[b] = np.array([],dtype=object)

# Y는 각 b에 Dummy Job 포함되어야함 --> 다른 Variable이랑 Index 차이남
# y_b_ijk인데, 정의하다보니 y_b_kij가 되어버렸음 ..
y_b_ijk_Set = np.empty((numberOfBlock), dtype=object)
for b in range(numberOfBlock):
    if Job_b_Set[b] is not None:
        numberOfYC = int(YC_b_Number_Set[b])
        numberOfJob = Job_b_Set[b].size
        # Dummy job is represented at first and last column
        # First Dummy Job --> i에 반영, Last Dummy Job --> j에 반영
        y_b_ijk = np.empty((numberOfYC, numberOfJob+2, numberOfJob+2), dtype=object)
        for k in range(numberOfYC):
            # Dummy Job (0, n+1)
            for i in range(numberOfJob+1):
                for j in range(1, numberOfJob+2):
                    if i != j:
                        # Dummy First Job
                        if i == 0:
                            if j < numberOfJob+1:
                                y_b_ijk[k][i][j] = solver.IntVar(0,1, 'y_'+str(b)+'_'+str(i)+str(j)+str(k))
                        else:

                            y_b_ijk[k][i][j] = solver.IntVar(0,1, 'y_'+str(b)+'_'+str(i)+str(j)+str(k))


        y_b_ijk_Set[b] = y_b_ijk
    else:
        y_b_ijk_Set[b] = np.array([],dtype=object)

# print(y_b_ijk_Set)

z_jt_Set = np.empty((Job_Set.size, YT_Set.size),dtype=object)
for j in range(Job_Set.size):
    for t in range(YT_Set.size):
        z_jt_Set[j][t] = solver.IntVar(0,1, 'z_'+str(j)+str(t))

# 4) Define Constraint
### 주의) Y_ijk가 사용된 constraint의 i와 j (Job index)는 양 끝에 Dummy Column을 가지고 있는 Y_ijk기준으로 통일, 아니면 Set 기준 -> 주의깊게 봐야함
# 1. ∑_(𝑗 ∈ 𝐽^𝑏) 𝑦_(0, 𝑗,𝑘)^𝑏  = 1           𝑓𝑜𝑟 𝑎𝑙𝑙 𝑘 ∈ 𝑌𝐶^𝑏 𝑎𝑛𝑑 𝑏 ∈ 𝐵
for b in range(numberOfBlock):
    if Job_b_Set[b] is not None:
        for k in range(int(YC_b_Number_Set[b])):
            constraint_expr = [y_b_ijk_Set[b][k][0][j] for j in range(1, int(Job_b_Set[b].size)+1)]
            solver.Add(sum(constraint_expr) == 1)

# 2. ∑_(𝑗 ∈ 𝐽^𝑏) 𝑦_(𝑗,𝑁,𝑘)^𝑏  = 1            𝑓𝑜𝑟 𝑎𝑙𝑙 𝑘 ∈ 𝑌𝐶^𝑏  𝑎𝑛𝑑 𝑏 ∈ 𝐵
for b in range(numberOfBlock):
    if Job_b_Set[b] is not None:
        for k in range(int(YC_b_Number_Set[b])):
            constraint_expr = [y_b_ijk_Set[b][k][j][int(Job_b_Set[b].size)+1] for j in range(1, int(Job_b_Set[b].size)+1)]
            solver.Add(sum(constraint_expr) == 1)

# 3. ∑_(𝑘 ∈ 𝑌𝐶^𝑏)∑_(𝑖 ∈ 𝐽_0^𝑏)𝑦_(𝑖, 𝑗,𝑘)^𝑏  = 1                                𝑓𝑜𝑟 𝑎𝑙𝑙 𝑗 ∈ 𝐽^𝑏   𝑎𝑛𝑑 𝑏 ∈ 𝐵 𝑠𝑢𝑐ℎ 𝑡ℎ𝑎𝑡 𝑖 ≠ 𝑗
for b in range(numberOfBlock):
    if Job_b_Set[b] is not None:
        for j in range(1, Job_b_Set[b].size+1):
            constraint_expr = solver.Sum([solver.Sum([y_b_ijk_Set[b][k][i][j] for k in range(int(YC_b_Number_Set[b]))]) for i in range(0, int(Job_b_Set[b].size)+1) if i != j])
            solver.Add(constraint_expr== 1)

# 4. ∑_(𝑘∈𝑌𝐶^𝑏) ∑_(𝑖 ∈ 𝐽_𝑁^𝑏) 𝑦_(𝑗,𝑖,𝑘)^𝑏  = 1                                 𝑓𝑜𝑟 𝑎𝑙𝑙 𝑗 ∈ 𝐽^𝑏 𝑎𝑛𝑑 𝑏 ∈ 𝐵 𝑠𝑢𝑐ℎ 𝑡ℎ𝑎𝑡 𝑖 ≠ 𝑗
for b in range(numberOfBlock):
    if Job_b_Set[b] is not None:
        for j in range(1, Job_b_Set[b].size+1):
            constraint_expr = solver.Sum([solver.Sum([y_b_ijk_Set[b][k][j][i] for k in range(int(YC_b_Number_Set[b]))]) for i in range(1, int(Job_b_Set[b].size)+2) if i != j])
            solver.Add(constraint_expr == 1)

# 5. ∑_(𝑖 ∈ 𝐽_0^𝑏)𝑦_(𝑖,𝑗,𝑘)^𝑏 = ∑_(𝑖 ∈ 𝐽_𝑁^𝑏) 𝑦_(𝑗,𝑖,𝑘)^𝑏                         𝑓𝑜𝑟 𝑎𝑙𝑙 𝑘 ∈ 𝑌𝐶^𝑏, 𝑗 ∈ 𝐽^𝑏,𝑏 ∈ 𝐵   𝑠𝑢𝑐ℎ 𝑡ℎ𝑎𝑡 𝑖 ≠ 𝑗
for b in range(numberOfBlock):
    if Job_b_Set[b] is not None:
        for k in range(int(YC_b_Number_Set[b])):
            for j in range(1, Job_b_Set[b].size+1):
                constraint_expr1 = solver.Sum([y_b_ijk_Set[b][k][i][j] for i in range(0, int(Job_b_Set[b].size) + 1) if i != j])
                constraint_expr2 = solver.Sum([y_b_ijk_Set[b][k][j][i] for i in range(1, int(Job_b_Set[b].size) + 2) if i != j])
                solver.Add(constraint_expr1 == constraint_expr2)

# for b in range(numberOfBlock):
#     if Job_b_Set[b] is not None:
#         for k in range(int(YC_b_Number_Set[b])):
#             for i in range(1, Job_b_Set[b].size + 1):
#                 for j in range(1, i):
#                     solver.Add(y_b_ijk_Set[b][k][i][j] + y_b_ijk_Set[b][k][j][i] <= 1)

# 6. 𝑠𝑦𝑐_𝑖+𝑡𝑦𝑐_(𝑖,𝑗)^𝑏+𝑝_𝑖  − 𝑠𝑦𝑐_𝑗 ≤𝑀(1−𝑦_(𝑖,𝑗, 𝑘 )^𝑏 )                 𝑓𝑜𝑟 𝑎𝑙𝑙 𝑖 , 𝑗 ∈ 𝐽^𝑏  𝑎𝑛𝑑 𝑘 ∈ 𝑌𝐶^𝑏, 𝑏 ∈ 𝐵
for b in range(numberOfBlock):
    if Job_b_Set[b] is not None:
        for k in range(int(YC_b_Number_Set[b])):
            for i in range(1, Job_b_Set[b].size + 1):
                for j in range(1, i):
                    # tyc_b_ij
                    # i, j : y_ijk 기준 index인데, Dummy Job Column을 양 끝에 가지고 있기 때문에 인덱스 조정해주어야 함
                    if Job_b_Set[b][i-1].type == "In":
                        i_row = Job_b_Set[b][i-1].destination[1]
                    elif Job_b_Set[b][i-1].type == "Out":
                        i_row = Job_b_Set[b][i-1].origin[1]
                    if Job_b_Set[b][j-1].type == "In":
                        j_row = Job_b_Set[b][j-1].destination[1]
                    elif Job_b_Set[b][j-1].type == "Out":
                        j_row = Job_b_Set[b][j-1].origin[1]

                    tyc_b_ij = abs(i_row - j_row) * movingTimePerUnit_YC
                    i_index = Job_b_Set[b][i-1].index
                    j_index = Job_b_Set[b][j-1].index
                    solver.Add(syc_j_Set[i_index] + tyc_b_ij + processingTime_YC - syc_j_Set[j_index] <= infinity * (1-y_b_ijk_Set[b][k][i][j]))
                    solver.Add(syc_j_Set[j_index] + tyc_b_ij + processingTime_YC - syc_j_Set[i_index] <= infinity * (1-y_b_ijk_Set[b][k][j][i]))

# 7.  𝑠𝑦𝑐_𝑗 ≥ 𝑟_𝑗 + 𝑡𝑦𝑡_𝑗                     𝑓𝑜𝑟 𝑎𝑙𝑙 𝑗 ∈ 𝐽^𝐼𝑛
# 9.  𝐶_𝑗≥ 𝑠𝑦𝑐_𝑗 + 𝑝_𝑗                       𝑓𝑜𝑟 𝑎𝑙𝑙 𝑗 ∈ 𝐽^𝐼𝑛
# 11. 𝐶_𝑗≥ 𝑠𝑦𝑐_𝑗 + 𝑝_𝑗  + 𝑡𝑦𝑡_𝑗               𝑓𝑜𝑟 𝑎𝑙𝑙 𝑗 ∈ 𝐽^𝑂𝑢𝑡
for j in range(Job_Set.size):
    if Job_Set[j].type == "In":
        # 7
        tyt_j = movingTimePerUnit_YT * (abs(Job_Set[j].origin[0] - Job_Set[j].destination[0]) + abs(Job_Set[j].origin[1] - Job_Set[j].destination[1]))
        solver.Add(syc_j_Set[j] >= Job_Set[j].releasedDate + tyt_j)
        # 9
        solver.Add(C_j_Set[j] >= syc_j_Set[j] + processingTime_YC)
    elif Job_Set[j].type == "Out":
        # 11
        tyt_j = movingTimePerUnit_YT * (abs(Job_Set[j].origin[0] - Job_Set[j].destination[0]) + abs(Job_Set[j].origin[1] - Job_Set[j].destination[1]))
        solver.Add(C_j_Set[j] >= syc_j_Set[j] + processingTime_YC + tyt_j)

# 8. 𝑠𝑦𝑐_𝑗 ≥ 𝑡𝑦𝑡_𝑗 + 𝑟𝑦𝑡_(𝑗,𝑡) ∗ 𝑧_(𝑗,𝑡)            𝑓𝑜𝑟 𝑎𝑙𝑙 𝑗 ∈ 𝐽^𝐼𝑛, 𝑡 ∈ 𝑇
# 10.   s𝑦𝑐_𝑗 + 𝑝_𝑗 ≥ 𝑟𝑦𝑡_(𝑗,𝑡) ∗ 𝑧_(𝑗,𝑡)          𝑓𝑜𝑟 𝑎𝑙𝑙 𝑗 ∈ 𝐽^𝑂𝑢𝑡, 𝑡 ∈ 𝑇
for t in range(YT_Set.size):
    for j in range(Job_Set.size):
        ryt_jt = movingTimePerUnit_YT * (abs(Job_Set[j].origin[0] - YT_Set[t].initial_location[0]) + abs(Job_Set[j].origin[1] - YT_Set[t].initial_location[1]))
        # 8
        if Job_Set[j].type == "In":
            tyt_j = movingTimePerUnit_YT * (abs(Job_Set[j].origin[0] - Job_Set[j].destination[0]) + abs(Job_Set[j].origin[1] - Job_Set[j].destination[1]))
            solver.Add(syc_j_Set[j] >= tyt_j + ryt_jt * z_jt_Set[j][t])
        # 10
        elif Job_Set[j].type == "Out":
            solver.Add(syc_j_Set[j] + processingTime_YC >= ryt_jt * z_jt_Set[j][t])

# Interference Information --> Delta & theta
Interference_Info = Environment.Parameter_data(Job_b_Set, YT_Set, YC_b_Number_Set, maximum_Column_Set_YC, safetyDistance_YC, movingTimePerUnit_YC, processingTime_YC)
theta = Interference_Info.theta
delta = Interference_Info.delta
np.set_printoptions(threshold=np.inf, linewidth = np.inf)
# print(delta)
# print(theta)
# for b in range(numberOfBlock):
#     if theta[b] is not None:
#         for ijvw in theta[b]:
#             print(delta[b][ijvw[0]][ijvw[1]][ijvw[2]][ijvw[3]])

# 12. ∑_(𝑢 ∈ 𝐽_0^𝑏) 𝑦_(𝑢,𝑖,𝑣)^𝑏 +∑_(𝑢 ∈ 𝐽_0^𝑏) 𝑦_(𝑢,𝑗,𝑤)^𝑏 ≤1+𝑥_(𝑖,  𝑗)^𝑏+𝑥_(𝑗,𝑖)^𝑏                                 𝑓𝑜𝑟 𝑎𝑙𝑙 (𝑖, 𝑗, 𝑣, 𝑤) ∈ 𝛩
# 14. 𝑠𝑦𝑐_𝑖 + 𝑝_𝑖 + 𝛥_(𝑖,𝑗,𝑣,𝑤)^𝑏− 𝑠𝑦𝑐_𝑗 ≤ 𝑀(3 − 𝑥_(𝑖,𝑗)^𝑏 − ∑_(𝑢∈𝐽_0^𝑏) 𝑦_(𝑢,𝑖,𝑣)^𝑏 + ∑_(𝑢 ∈ 𝐽_0^𝑏) 𝑦_(𝑢,𝑗,𝑤)^𝑏 )    𝑓𝑜𝑟 𝑎𝑙𝑙 (𝑖, 𝑗, 𝑣, 𝑤) ∈ 𝛩
for b in range(numberOfBlock):
    if Job_b_Set[b] is not None:
        if theta[b] is not None:
            if  theta[b].size > 0:
                for ijvw in theta[b]:
                    # 12
                    # y_b_ijk의 index y_b_kij로 되어있음 ..
                    constraint_expr1 = solver.Sum([y_b_ijk_Set[b][ijvw[2]][u][int(ijvw[0])+1] for u in range(0, int(Job_b_Set[b].size) + 1) if u != int(ijvw[0]+1)])
                    constraint_expr2 = solver.Sum([y_b_ijk_Set[b][ijvw[3]][u][int(ijvw[1])+1] for u in range(0, int(Job_b_Set[b].size) + 1) if u != int(ijvw[1]+1)])

                    solver.Add(constraint_expr1 + constraint_expr2 <= 1 + x_b_ij_Set[b][ijvw[0]][ijvw[1]] + x_b_ij_Set[b][ijvw[1]][ijvw[0]])

                    # 14
                    i_index = Job_b_Set[b][ijvw[0]].index
                    j_index = Job_b_Set[b][ijvw[1]].index

                    solver.Add(syc_j_Set[i_index] + processingTime_YC + delta[b][ijvw[0]][ijvw[1]][ijvw[2]][ijvw[3]] - syc_j_Set[j_index] <= infinity * (3 - x_b_ij_Set[b][ijvw[0]][ijvw[1]] - constraint_expr1 - constraint_expr2))

                    solver.Add(x_b_ij_Set[b][ijvw[0]][ijvw[1]] + x_b_ij_Set[b][ijvw[1]][ijvw[0]] <= 1)

# 13. 𝑠𝑦𝑐_𝑖 + 𝑝_𝑖  − 𝑠𝑦𝑐_𝑗 ≤ 𝑀(1−𝑥_(𝑖,𝑗 )^𝑏)              𝑓𝑜𝑟 𝑎𝑙𝑙 𝑖 , 𝑗 ∈ 𝐽^𝑏 𝑎𝑛𝑑 𝑏 ∈ 𝐵
for b in range(numberOfBlock):
    if Job_b_Set[b] is not None:
        for i in range(int(Job_b_Set[b].size)):
            for j in range(i):
                # i와 j의 index를 syc의 기준으로 구해줘야함
                i_index = Job_b_Set[b][i].index
                j_index = Job_b_Set[b][j].index
                solver.Add(syc_j_Set[i_index] + processingTime_YC - syc_j_Set[j_index] <= infinity * (1 - x_b_ij_Set[b][i][j]))
                solver.Add(syc_j_Set[j_index] + processingTime_YC - syc_j_Set[i_index] <= infinity * (1 - x_b_ij_Set[b][j][i]))

# 15. ∑_(𝑡 ∈ 𝑇) 𝑧_(𝑗,𝑡)  = 1                          𝑓𝑜𝑟 𝑎𝑙𝑙 𝑗 ∈ 𝐽
for j in range(int(Job_Set.size)):
    constraint_expr = solver.Sum([z_jt_Set[j][t] for t in range(YT_Set.size)])
    solver.Add(constraint_expr == 1)

# 16. ∑_(𝑗 ∈ 𝐽) 𝑧_(𝑗,𝑡)≤ 1                            𝑓𝑜𝑟 𝑎𝑙𝑙 𝑡 ∈ 𝑇
for t in range(int(YT_Set.size)):
    constraint_expr = solver.Sum([z_jt_Set[j][t] for j in range(Job_Set.size)])
    solver.Add(constraint_expr <= 1)

print('the number of constraints = ', solver.NumConstraints())

# 5) Objective Function
# solver.Minimize(solver.Sum([C_j_Set[j] - Job_Out_Set[j].dueDate for j in range(Job_Out_Set.size)]))

# Total Completion Time으로 Verification
solver.Minimize(solver.Sum([C_j_Set[j] for j in range(Job_Set.size)]))

# # Makespan으로 verification
# C_max = solver.NumVar(0.0, infinity, 'C_max')
# for j in range(Job_Set.size):
#     solver.Add(C_max >= C_j_Set[j])
#
# solver.Minimize(C_max)

# call the solver
status = solver.Solve()

# Display Solution
if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    print()
    print('------------------------------C_j----------------------------')
    for j in range(Job_Set.size):
        print('C_',j,' =', C_j_Set[j].solution_value())
    print()
    print('------------------------------syc_j----------------------------')
    for j in range(Job_Set.size):
        print('syc_',j,' =', syc_j_Set[j].solution_value())
    print()
    print('------------------------------z_jt----------------------------')
    for j in range(Job_Set.size):
        for t in range(YT_Set.size):
            if z_jt_Set[j][t].solution_value() > 0:
                print('z_', j, t, '=', z_jt_Set[j][t].solution_value())

                ryt_jt = movingTimePerUnit_YT * (abs(Job_Set[j].origin[0] - YT_Set[t].initial_location[0]) + abs(Job_Set[j].origin[1] - YT_Set[t].initial_location[1]))
                print('ryt_', j, t, '=', ryt_jt)

    print()
    print('------------------------------y_b_ijk----------------------------')
    for b in range(numberOfBlock):
        if Job_b_Set[b] is not None:
            for k in range(int(YC_b_Number_Set[b])):
                for j in range(1, Job_b_Set[b].size +1):
                    if y_b_ijk_Set[b][k][0][j] is not None:
                        if y_b_ijk_Set[b][k][0][j].solution_value() > 0:

                            j_index = Job_b_Set[b][j-1].index
                            print('y_', b, '_','firstdummy', j_index, k, ' =', y_b_ijk_Set[b][k][0][j].solution_value())
                for i in range(1, Job_b_Set[b].size +1):
                    for j in range(1, Job_b_Set[b].size +1):
                        if i != j and y_b_ijk_Set[b][k][i][j] is not None:
                            if y_b_ijk_Set[b][k][i][j].solution_value() > 0:
                                # y_b_ijk와 C_j의 index 다름 --> 통일시켜줘야 Verification하기 편함
                                i_index = Job_b_Set[b][i-1].index
                                j_index = Job_b_Set[b][j-1].index
                                print('y_',b,'_',i_index, j_index,k, ' =', y_b_ijk_Set[b][k][i][j].solution_value())

                for j in range(1, Job_b_Set[b].size + 1):
                    if y_b_ijk_Set[b][k][j][Job_b_Set[b].size + 1] is not None:
                        if y_b_ijk_Set[b][k][j][Job_b_Set[b].size + 1].solution_value() > 0:
                            j_index = Job_b_Set[b][j - 1].index
                            print('y_', b, '_', j_index,'lastdummy', k, ' =', y_b_ijk_Set[b][k][j][Job_b_Set[b].size + 1].solution_value())

    print()
    print('------------------------------x_b_ij----------------------------')
    for b in range(numberOfBlock):
        if Job_b_Set[b] is not None:
            for i in range(Job_b_Set[b].size):
                for j in range(Job_b_Set[b].size):
                    if i!=j and x_b_ij_Set[b][i][j] is not None:
                        if x_b_ij_Set[b][i][j].solution_value() > 0:
                            print('x_',b,'_',i,j,' =', x_b_ij_Set[b][i][j].solution_value())

else:
    print('The problem does not have an optimal solution.')

print('\nAdvanced usage:')
print('Problem solved in %f milliseconds' % solver.wall_time())
print('Problem solved in %d iterations' % solver.iterations())
print('Problem solved in %d branch-and-bound nodes' % solver.nodes())

solver.Objective().Value()


