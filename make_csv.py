import csv

def create_csv(activated_arcs, number_of_YT, grid):
    # 각 YT들이 어떤 경로로 이동하는지 저장하는 dictionary
    YT_traversing_arc = {}

    arcs_for_YT_traverse = activated_arcs.copy()

    # 딕셔너리에 key로 YT들 먼저 추가
    for _ in range(number_of_YT):
        for arc in arcs_for_YT_traverse:
        # 만약 arc의 i에 YT가 포함되고 아직 YT_traversing_arc에 추가되지 않았다면
            if (arc.i == ['YT', _]) and tuple(arc.i) not in YT_traversing_arc.keys():
                YT_traversing_arc[tuple(arc.i)] = [arc]
                arcs_for_YT_traverse.remove(arc)
                break


    # arcs_for_YT_traverse에 원소가 남아있는 동안
    while arcs_for_YT_traverse != []:
        for arc in arcs_for_YT_traverse:
                # YT_traversing_arc의 모든 value를 돌면서
            for values in YT_traversing_arc.values():
                for value in values:
                    # 만약 arc의 i가 value의 j와 같다면
                    if arc.i == value.j:
                        # 해당 value 뒤에 해당 arc를 추가
                        values.append(arc)
                        arcs_for_YT_traverse.remove(arc)
                        break

    # for v in YT_traversing_arc.values():
    #     print('')
    #     for arc in v:
    #         print(arc.i, arc.j)

    YT_traverse_path = {}

    # print('YT_traversing_arc: ')
    # for key, value in YT_traversing_arc.items():
    #     print(key, value)

    # YT_traverse_path
    # 1. YT_traversing_arc을 순회하며 key값은 그대로 가져오고 value값은 각 arc의 path를 이어붙인다.
    # 2. path를 이어붙일때는 아크 간의 겹치는 좌표 한칸은 제거한다.
    # 3. 중간중간 pick 혹은 drop 목적지 좌표를 pick_station 혹은 drop_station으로 따로 저장해준다.
    # 4. sink로 가는 arc는 제외한다.

    for key, value in YT_traversing_arc.items():
        path = []

        for arc in value:
            # sink로 가는 arc는 제외한다.
            if arc.j == ['Sink']:
                continue          
            # 만약 path가 비어있으면
            if path == []:
                path.extend(arc.path)
            else:
                # path의 마지막 원소와 arc의 첫번째 원소가 겹치는지 확인
                if path[-1] == arc.path[0]:
                    path.extend(arc.path[1:])
                else:
                    path.extend(arc.path)

        YT_traverse_path[key] = path



    # print('YT_traverse_path: ')
    # for key, value in YT_traverse_path.items():
    #     print(key, value)

    # Unity simulation에 넘겨줄 csv파일 생성
    # 1. Trucks.csv : Truck의 id, Route id, pick station, drop station, ...
    # 2. RoutePoints.csv : Route id, x, y, z
        
    tile_size = 75

    # 1. Trucks.csv
    # station에 좌표를 입력할때는 유니티 규격에 맞게 좌표를 수정해준다
    Trucks = [['Truck_id', 'Route_id', 'Pick_station', 'Drop_station']]

    for key, value in YT_traversing_arc.items():
        # print('key: ', key)
        # print('value: ', value)
        if len(value) != 1:
            # 해당 경로가 곧바로 sink노드로 가는 경로가 아니라면
            temp_list = []
            for arc in value:
                # print('i : ', arc.i, 'j : ', arc.j)
                # arc의 i가 YT라면
                if arc.i[0] == 'YT':
                    temp_list.append(arc.i[1])
                    temp_list.append(arc.i[1])

                # arc의 i가 Pick이라면
                if arc.i[0] == 'Pick':
                    # 유니티 규격에 맞게 좌표를 수정
                    x = arc.path[0][1]*tile_size
                    y = 0
                    z = ((len(grid)-1) - arc.path[0][0])*tile_size
                    temp_list.append((x, y, z))

                # arc의 j가 Drop이라면
                if arc.j[0] == 'Drop':
                    # 유니티 규격에 맞게 좌표를 수정
                    x = arc.path[-1][1]*tile_size
                    y = 0
                    z = ((len(grid)-1) - arc.path[-1][0])*tile_size
                    temp_list.append((x, y, z))

            Trucks.append(temp_list)
        
    filename = 'Trucks.csv'
    # 이중 리스트를 CSV 파일로 저장
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # 이중 리스트의 각 행을 CSV 파일에 씁니다.
        for row in Trucks:
            writer.writerow(row)


    # 2. RoutePoints.csv
    # YT_traverse_path를 순회하며 각 좌표를 csv파일에 저장한다.

    RoutePoints = {
        'Route_id' : [],
        'x' : [],
        'y' : [],
        'z' : []
    }

    for key, value in YT_traverse_path.items():
        # 해당 key의 value가 비어있지않다면
        if value != []:
            # x축 대칭, 가로세로 75배 확대
            for point in value:
                RoutePoints['Route_id'].append(key[1])
                RoutePoints['x'].append(point[1]*tile_size)
                RoutePoints['y'].append(0)
                RoutePoints['z'].append(((len(grid)-1) - point[0])*tile_size)

    filename = 'RoutePoints.csv'

    # 딕셔너리의 키를 CSV 파일의 헤더로 사용합니다.
    header = list(RoutePoints.keys())

    # CSV 파일을 쓰기 모드로 엽니다.
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # 헤더를 CSV 파일에 씁니다.
        writer.writerow(header)
        
        # 딕셔너리의 값을 한 줄씩 CSV 파일에 씁니다.
        for row in zip(*RoutePoints.values()):
            writer.writerow(row)

    return YT_traversing_arc, YT_traverse_path, Trucks, RoutePoints