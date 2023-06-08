import numpy as np
import pandas as pd
import csv

import make_arc
import network_LP
import route_algorithm as ra
import make_csv


def main():
    # Parameter

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
    
    YT_locations = {0: (0, 9), 1: (4, 15), 2: (4, 15), 3: (8, 15), 4: (2, 9), 5: (6, 3), 6: (0, 3), 7: (2, 15), 8: (6, 3), 9: (6, 9), 10: (8, 9), 11: (2, 9), 12: (4, 15), 13: (0, 15), 14: (6, 9), 15: (0, 3), 16: (0, 15), 17: (6, 15), 18: (8, 3), 19: (4, 3)}
    Job_locations = {0: [(6, 9), (6, 3)], 1: [(0, 15), (2, 15)], 2: [(4, 3), (4, 9)], 3: [(0, 3), (2, 9)], 4: [(6, 9), (8, 3)], 5: [(4, 9), (8, 15)], 6: [(4, 9), (0, 3)], 7: [(2, 3), (0, 3)], 8: [(4, 3), (6, 15)], 9: [(4, 9), (8, 9)], 10: [(4, 3), (2, 9)], 11: [(0, 9), (8, 9)], 12: 
    [(6, 3), (0, 15)], 13: [(2, 9), (8, 9)], 14: [(2, 15), (8, 3)], 15: [(6, 3), (2, 3)], 16: [(6, 15), (2, 15)], 17: [(8, 9), (8, 15)], 18: [(0, 3), (8, 9)], 19: [(4, 9), (6, 3)]}

    number_of_YT = 20
    number_of_Job = 20

    # 스케줄링 대상 YT 생성
    # YT_locations = {}
    # Job_locations = {}
    
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
    #         YT_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #     YT_locations[i] = YT_location
        
    # # 스케줄링 대상 작업 생성
    # for j in range(number_of_Job):
    #     Pick_location = None
    #     Drop_location = None
    #     while Pick_location is None or grid[Pick_location] == -1 or Drop_location is None or grid[Drop_location] == -1 or Pick_location == Drop_location:
    #         Pick_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #         Drop_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #     Job_locations[j] = [Pick_location, Drop_location]


    # print("YT_locations =", YT_locations)
    # print("Job_locations =", Job_locations)


    number_of_final_route = 3
    alpha1 = 0.5 # prev counter
    alpha2 = 0.5 # now counter
    alpha3 = 0 # distance
    prev_count = np.array([
    [397,  397,  397,  612,  517,  517,  724,  423,  423,  444,  414,  414, 633,  383,  383,  404,  195,  195,  195,],
    [397,    0,    0,    0,    0,    0,  508,    0,    0,    0,    0,    0, 469,    0,    0,    0,    0,    0,  195,],
    [533,  303,  303,  389,  174,  174,  800,  259,  259,  365,  279,  279, 786,  244,  244,  464,  214,  214,  278,],
    [366,    0,    0,    0,    0,    0,  659,    0,    0,    0,    0,    0, 580,    0,    0,    0,    0,    0,  147,],
    [452,  155,  155,  415,  355,  355, 1046,  383,  383,  585,  394,  394, 843,  177,  177,  292,  111,  111,  203,],
    [383,    0,    0,    0,    0,    0,  695,    0,    0,    0,    0,    0, 535,    0,    0,    0,    0,    0,  148,],
    [527,  257,  257,  446,  287,  287,  921,  254,  254,  361,  276,  276, 702,  161,  161,  167,   24,   24,  169,],
    [414,    0,    0,    0,    0,    0,  606,    0,    0,    0,    0,    0, 432,    0,    0,    0,    0,    0,  166,],
    [414,  414,  414,  522,  475,  475,  830,  579,  579,  710,  476,  476, 571,  234,  234,  250,  166,  166,  166]
    ])
    
    now_count = np.zeros((len(grid), len(grid[0])))
    ra.set_grid(grid)
    
 
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
    print('now_count')
    print(now_count)

    # Run network_LP
    objective_value, activated_arcs = network_LP.solve(all_arcs, number_of_YT, number_of_Job)
    
    # print('objective_value: ', objective_value)
    # print('activated_arcs: ', activated_arcs)

    # Create csv file for Unity simulation
    YT_traversing_arc, YT_traverse_path, Trucks, RoutePoints = make_csv.create_csv(activated_arcs, number_of_YT, grid)


if __name__ == "__main__":
    main()