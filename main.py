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
    
    # YT_locations = {0: (0, 3), 1: (8, 16), 2: (6, 17), 3: (2, 12), 4: (2, 14), 5: (3, 6), 6: (8, 2), 7: (2, 15), 8: (0, 17), 9: (2, 15), 10: (8, 9), 11: (3, 12), 12: (6, 14), 13: (2, 1), 14: (0, 2), 15: (6, 3), 16: (8, 0), 17: (2, 0), 18: (0, 3), 19: (2, 16), 20: (8, 10), 21: (2, 6), 22: (8, 17), 23: (0, 3), 24: (6, 3), 25: (6, 18), 26: (6, 16), 27: (8, 2), 28: (0, 18), 29: (3, 12), 30: (6, 16), 31: (6, 9), 32: (4, 0), 33: (4, 18), 34: (4, 6), 35: (4, 15), 36: (0, 10), 37: (0, 2), 38: (1, 12), 39: (4, 4), 40: (6, 14), 41: (4, 0), 42: (8, 10), 43: (6, 11), 44: (4, 16), 45: (4, 3), 46: (8, 0), 47: (4, 13), 48: (6, 18), 49: (4, 6)}
    # Job_locations = {0: [(8, 17), (2, 5)], 1: [(4, 4), (1, 12)], 2: [(8, 18), (2, 3)], 3: [(4, 16), (8, 13)], 4: [(4, 2), (8, 3)], 5: [(1, 0), (2, 3)], 6: [(6, 16), (8, 14)], 7: [(0, 17), (6, 7)], 8: [(8, 5), (2, 11)], 9: [(0, 2), (5, 12)], 10: [(4, 13), (2, 12)], 11: [(0, 18), (6, 18)], 12: [(5, 6), (0, 2)], 13: [(4, 10), (2, 10)], 14: [(2, 13), (8, 15)], 15: [(8, 0), (8, 14)], 
    # 16: [(0, 10), (6, 9)], 17: [(7, 6), (2, 18)], 18: [(2, 4), (2, 11)], 19: [(5, 6), (4, 6)], 20: [(2, 18), (4, 6)], 21: [(4, 17), (2, 14)], 22: [(4, 17), (6, 7)], 23: [(3, 18), (0, 13)], 24: [(8, 0), (4, 16)], 25: [(0, 5), (4, 15)], 26: [(6, 14), (4, 9)], 27: [(1, 12), (0, 4)], 28: [(8, 16), (1, 0)], 29: [(4, 13), (4, 14)], 30: [(4, 12), (4, 18)], 31: [(5, 0), (5, 12)], 32: [(8, 18), (5, 18)], 33: [(8, 8), (2, 1)], 34: [(0, 3), (4, 16)], 35: [(2, 6), (2, 8)], 36: [(2, 4), (4, 6)], 37: [(6, 5), (0, 10)], 38: [(8, 8), (6, 1)], 39: [(6, 4), (2, 10)], 40: [(4, 16), (1, 12)], 41: [(1, 0), (7, 12)], 42: [(8, 17), (6, 11)], 43: [(7, 12), (4, 13)], 44: [(2, 4), (0, 14)], 45: [(8, 3), (2, 13)], 46: [(1, 0), (6, 16)], 47: [(4, 5), (2, 14)], 48: [(0, 8), (2, 
    # 0)], 49: [(8, 1), (2, 16)]}

    number_of_YT = 2
    number_of_Job = 2
    filename_Truck = 'Truck_2_LP.csv'
    filename_RoutePoints = 'RoutePoints_2_LP.csv'

    # 스케줄링 대상 YT 생성
    YT_locations = {0: (0, 8), 1: (0, 9)}
    Job_locations = {0: [(8, 3), (0, 15)], 1: [(6, 3), (2, 15)]}
    
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


    number_of_final_route = 10
    alpha1 = 0 # prev counter
    alpha2 = 1 # now counter
    alpha3 = 0 # distance

    prev_count = np.array([
        [4, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [4, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2 ,3, 2, 2, 2, 2, 2, 4]])
    
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

    # Create csv file for Unity simulation
    YT_traversing_arc, YT_traverse_path, Trucks, RoutePoints = make_csv.create_csv(activated_arcs, number_of_YT, grid, filename_Truck, filename_RoutePoints)


if __name__ == "__main__":
    main()