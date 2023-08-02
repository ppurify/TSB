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
    
    filename_Truck = 'test_prev_RoutePoints_30_shortest.csv'
    filename_RoutePoints = 'test_prev_RoutePoints_30_shortest.csv'

    # 스케줄링 대상 YT 생성
    YT_locations = {0: (6, 27), 1: (0, 7), 2: (0, 17), 3: (0, 17), 4: (8, 7), 5: (8, 7), 6: (4, 17), 7: (6, 27), 8: (4, 7), 9: (0, 7), 10: (2, 7), 11: (8, 17), 12: (2, 27), 13: (2, 17), 14: (6, 27), 15: (0, 27), 16: (0, 27), 17: (6, 17), 18: (2, 7), 19: (2, 17), 20: (2, 27), 21: (0, 17), 22: (4, 27), 23: (6, 17), 24: (8, 17), 25: (2, 7), 26: (6, 17), 27: (0, 17), 28: (8, 7), 29: (4, 17)}
    Job_locations = {0: [(0, 25), (0, 15)], 1: [(4, 15), (8, 5)], 2: [(6, 25), (4, 25)], 3: [(4, 15), (8, 25)], 4: [(0, 25), (4, 15)], 5: [(6, 15), (8, 25)], 6: [(2, 25), (6, 15)], 7: [(0, 25), (6, 5)], 8: [(8, 15), (2, 15)], 9: [(4, 15), (6, 15)], 10: [(4, 25), (6, 15)], 11: [(8, 25), (2, 5)], 12: [(2, 25), (6, 5)], 13: [(0, 25), (0, 15)], 14: [(2, 25), (0, 25)], 15: [(0, 25), (2, 15)], 16: [(4, 15), (6, 15)], 17: [(4, 15), (8, 5)], 18: [(6, 15), (0, 15)], 19: [(6, 15), (8, 15)], 20: [(6, 15), (0, 15)], 21: [(0, 15), (4, 15)], 22: [(2, 15), (0, 5)], 23: [(2, 5), (6, 25)], 24: [(4, 25), (0, 25)], 25: [(8, 15), (0, 25)], 26: [(6, 5), (2, 15)], 27: [(4, 5), (6, 15)], 28: [(6, 5), (4, 15)], 29: [(4, 25), (6, 25)]}
    
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
    alpha1 = 0 # prev counter
    alpha2 = 0 # now counter
    alpha3 = 100 # distance

    prev_count= np.array([[ 6,  6,  6,  6,  6,  9,  9,  9,  9,  9, 11,  9,  9,  9,
   9, 12, 10, 10, 10, 10, 10,  6,  6,  6,  6,  7,  3,  3,
   3,  3,  3],
 [ 6,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  4,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  3],
 [ 7,  3,  3,  3,  3,  3,  0,  0,  0,  0,  5,  2,  2,  2,
   2,  4,  3,  3,  3,  3,  5,  1,  1,  1,  1,  4,  3,  3,
   3,  3,  5],
 [ 5,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  4],
 [ 7,  6,  6,  6,  6,  7,  1,  1,  1,  1,  5,  1,  1,  1,
   1,  2,  1,  1,  1,  1,  3,  0,  0,  0,  0,  3,  3,  3,
   3,  3,  6],
 [ 3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  5],
 [ 4,  1,  1,  1,  1,  1,  0,  0,  0,  0,  4,  1,  1,  1,
   1,  4,  3,  3,  3,  3,  6,  3,  3,  3,  3,  5,  2,  2,
   2,  2,  7],
 [ 4,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,
   0,  0,  7],
 [ 4,  4,  4,  4,  4, 10,  9,  9,  9,  9, 10,  8,  8,  8,
   8, 12,  9,  9,  9,  9,  9,  6,  6,  6,  6,  7,  7,  7,
   7,  7,  7]])
    
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