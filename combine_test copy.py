from ortools.linear_solver import pywraplp
import numpy as np
import heapq
import math
import sys

import route_algorithm as ra


# issues

# 3. move 함수 작성시 path라는 변수 없이도 재귀적으로 돌수있게 수정
# 4. 아크 다 순회한 now_count를 prev_count로 바꿔주는 코드 작성
# 5. 다른경우는 다 되는데 이상하게 YT보다 Job이 더 많을때는 LP가 안풀림(Optimal이 안나옴)

# parameter.
solver = pywraplp.Solver.CreateSolver('GLOP')
if not solver:
    print("Please check solver")

inf = solver.infinity()

grid = ra.grid

prev_count = np.array([
    [4, 2, 3, 2, 3, 2, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 1, 3, 1, 3, 1, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 1, 3, 1, 3, 1, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 1, 3, 1, 3, 1, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 2, 3, 2, 3, 2, 4],
])

now_count = np.zeros((len(grid), len(grid[0])))

alpha1 = 0.4
alpha2 = 0.3
alpha3 = 0.3

number_of_YT = 10
number_of_job = 10
# 다수의 route에서 최종적으로 몇개의 arc만 남길지
number_of_final_route = 3

# YT와 Job(Pick, Drop)의 인덱스, 위치를 저장하는 딕셔너리
YT_locations = {}
Job_locations = {}
# YT->Pick, Pick->Drop의 아크 객체(출발지, 도착지, 몇번째 경로인지, 경로 정보, cost)를 저장하는 딕셔너리

# A1
arcs_YT_to_Pick = []
# A2
arcs_Pick_to_Drop = []
# A3
arcs_Drop_to_Sink = []
# A4
arcs_YT_to_Sink = []
# A5
arcs_Drop_to_Pick = []


class arc:
    def __init__(self, i, j, k, path, cost, index):
        self.i = i
        self.j = j
        self.k = k
        self.path = path
        self.cost = 0
        self.index = None

        return


# route로 다수의 경로 받아서 최종 number_of_final_route개의 경로 final_three_route 반환
def penalty(prev_count, route, number_of_final_route, alpha1, alpha3):
    penalty_list = []

    for i in range(len(route)):
        sum_of_counter_of_prev_count = 0
        sum_of_move = len(route[i])
        for j in range(len(route[i])):
            sum_of_counter_of_prev_count += prev_count[(route[i][j][0], route[i][j][1])]

        # 각 경로의 penalty 산출하여 리스트에 저장
        penalty_list.append((alpha1 * sum_of_counter_of_prev_count) + (alpha3 * sum_of_move))

    # penalty가 가장 작은 number_of_final_route개의 경로의 인덱스를 추출하여 final_three_route 리스트에 저장
    final_route_idx = heapq.nsmallest(number_of_final_route, range(len(penalty_list)), key=penalty_list.__getitem__)
    final_route = [route[i] for i in final_route_idx]

    return final_route


# 주어진 path의 cost 계산, 더미 아크(path의 길이 0)는 cost 무한대
def cost(prev_count, now_count, path, alpha1, alpha2, alpha3):
    if len(path) == 0:
        cost = sys.maxsize
    else:
        sum_of_counter_of_prev_count = 0
        sum_of_counter_of_now_count = 0
        sum_of_move = len(path)
        for i in range(len(path)):
            sum_of_counter_of_prev_count += prev_count[(path[i][0], path[i][1])]
            sum_of_counter_of_now_count += now_count[(path[i][0], path[i][1])]

        # cost 산출(반올림)
        cost = round((alpha1 * sum_of_counter_of_prev_count) + (alpha2 * sum_of_counter_of_now_count) + (alpha3 * sum_of_move))

    return cost


# Experiment
# 스케줄링 대상 YT 생성
for i in range(number_of_YT):
    YT_location = None
    while YT_location is None or grid[YT_location] == -1:
        YT_location = (np.random.randint(9), np.random.randint(7))
    YT_locations[i] = YT_location
    
