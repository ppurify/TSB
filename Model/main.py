import numpy as np

import make_arc
import network_LP
import route_algorithm as ra
import make_csv
import os

import make_grid
import random

def generate_locations(grid, number_of_YT, number_of_Job, _YT_location_col_index, QC_locations, YC_locations):
    # Assuming you have YC_locations and QC_locations defined
    YT_locations = {}
    Job_locations = {}

    # Generate a shuffled list of all possible grid locations
    possible_locations = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
    random.shuffle(possible_locations)
    # location_index = 0  # Initialize the index

    # Create YT locations
    for i in range(number_of_YT):
        YT_location = None
        while YT_location is None or grid[YT_location] == -1 or YT_location[1] not in _YT_location_col_index:
            # YT_location = possible_locations[location_index]  # Use the current index
            if len(possible_locations) > 0:
              YT_location = possible_locations.pop()
            else:
              # print("No more possible YT locations")
              possible_locations = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
              random.shuffle(possible_locations)
              YT_location = possible_locations.pop()

        YT_locations[i] = YT_location

    # Shuffle YC and QC locations for better randomness
    possible_YC_locations = YC_locations.copy()
    possible_QC_locations = QC_locations.copy()

    random.shuffle(possible_YC_locations)
    random.shuffle(possible_QC_locations)

    # Create Job locations
    for j in range(number_of_Job):
        # choice random number 0 or 1
        random_num = np.random.randint(2)

        if(len(possible_YC_locations) > 0):
          YC_loc = possible_YC_locations.pop()

        else:
          # print("No more YC locations")
          possible_YC_locations = YC_locations.copy()
          random.shuffle(possible_YC_locations)
          YC_loc = possible_YC_locations.pop()

        if(len(possible_QC_locations) > 0):
          QC_loc = possible_QC_locations.pop()

        else:
          # print("No more QC locations")
          possible_QC_locations = QC_locations.copy()
          random.shuffle(possible_QC_locations)
          QC_loc = possible_QC_locations.pop()

        # 0 means Outbound => YC -> QC
        if random_num == 0:
            Pick_location = YC_loc  # Use random.choice for better randomness
            Drop_location = QC_loc
        # 1 means Inbound => QC -> YC
        else:
            Pick_location = QC_loc
            Drop_location = YC_loc

        Job_locations[j] = [Pick_location, Drop_location]

    return YT_locations, Job_locations


def main(_grid, _YT_locations, _Job_locations, number_of_YT, number_of_Job, _top_folder_name, time, prev_count, alpha1, alpha2, alpha3, rep):

    if time == 'prev':
      folder_name = f'prev_{number_of_YT}'
    else:
      folder_name = f'now_{number_of_YT}'
    
    # 폴더 없으면 생성
    os.makedirs(f'{_top_folder_name}/{folder_name}', exist_ok=True)
    
    filename_Truck = f'{_top_folder_name}/{folder_name}/{time}_Truck_{number_of_YT}_LP_{alpha1}_{alpha2}_{alpha3}_{rep}rep.csv'
    filename_RoutePoints = f'{_top_folder_name}/{folder_name}/{time}_RoutePoints_{number_of_YT}_LP_{alpha1}_{alpha2}_{alpha3}_{rep}rep.csv'

    number_of_final_route = 3
    now_count = np.zeros((len(_grid), len(_grid[0])))

    processing_time = 150
    time_consumed_per_grid = 1

    ra.set_grid(_grid)

    # Create arcs
    arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count = make_arc.create_arcs(
        YT_locations=_YT_locations, Job_locations=_Job_locations, number_of_final_route=number_of_final_route,
        alpha1=alpha1, alpha2=alpha2, alpha3=alpha3,
        grid=_grid, prev_count=prev_count, now_count=now_count, time_consumed_per_grid=time_consumed_per_grid, processing_time=processing_time)

    all_arcs = arcs_YT_to_Pick + arcs_Pick_to_Drop + \
        arcs_Drop_to_Pick + arcs_Drop_to_Sink + arcs_YT_to_Sink


    objective_value, activated_arcs = network_LP.solve(
        all_arcs, number_of_YT, number_of_Job)
    print('objective_value: ', objective_value)

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

    # Create csv file for Unity simulation/
    make_csv.create_csv(activated_arcs, number_of_YT, _grid, filename_Truck, filename_RoutePoints)

    return next_prev_count


