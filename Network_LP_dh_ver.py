from ortools.linear_solver import pywraplp
import numpy as np
import sys

solver = pywraplp.Solver.CreateSolver('GLOP')
if not solver:
    print("Please check solver")

inf = solver.infinity()
# Parameters
Agv_num = 3

#
# [[0번 agv가 0번 p로 가는 경로 수, 0번 agv가 1번 p로 가는 경로 수] ...]
# 추후 한번에 3개 경로로 통일
Agv_to_pick = [[3,3],
               [2,2],
               [1,3]]

Pick_to_drop = [3,2]



# Agv_num = 2

# # [[0번 agv가 0번 p로 가는 경로 수, 0번 agv가 1번 p로 가는 경로 수] ...]
# # 추후 한번에 3개 경로로 통일
# Agv_to_pick = [[2,2],
#                [2,3]]

# Pick_to_drop = [3,2]




# generate A부분에서 갱신됨. 0으로 놔둬야 됨
Number_of_job = 0

Arc_information = []


#추후 sink노드로 가는 아크들의 cost를 0으로 설정하도록 수정해야함
# generate A1
for a in range(len(Agv_to_pick)):
    for b in range(len(Agv_to_pick[a])):
        for c in range(Agv_to_pick[a][b]):
            Arc_information.append([['agv', a],['p', b],[c]])
        if b > Number_of_job : 
            Number_of_job = b
            
# generate A2
for a in range(len(Pick_to_drop)):
    for b in range(Pick_to_drop[a]):
        Arc_information.append([['p', a],['d', a],[b]])
    if a > Number_of_job : 
        Number_of_job = a
        
Number_of_job += 1
Drop_to_sink = Number_of_job
Total_arc_num = Agv_num + sum(sum(Agv_to_pick, [])) + sum(Pick_to_drop) + Drop_to_sink

# generate A3
for a in range(Drop_to_sink):
    Arc_information.append([['d', a],['s'],[0]])

# generate A4
for a in range(Agv_num):
    Arc_information.append([['agv', a],['s'],[0]])


Arc_information.sort()




# set cost(tmpt, not yet coded)
for i in range(len(Arc_information)):
    Arc_information[i].append([i])



for i in range(len(Arc_information)):
    print(Arc_information[i])

print()


# Decision Variables
x = np.empty(Total_arc_num, dtype=object)
for i in range(Total_arc_num):
    x[i] = solver.NumVar(0, 1, 'x[%i]' % i)



# Constraint 1
start_node_index = [0]
for i in range(len(Agv_to_pick)):
    start_node_index.append(sum(Agv_to_pick[i]) + 1)
    start_node_index[-1] += start_node_index[-2]
 
for i in range(len(start_node_index)-1):
    solver.Add(sum(x[j] for j in range(start_node_index[i], start_node_index[i+1])) == 1)
    
    # print(start_node_index[i], start_node_index[i+1])
    # print(" start_node_index[i] : ", start_node_index[i])
    # print(" start_node_index[i+1] : ", start_node_index[i+1])
    # for j in range(start_node_index[i], start_node_index[i+1]):
    #     print(j)

    # print(sum(x[j] for j in range(start_node_index[i]-1, start_node_index[i+1])))


# Constraint 2
arcs_to_sink_node = []
for i in range(len(Arc_information)):
    if Arc_information[i][1][0]=='s':
        arcs_to_sink_node.append(i)

# print(sum(x[j] for j in arcs_to_sink_node))
solver.Add(sum(x[j] for j in arcs_to_sink_node) == Agv_num)


# Constraint 3
for i in range(Number_of_job):
    arcs_from_pick_node = []
    arcs_to_pick_node = []
    arcs_from_drop_node = []
    arcs_to_drop_node = []

    for j in range(len(Arc_information)):
        # 출발지가 p이거나
        if Arc_information[j][0] == ['p', i] :
            arcs_from_pick_node.append(j)
        # 도착지가 p
        if Arc_information[j][1] == ['p', i] :
            arcs_to_pick_node.append(j)
        # 출발지가 d이거나
        if Arc_information[j][0] == ['d', i] :
            arcs_from_drop_node.append(j)
        # 도착지가 d
        if Arc_information[j][1] == ['d', i] :
            arcs_to_drop_node.append(j)

    solver.Add(sum(x[j] for j in arcs_from_pick_node) == sum(x[j] for j in arcs_to_pick_node))
    solver.Add(sum(x[j] for j in arcs_from_drop_node) == sum(x[j] for j in arcs_to_drop_node))


# Constraint 4
for j in range(Number_of_job):
    arcs_to_drop_node = []
    
    for i in range(len(Arc_information)):
        if Arc_information[i][1] == ['d', j]:
            arcs_to_drop_node.append(i)
    # print(arcs_to_drop_node)
    solver.Add(sum(x[j] for j in arcs_to_drop_node) == 1)



# Obejctive
objective = solver.Objective()
for i in range(Total_arc_num):
    objective.SetCoefficient(x[i], Arc_information[i][3][0])

objective.SetMinimization()

status = solver.Solve()
print("Total_arc_num : " , Total_arc_num)
print()
if status == pywraplp.Solver.OPTIMAL:
    print('Objective value =', solver.Objective().Value())
    print()
    for i in range(Total_arc_num):
        if x[i].solution_value() > 0:
            print(x[i].name(), ' = ', x[i].solution_value())
else:
    print('The problem does not have an optimal solution.')

