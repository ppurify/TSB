import sys
import heapq
import numpy as np

import route_algorithm as ra


class arc:
    def __init__(self, i, j, k, path, cost, index):
        self.i = i
        self.j = j
        self.k = k
        self.path = path
        self.cost = 0
        self.index = index
        return


def min_max_normalization(data):
    min_val = np.min(data)
    max_val = np.max(data)
    if min_val == max_val:
        normalized_data = np.zeros((len(data), len(data[0])))
    else:
        normalized_data = (data - min_val) / (max_val - min_val)
    
    return normalized_data


# route로 다수의 경로 받아서 최종 number_of_final_route개의 경로 final_route 반환
def penalty(normalized_prev_count, route, number_of_final_route, alpha1, alpha3):
    penalty_list = []

    for i in range(len(route)):
        sum_of_counter_of_prev_count = 0
        sum_of_move = len(route[i])
        for j in range(len(route[i])):
            sum_of_counter_of_prev_count += normalized_prev_count[(route[i][j][0], route[i][j][1])]

        # 각 경로의 penalty 산출하여 리스트에 저장
        # penalty_list.append((alpha1 * sum_of_counter_of_prev_count) + (alpha3 * sum_of_move))
        penalty_list.append((alpha1 * sum_of_counter_of_prev_count) + (sum_of_move))

    # penalty가 가장 작은 number_of_final_route개의 경로의 인덱스를 추출하여 final_three_route 리스트에 저장
    final_route_idx = heapq.nsmallest(number_of_final_route, range(len(penalty_list)), key=penalty_list.__getitem__)
    final_route = [route[i] for i in final_route_idx]
    return final_route

# pseudo code of penalty function
# for pair in pairs:
#     for arc in pair:
#         input : path, Q_(x,y)^prev count
#         for coordinate in path:
#             prev_count_sum += Q_(x,y)^prev count[coordinate]
#         penalty = alpha1 * prev_count_sum + alpha3 * len(path)
#     pick k' paths with the smallest penalty

# # 주어진 path의 cost 계산, 더미 아크(path의 길이 0)는 cost 무한대
# def get_cost(prev_count, now_count, path, alpha1, alpha2, alpha3):
#     if len(path) == 0:
#         total_cost = sys.maxsize
#     else:
#         sum_of_counter_of_prev_count = 0
#         sum_of_counter_of_now_count = 0
#         sum_of_move = len(path)
#         for i in range(len(path)):
#             sum_of_counter_of_prev_count += prev_count[(path[i][0], path[i][1])]
#             sum_of_counter_of_now_count += now_count[(path[i][0], path[i][1])]

#         # cost 산출(반올림)
#         total_cost = round((alpha1 * sum_of_counter_of_prev_count) + (alpha2 * sum_of_counter_of_now_count) + (alpha3 * sum_of_move))
#     return total_cost


def get_cost(normalized_prev_count, normalized_now_count, path, alpha1, alpha2, alpha3):

    if len(path) == 0:
        total_cost = sys.maxsize
    else:
        sum_of_counter_of_prev_count = 0
        sum_of_counter_of_now_count = 0
        sum_of_move = len(path)
        for i in range(len(path)):
            sum_of_counter_of_prev_count += normalized_prev_count[(path[i][0], path[i][1])]
            sum_of_counter_of_now_count += normalized_now_count[(path[i][0], path[i][1])]

        # cost 산출(반올림)
        total_cost = round((alpha1 * sum_of_counter_of_prev_count) + (alpha2 * sum_of_counter_of_now_count) + (alpha3 * sum_of_move))
    return total_cost