# 스케줄링 대상 작업 생성
for j in range(number_of_job):
    Pick_location = None
    Drop_location = None
    while Pick_location is None or grid[Pick_location] == -1 or Drop_location is None or grid[Drop_location] == -1 or Pick_location == Drop_location:
        Pick_location = (np.random.randint(9), np.random.randint(7))
        Drop_location = (np.random.randint(9), np.random.randint(7))
    Job_locations[j] = [Pick_location, Drop_location]




# YT에서 Pick으로 이동하는 경로 탐색, 아크 생성
for i in range(number_of_YT):
    kk = False
    for j in range(number_of_job):
        YT_location = YT_locations[i]
        Pick_location = Job_locations[j][0]
        
        # print('YT_location : ', YT_location)
        # print('Pick_location : ', Pick_location)

        path_YT_to_Pick = []
        route_YT_to_Pick = []

        # 모든 경우의 경로 탐색
        ra.move(YT_location, Pick_location, grid, path_YT_to_Pick, route_YT_to_Pick)
        # print('length of route_YT_to_Pick : ', len(route_YT_to_Pick))

        if len(route_YT_to_Pick) == 0:
            print('YT Number : ', i, 'location : ', YT_location)
            print('Pick Number : ', j, 'location : ', Pick_location)
            kk = True
            break
        if kk == True:
            break

        # 경로 수가 3개보다 많으면 패널티 함수 통해 3개로 줄이기
        if len(route_YT_to_Pick) > number_of_final_route :
            final_route_YT_to_Pick = penalty(prev_count, route_YT_to_Pick, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
        # 그렇지 않으면
        elif len(route_YT_to_Pick) < number_of_final_route:
            for _ in range(3 - len(route_YT_to_Pick)):
                # 빈 path 추가, 추후 해당 경로에 cost를 아주 큰 값으로 할당해서 해당 arc를 선택하지 않도록
                route_YT_to_Pick.append([])
            final_route_YT_to_Pick = route_YT_to_Pick
        else:
            final_route_YT_to_Pick = route_YT_to_Pick

        # print('final_route_YT_to_Pick : ', final_route_YT_to_Pick)
        # print('lengh of final_route_YT_to_Pick : ', len(final_route_YT_to_Pick))

        # 경로 1개당 arc 객체 생성(YT -> Pick)
        for k in range(len(final_route_YT_to_Pick)):
            # YT -> Pick 경로의 arc 객체 생성
            arcname = 'YT' + str(i) + 'to' + 'Pick' + str(j)
            # print("i : ", i, "j : ", j, "k : ", k)
            arcname = arc(i = ['YT', i], j = ['Pick', j], k = k, path = final_route_YT_to_Pick[k], cost = None, index=None)
            arcs_YT_to_Pick.append(arcname)
            # print('i : ', arcname.i, 'j : ', arcname.j, 'k : ', arcname.k, 'path : ', arcname.path)



# Pick에서 Drop으로 가는 경로 생성, 아크 생성
# 위의 for loop와 분리한이유 : YT -> Pick은 YT 하나에 모든 Job과 경로를 생성해야하지만 하나의 Job 안에서 Pick과 Drop의 연결은 한번만(경로는 세개 생성) 일어나야하기 때문
for j in range(number_of_job):
    Pick_location = Job_locations[j][0]
    Drop_location = Job_locations[j][1]

    # print('Pick_location : ', Pick_location)
    # print('Drop_location : ', Drop_location)

    path_Pick_to_Drop = []
    route_Pick_to_Drop = []

    # 모든 경우의 경로 탐색
    ra.move(Pick_location, Drop_location, grid, path_Pick_to_Drop, route_Pick_to_Drop)
    # print('length of route_Pick_to_Drop : ', len(route_Pick_to_Drop))
    # print('route_Pick_to_Drop')
    # for i in range(len(route_Pick_to_Drop)):
    #     print(route_Pick_to_Drop[i])


    # 경로 수가 3개보다 많으면 패널티 함수 통해 3개로 줄이기
    if len(route_Pick_to_Drop) > number_of_final_route :
        final_route_Pick_to_Drop = penalty(prev_count, route_Pick_to_Drop, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
    # 그렇지 않으면
    elif len(route_Pick_to_Drop) < number_of_final_route:
        for _ in range(3 - len(route_Pick_to_Drop)):
            # 빈 path 추가, 추후 해당 경로에 cost를 아주 큰 값으로 할당해서 해당 arc를 선택하지 않도록
            route_Pick_to_Drop.append([])
        final_route_Pick_to_Drop = route_Pick_to_Drop

    else :
        final_route_Pick_to_Drop = route_Pick_to_Drop

    # print('length of final_route_Pick_to_Drop : ', len(final_route_Pick_to_Drop))
    # for i in range(len(final_route_Pick_to_Drop)):
    #     print(final_route_Pick_to_Drop[i])

    # 경로 1개당 arc 객체 생성(Pick -> Drop)
    for k in range(len(final_route_Pick_to_Drop)):
        arcname = 'Pick' + str(j) + 'to' + 'Drop' + str(j)
        arcname = arc(i = ['Pick', j], j = ['Drop', j], k = k, path = final_route_Pick_to_Drop[k], cost = None, index=None)
        arcs_Pick_to_Drop.append(arcname)
        # print('i : ', arcname.i, 'j : ', arcname.j, 'k : ', arcname.k, 'path : ', arcname.path)



# Drop에서 다른 Job의 Pick으로 가는 경로생성, 아크 생성

# i : Drop, j : Pick 
for i in range(number_of_job):
    for j in range(number_of_job):
        if i != j:
            Drop_location = Job_locations[i][1]
            Pick_location = Job_locations[j][0]
            
            path_Drop_to_Pick = []
            route_Drop_to_Pick = []

            # 모든 경우의 경로 탐색
            ra.move(Drop_location, Pick_location, grid, path_Drop_to_Pick, route_Drop_to_Pick)
            # print('length of route_Drop_to_Pick : ', len(route_Drop_to_Pick))
            # print('route_Drop_to_Pick')
            # for i in range(len(route_Drop_to_Pick)):
            #     print(route_Drop_to_Pick[i])

            # 경로 수가 3개보다 많으면 패널티 함수 통해 3개로 줄이기
            if len(route_Drop_to_Pick) > number_of_final_route :
                final_route_Drop_to_Pick = penalty(prev_count, route_Drop_to_Pick, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
            # 그렇지 않으면
            elif len(route_Drop_to_Pick) < number_of_final_route:
                for _ in range(3 - len(route_Drop_to_Pick)):
                    # 빈 path 추가, 추후 해당 경로에 cost를 아주 큰 값으로 할당해서 해당 arc를 선택하지 않도록
                    route_Drop_to_Pick.append([])
                final_route_Drop_to_Pick = route_Drop_to_Pick

            else :
                final_route_Drop_to_Pick = route_Drop_to_Pick

            # print('length of final_route_Drop_to_Pick : ', len(final_route_Drop_to_Pick))
            # for i in range(len(final_route_Drop_to_Pick)):
            #     print(final_route_Drop_to_Pick[i])

            # 경로 1개당 arc 객체 생성(Drop -> Pick)
            for k in range(len(final_route_Drop_to_Pick)):
                arcname = 'Drop' + str(i) + 'to' + 'Pick' + str(j)
                arcname = arc(i = ['Drop', i], j = ['Pick', j], k = k, path = final_route_Drop_to_Pick[k], cost = None, index=None)
                arcs_Drop_to_Pick.append(arcname)
                # print('i : ', arcname.i, 'j : ', arcname.j, 'k : ', arcname.k, 'path : ', arcname.path)

















# !!! 현재는 YT->Pick 아크들 먼저 길이순 오름차순 정렬하여 cost 계산 후 Pick->Drop 아크들 길이순 오름차순 정렬하여 cost 계산하는 방식으로 진행
# !!! 따라서 앞부분 아크들이 우선적으로 cost계산되어 더 높은 우선순위로 인식됨

# YT_to_Pick의 arc 객체들의 cost 계산

# 객체들의 path 길이에 따른 sorting
arcs_YT_to_Pick.sort(key = lambda x : len(x.path))

# 1. 각 arc들을 순회하며 cost 계산
# 2. 각 arc를 순회하며 해당 path를 now_count에 반영(밟는칸에 +1씩 count)
for i in range(len(arcs_YT_to_Pick)):
    # cost 계산
    arcs_YT_to_Pick[i].cost = cost(prev_count, now_count, arcs_YT_to_Pick[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)
    # print('cost : ', arcs_YT_to_Pick[i].cost)

    # now_count에 path 반영
    for j in range(len(arcs_YT_to_Pick[i].path)):
        now_count[(arcs_YT_to_Pick[i].path[j][0], arcs_YT_to_Pick[i].path[j][1])] += 1




# Pick_to_Drop의 arc 객체들의 cost 계산

# 객체들의 path 길이에 따른 sorting
arcs_Pick_to_Drop.sort(key = lambda x : len(x.path))

# 1. 각 arc들을 순회하며 cost 계산
# 2. 각 arc를 순회하며 해당 path를 now_count에 반영(밟는칸에 +1씩 count)
for i in range(len(arcs_Pick_to_Drop)):
    # cost 계산
    arcs_Pick_to_Drop[i].cost = cost(prev_count, now_count, arcs_Pick_to_Drop[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)
    # print('cost : ', arcs_Pick_to_Drop[i].cost)

    # now_count에 path 반영
    for j in range(len(arcs_Pick_to_Drop[i].path)):
        now_count[(arcs_Pick_to_Drop[i].path[j][0], arcs_Pick_to_Drop[i].path[j][1])] += 1

# Drop_to_Pick의 arc 객체들의 cost 계산

# 객체들의 path 길이에 따른 sorting
arcs_Drop_to_Pick.sort(key = lambda x : len(x.path))

# 1. 각 arc들을 순회하며 cost 계산
# 2. 각 arc를 순회하며 해당 path를 now_count에 반영(밟는칸에 +1씩 count)
for i in range(len(arcs_Drop_to_Pick)):
    # cost 계산
    arcs_Drop_to_Pick[i].cost = cost(prev_count, now_count, arcs_Drop_to_Pick[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)
    # print('cost : ', arcs_Drop_to_Pick[i].cost)

    # now_count에 path 반영
    for j in range(len(arcs_Drop_to_Pick[i].path)):
        now_count[(arcs_Drop_to_Pick[i].path[j][0], arcs_Drop_to_Pick[i].path[j][1])] += 1








# Drop에서 Sink노드로 가는 arc 객체 생성
for i in range(number_of_job):
    arcname = 'Drop' + str(i) + 'to' + 'Sink'
    arcname = arc(i = ['Drop', i], j = ['Sink'], k = 0, path = [], cost = 0, index=None)
    arcs_Drop_to_Sink.append(arcname)

# YT에서  Sink노드로 가는 arc 객체 생성
for i in range(number_of_YT):
    arcname = 'YT' + str(i) + 'to' + 'Sink'
    arcname = arc(i = ['YT', i], j = ['Sink'], k = 0, path = [], cost = 0, index=None)
    arcs_YT_to_Sink.append(arcname)


# 모든 arc 객체들을 하나의 리스트에 저장, index부여

all_arcs = arcs_YT_to_Pick + arcs_Pick_to_Drop + arcs_Drop_to_Pick + arcs_Drop_to_Sink + arcs_YT_to_Sink
# print('all_arcs : ', all_arcs)
# print('lengt of all_arcs : ', len(all_arcs))
for _ in range(len(all_arcs)):
    all_arcs[_].index = _
    #print('index : ', all_arcs[_].index)

# 각 아크의 cost 출력
for i in range(len(all_arcs)):
    print('i : ', all_arcs[i].i,
          'j : ', all_arcs[i].j,
          'k : ', all_arcs[i].k,
          'cost : ', all_arcs[i].cost,
          'index : ', all_arcs[i].index)

Total_arc_num = len(arcs_YT_to_Pick) + len(arcs_Pick_to_Drop) + len(arcs_Drop_to_Pick) + len(arcs_Drop_to_Sink) + len(arcs_YT_to_Sink)



# for i in range(len(all_arcs)):
#     print(all_arcs[i].index)













# Decision Variables
# x : 어떤 아크가 활성화 되는지 나타내는 변수(활성화 : 1, 비활성화 : 0)
x = np.empty(Total_arc_num, dtype=object)
for i in range(Total_arc_num):
    x[i] = solver.IntVar(0, 1, 'x[%i]' % i)



# Constraints 1 : 한 YT에서 활성화되는 아크들의 합은 1
# 출발지(i)가 같은 YT인 아크들의 합을 1로
for l in range(number_of_YT):
    list_for_const1 = []
    for a in all_arcs:
        if a.i == ['YT', l]:
            list_for_const1.append(a.index)
    # print('l : ', l)
    # print('list_for_const1 : ', list_for_const1)
    solver.Add(sum(x[j] for j in list_for_const1) == 1)
    # print('sum(x[j] for j in list_for_const1) : ', sum(x[j] for j in list_for_const1))

# Constraint 2 : sink node로 들어오는 아크들의 합은 YT의 수
list_for_const2 = []
for a in all_arcs:
    if a.j[0] == 'Sink':
        list_for_const2.append(a.index)

solver.Add(sum(x[j] for j in list_for_const2) == number_of_YT)
#print(list_for_const2)


# Constraint 3 : Pick 노드와 Drop노드 대상으로,각 노드에 들어오는 아크와 나가는 아크의 수의 합이 같아야함
for l in range(number_of_job):
    list_for_const3_from_Pick = []
    list_for_const3_to_Pick = []
    list_for_const3_from_Drop = []
    list_for_const3_to_Drop = []

    for a in all_arcs:
        if a.i == ['Pick', l]:
            list_for_const3_from_Pick.append(a.index)
        if a.j == ['Pick', l]:
            list_for_const3_to_Pick.append(a.index)
        if a.i == ['Drop', l]:
            list_for_const3_from_Drop.append(a.index)
        if a.j == ['Drop', l]:
            list_for_const3_to_Drop.append(a.index)

    solver.Add(sum(x[j] for j in list_for_const3_from_Pick) == sum(x[j] for j in list_for_const3_to_Pick))
    solver.Add(sum(x[j] for j in list_for_const3_from_Drop) == sum(x[j] for j in list_for_const3_to_Drop))
    # print('l : ', l)
    # print('list_for_const3_from_Pick : ', list_for_const3_from_Pick)
    # print('list_for_const3_to_Pick : ', list_for_const3_to_Pick)
    # print('list_for_const3_from_Drop : ', list_for_const3_from_Drop)
    # print('list_for_const3_to_Drop : ', list_for_const3_to_Drop)



# Constraint 4 : Drop노드 대상으로, 각 Drop노드에 들어오는 아크의 합이 1
for l in range(number_of_job):
    list_for_const4 = []

    for a in all_arcs:
        if a.j == ['Drop', l]:
            list_for_const4.append(a.index)
    solver.Add(sum(x[j] for j in list_for_const4) == 1)








# for i in range(len(all_arcs)):
#     print('i : ', all_arcs[i].i, 'j : ', all_arcs[i].j, 'cost : ', all_arcs[i].cost, 'index : ', all_arcs[i].index)




# for i in range(len(all_arcs)):
#     print(i == all_arcs[i].index)

# Obejctive
objective = solver.Objective()
for i in range(Total_arc_num):
    # 인덱스가 i인 arc의 cost를 x[i]와 곱해서 objective에 추가
    objective.SetCoefficient(x[i], all_arcs[i].cost)
    

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










