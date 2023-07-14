import sys
import heapq

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

# route로 다수의 경로 받아서 최종 number_of_final_route개의 경로 final_route 반환
def get_penalty(prev_count, route, number_of_final_route, alpha1, alpha3):
    penalty_list = []

    for i in range(len(route)):
        # print('lenght of route : ', len(route[i]))
        sum_of_counter_of_prev_count = sum(prev_count[coordinate] for coordinate in route[i])
        sum_of_move = len(route[i])
        penalty = alpha1 * sum_of_counter_of_prev_count + alpha3 * sum_of_move
        penalty_list.append(penalty)
        # print('penalty : ', penalty)

    final_route_idx = heapq.nsmallest(number_of_final_route, range(len(penalty_list)), key=penalty_list.__getitem__)
    final_route = [route[i] for i in final_route_idx]
    return final_route


def get_cost(prev_count, now_count, path, alpha1, alpha2, alpha3):
    if not path:
        total_cost = sys.maxsize
    else:
        sum_of_counter_of_prev_count = sum(prev_count[node] for node in path)
        sum_of_counter_of_now_count = sum(now_count[node] for node in path)
        sum_of_move = len(path)
        # cost 산출(반올림)
        total_cost = round(alpha1 * sum_of_counter_of_prev_count + alpha2 * sum_of_counter_of_now_count + alpha3 * sum_of_move)
    return total_cost



# !!! 현재는 YT->Pick 아크들 먼저 길이순 오름차순 정렬하여 cost 계산 후 Pick->Drop 아크들 길이순 오름차순 정렬하여 cost 계산하는 방식으로 진행
# !!! 따라서 앞부분 아크들(YT->Pick, Pick->Drop, Drop->다른 Pick 순서)이 우선적으로 cost계산되어 더 높은 우선순위로 인식됨
def sort_and_cost(arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink,
                  prev_count, now_count_A1, now_count_A2, now_count_A3, alpha1, alpha2, alpha3):
    # A1
    arcs_YT_to_Pick.sort(key=lambda x: len(x.path))
    for arc in arcs_YT_to_Pick:
        arc.cost = get_cost(prev_count, now_count_A1, arc.path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)
        for node in arc.path:
            now_count_A1[node] += 1
    # print('now_count_A1 : ')
    # print(now_count_A1)

    # A2
    arcs_Pick_to_Drop.sort(key=lambda x: len(x.path))
    for arc in arcs_Pick_to_Drop:
        arc.cost = get_cost(prev_count, now_count_A2, arc.path, alpha1=0, alpha2=alpha2, alpha3=alpha3)
        for node in arc.path:
            now_count_A2[node] += 1
    # print('now_count_A2 : ')
    # print(now_count_A2)
    # A3
    arcs_Drop_to_Pick.sort(key=lambda x: len(x.path))
    for arc in arcs_Drop_to_Pick:
        arc.cost = get_cost(prev_count, now_count_A3, arc.path, alpha1=0, alpha2=alpha2, alpha3=alpha3)
        for node in arc.path:
            now_count_A3[node] += 1
    # print('now_count_A3 : ')
    # print(now_count_A3)
    
    # A4
    for arc in arcs_Drop_to_Sink:
        arc.cost = 0

    # A5
    for arc in arcs_YT_to_Sink:
        arc.cost = 0

    return arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink



