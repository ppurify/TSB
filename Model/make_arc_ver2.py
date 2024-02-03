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
        normalized_data = np.full((len(data), len(data[0])), 0.5)
    else:
        normalized_data = (data - min_val) / (max_val - min_val)
    
    return normalized_data


def penalty(normalized_prev_count, route, number_of_final_route, alpha1, alpha3, time_consumed_per_grid):
    """arc trimming"""
    penalty_list = []

    for i in range(len(route)):
        sum_of_counter_of_prev_count = 0
        sum_of_move = len(route[i])
        for j in range(len(route[i])):
            sum_of_counter_of_prev_count += normalized_prev_count[(route[i][j][0], route[i][j][1])]

        # route 내의 각 경로의 penalty 산출하여 리스트에 저장
        penalty_list.append((alpha1 * sum_of_counter_of_prev_count) + alpha3 * (sum_of_move * time_consumed_per_grid))
        
    # penalty가 가장 작은 number_of_final_route개의 경로의 인덱스를 추출하여 final_route 리스트에 저장
    final_route_idx = heapq.nsmallest(number_of_final_route, range(len(penalty_list)), key=penalty_list.__getitem__)
    final_route = [route[i] for i in final_route_idx]
    return final_route


def get_cost(normalized_prev_count, normalized_now_count, path, alpha1, alpha2, alpha3, time_consumed_per_grid, processing_time):
    """arc cost 계산"""
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
        total_cost = round((alpha1 * sum_of_counter_of_prev_count) + (alpha2 * sum_of_counter_of_now_count) + (alpha3 * (sum_of_move * time_consumed_per_grid + 2*processing_time)))

    return total_cost


def sort_and_cost(arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, prev_count, now_count, alpha1, alpha2, alpha3, time_consumed_per_grid, processing_time):

    # A1를 now_count에 path 반영
    for i in range(len(arcs_YT_to_Pick)):
        for j in range(len(arcs_YT_to_Pick[i].path)):
            now_count[(arcs_YT_to_Pick[i].path[j][0], arcs_YT_to_Pick[i].path[j][1])] += 1

    # 이전, 현재 혼잡도 정규화
    normalized_prev_count = min_max_normalization(prev_count)
    normalized_A1_now_count = min_max_normalization(now_count)

    # A1 cost 계산
    for i in range(len(arcs_YT_to_Pick)):
        arcs_YT_to_Pick[i].cost = get_cost(normalized_prev_count, normalized_A1_now_count, arcs_YT_to_Pick[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3, time_consumed_per_grid=time_consumed_per_grid, processing_time = 0)
    # A2 계산을 위해 now_count 초기화
    now_count = np.zeros((len(prev_count), len(prev_count[0])))
    

    # A2를 now_count에 path 반영
    for i in range(len(arcs_Pick_to_Drop)):
        for j in range(len(arcs_Pick_to_Drop[i].path)):
            now_count[(arcs_Pick_to_Drop[i].path[j][0], arcs_Pick_to_Drop[i].path[j][1])] += 1

    # 이전혼잡도는 임시적으로 0으로 초기화, 현재 혼잡도 정규화
    A2_prev_count_for_cost = np.zeros((len(prev_count), len(prev_count[0])))
    normalized_A2_now_count = min_max_normalization(now_count)

    # A2 cost 계산
    for i in range(len(arcs_Pick_to_Drop)):
        arcs_Pick_to_Drop[i].cost = get_cost(A2_prev_count_for_cost, normalized_A2_now_count, arcs_Pick_to_Drop[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3, time_consumed_per_grid=time_consumed_per_grid, processing_time = 0)
    # A3 계산을 위해 now_count 초기화
    now_count = np.zeros((len(prev_count), len(prev_count[0])))



    # A3를 now_count에 path 반영
    for i in range(len(arcs_Drop_to_Pick)):
        for j in range(len(arcs_Drop_to_Pick[i].path)):
            now_count[(arcs_Drop_to_Pick[i].path[j][0], arcs_Drop_to_Pick[i].path[j][1])] += 1

    # 이전혼잡도는 임시적으로 0으로 초기화, 현재 혼잡도 정규화
    A3_prev_count_for_cost = np.zeros((len(prev_count), len(prev_count[0])))
    normalized_A3_now_count = min_max_normalization(now_count)

    # A3 cost 계산
    for i in range(len(arcs_Drop_to_Pick)):
        # print('A3 : ', i)
        arcs_Drop_to_Pick[i].cost = get_cost((A3_prev_count_for_cost), (normalized_A3_now_count), arcs_Drop_to_Pick[i].path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3, time_consumed_per_grid=time_consumed_per_grid, processing_time = processing_time)
    
    # A4 cost 계산
    for i in range(len(arcs_Drop_to_Sink)):
        arcs_Drop_to_Sink[i].cost = 0
    # A5 cost 계산
    for i in range(len(arcs_YT_to_Sink)):
        arcs_YT_to_Sink[i].cost = 0

    return arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count



def create_arcs(YT_locations, Job_locations, number_of_final_route, alpha1, alpha2, alpha3, grid, prev_count, now_count, time_consumed_per_grid, processing_time):
    """아크생성, penalty, cost함수 실행"""
    # A1
    arcs_YT_to_Pick = []
    # A2
    arcs_Pick_to_Drop = []
    # A3
    arcs_Drop_to_Pick = []
    # A4
    arcs_Drop_to_Sink = []
    # A5
    arcs_YT_to_Sink = []

    # 아크 인덱스
    now_index = 0
    # 이전 A2경로들의 누적 path정보 정규화
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
                final_route_YT_to_Pick = penalty(normalized_prev_count, route_YT_to_Pick, number_of_final_route, alpha1=alpha1, alpha3=alpha3, time_consumed_per_grid=time_consumed_per_grid)
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
        
        # A2_prev_count_for_penalty : 이전 A3의 누적 path정보를 누적한 grid 생성, 임시적으로 0으로 초기화
        A2_prev_count_for_penalty = np.zeros((len(grid), len(grid[0])))

        # 경로 수가 3개보다 많으면 패널티 함수 통해 3개로 줄이기
        if len(route_Pick_to_Drop) > number_of_final_route:
            final_route_Pick_to_Drop = penalty(A2_prev_count_for_penalty, route_Pick_to_Drop, number_of_final_route, alpha1=alpha1, alpha3=alpha3, time_consumed_per_grid=time_consumed_per_grid)
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

                # A3_prev_count_for_penalty : 임시적으로 0으로 초기화
                A3_prev_count_for_penalty = np.zeros((len(grid), len(grid[0])))
               
                # 경로 수가 3개보다 많으면 패널티 함수 통해 3개로 줄이기
                if len(route_Drop_to_Pick) > number_of_final_route :
                    final_route_Drop_to_Pick = penalty(A3_prev_count_for_penalty, route_Drop_to_Pick, number_of_final_route, alpha1=alpha1, alpha3=alpha3, time_consumed_per_grid=time_consumed_per_grid)
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


    arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count = sort_and_cost(
        arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, prev_count, now_count, alpha1, alpha2, alpha3, time_consumed_per_grid, processing_time)

    return arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count