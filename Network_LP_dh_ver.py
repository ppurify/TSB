from ortools.linear_solver import pywraplp
import numpy as np

solver = pywraplp.Solver.CreateSolver('GLOP')
if not solver:
    print("Please check solver")

# Parameters
Agv_num = 3
Agv_to_pick = [[3,3],
               [2,2],
               [1,3]]

Pick_to_drop = [3,2]
Drop_to_sink = Agv_num

Total_arc_num = Agv_num + sum(sum(Agv_to_pick, [])) + sum(Pick_to_drop) + Drop_to_sink

Arc_information = []

# generate A1
for a in range(len(Agv_to_pick)):
    for b in range(len(Agv_to_pick[a])):
        for c in range(Agv_to_pick[a][b]):
            Arc_information.append([['agv', a],['p', b],[c]])
            
# generate A2
for a in range(len(Pick_to_drop)):
    for b in range(Pick_to_drop[a]):
        Arc_information.append([['p', a],['d', a],[b]])

# generate A3
for a in range(Drop_to_sink):
    Arc_information.append([['d', a],['s'],[0]])

# generate A4
for a in range(Agv_num):
    Arc_information.append([['agv', a],['s'],[0]])


# set cost(tmpt, not yet coded)
for i in range(len(Arc_information)):
    Arc_information[i].append([i])
    

for i in range(len(Arc_information)):
    print(Arc_information[i])
# Make Arc index bundles
# Arc_bundles = []
# for i in range(Agv_num * 2 + 1):
#     if i == 0:
#         Arc_bundles.append(list(range(0, Agv_to_pick[i] + 1)))

#     elif (i > 0) & (i < Agv_num):
#         Previous_value = Arc_bundles[i-1][-1]
#         Arc_bundles.append(list(range(Previous_value + 1, Previous_value + 1 + Agv_to_pick[i] + 1)))

#     elif (i >= Agv_num) & (i < Agv_num*2):
#         Previous_value = Arc_bundles[i-1][-1]
#         Arc_bundles.append(list(range(Previous_value + 1, Previous_value + 1 + Pick_to_drop[i%Agv_num])))
    
#     else:
#         Previous_value = Arc_bundles[i-1][-1]
#         Arc_bundles.append(list(range(Previous_value + 1, Total_arc_num)))

# Index with cost
# Agv_to_pick_costs = [[1,2,3], [4,5], [3,2,1]]
# Pick_to_drop_costs = [[2,1], [1,2,3,4], [1,2]]

# for i in range(Agv_num):
#     if len(Agv_to_pick_costs[i]) != Agv_to_pick[i]:
#         print("Please Check Agv_to_pick_costs or Agv_to_pick[", i, "]"  )
#     elif len(Pick_to_drop_costs[i]) != Pick_to_drop[i]:
#         print("Please Check Pick_to_drop_costs or Pick_to_drop[", i , "]"  )

# Arc_costs = np.zeros(Total_arc_num)

# for i in range(Agv_num *2):
#     if i < Agv_num:
#         Arc_index_list = Arc_bundles[i][1:]
#         for j in range(len(Arc_index_list)):
#             Arc_costs[Arc_index_list[j]] = Agv_to_pick_costs[i%Agv_num][j]
#     else:
#         Arc_index_list = Arc_bundles[i]
#         for j in range(len(Arc_index_list)):
#             Arc_costs[Arc_index_list[j]] = Pick_to_drop_costs[i%Agv_num][j]


# Decision Variables
x = np.empty(Total_arc_num, dtype=object)
for i in range(Total_arc_num):
    x[i] = solver.NumVar(0, 1, 'x[%i]' % i)


# Constraint 1 
for i in range(len(Arc_information)):
    solver.Add(sum(x[j] for j in Arc_bundles[i]) == 1)

# Constraint 2
# Make forward to sink node
To_sink_node = Arc_bundles[-1]
for i in range(Agv_num):
    To_sink_node = To_sink_node + [Arc_bundles[i][0]]
solver.Add(sum(Arc_status[i] for i in To_sink_node) == Agv_num)

# Constraint 3
for i in range(Agv_num):
    Pick_to_drop_arc = Arc_bundles[Agv_num + i]
    solver.Add(sum(Arc_status[k] for k in Arc_bundles[i][1:]) == sum(Arc_status[j] for j in Pick_to_drop_arc))
    solver.Add(sum(Arc_status[j] for j in Pick_to_drop_arc) == Arc_status[Arc_bundles[-1][i]])

# Constraint 4
for i in range(Agv_num):
    Pick_to_drop_arc = Arc_bundles[Agv_num + i]
    solver.Add(sum(Arc_status[j] for j in Pick_to_drop_arc) == 1)

# Obejctive
objective = solver.Objective()
for i in range(Total_arc_num):
    objective.SetCoefficient(Arc_status[i], Arc_costs[i])

objective.SetMinimization()

status = solver.Solve()
print("Total_arc_num : " , Total_arc_num)
print()
if status == pywraplp.Solver.OPTIMAL:
    print('Objective value =', solver.Objective().Value())
    print()
    for i in range(Total_arc_num):
        print(Arc_status[i].name(), ' = ', Arc_status[i].solution_value())
else:
    print('The problem does not have an optimal solution.')