# 아크생성, penalty 계산, cost 계산
def create_arcs(YT_locations, Job_locations, number_of_final_route, alpha1, alpha2, alpha3,
                grid, prev_count, now_count_A1, now_count_A2, now_count_A3):
    
    arcs_YT_to_Pick = []
    arcs_Pick_to_Drop = []
    arcs_Drop_to_Pick = []
    arcs_Drop_to_Sink = []
    arcs_YT_to_Sink = []

    now_index = 0

    def generate_routes(origin, destination):
        """origin에서 destination까지의 다수의 경로를 생성하고 해당 정보를 가진 아크 객체 생성하여 arcs_list에 추가"""
        path = []
        route = []

        # 모든 경우의 경로 탐색
        route = ra.move(origin, destination, grid, path, route)

        # 경로 수가 number_of_final_route보다 많으면 penalty 계산하여 최종 경로 number_of_final_route개로 축소
        if len(route) > number_of_final_route:
            final_routes = get_penalty(prev_count, route, number_of_final_route, alpha1, alpha3)
        else:
            final_routes = route
            
        return final_routes

    # def generate_arcs(i, j, k, path, now_index, arc_list):
    #     """경로를 받아서 아크 생성"""
    #     arcname = 'YT' + str(i) + 'to' + 'Pick' + str(j) + 'path' + str(k)
    #     arcname = arc(i=['YT', i], j=['Pick', j], k=k, path=path, cost=None, index = now_index)
    #     # print('arcname : ',arcname)
    #     # print('i : ',i)
    #     # print('j : ',j)
    #     # print('k : ',k)
    #     # print('path : ',path)
    #     # print('now_index : ',now_index)
    #     # print('')

    #     now_index += 1
    #     arc_list.append(arcname)

    #     # return arc_list

    # def generate_arcs(i, j, k, path, now_index, arcs_list):
    #     """i, j, k에 해당하는 정보를 가진 아크 객체 생성하여 arcs_list에 추가"""
    #     arcname = 'YT' + str(i) + 'to' + 'Pick' + str(j) + 'path' + str(k)
    #     arcname = arc(i=['YT', i], j=['Pick', j], k=k, path=path, cost=None, index=now_index)
    #     now_index += 1
    #     arcs_list.append(arcname)
    #     return arcs_list


    # 1. YT -> Pick 경로, 아크 생성
    for i in range(len(YT_locations)):
        for j in range(len(Job_locations)):
            route_YT_to_Pick = generate_routes(YT_locations[i], Job_locations[j][0])
    
            # for _ in range(len(route_YT_to_Pick)):
            #     print('route_YT_to_Pick : ',route_YT_to_Pick[_])
                


            # 경로 1개당 arc 객체 생성
            for k in range(len(route_YT_to_Pick)):
                # generate_arcs(i, j, k, route_YT_to_Pick[k], now_index, arcs_YT_to_Pick)
                # print('arcs_YT_to_Pick : ',arcs_YT_to_Pick)
                arcname = 'YT' + str(i) + 'to' + 'Pick' + str(j) + 'path' + str(k)
                arcname = arc(i=['YT', i], j=['Pick', j], k=k, path=route_YT_to_Pick[k], cost=None, index = now_index)
                now_index += 1
                arcs_YT_to_Pick.append(arcname)


    # 2. Pick -> Drop 경로, 아크 생성
    for j in range(len(Job_locations)):
        route_Pick_to_Drop = generate_routes(Job_locations[j][0], Job_locations[j][1])

        # for _ in range(len(route_Pick_to_Drop)):
        #     print('route_Pick_to_Drop : ',route_Pick_to_Drop[_])

        # 경로 1개당 arc 객체 생성(Pick -> Drop)
        for k in range(len(route_Pick_to_Drop)):
            # arcs_Pick_to_Drop = generate_arcs(j, j, k, route_Pick_to_Drop[k], now_index, arcs_Pick_to_Drop)
            arcname = 'Pick' + str(j) + 'to' + 'Drop' + str(j) + 'path' + str(k)
            arcname = arc(i=['Pick', j], j=['Drop', j], k=k, path=route_Pick_to_Drop[k], cost=None, index=now_index)
            now_index += 1
            arcs_Pick_to_Drop.append(arcname)


    # 3. Drop -> 다른 Job의 Pick 경로, 아크 생성
    for i in range(len(Job_locations)):
        for j in range(len(Job_locations)):
            if i != j:
                route_Drop_to_Pick = generate_routes(Job_locations[i][1], Job_locations[j][0])

                # 경로 1개당 arc 객체 생성(Drop -> Pick)
                for k in range(len(route_Drop_to_Pick)):
                    arcname = 'Drop' + str(i) + 'to' + 'Pick' + str(j) + 'path' + str(k)
                    arcname = arc(i = ['Drop', i], j = ['Pick', j], k = k, path = route_Drop_to_Pick[k], cost = None, index=now_index)
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

    arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink = sort_and_cost(arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink,
                    prev_count, now_count_A1, now_count_A2, now_count_A3, alpha1, alpha2, alpha3)
    
    return (arcs_YT_to_Pick,
            arcs_Pick_to_Drop,
            arcs_Drop_to_Pick,
            arcs_Drop_to_Sink,
            arcs_YT_to_Sink)





