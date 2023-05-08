import numpy as np
import matplotlib.pyplot as plt
import time
import math
import heapq

import route_algorithm as ra


# issues
# 1. arc 리스트에 arcname으로 안담김
# 2. [해결], 경로 수 3개보다 작을때 더미 path추가 해주고 그 경로의 cost는 무한대로 해줘야함
# 3. move 함수 작성시 path라는 변수 없이도 재귀적으로 돌수있게 수정
# 4. 아크 다 순회한 now_count를 prev_count로 바꿔주는 코드 작성



# parameter
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

now_count = np.zeros((9,7))

alpha1 = 0.4
alpha2 = 0.3
alpha3 = 0.3

number_of_YT = 2
number_of_job = 2
# 다수의 route에서 최종적으로 몇개의 arc만 남길지
number_of_final_route = 3

# YT와 Job(Pick, Drop)의 인덱스, 위치를 저장하는 딕셔너리
YT_locations = {}
Job_locations = {}
# YT->Pick, Pick->Drop의 아크 객체(출발지, 도착지, 몇번째 경로인지, 경로 정보, cost)를 저장하는 딕셔너리
arcs_YT_to_Pick = []
arcs_Pick_to_Drop = []


class arc:
    def __init__(self, i, j, k, path, cost):
        
        self.i = i
        self.j = j
        self.k = k
        self.path = path
        self.cost = None

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

    # print(penalty_list)
    # print(final_three_route)

    return final_route


# 주어진 path의 cost 계산, 더미 아크(path의 길이 0)는 cost 무한대
def cost(prev_count, now_count, path, alpha1, alpha2, alpha3):
    if len(path) == 0:
        cost = math.inf
    else:
        sum_of_counter_of_prev_count = 0
        sum_of_counter_of_now_count = 0
        sum_of_move = len(path)
        for i in range(len(path)):
            sum_of_counter_of_prev_count += prev_count[(path[i][0], path[i][1])]
            sum_of_counter_of_now_count += now_count[(path[i][0], path[i][1])]

        # cost 산출
        cost = (alpha1 * sum_of_counter_of_prev_count) + (alpha2 * sum_of_counter_of_now_count) + (alpha3 * sum_of_move)
        
    return cost

# Experiment
# 스케줄링 대상 YT 생성
for i in range(number_of_YT):
    YT_position = None
    while YT_position is None or grid[YT_position] == -1:
        YT_position = (np.random.randint(9), np.random.randint(7))
    YT_locations[i] = YT_position

# 스케줄링 대상 작업 생성
for j in range(number_of_job):
    Pick_position = None
    Drop_position = None
    while Pick_position is None or grid[Pick_position] == -1 or Drop_position is None or grid[Drop_position] == -1 or Pick_position == Drop_position:
        Pick_position = (np.random.randint(9), np.random.randint(7))
        Drop_position = (np.random.randint(9), np.random.randint(7))
    Job_locations[j] = [Pick_position, Drop_position]



