import numpy as np
import pandas as pd
import csv

import make_arc
import network_LP
import route_algorithm as ra
import make_csv
import test_make_csv

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

    number_of_YT = 20
    number_of_Job = 20
    filename_Truck = 'Test_Truck_20_LP.csv'
    filename_RoutePoints = 'Test_RoutePoints_20_LP.csv'

    # 스케줄링 대상 YT 생성
    # YT_locations = {0: (4, 3), 1: (6, 14), 2: (0, 15)}
    # Job_locations =  {0: [(6, 15), (6, 9)], 1: [(6, 3), (0, 3)]}
    # YT_locations = {0: (4, 3)}
    # Job_locations =  {0: [(6, 15), (6, 9)]}
    
    YT_locations = {}
    Job_locations = {}

    # 임의의 위치에 YT 생성
    for i in range(number_of_YT):
        YT_location = None
        while YT_location is None or grid[YT_location] == -1:
            YT_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
        YT_locations[i] = YT_location

    # 3, 9, 15열이면서 블럭이 아닌 임의의 좌표에 Job 생성
    for j in range(number_of_Job):
        Pick_location = None
        Drop_location = None
        while Pick_location is None or grid[Pick_location] == -1 or Drop_location is None or grid[Drop_location] == -1 or Pick_location == Drop_location or Pick_location[1] not in [3, 9, 15] or Drop_location[1] not in [3, 9, 15]:
            Pick_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
            Drop_location = (np.random.randint(len(grid)), np.random.randint(len(grid[0])))
        Job_locations[j] = [Pick_location, Drop_location]


    # print("YT_locations =", YT_locations)
    # print("Job_locations =", Job_locations)


    number_of_final_route = 3

    alpha1 = 1 # prev counter
    alpha2 = 0 # now counter
    alpha3 = 0 # distance

    # prev_count = np.array([
    #     [3095, 3095, 3566, 4074, 3722, 3867, 5144, 4172, 4172, 4712, 4372, 4331, 5299, 3495, 3495, 3714, 3260, 3260, 3122],
    #     [3095,    0,    0,    0,    0,    0, 2257,    0,    0,    0,    0,    0, 2772,    0,    0,    0,    0,    0, 3122],
    #     [4060, 1897, 1897, 2738, 2321, 2321, 4811, 1370, 1243, 1866, 1750, 1750, 4851, 1219, 1219, 1752, 1398, 1398, 3398],
    #     [3012,    0,    0,    0,    0,    0, 3960,    0,    0,    0,    0,    0, 3961,    0,    0,    0,    0,    0, 2276],
    #     [3887, 1855, 1855, 1857, 1652, 1652, 6000, 2246, 2246, 3192, 3173, 3066, 5972,  485,  485, 3769, 3606, 3606, 4073],
    #     [2934,    0,    0,    0,    0,    0, 4169,    0,    0,    0,    0,    0, 4539,    0,    0,    0,    0,    0, 2366],
    #     [3979, 1786, 1786, 1955, 1537, 1537, 4735, 1515, 1515, 1695, 1465, 1465, 5576, 1865, 1865, 1745, 1143,  988, 3279],
    #     [3244,    0,    0,    0,    0,    0, 1993,    0,    0,    0,    0,    0, 3128,    0,    0,    0,    0,    0, 3052],
    #     [3161, 3161, 3161, 3308, 3297, 3297, 4732, 4174, 4286, 4474, 4141, 4141, 5655, 4107, 3989, 4347, 3222, 3222, 3052]])
    prev_count = np.array([[ 5,  5,  5,  7, 10, 10, 13,  9,  9, 11, 12, 12, 15, 10,
  10,  5,  3,  3,  3],
 [ 5,  0,  0,  0,  0,  0,  8,  0,  0,  0,  0,  0,  8,  0,
   0,  0,  0,  0,  3],
 [ 5,  3,  3,  3,  3,  3, 11,  4,  4,  4,  5,  5, 10,  1,
   1,  1,  1,  1,  3],
 [ 2,  0,  0,  0,  0,  0,  8,  0,  0,  0,  0,  0,  6,  0,
   0,  0,  0,  0,  2],
 [ 2,  1,  1,  1,  1,  1, 10,  2,  1,  1,  1,  1,  6,  0,
   0,  0,  1,  1,  3],
 [ 1,  0,  0,  0,  0,  0,  9,  0,  0,  0,  0,  0,  5,  0,
   0,  0,  0,  0,  3],
 [ 3,  3,  3,  3,  3,  3, 10,  2,  2,  2,  2,  2,  7,  2,
   2,  2,  2,  2,  4],
 [ 2,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  5,  0,
   0,  0,  0,  0,  3],
 [ 2,  2,  2,  2,  3,  3,  6,  4,  4,  5,  6,  6,  9,  7,
   7,  5,  3,  3,  3]])

    prev_count = np.zeros((len(grid), len(grid[0])))

    now_count_A1 = np.zeros((len(grid), len(grid[0])))
    now_count_A2 = np.zeros((len(grid), len(grid[0])))
    now_count_A3 = np.zeros((len(grid), len(grid[0])))

    ra.set_grid(grid)
    
    
    # Create arcs
    arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink = make_arc.create_arcs(
        YT_locations=YT_locations, Job_locations=Job_locations, number_of_final_route=number_of_final_route,
        alpha1=alpha1, alpha2=alpha2, alpha3=alpha3,
        grid=grid, prev_count=prev_count, now_count_A1=now_count_A1, now_count_A2=now_count_A2, now_count_A3=now_count_A3)

    all_arcs = arcs_YT_to_Pick + arcs_Pick_to_Drop + arcs_Drop_to_Pick + arcs_Drop_to_Sink + arcs_YT_to_Sink

    # print('now_count')
    # print(now_count)

    # Run network_LP
    objective_value, activated_arcs = network_LP.solve(all_arcs, number_of_YT, number_of_Job)
    
    print('activated arcs 갯수 : ' , len(activated_arcs))
    # for i in range(len(activated_arcs)):
    #     print('activated arcs path : ', activated_arcs[i].path)

    # activated_arcs 순회하며 각 arc의 path를 순회하며 prev_count 업데이트
    new_prev_count = np.zeros((len(grid), len(grid[0])))
    for arc in activated_arcs:
        for i in range(len(arc.path)-1):
            new_prev_count[arc.path[i][0]][arc.path[i][1]] += 1

    # print('prev_count')
    # print(prev_count)

    # 업데이트된 prev_count를 바로 복사 할수 있도록 원소의 마침표는 제거하고 원소 사이사이에 쉼표 추가하여 출력
    print('new_prev_count')
    print(np.array2string(prev_count, separator=', ').replace('.', ''))



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

    # Create csv file for Unity simulation
    YT_traversing_arc, YT_traverse_path, Trucks, RoutePoints = test_make_csv.create_csv(activated_arcs, number_of_YT, grid, filename_Truck, filename_RoutePoints)
    print("DONE")

if __name__ == "__main__":
    main()