# def create_arcs_combined(YT_locations, Job_locations, number_of_final_route, alpha1, alpha2, alpha3, grid, prev_count, now_count):
#     arcs_YT_to_Pick = []
#     arcs_Pick_to_Drop = []
#     arcs_Drop_to_Pick = []
#     arcs_Drop_to_Sink = []
#     arcs_YT_to_Sink = []

#     now_index = 0

#     def calculate_cost(arcs, alpha1, alpha2, alpha3):
#         for arc in arcs:
#             arc.cost = get_cost(prev_count, now_count, arc.path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)
#             for node in arc.path:
#                 now_count[node] += 1

#     def create_arc(i, j, k, path, cost):
#         arc = arc(i=i, j=j, k=k, path=path, cost=cost, index=now_index)
#         now_index += 1
#         return arc

#     def create_arcs_route(source, destination, arc_list):
#         for i in range(len(source)):
#             for j in range(len(destination)):
#                 source_location = source[i]
#                 destination_location = destination[j][0]

#                 path = []
#                 route = []

#                 # 모든 경우의 경로 탐색
#                 route = ra.move(source_location, destination_location, grid, path, route)

#                 # 경로 수가 number_of_final_route개보다 많으면 패널티 함수 통해 number_of_final_route개로 줄이기
#                 if len(route) > number_of_final_route:
#                     final_route = penalty(prev_count, route, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
#                 else:
#                     final_route = route

#                 # 경로 1개당 arc 객체 생성
#                 for k in range(len(final_route)):
#                     arcname = create_arc(i, j, k, final_route[k], None)
#                     arc_list.append(arcname)

#     # 1. YT -> Pick 경로, 아크 생성
#     create_arcs_route(YT_locations, Job_locations, arcs_YT_to_Pick)

#     # 2. Pick -> Drop 경로, 아크 생성
#     create_arcs_route(Job_locations, Job_locations, arcs_Pick_to_Drop)

#     # 3. Drop -> 다른 Job의 Pick 경로, 아크 생성
#     create_arcs_route(Job_locations, Job_locations, arcs_Drop_to_Pick)

#     # 4. Drop -> Sink 아크 생성
#     for i in range(len(Job_locations)):
#         arcname = create_arc(['Drop', i], ['Sink'], 0, [], 0)
#         arcs_Drop_to_Sink.append(arcname)

#     # 5. YT -> Sink 아크 생성
#     for i in range(len(YT_locations)):
#         arcname = create_arc(['YT', i], ['Sink'], 0, [], 0)
#         arcs_YT_to_Sink.append(arcname)

#     calculate_cost(arcs_YT_to_Pick, alpha1, alpha2, alpha3)
#     calculate_cost(arcs_Pick_to_Drop, 0, alpha2, alpha3)
#     calculate_cost(arcs_Drop_to_Pick, 0, alpha2, alpha3)

#     return (
#         arcs_YT_to_Pick,
#         arcs_Pick_to_Drop,
#         arcs_Drop_to_Pick,
#         arcs_Drop_to_Sink,
#         arcs_YT_to_Sink,
#         now_count
#     )
