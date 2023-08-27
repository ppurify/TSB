import numpy as np
import pandas as pd
import csv

import make_arc
import network_LP
import route_algorithm as ra
import make_csv

import make_grid
import random

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

    # filename_Truck = 'prev_Truck_65_LP_0_20_80.csv'
    # filename_RoutePoints = 'prev_RoutePoints_65_LP_0_20_80.csv'
    filename_Truck = 'now_Truck_1_LP_70_20_10_with_prev_Truck_70_LP_0_20_80.csv'
    filename_RoutePoints = 'now_RoutePoints_1_LP_70_20_10_with_prev_Truck_70_LP_0_20_80.csv'
    
    YT_locations = {0: (2, 7)}
    Job_locations = {0: [(0, 25), (6, 25)]}

    # # Assuming you have YC_locations and QC_locations defined
    # YT_locations = {}
    # Job_locations = {}
    
    # # Generate a shuffled list of all possible grid locations
    # possible_locations = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
    # random.shuffle(possible_locations)

    # # Create YT locations
    # for i in range(number_of_YT):
    #     YT_location = None
    #     while YT_location is None or grid[YT_location] == -1 or YT_location[1] not in _YT_location_col_index:
    #         # YT_location = possible_locations[location_index]  # Use the current index
    #         if len(possible_locations) > 0:
    #           YT_location = possible_locations.pop()
    #         else:
    #           # print("No more possible YT locations")
    #           possible_locations = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
    #           random.shuffle(possible_locations)
    #           YT_location = possible_locations.pop()
      
    #     YT_locations[i] = YT_location

    # # Shuffle YC and QC locations for better randomness
    # possible_YC_locations = YC_locations.copy()
    # possible_QC_locations = QC_locations.copy()
    
    # random.shuffle(possible_YC_locations)
    # random.shuffle(possible_QC_locations)
    
    # # Create Job locations
    # for j in range(number_of_Job):
    #     # choice random number 0 or 1
    #     random_num = np.random.randint(2)
        
    #     if(len(possible_YC_locations) > 0):
    #       YC_loc = possible_YC_locations.pop()
        
    #     else:
    #       # print("No more YC locations")
    #       possible_YC_locations = YC_locations.copy()
    #       random.shuffle(possible_YC_locations)
    #       YC_loc = possible_YC_locations.pop()
          
    #     if(len(possible_QC_locations) > 0):
    #       QC_loc = possible_QC_locations.pop()
          
    #     else:
    #       # print("No more QC locations")
    #       possible_QC_locations = QC_locations.copy()
    #       random.shuffle(possible_QC_locations)
    #       QC_loc = possible_QC_locations.pop()
          
    #     # 0 means Outbound => YC -> QC
    #     if random_num == 0:
    #         Pick_location = YC_loc  # Use random.choice for better randomness
    #         Drop_location = QC_loc
    #     # 1 means Inbound => QC -> YC
    #     else:
    #         Pick_location = QC_loc
    #         Drop_location = YC_loc
        
    #     Job_locations[j] = [Pick_location, Drop_location]

    # print("YT_locations =", YT_locations)
    # print("Job_locations =", Job_locations)

    number_of_final_route = 3
    alpha1 = 70  # prev counter
    alpha2 = 20  # now counter
    alpha3 = 10 # distance

    # prev_count : t-1시점의 활성화된 A2 + A3의 누적 path정보
    # prev_count = np.zeros((len(grid), len(grid[0])))
    prev_count = np.array([[18, 18, 18, 18, 18, 33, 25, 25, 25, 25, 35, 24, 24, 24,
  24, 35, 23, 23, 23, 23, 32, 20, 20, 20, 20, 27, 10, 10,
  10, 10, 10],
 [18,  0,  0,  0,  0,  0,  0,  0,  0,  0, 21,  0,  0,  0,
   0,  0,  0,  0,  0,  0, 21,  0,  0,  0,  0,  0,  0,  0,
   0,  0, 10],
 [18,  4,  4,  4,  4,  6,  2,  2,  2,  2, 21,  5,  5,  5,
   5,  7,  3,  3,  3,  3, 22,  4,  4,  4,  4,  6,  2,  2,
   2,  2, 10],
 [14,  0,  0,  0,  0,  0,  0,  0,  0,  0, 14,  0,  0,  0,
   0,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  8],
 [14,  5,  5,  5,  5,  6,  1,  1,  1,  1, 14,  4,  4,  4,
   4,  9,  8,  8,  8,  8, 19,  3,  3,  3,  3,  6,  3,  3,
   3,  3,  8],
 [ 9,  0,  0,  0,  0,  0,  0,  0,  0,  0,  9,  0,  0,  0,
   0,  0,  0,  0,  0,  0, 11,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  5],
 [ 9,  4,  4,  4,  4,  6,  2,  2,  2,  2,  9,  3,  3,  3,
   3,  5,  2,  2,  2,  2, 11,  3,  3,  3,  3,  6,  3,  3,
   3,  3,  5],
 [ 5,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  2],
 [ 5,  5,  5,  5,  5,  6,  1,  1,  1,  1,  4,  3,  3,  3,
   3,  7,  6,  6,  6,  6,  8,  4,  4,  4,  4,  6,  2,  2,
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

    # 붙여넣기 쉽게 원소사이에 , 추가하여 출력
    print('next_prev_count')
    print(np.array2string(next_prev_count, separator=', ').replace('.', ''))


    # Create csv file for Unity simulation
    make_csv.create_csv(activated_arcs, number_of_YT, grid, filename_Truck, filename_RoutePoints)


if __name__ == "__main__":
    main()