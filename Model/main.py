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
        [4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
    ])
    
    number_of_YT = 1
    number_of_Job = 1
    
    filename_Truck = 'Truck_1_LP_50_40_10.csv'
    filename_RoutePoints = 'RoutePoints_1_LP_50_40_10.csv'

    # 스케줄링 대상 YT 생성
    # YT_locations = {0: (2, 27), 1: (6, 17), 2: (6, 27), 3: (4, 17), 4: (2, 27), 5: (4, 27), 6: (8, 7), 7: (4, 27), 8: (4, 7), 9: (0, 7), 10: (8, 17), 11: (8, 17), 12: (2, 7), 13: (4, 27), 14: (2, 7), 15: (4, 27), 16: (8, 7), 17: (6, 17), 18: (0, 17), 19: (4, 17), 20: (6, 27), 21: (6, 27), 22: (6, 27), 23: (0, 7), 24: (6, 27), 25: (6, 27), 26: (4, 7), 27: (6, 17), 28: (2, 27), 29: (2, 27)}
    # Job_locations = {0: [(8, 5), (6, 5)], 1: [(6, 15), (2, 15)], 2: [(0, 5), (8, 15)], 3: [(6, 15), (8, 5)], 4: [(0, 15), (6, 15)], 5: [(8, 25), (2, 25)], 6: [(8, 25), (2, 5)], 7: [(8, 15), (0, 15)], 8: [(4, 25), (6, 15)], 9: [(0, 5), (8, 5)], 10: [(6, 15), (4, 15)], 11: [(6, 25), (0, 15)], 12: [(0, 15), (8, 15)], 13: [(8, 5), (4, 15)], 14: [(6, 25), (2, 5)], 15: [(4, 15), (2, 25)], 16: [(2, 5), (4, 25)], 17: [(0, 5), (0, 25)], 18: [(2, 15), (8, 5)], 19: [(8, 25), (0, 25)], 20: [(2, 5), (6, 25)], 21: [(8, 25), (2, 5)], 22: [(2, 15), (6, 25)], 23: [(6, 15), (2, 15)], 24: [(0, 15), (6, 25)], 25: [(6, 15), (4, 25)], 26: [(4, 5), (0, 15)], 27: [(4, 5), (2, 25)], 28: [(6, 5), (4, 5)], 29: [(6, 5), (0, 25)]}
    YT_locations = {0: (4, 17)}
    Job_locations = {0: [(2, 15), (2, 25)]}
    # YT_locations = {}
    # Job_locations = {}

    # # 임의의 위치에 YT 생성
    # for i in range(number_of_YT):
    #     YT_location = None
    #     while YT_location is None or grid[YT_location] == -1 or YT_location[1] not in [7, 17, 27]:
    #         YT_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #     YT_locations[i] = YT_location

    # # 5, 15, 25열이면서 블럭이 아닌 임의의 좌표에 Job 생성
    # for j in range(number_of_Job):
    #     Pick_location = None
    #     Drop_location = None
    #     while Pick_location is None or grid[Pick_location] == -1 or Drop_location is None or grid[Drop_location] == -1 or Pick_location == Drop_location or Pick_location[1] not in [5, 15, 25] or Drop_location[1] not in [5, 15, 25]:
    #         Pick_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #         Drop_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #     Job_locations[j] = [Pick_location, Drop_location]


    # print("YT_locations =", YT_locations)
    # print("Job_locations =", Job_locations)


    number_of_final_route = 3
    alpha1 = 50 # prev counter
    alpha2 = 40 # now counter
    alpha3 = 10 # distance

    prev_count= np.array([[ 4,  4,  4,  4,  4,  5,  5,  5,  5,  5,  9,  7,  7,  7,
   7,  9,  7,  7,  7,  7,  9,  8,  8,  8,  8,  8,  6,  6,
   6,  6,  6],
 [ 4,  0,  0,  0,  0,  0,  0,  0,  0,  0,  6,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  6],
 [ 4,  2,  2,  2,  2,  6,  4,  4,  4,  4, 10,  4,  4,  4,
   4,  6,  2,  2,  2,  2,  9,  5,  5,  5,  5,  7,  2,  2,
   2,  2,  6],
 [ 2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  6,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  8,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  4],
 [ 3,  3,  3,  3,  3,  4,  1,  1,  1,  1,  8,  1,  1,  1,
   1,  4,  3,  3,  3,  3, 10,  1,  1,  1,  1,  5,  4,  4,
   4,  4,  5],
 [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  8,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  8,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  2],
 [ 3,  2,  2,  2,  2,  5,  3,  3,  3,  3, 10,  4,  4,  4,
   4,  6,  5,  5,  5,  5, 11,  2,  2,  2,  2,  6,  4,  4,
   4,  4,  5],
 [ 3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  7,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  4],
 [ 3,  3,  3,  3,  3,  6,  6,  6,  6,  6,  8,  5,  5,  5,
   5,  8,  8,  8,  8,  8, 10,  5,  5,  5,  5,  5,  4,  4,
   4,  4,  4]])
    
    # prev_count = np.zeros((len(grid), len(grid[0])))
    now_count = np.zeros((len(grid), len(grid[0])))

    ra.set_grid(grid)
    
  # Create arcs
    arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count = make_arc.create_arcs(
        YT_locations=YT_locations, Job_locations=Job_locations, number_of_final_route=number_of_final_route,
        alpha1=alpha1, alpha2=alpha2, alpha3=alpha3,
        grid=grid, prev_count=prev_count, now_count=now_count)

    all_arcs = arcs_YT_to_Pick + arcs_Pick_to_Drop + arcs_Drop_to_Pick + arcs_Drop_to_Sink + arcs_YT_to_Sink

    # print('now_count')
    # print(now_count)

    # Run network_LP
    objective_value, activated_arcs = network_LP.solve(all_arcs, number_of_YT, number_of_Job)
    
    # activated_arcs들의 각 정보 출력
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

    # # 붙여넣기 쉽게 원소사이에 , 추가하여 출력
    print('next_prev_count')
    print(np.array2string(next_prev_count, separator=', ').replace('.', ''))


    # Create csv file for Unity simulation
    YT_traversing_arc, YT_traverse_path, Trucks, RoutePoints = make_csv.create_csv(activated_arcs, number_of_YT, grid, filename_Truck, filename_RoutePoints)


if __name__ == "__main__":
    main()