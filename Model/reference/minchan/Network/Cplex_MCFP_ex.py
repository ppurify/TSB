import docplex.cp.expression
from docplex.mp.model import Model
import numpy as np
from docplex.mp.progress import *
from docplex.mp.progress import SolutionRecorder
from cplex import Cplex

# Create a new model
m = Model(name="minimum_cost_flow")

# 1. Grid World
NumberOfJob = 6
NumberOfAGV = 6

# 2. LP 모델 기반 (Node, Arc는 코드에서 만들지 않음)
## 각 AGV의 초기 위치, Job의 픽업/드랍장소간 이동하는 데에는
## 3가지 Route가 있다고 가정 (Route 내부를 도로로 나누는 작업은 하지 않았음)
# 1. Parameter
# The number of arc
NumberofArc = 19*6 + 18*6 + 6 + 3*6 + 3*6 + 6 + 6
# Cost for each flow
Cost = np.array([])

#1. 첫번째/두번째 column (AGV --> Dummy / Sink Node)
k = 1
for i in range(19 * 6):
    if i % 19 == 0:
        Cost = np.append(Cost, 0)
    else:
        Cost = np.append(Cost, k)
        k += 2

for i in range(18 * 6):
    Cost = np.append(Cost, 0)

#2. 세 번째 Column (Dummy --> Pick)
for i in range(6):
    Cost = np.append(Cost, 0)

#3. 네 번째, 다섯 번쨰 Column (Pick --> Dummy)
k = 1
for i in range(3 * 6):
    Cost = np.append(Cost, k)
    k += 1

for i in range(3 * 6):
    Cost = np.append(Cost, 0)

#5. 여섯 번째, 일곱 번쨰 (Dummy --> Drop --> Sink)
for i in range(12):
    Cost = np.append(Cost, 0)

# 2. 변수 (x_ij) 정의
x_ij = np.empty(NumberofArc, dtype=object)

for i in range(NumberofArc):
    if i >= 19*6 + 18*6 and i < 19*6 + 18*6 + 6:
        x_ij[i] = m.continuous_var(1, 1)

    elif i >= 19*6 + 18*6 + 6 + 3*6 + 3*6 and i < 19*6 + 18*6 + 6 + 3*6 + 3*6 + 6:
        x_ij[i] = m.continuous_var(1, 1)

    else:
        x_ij[i] = m.continuous_var(0, 100)

# 3. Consraint 정의
 # 1) Supply (AGV)
for i in range(6):
    m.add_constraint(m.sum(x_ij[19*i + j] for j in range(19)) == 1)

 # 2) Demand (Sink)
m.add_constraint(m.sum(x_ij[19*i] for i in range(6)) + m.sum(x_ij[19*6 + 18*6 + 6 + 3*6 + 3*6 + 6 + i] for i in range(6)) == 6)

 # 3) 들어오는 Flow = 나가는 Flow
# 첫 번째 = 두 번째 column
numberofArcUntilFirstColumn = 19 * 6
for i in range(6):
    for j in range(1, 4):
        m.add_constraint(x_ij[19*i +j] == x_ij[numberofArcUntilFirstColumn -1 + 18*i + j])

    for j in range(4, 7):
        m.add_constraint(x_ij[19*i +j] == x_ij[numberofArcUntilFirstColumn -1 + 18*i + j])

    for j in range(7, 10):
        m.add_constraint(x_ij[19*i +j] == x_ij[numberofArcUntilFirstColumn -1 + 18*i + j])

    for j in range(10, 13):
        m.add_constraint(x_ij[19*i +j] == x_ij[numberofArcUntilFirstColumn -1 + 18*i + j])

    for j in range(13, 16):
        m.add_constraint(x_ij[19*i +j] == x_ij[numberofArcUntilFirstColumn -1 + 18*i + j])

    for j in range(16, 19):
        m.add_constraint(x_ij[19*i +j] == x_ij[numberofArcUntilFirstColumn -1 + 18*i + j])

# 두 번째 = 세 번째 Column
numberofArcUntilSecondColumn = numberofArcUntilFirstColumn + 18 * 6
for i in range(6):
    m.add_constraint(m.sum(m.sum(x_ij[numberofArcUntilFirstColumn + 18*k + j] for j in range(3*i, 3*i+3)) for k in range(6)) == x_ij[numberofArcUntilSecondColumn + i])

# 세 번째 = 네 번째 Column
numberofArcUntilThirdColumn = numberofArcUntilSecondColumn + 6
for i in range(6):
    m.add_constraint(x_ij[numberofArcUntilSecondColumn+i] == m.sum(x_ij[numberofArcUntilThirdColumn + 3*i + j] for j in range(3)))

# 네 번째 = 다섯 번째 Column
numberofArcUntil4thColumn = numberofArcUntilThirdColumn + 3*6
for i in range(6):
    for j in range(3):
        m.add_constraint(x_ij[numberofArcUntilThirdColumn+3*i+j] == x_ij[numberofArcUntil4thColumn+3*i+j])

# 다섯 번째 = 여섯 번째 Column
numberofArcUntil5thColumn = numberofArcUntil4thColumn + 3*6
for i in range(6):
    m.add_constraint(m.sum(x_ij[numberofArcUntil4thColumn + 3*i + j] for j in range(3)) == x_ij[numberofArcUntil5thColumn+i])

# 여섯 번째 = 일곱번째 Column
numberofArcUntil6thColumn = numberofArcUntil5thColumn + 6
for i in range(6):
    m.add_constraint(x_ij[numberofArcUntil5thColumn + i] == x_ij[numberofArcUntil6thColumn + i])

OBJ = m.sum(Cost[i]*x_ij[i] for i in range(NumberofArc))
## Objective Function
m.minimize(OBJ)
m.print_information()

# Solve the model
m_solver = m.solve()
# Check the solution status
# sol=m.solution
# sol_status = m.solution.get_status()

# If the solution status is optimal (101), proceed with retrieving the solution value
# if sol_status == 101:
sol = m.solution
obj_val = sol.get_objective_value()
print("Objective value: ", obj_val)
# else:
#     print("The optimization problem was not solved successfully.")

for i in range(NumberofArc):
    if m_solver.get_value(x_ij[i]) > 0:
        print('x', i, '=', m_solver.get_value(x_ij[i]))

print(Cost)
# print("Minimum cost:", m_solver.objective_value())

# for i, j in arcs:
#     if flow[i, j].solution_value > 0:
#         print(f"{i} -> {j}: {flow[i, j].solution_value}")


# # Create the modeler/solver.
# m = Model(name='As-Is Model')
# inf = docplex.cp.expression.INFINITY
# # Define the flow variables
# flow = mdl.continuous_var_dict(arcs, lb=0, name="flow")
#
# # Define the objective function: minimize the sum of the costs
# mdl.minimize(mdl.sum(cost[i, j] * flow[i, j] for i, j in arcs))
#
# # Define the capacity constraints
# for i, j in arcs:
#     mdl.add_constraint(flow[i, j] <= capacity[i, j])
#
# # Define the balance constraints
# for node in nodes:
#     out_flow = mdl.sum(flow[i, j] for i, j in arcs if i == node)
#     in_flow = mdl.sum(flow[i, j] for i, j in arcs if j == node)
#     mdl.add_constraint(out_flow == in_flow)
#
# # Solve the problem
# mdl.solve()
#
# # Print the solution
# print("Minimum cost:", mdl.objective_value)
# for i, j in arcs:
#     if flow[i, j].solution_value > 0:
#         print(f"{i} -> {j}: {flow[i, j].solution_value}")









