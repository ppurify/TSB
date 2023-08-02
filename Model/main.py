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
    
    number_of_YT = 30
    number_of_Job = 30
    
    filename_Truck = 'compared_Truck_30_LP_50_40_10.csv'
    filename_RoutePoints = 'compared_RoutePoints_30_LP_50_40_10.csv'

    # 스케줄링 대상 YT 생성
    YT_locations = {0: (6, 27), 1: (4, 7), 2: (2, 17), 3: (8, 27), 4: (4, 7), 5: (2, 17), 6: (2, 7), 7: (4, 17), 8: (8, 27), 9: (6, 7), 10: (8, 17), 11: (0, 17), 12: (2, 17), 13: (2, 17), 14: (0, 27), 15: (6, 27), 16: (8, 7), 17: (0, 27), 18: (2, 17), 19: (6, 7), 20: (8, 17), 21: (6, 7), 22: (8, 27), 23: (0, 7), 24: (0, 17), 25: (2, 27), 26: (8, 17), 27: (4, 7), 28: (8, 7), 29: (0, 27)}
    Job_locations = {0: [(6, 25), (0, 15)], 1: [(6, 5), (6, 25)], 2: [(8, 5), (2, 25)], 3: [(8, 15), (6, 15)], 4: [(8, 15), (2, 25)], 5: [(4, 5), (8, 5)], 6: [(6, 15), (4, 5)], 7: [(8, 5), (8, 15)], 8: [(4, 15), (0, 15)], 9: [(2, 5), (2, 25)], 10: [(4, 5), (2, 15)], 11: [(4, 5), (0, 25)], 12: [(2, 5), (4, 25)], 13: [(6, 25), (0, 15)], 14: [(2, 25), (0, 5)], 15: [(8, 15), (4, 25)], 16: [(8, 5), (0, 15)], 17: [(8, 5), (6, 15)], 18: [(0, 25), (8, 25)], 19: [(0, 25), (0, 15)], 20: [(6, 25), (4, 15)], 21: [(2, 15), (4, 25)], 22: [(4, 5), (8, 15)], 23: [(2, 5), (6, 25)], 24: [(4, 5), (2, 15)], 25: [(0, 5), (0, 25)], 26: [(8, 15), (6, 15)], 27: [(8, 5), (8, 15)], 28: [(4, 5), (0, 25)], 29: [(8, 5), (0, 5)]}
    
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

    prev_count = np.array([[ 2,  2,  2,  2,  2,  3,  6,  7,  5,  5,  7,  4,  4,  4,
   4,  4,  4,  4,  4,  4,  9,  6,  6,  6,  6,  6,  6,  6,
   2,  2,  2],
 [ 2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  8,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  2],
 [ 2,  1,  1,  1,  1,  1,  3,  3,  2,  2,  8,  2,  2,  2,
   2,  2,  4,  4,  3,  3,  9,  1,  1,  1,  1,  1,  2,  2,
   1,  1,  2],
 [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  1],
 [ 3,  2,  2,  2,  2,  2,  4,  4,  3,  3,  9,  1,  1,  1,
   1,  1,  1,  1,  0,  0,  8,  2,  2,  2,  2,  2,  2,  2,
   0,  0,  1],
 [ 3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  8,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  1],
 [ 3,  1,  1,  1,  1,  1,  4,  4,  4,  4, 12,  6,  6,  6,
   6,  6,  9,  9,  8,  8, 12,  3,  3,  3,  3,  3,  4,  4,
   3,  3,  3],
 [ 2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  2],
 [ 2,  2,  2,  2,  2,  4,  8,  8,  6,  6, 10,  7,  7,  7,
   7,  7,  7,  7,  6,  6,  8,  5,  5,  5,  5,  3,  3,  3,
   2,  2,  2]])

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
    for arc in activated_arcs:
        print('arc.i : ', arc.i)
        print('arc.j : ', arc.j)
        print('arc.k : ', arc.k)
        print('arc cost : ', arc.cost)
        print('arc path : ', arc.path)
        print("")
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

    print('next_prev_count')
    print(next_prev_count)

    # # 붙여넣기 쉽게 원소사이에 , 추가하여 출력
    # print('next_prev_count')
    # print(np.array2string(next_prev_count, separator=', ').replace('.', ''))


    # Create csv file for Unity simulation
    YT_traversing_arc, YT_traverse_path, Trucks, RoutePoints = make_csv.create_csv(activated_arcs, number_of_YT, grid, filename_Truck, filename_RoutePoints)


if __name__ == "__main__":
    main()