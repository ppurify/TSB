import csv
import os

def create_csv(activated_arcs, number_of_YT, grid, filename_Truck, filename_RoutePoints):
    # Traversing_info : 각 YT들이 어떤 노드를 거치는지 저장하는 dictionary
    Traversing_info = {tuple(['YT', i]): [] for i in range(number_of_YT)}

    # activated_arcs 순회하며 출발지가 YT인 아크들을 Traversing_info에 저장
    for arc in activated_arcs:
        if arc.i[0] == 'YT':
            Traversing_info[tuple(arc.i)].append(arc)

    # Traversing_info와 activated_arcs를 순회하며 한 YT가 수행하는 경로를 노드 단위로 완성
    for i in range(number_of_YT):
        while Traversing_info[tuple(['YT', i])][-1].j[0] != 'Sink':
            arc_j = Traversing_info[tuple(['YT', i])][-1].j
            next_arc = next((arc for arc in activated_arcs if arc.i == arc_j), None)
            if next_arc:
                Traversing_info[tuple(['YT', i])].append(next_arc)
            else:
                break

    # YT_traverse_path : 각 YT들이 거치는 경로의 좌표정보를 저장하는 dictionary
        YT_traverse_path = {}

        for key, value in Traversing_info.items():
            path = []
            prev_node = None

            for arc in value:
                # sink로 가는 arc는 제외
                if arc.j == ['Sink']:
                    continue

                if prev_node is None:
                    path.extend(arc.path)
                else:
                    # path를 이어붙일때는 아크 간의 겹치는 좌표 한칸은 제거
                    path.extend(arc.path[1:])

                prev_node = arc.j

            YT_traverse_path[key] = path

    # Trucks.csv : 각 YT들이 거치는 경로, pick, drop station정보를 저장
    tile_size = 25
    Trucks = [['Truck_id', 'Route_id', 'Path_length', 'Completion_Time_alone', 'Pick_station', 'Drop_station']]

    # Iterate over Traversing_info
    for key, value in Traversing_info.items():
        if len(value) != 1:
            temp_list = []
            # Iterate over arcs in the value list
            for arc in value:
                if arc.i[0] == 'YT':
                    temp_list.extend([arc.i[1], arc.i[1]])
                    # Path_length, Completione_Time_alone 추가
                    temp_list.append(len(YT_traverse_path[key]))
                    temp_list.append(len(YT_traverse_path[key]) * 1.7921759583979195 + 14.381676327377548)                

                if arc.i[0] == 'Pick':
                    x = arc.path[0][1] * tile_size
                    z = (len(grid) - 1 - arc.path[0][0]) * tile_size
                    temp_list.append((x, 0, z))

                if arc.j[0] == 'Drop':
                    x = arc.path[-1][1] * tile_size
                    z = (len(grid) - 1 - arc.path[-1][0]) * tile_size
                    temp_list.append((x, 0, z))

            Trucks.append(temp_list)

    # Write the Trucks list to a CSV file
    filename = filename_Truck
    
    # if directory does not exist, create one
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(Trucks)


    # 2. RoutePoints.csv
    RoutePoints = {
        'Route_id': [],
        'x': [],
        'y': [],
        'z': []
    }

    for key, value in YT_traverse_path.items():
        if value:
            for point in value:
                RoutePoints['Route_id'].append(key[1])
                RoutePoints['x'].append(point[1] * tile_size)
                RoutePoints['y'].append(0)
                RoutePoints['z'].append((len(grid) - 1 - point[0]) * tile_size)

    filename = filename_RoutePoints
    header = list(RoutePoints.keys())

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(zip(*RoutePoints.values()))

    return Traversing_info, YT_traverse_path, Trucks, RoutePoints