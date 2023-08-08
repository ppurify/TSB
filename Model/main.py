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
    
    number_of_YT = 40
    number_of_Job = 40
    
    filename_Truck = 'Truck_40_LP_70_20_10.csv'
    filename_RoutePoints = 'RoutePoints_40_LP_70_20_10.csv'

    # 스케줄링 대상 YT 생성
    YT_locations = {0: (6, 17), 1: (8, 27), 2: (4, 27), 3: (8, 7), 4: (6, 7), 5: (8, 7), 6: (4, 27), 7: (2, 7), 8: (6, 7), 9: (4, 27), 10: (6, 17), 11: (4, 27), 12: (4, 7), 13: (6, 7), 14: (2, 27), 15: (4, 27), 16: (6, 27), 17: (8, 17), 18: (2, 7), 19: (4, 17), 20: (6, 17), 21: (8, 27), 22: (4, 17), 23: (0, 7), 24: (6, 17), 25: (4, 27), 26: (6, 7), 27: (4, 27), 28: (6, 27), 29: (2, 7), 30: (6, 27), 31: (2, 17), 32: (4, 17), 33: (2, 27), 34: (2, 17), 35: (8, 27), 36: (0, 7), 37: (8, 17), 38: (6, 7), 39: (2, 7)}
    Job_locations = {0: [(4, 5), (8, 15)], 1: [(6, 5), (6, 15)], 2: [(6, 25), (6, 15)], 3: [(2, 5), (6, 15)], 4: [(0, 25), (4, 25)], 5: [(6, 15), (8, 5)], 6: [(0, 25), (6, 25)], 7: [(6, 5), (6, 15)], 8: [(4, 15), (0, 25)], 9: [(0, 25), (8, 25)], 10: [(0, 25), (6, 15)], 11: [(6, 5), (0, 15)], 12: [(6, 25), (6, 5)], 13: [(6, 15), (2, 25)], 14: [(4, 25), (6, 15)], 15: [(0, 15), (8, 5)], 16: [(4, 25), (0, 15)], 17: [(0, 15), (0, 5)], 18: [(0, 25), (6, 15)], 19: [(2, 15), (6, 15)], 20: [(0, 25), (8, 25)], 21: [(0, 25), (4, 15)], 22: [(0, 25), (6, 25)], 23: [(2, 15), (0, 5)], 24: [(2, 15), (4, 25)], 25: [(0, 5), (4, 15)], 26: [(6, 15), (0, 25)], 27: [(0, 5), (0, 15)], 28: [(2, 5), (8, 25)], 29: [(2, 25), (6, 25)], 30: [(6, 5), (4, 15)], 31: [(2, 15), (0, 15)], 32: [(2, 15), (0, 25)], 33: [(6, 5), (0, 5)], 34: [(2, 5), (0, 25)], 35: [(2, 5), (2, 25)], 36: [(6, 25), (6, 5)], 37: [(6, 15), (0, 5)], 38: [(2, 15), (4, 25)], 39: [(0, 25), (0, 5)]}

    # YT_locations = {0: (4, 17)}
    # Job_locations = {0: [(2, 15), (2, 25)]}
    
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
    alpha1 = 70 # prev counter
    alpha2 = 20 # now counter
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