if __name__ == "__main__":

    casename = 'Congestion'
    Prev_number_of_YT = 25
    Prev_number_of_Job = 25
    Now_number_of_YT = 25
    Now_number_of_Job = 25
    
    top_folder_name = f'Simulation/Assets/Data/{casename}/prev_{Prev_number_of_YT}_now_{Now_number_of_YT}'

    # 가로로 3개
    block_num_in_row = 3
    block_length = 9
    block_height = 1
    grid_length = 31
    grid_height = 9
    grid, YT_location_col_index, QC_locations, YC_locations = make_grid.Grid(grid_length, grid_height, block_length, block_height, block_num_in_row)
    
    reps = 1

    alphas = [[0, 80, 70, 60, 50, 40, 30, 20, 10],
              [0, 10, 20, 30, 40, 50, 60, 70, 80],
              [100, 10, 10, 10, 10, 10, 10, 10, 10]]
    
    for rep in range(reps):
      
      prev_YT_locations, prev_Job_locations = generate_locations(grid, Prev_number_of_YT, Prev_number_of_Job, YT_location_col_index, QC_locations, YC_locations)
      print("------- prev \n YT_locations =", prev_YT_locations)
      print("------- prev \n Job_locations =", prev_Job_locations)
      
      now_YT_locations, now_Job_locations = generate_locations(grid, Prev_number_of_YT, Prev_number_of_Job, YT_location_col_index, QC_locations, YC_locations)
      print("------- now \n YT_locations =", now_YT_locations)
      print("------- now \n Job_locations =", now_Job_locations)
      
      for i in range(len(alphas[0])):
        
        alpha1 = alphas[0][i]
        alpha2 = alphas[1][i]
        alpha3 = alphas[2][i]
        
        # Prev
        # prev_count = np.zeros((9, 31),dtype=np.int8)
        prev_count = np.zeros((len(grid), len(grid[0])))

        next_prev_count = main(grid, prev_YT_locations, prev_Job_locations, Prev_number_of_YT, Prev_number_of_Job, top_folder_name, 'prev', prev_count, alpha1, alpha2, alpha3, rep)
        
        main(grid, now_YT_locations, now_Job_locations, Now_number_of_YT, Now_number_of_Job, top_folder_name, 'now', next_prev_count, alpha1, alpha2, alpha3, rep)
        
    # for i in range(len(alphas[0])):
    #     alpha1 = alphas[0][i]
    #     alpha2 = alphas[1][i]
    #     alpha3 = alphas[2][i]
        
    #     for rep in range(reps):
    #         # Prev
    #         # prev_count = np.zeros((9, 31),dtype=np.int8)
    #         prev_count = np.zeros((len(grid), len(grid[0])))
    #         prev_YT_locations, prev_Job_locations = generate_locations(grid, Prev_number_of_YT, Prev_number_of_Job, YT_location_col_index, QC_locations, YC_locations)

    #         print("------- prev \n YT_locations =", prev_YT_locations)
    #         print("------- prev \n Job_locations =", prev_Job_locations)
            
    #         next_prev_count = main(grid, prev_YT_locations, prev_Job_locations, Prev_number_of_YT, Prev_number_of_Job, top_folder_name, 'prev', prev_count, alpha1, alpha2, alpha3, rep)
            
            
    #         # Now
            
    #         now_YT_locations, now_Job_locations = generate_locations(grid, Prev_number_of_YT, Prev_number_of_Job, YT_location_col_index, QC_locations, YC_locations)

    #         print("------- now \n YT_locations =", now_YT_locations)
    #         print("------- now \n Job_locations =", now_Job_locations)
            
    #         prev_count = next_prev_count
    #         main(grid, now_YT_locations, now_Job_locations, Now_number_of_YT, Now_number_of_Job, top_folder_name, 'now', prev_count, alpha1, alpha2, alpha3, rep)