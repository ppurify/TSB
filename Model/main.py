import numpy as np
import pandas as pd
import csv

import make_arc
import network_LP
import route_algorithm as ra
import make_csv

import make_grid

def main():
    
    # 가로로 3개
    block_num_in_row = 3
    
    block_length = 9
    block_height = 1

    grid_length = 31
    grid_height = 9
    

    grid, _YT_location_col_index, QC_locations, YC_locations = make_grid.Grid(grid_length, grid_height, block_length, block_height, block_num_in_row)
    
    
    number_of_YT = 30
    number_of_Job = 30
    filename_Truck = 'now_Truck_30_shortest_with_30_shortest.csv'
    filename_RoutePoints = 'now_RoutePoints_30_shortest_with_30_shortest.csv'

    # YT_locations = {0: (2, 7)}
    # Job_locations = {0: [(0, 25), (6, 25)]}
    
    YT_locations = {0: (4, 27), 1: (2, 17), 2: (0, 27), 3: (2, 7), 4: (0, 27), 5: (2, 7), 6: (0, 27), 7: (4, 27), 8: (8, 7), 9: (0, 7), 10: (0, 17), 11: (0, 17), 12: (8, 17), 13: (6, 7), 14: (2, 27), 15: (0, 17), 16: (8, 27), 17: (8, 7), 18: (6, 17), 19: (2, 27), 20: (6, 27), 21: (4, 27), 22: (0, 7), 23: (2, 27), 24: (2, 27), 25: (8, 27), 26: (6, 27), 27: (6, 27), 28: (6, 27), 29: (0, 17)}
    Job_locations = {0: [(2, 15), (0, 25)], 1: [(0, 25), (2, 5)], 2: [(0, 5), (4, 15)], 3: [(8, 15), (0, 15)], 4: [(0, 5), (8, 25)], 5: [(0, 25), (4, 15)], 6: [(8, 25), (0, 25)], 7: [(0, 5), (8, 5)], 8: [(0, 5), (4, 25)], 9: [(2, 25), (0, 25)], 10: [(0, 15), (6, 5)], 11: [(0, 25), (8, 15)], 12: [(2, 5), (0, 25)], 13: [(0, 15), (6, 5)], 14: [(0, 5), (4, 15)], 15: [(0, 5), (6, 25)], 16: [(0, 25), (8, 25)], 17: [(4, 5), (0, 5)], 18: 
[(0, 5), (2, 15)], 19: [(0, 25), (2, 15)], 20: [(4, 15), (0, 5)], 21: [(0, 5), (8, 15)], 22: [(6, 5), (0, 5)], 23: [(6, 5), (0, 25)], 24: [(0, 5), (8, 25)], 25: [(8, 5), (0, 5)], 26: [(0, 25), (6, 5)], 27: [(0, 15), (6, 25)], 28: [(0, 15), (4, 5)], 29: [(8, 5), (0, 25)]}
   
    # 스케줄링 대상 YT 생성
    # YT_locations = {}
    # Job_locations = {}

    # # # 임의의 위치에 YT 생성
    # for i in range(number_of_YT):
    #     YT_location = None
    #     while YT_location is None or grid[YT_location] == -1 or YT_location[1] not in _YT_location_col_index:
    #         YT_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #     YT_locations[i] = YT_location

    # for j in range(number_of_Job):
    #     # choice random number 0 or 1
    #     random_num = np.random.randint(2)
        
    #     # 0이면 Outbound => YC -> QC
    #     if random_num == 0:
    #         Pick_location = (YC_locations[np.random.randint(len(YC_locations))])
    #         Drop_location = (QC_locations[np.random.randint(len(QC_locations))])
    #     # 1이면 Inbound => QC -> YC
    #     else:
    #         Pick_location = (QC_locations[np.random.randint(len(QC_locations))])
    #         Drop_location = (YC_locations[np.random.randint(len(YC_locations))])
        
    #     Job_locations[j] = [Pick_location, Drop_location]

    # print("YT_locations =", YT_locations)
    # print("Job_locations =", Job_locations)


    number_of_final_route = 3
    alpha1 = 0  # prev counter
    alpha2 = 0  # now counter
    alpha3 = 100 # distance

    # prev_count : t-1시점의 활성화된 A2 + A3의 누적 path정보
    # prev_count = np.zeros((len(grid), len(grid[0])))
    prev_count = np.array([[ 4,  4,  4,  4,  4, 11, 10, 10, 10, 10, 15, 10, 10, 10,
  10, 17, 13, 13, 13, 13, 17,  9,  9,  9,  9, 12,  4,  4,
   4,  4,  4],
 [ 4,  0,  0,  0,  0,  0,  0,  0,  0,  0, 10,  0,  0,  0,
   0,  0,  0,  0,  0,  0, 12,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  4],
 [ 4,  3,  3,  3,  3,  3,  0,  0,  0,  0, 10,  2,  2,  2,
   2,  4,  4,  4,  4,  4, 14,  2,  2,  2,  2,  3,  1,  1,
   1,  1,  4],
 [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  8,  0,  0,  0,
   0,  0,  0,  0,  0,  0, 10,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  3],
 [ 1,  0,  0,  0,  0,  1,  1,  1,  1,  1,  8,  5,  5,  5,
   5,  9,  4,  4,  4,  4, 10,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  3],
 [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  3],
 [ 1,  1,  1,  1,  1,  2,  1,  1,  1,  1,  2,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  6,  2,  2,  2,  2,  3,  1,  1,
   1,  1,  3],
 [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  4,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  2],
 [ 0,  0,  0,  0,  0,  2,  2,  2,  2,  2,  2,  1,  1,  1,
   1,  3,  3,  3,  3,  3,  4,  1,  1,  1,  1,  3,  2,  2,
   2,  2,  2]])
    
    now_count = np.zeros((len(grid), len(grid[0])))

    processing_time = 150
    time_consumed_per_grid = 2.35

    ra.set_grid(grid)
    
 
    # Create arcs
    arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count = make_arc.create_arcs(
        YT_locations=YT_locations, Job_locations=Job_locations, number_of_final_route=number_of_final_route,
        alpha1=alpha1, alpha2=alpha2, alpha3=alpha3,
        grid=grid, prev_count=prev_count, now_count=now_count, time_consumed_per_grid=time_consumed_per_grid, processing_time=processing_time)

    all_arcs = arcs_YT_to_Pick + arcs_Pick_to_Drop + arcs_Drop_to_Pick + arcs_Drop_to_Sink + arcs_YT_to_Sink

    # print('now_count')
    # print(now_count)

    # Run network_LP
    objective_value, activated_arcs = network_LP.solve(all_arcs, number_of_YT, number_of_Job)
    
    # # activated_arcs들의 각 정보 출력
    # for arc in activated_arcs:
    #     print('arc.i : ', arc.i)
    #     print('arc.j : ', arc.j)
    #     print('arc.k : ', arc.k)
    #     print('arc cost : ', arc.cost)
    #     print('arc path : ', arc.path)
    #     print("")
    # print('objective_value: ', objective_value)
    # print('activated_arcs: ', activated_arcs)

    # 다음번 스케줄링을 위한 next_prev_count : A2 + A3의 누적 path정보
    next_prev_count = np.zeros((len(grid), len(grid[0])))
    for arc in activated_arcs:
        # A2이거나 A3이면
        if arc.i[0] == 'Pick':
            # arc.path에 있는 모든 좌표에 1씩 더해줌
            for i in range(len(arc.path)):
                next_prev_count[arc.path[i][0]][arc.path[i][1]] += 1   
        elif arc.i[0] == 'Drop' and arc.j[0] == 'Pick':
            for i in range(len(arc.path)):
                next_prev_count[arc.path[i][0]][arc.path[i][1]] += 1

    # print('next_prev_count')
    # print(next_prev_count)

    # 붙여넣기 쉽게 원소사이에 , 추가하여 출력
    print('next_prev_count')
    print(np.array2string(next_prev_count, separator=', ').replace('.', ''))


    # Create csv file for Unity simulation
    make_csv.create_csv(activated_arcs, number_of_YT, grid, filename_Truck, filename_RoutePoints)


if __name__ == "__main__":
    main()