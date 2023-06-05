import numpy as np
import pandas as pd
import csv

import make_arc
import network_LP
import route_algorithm as ra
import make_csv
def main():
    # Parameter
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
    
    # 3, 9, 15열이면서 블럭이 아닌 임의의 좌표에 YT, Job 생성
    YT_locations = {0: (0, 15), 1: (0, 9), 2: (0, 15), 3: (8, 9), 4: (2, 3),
                    5: (4, 9),6: (2, 9), 7: (6, 9), 8: (2, 9), 9: (6, 9),
                    10: (8, 15), 11: (8, 9),12: (6, 9), 13: (4, 3), 14: (6, 3),
                    15: (0, 3), 16: (2, 9), 17: (4, 9), 18: (0, 3), 19: (4, 15)}
    
    Job_locations = {0: [(2, 3), (6, 15)], 1: [(4, 3), (6, 3)], 2: [(2, 3), (0, 9)],
                     3: [(8, 9), (0, 9)], 4: [(4, 15), (4, 9)], 5: [(0, 15), (2, 15)],
                     6: [(2, 9), (6, 3)], 7: [(8, 9), (6, 3)], 8: [(0, 3), (8, 9)],
                     9: [(4, 9), (4, 15)], 10: [(6, 15), (0, 15)], 11: [(6, 3), (2, 15)],
                     12: [(4, 3), (2, 15)], 13: [(8, 9), (6, 9)], 14: [(0, 15), (2, 15)],
                     15: [(4, 3), (8, 3)], 16: [(0, 15), (6, 15)], 17: [(8, 9), (0, 9)],
                     18: [(8, 15), (2, 9)], 19: [(8, 15), (6, 15)]}

    # 스케줄링 대상 YT 생성
    number_of_YT = 20
    number_of_Job = 20
    
    # 3, 9, 15열이면서 블럭이 아닌 임의의 좌표에 YT, Job 생성
    # for i in range(number_of_YT):
    #     YT_location = None
    #     while YT_location is None or grid[YT_location] == -1 or YT_location[1] not in [3, 9, 15]:
    #         YT_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #     YT_locations[i] = YT_location

    # for j in range(number_of_Job):
    #     Pick_location = None
    #     Drop_location = None
    #     while Pick_location is None or grid[Pick_location] == -1 or Drop_location is None or grid[Drop_location] == -1 or Pick_location == Drop_location or Pick_location[1] not in [3, 9, 15] or Drop_location[1] not in [3, 9, 15]:
    #         Pick_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #         Drop_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #     Job_locations[j] = [Pick_location, Drop_location]



    # for i in range(number_of_YT):
    #     YT_location = None
    #     while YT_location is None or grid[YT_location] == -1:
    #         YT_location = (np.random.randint(9), np.random.randint(7))
    #     YT_locations[i] = YT_location
        
    # # 스케줄링 대상 작업 생성
    # for j in range(number_of_Job):
    #     Pick_location = None
    #     Drop_location = None
    #     while Pick_location is None or grid[Pick_location] == -1 or Drop_location is None or grid[Drop_location] == -1 or Pick_location == Drop_location:
    #         Pick_location = (np.random.randint(9), np.random.randint(7))
    #         Drop_location = (np.random.randint(9), np.random.randint(7))
    #     Job_locations[j] = [Pick_location, Drop_location]

    # print("YT_locations: ", YT_locations)
    # print("Job_locations: ", Job_locations)
  
    number_of_final_route = 3
    alpha1 = 0.8
    alpha2 = 0.1
    alpha3 = 0.1
    prev_count = np.array([
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
    now_count = np.zeros((len(grid), len(grid[0])))
    ra.set_grid(grid)
    
    # YT_locations = {0 : (4,2), 1 : (8,0), 2: (5, 6)}
    # Job_locations = {0 : [(2,4), (5,6)], 1 : [(4,2), (8,0)]}

    # grid = np.array([
    # [4, 2, 3, 2, 3, 2, 4],
    # [2, -1, 2, -1, 2, -1, 2],
    # [4, 1, 3, 1, 3, 1, 4],
    # [2, -1, 2, -1, 2, -1, 2],
    # [4, 1, 3, 1, 3, 1, 4],
    # [2, -1, 2, -1, 2, -1, 2],
    # [4, 1, 3, 1, 3, 1, 4],
    # [2, -1, 2, -1, 2, -1, 2],
    # [4, 2, 3, 2, 3, 2, 4],
    # ])

    # grid = np.array([
    #     [4, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 4],
    #     [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
    #     [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
    #     [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
    #     [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
    #     [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
    #     [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
    #     [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
    #     [4, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2 ,3, 2, 2, 2, 2, 2, 4]
    # ])

    

    # number_of_YT = len(YT_locations)
    # number_of_Job = len(Job_locations)


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

    # Run network_LP
    objective_value, activated_arcs = network_LP.solve(all_arcs, number_of_YT, number_of_Job)
    
    # print('objective_value: ', objective_value)
    # print('activated_arcs: ', activated_arcs)

    # Create csv file for Unity simulation
    YT_traversing_arc, YT_traverse_path, Trucks, RoutePoints = make_csv.create_csv(activated_arcs, number_of_YT, grid)


if __name__ == "__main__":
    main()