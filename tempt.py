# !!! 현재는 YT->Pick 아크들 먼저 길이순 오름차순 정렬하여 cost 계산 후 Pick->Drop 아크들 길이순 오름차순 정렬하여 cost 계산하는 방식으로 진행
# !!! 따라서 앞부분 아크들(YT->Pick, Pick->Drop, Drop->다른 Pick 순서)이 우선적으로 cost계산되어 더 높은 우선순위로 인식됨
def sort_and_cost(arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, prev_count, now_count, alpha1, alpha2, alpha3):
    def calculate_cost(arcs, alpha1, alpha2, alpha3):
        for arc in arcs:
            arc.cost = get_cost(prev_count, now_count, arc.path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)
            for node in arc.path:
                now_count[node] += 1
    # A1
    arcs_YT_to_Pick.sort(key=lambda x: len(x.path))
    calculate_cost(arcs_YT_to_Pick, alpha1, alpha2, alpha3)
    # A2
    arcs_Pick_to_Drop.sort(key=lambda x: len(x.path))
    calculate_cost(arcs_Pick_to_Drop, 0, alpha2, alpha3)
    # A3
    arcs_Drop_to_Pick.sort(key=lambda x: len(x.path))
    calculate_cost(arcs_Drop_to_Pick, 0, alpha2, alpha3)
    # A4
    for arc in arcs_Drop_to_Sink:
        arc.cost = 0
    # A5
    for arc in arcs_YT_to_Sink:
        arc.cost = 0

    return arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count


# 아크생성, penalty 계산, cost 계산
def create_arcs(YT_locations, Job_locations, number_of_final_route, alpha1, alpha2, alpha3, grid, prev_count, now_count):
    arcs_YT_to_Pick = []
    arcs_Pick_to_Drop = []
    arcs_Drop_to_Pick = []
    arcs_Drop_to_Sink = []
    arcs_YT_to_Sink = []

    now_index = 0


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
                final_route_YT_to_Pick = penalty(prev_count, route_YT_to_Pick, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
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
            final_route_Pick_to_Drop = penalty(prev_count, route_Pick_to_Drop, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
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
                    final_route_Drop_to_Pick = penalty(prev_count, route_Drop_to_Pick, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
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

    sort_and_cost(arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, prev_count, now_count, alpha1, alpha2, alpha3)

    return (arcs_YT_to_Pick,
            arcs_Pick_to_Drop,
            arcs_Drop_to_Pick,
            arcs_Drop_to_Sink,
            arcs_YT_to_Sink,
            now_count)





























def create_arcs_combined(YT_locations, Job_locations, number_of_final_route, alpha1, alpha2, alpha3, grid, prev_count, now_count):
    arcs_YT_to_Pick = []
    arcs_Pick_to_Drop = []
    arcs_Drop_to_Pick = []
    arcs_Drop_to_Sink = []
    arcs_YT_to_Sink = []

    now_index = 0

    def calculate_cost(arcs, alpha1, alpha2, alpha3):
        for arc in arcs:
            arc.cost = get_cost(prev_count, now_count, arc.path, alpha1=alpha1, alpha2=alpha2, alpha3=alpha3)
            for node in arc.path:
                now_count[node] += 1

    def create_arc(name, i, j, k, path, cost):
        arc = arcname = arc(i=i, j=j, k=k, path=path, cost=cost, index=now_index)
        now_index += 1
        return arc

    def create_arcs_route(source, destination, arc_list):
        for i in range(len(source)):
            for j in range(len(destination)):
                source_location = source[i]
                destination_location = destination[j][0]

                path = []
                route = []

                # 모든 경우의 경로 탐색
                route = ra.move(source_location, destination_location, grid, path, route)

                # 경로 수가 number_of_final_route개보다 많으면 패널티 함수 통해 number_of_final_route개로 줄이기
                if len(route) > number_of_final_route:
                    final_route = penalty(prev_count, route, number_of_final_route, alpha1=alpha1, alpha3=alpha3)
                else:
                    final_route = route

                # 경로 1개당 arc 객체 생성
                for k in range(len(final_route)):
                    arcname = create_arc(name, i, j, k, final_route[k], None)
                    arc_list.append(arcname)

    # 1. YT -> Pick 경로, 아크 생성
    create_arcs_route(YT_locations, Job_locations, arcs_YT_to_Pick)

    # 2. Pick -> Drop 경로, 아크 생성
    create_arcs_route(Job_locations, Job_locations, arcs_Pick_to_Drop)

    # 3. Drop -> 다른 Job의 Pick 경로, 아크 생성
    create_arcs_route(Job_locations, Job_locations, arcs_Drop_to_Pick)

    # 4. Drop -> Sink 아크 생성
    for i in range(len(Job_locations)):
        arcname = create_arc('Drop_to_Sink', ['Drop', i], ['Sink'], 0, [], 0)
        arcs_Drop_to_Sink.append(arcname)

    # 5. YT -> Sink 아크 생성
    for i in range(len(YT_locations)):
        arcname = create_arc('YT_to_Sink', ['YT', i], ['Sink'], 0, [], 0)
        arcs_YT_to_Sink.append(arcname)

    calculate_cost(arcs_YT_to_Pick, alpha1, alpha2, alpha3)
    calculate_cost(arcs_Pick_to_Drop, 0, alpha2, alpha3)
    calculate_cost(arcs_Drop_to_Pick, 0, alpha2, alpha3)

    return (
        arcs_YT_to_Pick,
        arcs_Pick_to_Drop,
        arcs_Drop_to_Pick,
        arcs_Drop_to_Sink,
        arcs_YT_to_Sink,
        now_count
    )
