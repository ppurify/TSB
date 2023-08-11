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
        [4, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2 ,4, 2, 2, 2, 2, 2, 4]
    ])

    number_of_YT = 30
    number_of_Job = 30
    filename_Truck = 'Test_Truck_30_solution_3.csv'
    filename_RoutePoints = 'Test_RoutePoints_30_solution_3.csv'

    # 스케줄링 대상 YT 생성
    YT_locations = {0: (4, 3), 1: (6, 14), 2: (0, 15), 3: (8, 17), 4: (4, 2), 5: (0, 1), 6: (4, 7), 7: (8, 13), 8: (0, 18), 9: (0, 16), 10: (6, 2), 11: (0, 3), 12: (1, 18), 13: (7, 18), 14: (2, 12), 15: (2, 15), 16: (4, 3), 17: (0, 18), 18: (8, 13), 19: (8, 16), 20: (8, 16), 21: (2, 3), 22: (0, 9), 23: (1, 0), 24: (0, 18), 25: (1, 6), 26: (2, 3), 27: (8, 10), 28: (2, 12), 29: (0, 0)}
    Job_locations =  {0: [(6, 15), (6, 9)], 1: [(6, 3), (0, 3)], 2: [(2, 9), (0, 3)], 3: [(2, 9), (6, 15)], 4: [(0, 15), (2, 9)], 5: [(2, 15), (6, 15)], 6: [(4, 9), (4, 3)], 7: [(6, 9), (2, 3)], 8: [(6, 15), (0, 15)], 9: [(0, 9), (4, 3)], 10: [(4, 15), (2, 3)], 11: [(6, 9), (8, 15)], 12: [(6, 15), (6, 9)], 13: [(8, 3), (6, 15)], 14: [(4, 9), (6, 9)], 15: [(2, 3), (4, 9)], 16: [(6, 9), (4, 9)], 17: [(6, 15), (4, 9)], 18: [(6, 3), (8, 15)], 19: [(4, 9), (8, 3)], 20: [(0, 3), (2, 3)], 21: [(4, 15), (8, 3)], 22: [(2, 3), (8, 3)], 23: [(8, 3), (6, 15)], 24: [(8, 9), (6, 9)], 25: [(4, 15), (4, 9)], 26: [(4, 9), (6, 9)], 27: [(2, 15), (6, 3)], 28: [(2, 9), (6, 9)], 29: [(0, 3), (2, 9)]}

    # YT_locations = {0: (4, 3), 1: (6, 14), 2 : (0, 3)}
    # Job_locations =  {0: [(6, 15), (6, 9)], 1: [(6, 3), (0, 3)]}

    # YT_locations = {0: (4, 10), 1: (6, 8), 2: (0, 8), 3: (8, 17), 4: (6, 10)}
    # Job_locations = {0: [(4, 15), (0, 3)], 1: [(4, 15), (2, 15)], 2: [(4, 3), (8, 15)], 3: [(4, 15), (8, 9)], 4: [(4, 3), (4, 9)]}
    
    # YT_locations = {}
    # Job_locations = {}

    # # 임의의 위치에 YT 생성
    # for i in range(number_of_YT):
    #     YT_location = None
    #     while YT_location is None or grid[YT_location] == -1:
    #         YT_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #     YT_locations[i] = YT_location

    # # 3, 9, 15열이면서 블럭이 아닌 임의의 좌표에 Job 생성
    # for j in range(number_of_Job):
    #     Pick_location = None
    #     Drop_location = None
    #     while Pick_location is None or grid[Pick_location] == -1 or Drop_location is None or grid[Drop_location] == -1 or Pick_location == Drop_location or Pick_location[1] not in [3, 9, 15] or Drop_location[1] not in [3, 9, 15]:
    #         Pick_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #         Drop_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
    #     Job_locations[j] = [Pick_location, Drop_location]


    # print("YT_locations =", YT_locations)
    # print("Job_locations =", Job_locations)


    number_of_final_route = 3
    alpha1 = 0 # prev counter
    alpha2 = 0 # now counter
    alpha3 = 100 # distance

    # prev_count : t-1시점의 활성화된 A2 + A3의 누적 path정보
    prev_count = np.array([
        [3, 5, 6, 4, 2, 7, 5, 2, 4, 4, 2, 1, 9, 5, 5, 4, 0, 0, 2],
        [3, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3],
        [4, 7, 7, 8, 1, 1, 1, 0, 3, 6, 0, 0, 1, 9, 9, 2, 8, 8, 8],
        [3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 6],
        [7, 5, 5, 7, 2, 2, 6, 6, 2, 3, 3, 3, 2, 5, 5, 9, 3, 3, 3],
        [4, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 6],
        [9, 6, 6, 5, 7, 7, 5, 1, 1, 1, 1, 1, 5, 1, 1, 5, 3, 8, 9],
        [4, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 2],
        [1, 1, 1, 8, 7, 7, 4, 4, 6, 4, 1, 1, 5, 4, 9, 4, 3, 3, 3]])
    
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

    # print('now_count')
    # print(now_count)

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

    # print('next_prev_count')
    # print(next_prev_count)

    # # 붙여넣기 쉽게 원소사이에 , 추가하여 출력
    # print('next_prev_count')
    # print(np.array2string(next_prev_count, separator=', ').replace('.', ''))


    # Create csv file for Unity simulation
    YT_traversing_arc, YT_traverse_path, Trucks, RoutePoints = make_csv.create_csv(activated_arcs, number_of_YT, grid, filename_Truck, filename_RoutePoints)


if __name__ == "__main__":
    main()