def sort_and_cost(YT_locations, Job_locations, arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, prev_count, now_count, alpha1, alpha2, alpha3):

    # A1를 now_count에 path 반영
    for i in range(len(arcs_YT_to_Pick)):
        for j in range(len(arcs_YT_to_Pick[i].path)):
            now_count[(arcs_YT_to_Pick[i].path[j][0], arcs_YT_to_Pick[i].path[j][1])] += 1


    normalized_prev_count = min_max_normalization(prev_count)
    normalized_A1_now_count = min_max_normalization(now_count)
    max_A1_now_count = np.max(normalized_A1_now_count)

    # A1 cost 계산
    for i in range(len(arcs_YT_to_Pick)):
        arcs_YT_to_Pick[i].cost = get_cost(normalized_prev_count, normalized_A1_now_count, arcs_YT_to_Pick[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)

    # now_count 초기화
    now_count = np.zeros((len(prev_count), len(prev_count[0])))
    
    # A2를 now_count에 path 반영
    for i in range(len(arcs_Pick_to_Drop)):
        for j in range(len(arcs_Pick_to_Drop[i].path)):
            now_count[(arcs_Pick_to_Drop[i].path[j][0], arcs_Pick_to_Drop[i].path[j][1])] += 1

    # pair : 같은 출발지 i와 도착지 j를 가지는 arc들의 집합
    # A1에서 각 pair마다 cost가 가장 작은 아크만 반영하여 prev count 생성
    A2_prev_count = np.zeros((len(prev_count), len(prev_count[0])))
    for i in range(len(YT_locations)):
        for j in range(len(Job_locations)):
            min_cost_in_pair = sys.maxsize
            for k in range(len(arcs_YT_to_Pick)):
                if arcs_YT_to_Pick[k].i == ['YT', i] and arcs_YT_to_Pick[k].j == ['Pick', j]:
                    if min_cost_in_pair > arcs_YT_to_Pick[k].cost:
                        min_cost_in_pair = arcs_YT_to_Pick[k].cost
                        min_cost_in_pair_index = k
            if min_cost_in_pair != sys.maxsize:
                for l in range(len(arcs_YT_to_Pick[min_cost_in_pair_index].path)):
                    A2_prev_count[(arcs_YT_to_Pick[min_cost_in_pair_index].path[l][0], arcs_YT_to_Pick[min_cost_in_pair_index].path[l][1])] += 1

    normalized_A2_prev_count = min_max_normalization(now_count)
    normalized_A2_now_count = min_max_normalization(now_count)
    # max_A2_now_count = np.max(normalized_A2_now_count)

    # A2 cost 계산
    for i in range(len(arcs_Pick_to_Drop)):
        arcs_Pick_to_Drop[i].cost = get_cost(normalized_A2_prev_count, normalized_A2_now_count, arcs_Pick_to_Drop[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)

    # now_count 초기화
    now_count = np.zeros((len(prev_count), len(prev_count[0])))

    # A3를 now_count에 path 반영
    for i in range(len(arcs_Drop_to_Pick)):
        for j in range(len(arcs_Drop_to_Pick[i].path)):
            now_count[(arcs_Drop_to_Pick[i].path[j][0], arcs_Drop_to_Pick[i].path[j][1])] += 1


    # A2에서 각 pair마다 cost가 가장 작은 아크만 반영하여 prev count 생성
    A3_prev_count = np.zeros((len(prev_count), len(prev_count[0])))
    for i in range(len(Job_locations)):
        min_cost_in_pair = sys.maxsize
        for k in range(len(arcs_Pick_to_Drop)):
            if arcs_Pick_to_Drop[k].i == ['Pick', i] and arcs_Pick_to_Drop[k].j == ['Drop', i]:
                if min_cost_in_pair > arcs_Pick_to_Drop[k].cost:
                    min_cost_in_pair = arcs_Pick_to_Drop[k].cost
                    min_cost_in_pair_index = k
        if min_cost_in_pair != sys.maxsize:
            for l in range(len(arcs_Pick_to_Drop[min_cost_in_pair_index].path)):
                A3_prev_count[(arcs_Pick_to_Drop[min_cost_in_pair_index].path[l][0], arcs_Pick_to_Drop[min_cost_in_pair_index].path[l][1])] += 1

    normalized_A3_prev_count = min_max_normalization(now_count)
    normalized_A3_now_count = min_max_normalization(now_count)

    # max_A3_now_count = np.max(normalized_A3_now_count)/

    # A3 cost 계산
    for i in range(len(arcs_Drop_to_Pick)):
        arcs_Drop_to_Pick[i].cost = get_cost((normalized_A3_prev_count), (normalized_A3_now_count), arcs_Drop_to_Pick[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)+1000000

    # A4 cost 계산
    for i in range(len(arcs_Drop_to_Sink)):
        arcs_Drop_to_Sink[i].cost = 0

    # A5 cost 계산
    for i in range(len(arcs_YT_to_Sink)):
        arcs_YT_to_Sink[i].cost = 0


    # print('A1_now_count : ', normalized_A1_now_count)
    # print('')
    # print('A2_now_count : ', normalized_A2_now_count)
    # print('')
    # print('A3_now_count : ', normalized_A3_now_count)

    return arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count






# # !!! 현재는 YT->Pick 아크들 먼저 길이순 오름차순 정렬하여 cost 계산 후 Pick->Drop 아크들 길이순 오름차순 정렬하여 cost 계산하는 방식으로 진행
# # !!! 따라서 앞부분 아크들(YT->Pick, Pick->Drop, Drop->다른 Pick 순서)이 우선적으로 cost계산되어 더 높은 우선순위로 인식됨
# def sort_and_cost(arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, prev_count, now_count, alpha1, alpha2, alpha3):

#     # A1(YT_to_Pick)
#     # 객체들의 path 길이에 따른 sorting
#     arcs_YT_to_Pick.sort(key = lambda x : len(x.path))

#     # 1. 각 arc들을 순회하며 cost 계산
#     # 2. 각 arc를 순회하며 해당 path를 now_count에 반영(밟는칸에 +1씩 count)
#     for i in range(len(arcs_YT_to_Pick)):
#         # cost 계산
#         arcs_YT_to_Pick[i].cost = get_cost(prev_count, now_count, arcs_YT_to_Pick[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)

#         # now_count에 path 반영
#         for j in range(len(arcs_YT_to_Pick[i].path)):
#             now_count[(arcs_YT_to_Pick[i].path[j][0], arcs_YT_to_Pick[i].path[j][1])] += 1

#     # now count 초기화
#     now_count = np.zeros((len(prev_count), len(prev_count[0])))
    
#     # A2(Pick_to_Drop)
#     arcs_Pick_to_Drop.sort(key = lambda x : len(x.path))

#     for i in range(len(arcs_Pick_to_Drop)):
#         arcs_Pick_to_Drop[i].cost = get_cost(prev_count, now_count, arcs_Pick_to_Drop[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)

#         # now_count에 path 반영
#         for j in range(len(arcs_Pick_to_Drop[i].path)):
#             now_count[(arcs_Pick_to_Drop[i].path[j][0], arcs_Pick_to_Drop[i].path[j][1])] += 1


#     # now count 초기화
#     now_count = np.zeros((len(prev_count), len(prev_count[0])))
    
#     # A3(Drop_to_Pick)
#     arcs_Drop_to_Pick.sort(key = lambda x : len(x.path))

#     for i in range(len(arcs_Drop_to_Pick)):
#         arcs_Drop_to_Pick[i].cost = get_cost(prev_count, now_count, arcs_Drop_to_Pick[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)

#         # now_count에 path 반영
#         for j in range(len(arcs_Drop_to_Pick[i].path)):
#             now_count[(arcs_Drop_to_Pick[i].path[j][0], arcs_Drop_to_Pick[i].path[j][1])] += 1

#     # A4
#     for i in range(len(arcs_Drop_to_Sink)):
#         arcs_Drop_to_Sink[i].cost = 0

#     # A5
#     for i in range(len(arcs_YT_to_Sink)):
#         arcs_YT_to_Sink[i].cost = 0

#     return arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count





def create_arcs(YT_locations, Job_locations, number_of_final_route, alpha1, alpha2, alpha3, grid, prev_count, now_count):
    arcs_YT_to_Pick = []
    arcs_Pick_to_Drop = []
    arcs_Drop_to_Pick = []
    arcs_Drop_to_Sink = []
    arcs_YT_to_Sink = []

    now_index = 0
    normalized_prev_count = min_max_normalization(prev_count)
    
    # 1. YT -> Pick 경로, 아크 생성
    for i in range(len(YT_locations)):
        for j in range(len(Job_locations)):
            YT_location = YT_locations[i]
            Pick_location = Job_locations[j][0]

            path_YT_to_Pick = []
            route_YT_to_Pick = []

            # 모든 경우의 경로 탐색
            route_YT_to_Pick = ra.move(YT_location, Pick_location, grid, path_YT_to_Pick, route_YT_to_Pick)

            # 경로 수가 number_of_final_route개보다 많으면 패널티 함수 통해 number_of_final_route개로 줄이기
            if len(route_YT_to_Pick) > number_of_final_route:
                final_route_YT_to_Pick = penalty(normalized_prev_count, route_YT_to_Pick, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
            else:
                final_route_YT_to_Pick = route_YT_to_Pick

            # 경로 1개당 arc 객체 생성(YT -> Pick)
            for k in range(len(final_route_YT_to_Pick)):
                arcname = 'YT' + str(i) + 'to' + 'Pick' + str(j) + 'path' + str(k)
                arcname = arc(i=['YT', i], j=['Pick', j], k=k, path=final_route_YT_to_Pick[k], cost=None, index = now_index)
                now_index += 1
                arcs_YT_to_Pick.append(arcname)


    # 2. Pick -> Drop 경로, 아크 생성
    for j in range(len(Job_locations)):
        Pick_location = Job_locations[j][0]
        Drop_location = Job_locations[j][1]

        path_Pick_to_Drop = []
        route_Pick_to_Drop = []

        # 모든 경우의 경로 탐색
        route_Pick_to_Drop = ra.move(Pick_location, Drop_location, grid, path_Pick_to_Drop, route_Pick_to_Drop)

        # 경로 수가 3개보다 많으면 패널티 함수 통해 3개로 줄이기
        if len(route_Pick_to_Drop) > number_of_final_route:
            final_route_Pick_to_Drop = penalty(normalized_prev_count, route_Pick_to_Drop, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
        else:
            final_route_Pick_to_Drop = route_Pick_to_Drop

        # 경로 1개당 arc 객체 생성(Pick -> Drop)
        for k in range(len(final_route_Pick_to_Drop)):
            arcname = 'Pick' + str(j) + 'to' + 'Drop' + str(j) + 'path' + str(k)
            arcname = arc(i=['Pick', j], j=['Drop', j], k=k, path=final_route_Pick_to_Drop[k], cost=None, index=now_index)
            now_index += 1
            arcs_Pick_to_Drop.append(arcname)


    # 3. Drop -> 다른 Job의 Pick 경로, 아크 생성
    for i in range(len(Job_locations)):
        for j in range(len(Job_locations)):
            if i != j:
                Drop_location = Job_locations[i][1]
                Pick_location = Job_locations[j][0]
                
                path_Drop_to_Pick = []
                route_Drop_to_Pick = []

                # 모든 경우의 경로 탐색
                route_Drop_to_Pick = ra.move(Drop_location, Pick_location, grid, path_Drop_to_Pick, route_Drop_to_Pick)

                # 경로 수가 3개보다 많으면 패널티 함수 통해 3개로 줄이기
                if len(route_Drop_to_Pick) > number_of_final_route :
                    final_route_Drop_to_Pick = penalty(normalized_prev_count, route_Drop_to_Pick, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
                else:
                    final_route_Drop_to_Pick = route_Drop_to_Pick

                # 경로 1개당 arc 객체 생성(Drop -> Pick)
                for k in range(len(final_route_Drop_to_Pick)):
                    arcname = 'Drop' + str(i) + 'to' + 'Pick' + str(j) + 'path' + str(k)
                    arcname = arc(i = ['Drop', i], j = ['Pick', j], k = k, path = final_route_Drop_to_Pick[k], cost = None, index=now_index)
                    now_index += 1
                    arcs_Drop_to_Pick.append(arcname)


    # 4. Drop -> Sink 아크 생성
    for i in range(len(Job_locations)):
        arcname = 'Drop' + str(i) + 'to' + 'Sink'
        arcname = arc(i = ['Drop', i], j = ['Sink'], k = 0, path = [], cost = 0, index=now_index)
        now_index += 1
        arcs_Drop_to_Sink.append(arcname)

    # 5. YT -> Sink 아크 생성
    for i in range(len(YT_locations)):
        arcname = 'YT' + str(i) + 'to' + 'Sink'
        arcname = arc(i = ['YT', i], j = ['Sink'], k = 0, path = [], cost = 0, index=now_index)
        now_index += 1
        arcs_YT_to_Sink.append(arcname)


    sort_and_cost(YT_locations, Job_locations, arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, prev_count, now_count, alpha1, alpha2, alpha3)

    return arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count



