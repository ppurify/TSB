import sys
import numpy as np
import random
from docplex.mp.model import Model

# 1. Grid World
maximum_row = 7
maximum_column = 7

Job_Start_location = np.array([[0, 1], [0, 5], [4, 2], [6, 3], [5, 4], [2, 6]])
Job_Start_location = np.array([[3, 5], [4, 2], [0, 6], [0, 2], [0, 4], [0, 3]])

AGV_location = np.array([[2, 4], [3, 3], [0, 6], [6, 3], [4, 5], [1, 3], ])

# 2. LP 모델 기반 (Node, Arc는 코드에서 만들지 않음)
## 각 AGV의 초기 위치, Job의 픽업/드랍장소로 이동하는 데에는
## 3가지 Route가 있다고 가정 ( Route 내부를 도로로 나누는 작업은 하지 않았음)
## OR-Tools에 Network Flow 솔버 쓰고 싶었는데, 새로운 LP 제약식을 사용하는 문법이 뭔지 몰라서 그냥 LP 솔버로 썼음 (자료안나옴)

solver = pywraplp.Solver.CreateSolver('GLOP')

NumberofArc = 19 * 6 + 18 * 6 + 6 + 18 * 6 + 18 * 6 + 6 + 6

x_ij = np.empty(NumberofArc, dtype=object)

for i in range(NumberofArc):
    if i >= 19 * 6 + 18 * 6 and i < 19 * 6 + 18 * 6 + 6:
        x_ij[i] = solver.NumVar(1, 1)

    elif i >= 19 * 6 + 18 * 6 + 6 + 18 * 6 + 18 * 6 and i < 19 * 6 + 18 * 6 + 6 + 18 * 6 + 18 * 6 + 6:
        x_ij[i] = solver.NumVar(1, 1)

    else:
        x_ij[i] = solver.NumVar(0, 1)
