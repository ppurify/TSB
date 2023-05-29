import numpy as np
import pandas as pd

import make_arc
import network_LP_final
import route_algorithm as ra

def main():
    # Parameter
    YT_locations = {0 : (4,2)}
    Job_locations = {0 : [(2,4), (5,6)], 1 : [(4,2), (8,0)]}
    number_of_final_route = 3
    alpha1 = 0.4
    alpha2 = 0.4
    alpha3 = 0.3
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

    grid = np.array([
        [4, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2 ,3, 2, 2, 2, 2, 2, 4]
    ])
    ra.set_grid(grid)
    now_count = np.zeros((len(grid), len(grid[0])))

    number_of_YT = len(YT_locations)
    number_of_Job = len(Job_locations)

    # # 스케줄링 대상 YT 생성
    # for i in range(number_of_YT):
    #     YT_location = None
    #     while YT_location is None or grid[YT_location] == -1:
    #         YT_location = (np.random.randint(9), np.random.randint(7))
    #     YT_locations[i] = YT_location
        
    # # 스케줄링 대상 작업 생성
    # for j in range(number_of_job):
    #     Pick_location = None
    #     Drop_location = None
    #     while Pick_location is None or grid[Pick_location] == -1 or Drop_location is None or grid[Drop_location] == -1 or Pick_location == Drop_location:
    #         Pick_location = (np.random.randint(9), np.random.randint(7))
    #         Drop_location = (np.random.randint(9), np.random.randint(7))
    #     Job_locations[j] = [Pick_location, Drop_location]

    # Create arcs
    arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count = make_arc.create_arcs(
        YT_locations=YT_locations,
        Job_locations=Job_locations,
        number_of_final_route=number_of_final_route,
        alpha1=alpha1,
        alpha2=alpha2,
        alpha3=alpha3,
        grid=grid,
        prev_count=prev_count,
        now_count=now_count
    )

    all_arcs = arcs_YT_to_Pick + arcs_Pick_to_Drop + arcs_Drop_to_Pick + arcs_Drop_to_Sink + arcs_YT_to_Sink

    # Run network_LP_final
    objective_value, activated_arcs = network_LP_final.solve(all_arcs, number_of_YT, number_of_Job)
    
    # print('objective_value: ', objective_value)
    # print('activated_arcs: ', activated_arcs)



    # 각 YT들이 어떤 경로로 

    # 1. activated_arcs에서 작업을 수행하는 YT들의 index를 추출
    for i in range(len(activated_arcs)):
        








    # tile_size = 75
    # length_og_grid = len(grid)-1
    # # Create an empty DataFrame to store the route points
    # df = pd.DataFrame(columns=['Route', 'x', 'y', 'z'])

    # # Traverse all_arcs and extract route points
    # for i, arc in enumerate(activated_arcs):
    #     # sink로 가는 arc는 제외
    #     if len(arc.path) == 0:
    #         continue
    #     else:
    #         route_points = arc.path
            
    #         # Add route points to the DataFrame
    #         # 1. unity 맵 크기에 맞추기 위해 tile_size만큼 확대
    #         # 2. 파이썬의 리스트인덱싱 순서와 유니티 상에서 구현한 맵의 인덱싱이 달라서, x축 대칭으로 맞춰줌
    #         # 3. 한 YT가 여러 작업을 하는 경우는, 해당 패스들을 모두 이어서 하나의 Route로 df에 append
    #         for j, point in enumerate(route_points):
    #             x = (length_og_grid - point[0]) * tile_size  # x축 대칭
    #             y = 0
    #             z = point[1] * tile_size
    #             df = df.append({'Route': i, 'x': x, 'y': y, 'z': z}, ignore_index=True)

    # # Save the DataFrame to a CSV file
    # df.to_csv('Routepoints.csv', index=False)

    # YT_traversing_route = {}
    # # activated_arcs를 순회하며, 출발지 arc.i와 도착지 arc.j가 같은 아크들의 path를 하나의 route로 합쳐서 저장
    # def merge_path(activated_arcs):
    #     # key : YT 번호, value : YT가 이동하는 path
    #     merged_paths = {}
    #     for a in range(len(activated_arcs)):
    #         for b in range(len(activated_arcs)):
    #             if activated_arcs[a].j == activated_arcs[b].i:
    #                 # activated_arcs[a]와 activated_arcs[b]의 path 합칠 때, 중복되는 출발좌표와 도착좌표 제거
    #                 merged_path += activated_arcs[a].path + activated_arcs[b].path[1:]
                    
if __name__ == "__main__":
    main()