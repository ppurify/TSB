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
    
    
    number_of_YT = 40
    number_of_Job = 40
    filename_Truck = 'now_Truck_40_LP_70_20_10_with_30_shortest.csv'
    filename_RoutePoints = 'now_RoutePoints_40_LP_70_20_10_with_30_shortest.csv'

    # YT_locations = {0: (2, 7)}
    # Job_locations = {0: [(0, 25), (6, 25)]}
    
    YT_locations = {0: (6, 27), 1: (8, 27), 2: (4, 27), 3: (0, 17), 4: (4, 17), 5: (8, 27), 6: (4, 17), 7: (2, 17), 8: (8, 17), 9: (6, 27), 10: (4, 17), 11: (8, 27), 12: (0, 27), 13: (6, 27), 14: (8, 7), 15: (4, 27), 16: (4, 7), 17: (0, 27), 18: (8, 27), 19: (4, 27), 20: (6, 7), 21: (4, 7), 22: (4, 27), 23: (0, 27), 24: (2, 17), 25: (2, 27), 26: (8, 7), 27: (0, 7), 28: (8, 17), 29: (0, 7), 30: (8, 17), 31: (2, 17), 32: (4, 27), 33: (8, 27), 34: (2, 27), 35: (4, 17), 36: (2, 27), 37: (8, 27), 38: (0, 7), 39: (0, 17)}
    Job_locations = {0: [(2, 15), (0, 5)], 1: [(6, 25), (0, 25)], 2: [(4, 25), (0, 25)], 3: [(0, 15), (8, 5)], 4: [(8, 25), (0, 15)], 5: [(6, 15), (0, 5)], 6: [(0, 5), (6, 15)], 7: [(4, 15), (0, 25)], 8: [(8, 5), (0, 15)], 9: [(6, 5), (0, 15)], 10: [(0, 25), (8, 15)], 11: [(2, 25), (0, 15)], 12: [(0, 15), (2, 25)], 13: [(2, 5), (0, 15)], 14: [(0, 5), (2, 25)], 15: [(0, 15), (8, 25)], 16: [(4, 15), (0, 25)], 17: [(4, 5), (0, 15)], 18: [(2, 5), (0, 25)], 19: [(0, 15), (4, 5)], 20: [(0, 5), (6, 5)], 21: [(2, 5), (0, 15)], 22: [(2, 15), (0, 25)], 23: [(0, 5), (4, 25)], 24: [(0, 5), (6, 15)], 25: [(0, 25), (8, 25)], 26: [(0, 15), (8, 25)], 27: [(0, 5), (2, 5)], 28: [(2, 25), (0, 5)], 29: [(2, 25), (0, 25)], 30: [(4, 15), (0, 15)], 31: [(2, 5), (0, 15)], 32: [(2, 25), (0, 15)], 33: [(0, 15), (8, 25)], 34: [(4, 25), (0, 5)], 35: [(6, 25), (0, 15)], 36: [(0, 5), (6, 15)], 37: [(6, 25), (0, 15)], 38: [(4, 25), (0, 5)], 39: [(0, 25), (8, 5)]}


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
    alpha1 = 70  # prev counter
    alpha2 = 20  # now counter
    alpha3 = 10 # distance

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