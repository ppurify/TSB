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

    
    prev_YT_counter = 25
    prev_Job_counter = 25
    
    now_YT_counter = 25
    now_Job_counter = 25
    
    if(now_YT_counter == 0):
        number_of_YT = prev_YT_counter
        number_of_Job = prev_Job_counter
        
    else:
        number_of_YT = now_YT_counter
        number_of_Job = now_Job_counter
    
    
    alpha1 = 80  # prev counter
    alpha2 = 10  # now counter
    alpha3 = 10 # distance
    
    folder_path = 'Simulation/Assets/Data/Congestion'
    
    YT_locations = {0: (8, 27), 1: (2, 7), 2: (6, 17), 3: (4, 7), 4: (0, 7), 5: (4, 27), 6: (2, 17), 7: (2, 27), 8: (0, 17), 9: (4, 17), 10: (6, 27), 11: (8, 7), 12: (8, 17), 13: (6, 7), 14: (0, 27), 15: (0, 27), 16: (8, 27), 17: (4, 27), 18: (4, 7), 19: (4, 17), 20: (2, 27), 21: (6, 17), 22: (2, 17), 23: (6, 27), 24: (0, 7)}
    Job_locations = {0: [(0, 15), (6, 15)], 1: [(0, 5), (4, 25)], 2: [(8, 5), (0, 25)], 3: [(0, 5), (2, 5)], 4: [(0, 15), (2, 25)], 5: [(0, 25), (4, 15)], 6: [(8, 25), (0, 5)], 7: [(6, 5), (0, 25)], 8: [(4, 5), (0, 15)], 9: [(0, 5), (6, 25)], 10: [(0, 25), (8, 15)], 11: [(2, 15), (0, 15)], 12: [(6, 15), (0, 5)], 13: [(2, 15), (0, 25)], 14: [(0, 15), (6, 5)], 15: [(0, 25), (8, 15)], 16: [(2, 25), (0, 15)], 17: [(0, 5), (8, 25)], 18: [(2, 5), (0, 25)], 19: [(0, 15), (4, 5)], 20: [(8, 5), (0, 5)], 21: [(0, 5), (4, 25)], 22: [(4, 15), (0, 15)], 23: [(0, 25), (6, 25)], 24: [(0, 15), (2, 5)]}

    # # Assuming you have YC_locations and QC_locations defined
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
    

    # prev_count : t-1시점의 활성화된 A2 + A3의 누적 path정보
    # prev_count = np.zeros((len(grid), len(grid[0])))
    prev_count = np.array([[ 7,  7,  7,  7,  7, 12,  9,  9,  9,  9, 12,  9,  9,  9,
   9, 13,  8,  8,  8,  8, 11,  7,  7,  7,  7, 10,  5,  5,
   5,  5,  5],
 [ 7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  6,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  7,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  5],
 [ 7,  2,  2,  2,  2,  3,  1,  1,  1,  1,  6,  2,  2,  2,
   2,  3,  2,  2,  2,  2,  8,  1,  1,  1,  1,  2,  1,  1,
   1,  1,  5],
 [ 5,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  4],
 [ 5,  2,  2,  2,  2,  2,  0,  0,  0,  0,  3,  0,  0,  0,
   0,  2,  2,  2,  2,  2,  6,  1,  1,  1,  1,  2,  1,  1,
   1,  1,  4],
 [ 3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  3],
 [ 3,  1,  1,  1,  1,  2,  1,  1,  1,  1,  3,  1,  1,  1,
   1,  2,  1,  1,  1,  1,  4,  1,  1,  1,  1,  3,  3,  3,
   3,  3,  3],
 [ 2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  0],
 [ 2,  2,  2,  2,  2,  2,  0,  0,  0,  0,  1,  1,  1,  1,
   1,  3,  3,  3,  3,  3,  4,  2,  2,  2,  2,  2,  0,  0,
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

    if now_YT_counter == 0:
        truck_filename = f'prev_{prev_YT_counter}/prev_Truck_{prev_YT_counter}'
        route_filename = f'prev_{prev_YT_counter}/prev_RoutePoints_{prev_YT_counter}'
    else:
        truck_filename = f'prev_{prev_YT_counter}_now_{now_YT_counter}/now_Truck_{now_YT_counter}_with_prev_Truck_{prev_YT_counter}'
        route_filename = f'prev_{prev_YT_counter}_now_{now_YT_counter}/now_RoutePoints_{now_YT_counter}_with_prev_RoutePoints_{prev_YT_counter}'
    
    filename_Truck = f'{folder_path}/{truck_filename}_LP_{alpha1}_{alpha2}_{alpha3}.csv'
    filename_RoutePoints = f'{folder_path}/{route_filename}_LP_{alpha1}_{alpha2}_{alpha3}.csv'
        
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