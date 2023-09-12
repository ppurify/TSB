import numpy as np
import os
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





    number_of_YT = 30
    number_of_Job = 30
    filename_Truck = 'Simulation/Assets/Data/Congestion/prev_25_now_30/now_Truck_30_with_prev_Truck_25_LP_10_80_10.csv'
    filename_RoutePoints = 'Simulation/Assets/Data/Congestion/prev_25_now_30/now_RoutePoints_30_with_prev_RoutePoints_25_LP_10_80_10.csv'
    
    
    YT_locations = {0: (2, 27), 1: (6, 27), 2: (8, 27), 3: (2, 7), 4: (0, 17), 5: (6, 17), 6: (6, 7), 7: (0, 27), 8: (8, 7), 9: (2, 17), 10: (4, 17), 11: (4, 7), 12: (0, 7), 13: (8, 17), 14: (4, 27), 15: (2, 17), 16: (4, 17), 17: (6, 27), 18: (0, 17), 19: (2, 27), 20: (2, 7), 21: (0, 27), 22: (8, 7), 23: (0, 7), 24: (8, 27), 25: (4, 27), 26: (6, 17), 27: (6, 7), 28: (4, 7), 29: (8, 17)}
    Job_locations = {0: [(0, 25), (2, 15)], 1: [(0, 15), (8, 25)], 2: [(0, 5), (8, 15)], 3: [(8, 5), (0, 25)], 4: [(2, 25), (0, 5)], 5: [(0, 15), (6, 5)], 6: [(4, 25), (0, 25)], 7: [(4, 15), (0, 15)], 8: [(4, 5), (0, 5)], 9: [(6, 25), (0, 5)], 10: [(0, 15), (2, 5)], 11: [(0, 25), (6, 15)], 12: [(4, 25), (0, 15)], 13: [(0, 25), (8, 15)], 14: [(0, 5), (6, 25)], 15: [(8, 5), (0, 5)], 16: [(6, 15), (0, 25)], 17: [(4, 15), (0, 15)], 18: [(2, 15), (0, 5)], 19: [(2, 5), (0, 25)], 20: [(6, 5), (0, 15)], 21: [(2, 25), (0, 15)], 22: [(0, 25), (4, 5)], 23: [(8, 25), (0, 5)], 24: [(8, 25), (0, 15)], 25: [(0, 25), (2, 25)], 26: [(4, 15), (0, 5)], 27: [(0, 25), (6, 5)], 28: [(0, 5), (4, 25)], 29: [(0, 15), (6, 15)]}

    # Assuming you have YC_locations and QC_locations defined
    # YT_locations = {}
    # Job_locations = {}
    
    # # Generate a shuffled list of all possible grid locations
    # possible_locations = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
    # random.shuffle(possible_locations)
    # # location_index = 0  # Initialize the index

    # # Create YT locations
    # for i in range(number_of_YT):
    #     YT_location = None
    #     while YT_location is None or grid[YT_location] == -1 or YT_location[1] not in _YT_location_col_index:
    #         # YT_location = possible_locations[location_index]  # Use the current index
    #         if len(possible_locations) > 0:
    #             YT_location = possible_locations.pop()
    #         else:
    #             # print("No more possible YT locations")
    #             possible_locations = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
    #             random.shuffle(possible_locations)
    #             YT_location = possible_locations.pop()
        
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
    #         YC_loc = possible_YC_locations.pop()
        
    #     else:
    #         # print("No more YC locations")
    #         possible_YC_locations = YC_locations.copy()
    #         random.shuffle(possible_YC_locations)
    #         YC_loc = possible_YC_locations.pop()
            
    #     if(len(possible_QC_locations) > 0):
    #         QC_loc = possible_QC_locations.pop()
            
    #     else:
    #         # print("No more QC locations")
    #         possible_QC_locations = QC_locations.copy()
    #         random.shuffle(possible_QC_locations)
    #         QC_loc = possible_QC_locations.pop()
            
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
    alpha1 = 10  # prev counter
    alpha2 = 80  # now counter
    alpha3 = 10 # distance

    # prev_count : t-1시점의 활성화된 A2 + A3의 누적 path정보
    # prev_count = np.zeros((len(grid), len(grid[0])))
    prev_count = np.array([[ 7,  7,  7,  7,  7, 12,  9,  9,  9,  9, 13, 10, 10, 10,
  10, 13,  7,  7,  7,  7, 10,  7,  7,  7,  7, 10,  5,  5,
   5,  5,  5],
 [ 7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  5],
 [ 7,  2,  2,  2,  2,  3,  1,  1,  1,  1,  7,  2,  2,  2,
   2,  3,  2,  2,  2,  2,  7,  1,  1,  1,  1,  2,  1,  1,
   1,  1,  5],
 [ 5,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  4],
 [ 5,  2,  2,  2,  2,  2,  0,  0,  0,  0,  4,  0,  0,  0,
   0,  2,  2,  2,  2,  2,  5,  1,  1,  1,  1,  2,  1,  1,
   1,  1,  4],
 [ 3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  3],
 [ 3,  1,  1,  1,  1,  2,  1,  1,  1,  1,  4,  1,  1,  1,
   1,  2,  1,  1,  1,  1,  3,  1,  1,  1,  1,  3,  3,  3,
   3,  3,  3],
 [ 2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  0],
 [ 2,  2,  2,  2,  2,  2,  0,  0,  0,  0,  2,  2,  2,  2,
   2,  3,  2,  2,  2,  2,  3,  2,  2,  2,  2,  2,  0,  0,
   0,  0,  0]])

    now_count = np.zeros((len(grid), len(grid[0])))

    processing_time = 150
    time_consumed_per_grid = 1

    ra.set_grid(grid)

    # Create arcs
    arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count = make_arc.create_arcs(
        YT_locations=YT_locations, Job_locations=Job_locations, number_of_final_route=number_of_final_route,
        alpha1=alpha1, alpha2=alpha2, alpha3=alpha3,
        grid=grid, prev_count=prev_count, now_count=now_count, time_consumed_per_grid=time_consumed_per_grid, processing_time=processing_time)

    all_arcs = arcs_YT_to_Pick + arcs_Pick_to_Drop + arcs_Drop_to_Pick + arcs_Drop_to_Sink + arcs_YT_to_Sink


    objective_value, activated_arcs = network_LP.solve(all_arcs, number_of_YT, number_of_Job)

    # activated_arcs들의 각 정보 출력
    # print('activated_arcs')
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


  # Heatmap을 위한 grid_for_visualization
  # grid_for_visualization = np.zeros((len(grid), len(grid[0])))
  # for arc in activated_arcs:
  #     for i in range(len(arc.path)):
  #         grid_for_visualization[arc.path[i][0]][arc.path[i][1]] += 1

  # print('grid_for_visualization')
  # print(np.array2string(grid_for_visualization, separator=', ').replace('.', ''))


    # Create csv file for Unity simulation/
    make_csv.create_csv(activated_arcs, number_of_YT, grid, filename_Truck, filename_RoutePoints)


    log_file_path =  "Model/Logs/Congestion/" + os.path.basename(filename_Truck) + ".txt"

    with open(log_file_path, 'w') as file:
        file.write("YT_locations = " + str(YT_locations) + "\n")
        file.write("Job_locations = " + str(Job_locations) + "\n")
        file.write("objective_value: " + str(objective_value) + "\n")
        next_prev_count_str = np.array2string(next_prev_count, separator=', ').replace('.', '')
        file.write("next_prev_count: " + next_prev_count_str + "\n")


if __name__ == "__main__":
    main()