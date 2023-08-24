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
    
    
    number_of_YT = 1
    number_of_Job = 1
    filename_Truck = 'now_Truck_1_LP_40_50_10_with_70_shortest.csv'
    filename_RoutePoints = 'now_RoutePoints_1_LP_40_50_10_with_70_shortest.csv'

    YT_locations = {0: (2, 7)}
    Job_locations = {0: [(0, 25), (6, 25)]}
    
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
    alpha1 = 40  # prev counter
    alpha2 = 50  # now counter
    alpha3 = 10 # distance

    # prev_count : t-1시점의 활성화된 A2 + A3의 누적 path정보
    # prev_count = np.zeros((len(grid), len(grid[0])))
    prev_count = np.array([[11, 11, 11, 11, 11, 34, 29, 29, 29, 29, 36, 21, 21, 21,
  21, 29, 22, 22, 22, 22, 40, 29, 29, 29, 29, 32,  8,  8,
   8,  8,  8],
 [11,  0,  0,  0,  0,  0,  0,  0,  0,  0, 22,  0,  0,  0,
   0,  0,  0,  0,  0,  0, 29,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  8],
 [11,  3,  3,  3,  3,  4,  1,  1,  1,  1, 23,  4,  4,  4,
   4,  7,  6,  6,  6,  6, 31,  3,  3,  3,  3,  4,  1,  1,
   1,  1,  8],
 [ 8,  0,  0,  0,  0,  0,  0,  0,  0,  0, 19,  0,  0,  0,
   0,  0,  0,  0,  0,  0, 24,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  7],
 [ 8,  6,  6,  6,  6,  9,  3,  3,  3,  3, 20,  5,  5,  5,
   5,  7,  3,  3,  3,  3, 24,  2,  2,  2,  2,  5,  3,  3,
   3,  3,  7],
 [ 2,  0,  0,  0,  0,  0,  0,  0,  0,  0, 13,  0,  0,  0,
   0,  0,  0,  0,  0,  0, 19,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  4],
 [ 2,  2,  2,  2,  2,  4,  2,  2,  2,  2, 14,  4,  4,  4,
   4,  9,  7,  7,  7,  7, 20,  7,  7,  7,  7, 10,  3,  3,
   3,  3,  4],
 [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  9,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  7,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  1],
 [ 0,  0,  0,  0,  0,  4,  4,  4,  4,  4, 11,  9,  9,  9,
   9, 12,  8,  8,  8,  8, 10,  5,  5,  5,  5,  6,  1,  1,
   1,  1,  1]])
    
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