# YT에서 Pick으로 이동하는 경로 탐색, 아크 생성
for i in range(number_of_YT):
    for j in range(number_of_job):
        YT_position = YT_locations[i]
        Pick_position = Job_locations[j][0]
        
        # print('YT_position : ', YT_position)
        # print('Pick_position : ', Pick_position)

        path_YT_to_Pick = []
        route_YT_to_Pick = []

        # 모든 경우의 경로 탐색
        ra.move(YT_position, Pick_position, grid, path_YT_to_Pick, route_YT_to_Pick)
        # print('length of route_YT_to_Pick : ', len(route_YT_to_Pick))


        # 경로 수가 3개보다 많으면 패널티 함수 통해 3개로 줄이기
        if len(route_YT_to_Pick) > 3 :
            final_route_YT_to_Pick = penalty(prev_count, route_YT_to_Pick, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
        # 그렇지 않으면 (더미 추가했지만 더미 경로 내용 안정해줌 !!)
        else:
            for i in range(3 - len(route_YT_to_Pick)):
                # 빈 path 추가, 추후 해당 경로에 cost를 아주 큰 값으로 할당해서 해당 arc를 선택하지 않도록
                route_YT_to_Pick.append([])
            final_route_YT_to_Pick = route_YT_to_Pick

        # print('final_route_YT_to_Pick : ', final_route_YT_to_Pick)
        # print('lengh of final_route_YT_to_Pick : ', len(final_route_YT_to_Pick))

        # 경로 1개당 arc 객체 생성(YT -> Pick)
        for k in range(len(final_route_YT_to_Pick)):
            # YT -> Pick 경로의 arc 객체 생성
            arcname = 'YT' + str(i) + 'to' + 'Pick' + str(j)
            arcname = arc(i = ['YT', i], j = ['Pick', j], k = k, path = final_route_YT_to_Pick[k], cost = None)
            arcs_YT_to_Pick.append(arcname)



# Pick에서 Drop으로 가는 경로 생성, 아크 생성
# 위의 for loop와 분리한이유 : YT -> Pick은 YT 하나에 모든 Job과 경로를 생성해야하지만 하나의 Job 안에서 Pick과 Drop의 연결은 한번만(경로는 세개 생성) 일어나도 되기 때문
for j in range(number_of_job):
    Pick_position = Job_locations[j][0]
    Drop_position = Job_locations[j][1]

    print('Pick_position : ', Pick_position)
    print('Drop_position : ', Drop_position)

    path_Pick_to_Drop = []
    route_Pick_to_Drop = []

    # 모든 경우의 경로 탐색
    ra.move(Pick_position, Drop_position, grid, path_Pick_to_Drop, route_Pick_to_Drop)
    print('length of route_Pick_to_Drop : ', len(route_Pick_to_Drop))
    print('route_Pick_to_Drop')
    for i in range(len(route_Pick_to_Drop)):
        print(route_Pick_to_Drop[i])


    # 경로 수가 3개보다 많으면 패널티 함수 통해 3개로 줄이기
    if len(route_Pick_to_Drop) > 3 :
        final_route_Pick_to_Drop = penalty(prev_count, route_Pick_to_Drop, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
    # 그렇지 않으면
    else:
        for i in range(3 - len(route_Pick_to_Drop)):
            # 빈 path 추가, 추후 해당 경로에 cost를 아주 큰 값으로 할당해서 해당 arc를 선택하지 않도록
            route_Pick_to_Drop.append([])
        final_route_Pick_to_Drop = route_Pick_to_Drop

    print('length of final_route_Pick_to_Drop : ', len(final_route_Pick_to_Drop))
    for i in range(len(final_route_Pick_to_Drop)):
        print(final_route_Pick_to_Drop[i])

    # 경로 1개당 arc 객체 생성(Pick -> Drop)
    for k in range(len(final_route_Pick_to_Drop)):
        arcname = 'Pick' + str(j) + 'to' + 'Drop' + str(j)
        arcname = arc(i = ['Pick', j], j = ['Drop', j], k = k, path = final_route_Pick_to_Drop[k], cost = None)
        arcs_Pick_to_Drop.append(arcname)



# !!! 현재는 YT->Pick 아크들 먼저 길이순 오름차순 정렬하여 cost 계산 후 Pick->Drop 아크들 길이순 오름차순 정렬하여 cost 계산하는 방식으로 진행
# !!! 따라서 앞부분 아크들이 우선적으로 cost계산되어 더 높은 우선순위로 인식됨

# YT_to_Pick의 arc 객체들의 cost 계산

# 객체들의 path 길이에 따른 sorting
arcs_YT_to_Pick.sort(key = lambda x : len(x.path))

# 1. 각 arc들을 순회하며 cost 계산
# 2. 각 arc를 순회하며 해당 path를 now_count에 반영(밟는칸에 +1씩 count)
for i in range(len(arcs_YT_to_Pick)):
    # print('YT_to_Pick : ', i)
    # print('path : ', arcs_YT_to_Pick[i].path)
    # print('length of path : ', len(arcs_YT_to_Pick[i].path))
    # print('cost : ', arcs_YT_to_Pick[i].cost)

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
