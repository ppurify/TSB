import numpy as np

import make_arc
import network_LP
import route_algorithm as ra
import make_csv

import make_grid
import random


def main():

    # 가로로 3개
    block_num_in_row = 3
    block_length = 9
    block_height = 1
    grid_length = 31
    grid_height = 9
    grid, _YT_location_col_index, QC_locations, YC_locations = make_grid.Grid(
        grid_length, grid_height, block_length, block_height, block_num_in_row)

    number_of_YT = 30
    number_of_Job = 30
    filename_Truck = 'Model-DH/Result-DH/cost_traveltime_correlation/Now_Truck_30_20_70_10_Middle.csv'
    filename_RoutePoints = 'Model-DH/Result-DH/cost_traveltime_correlation/Now_RoutePoints_30_20_70_10_Middle.csv'

    # YT_locations = {0: (4, 27), 1: (2, 17), 2: (0, 7), 3: (6, 27), 4: (4, 17), 5: (4, 7), 6: (2, 27), 7: (8, 17), 8: (0, 27), 9: (0, 17), 10: (2, 7), 11: (6, 17), 12: (6, 7), 13: (8, 7), 14: (8, 27), 15: (4, 7), 16: (6, 7), 17: (4, 27), 18: (8, 27), 19: (6, 27), 20: (6, 17), 21: (8, 7), 22: (2, 17), 23: (0, 27), 24: (2, 27), 25: (2, 7), 26: (0, 7), 27: (4, 17), 28: (8, 17), 29: (0, 17)}
    # Job_locations = {0: [(2, 5), (0, 15)], 1: [(0, 25), (6, 25)], 2: [(4, 15), (0, 5)], 3: [(8, 25), (0, 15)], 4: [(0, 5), (2, 25)], 5: [(4, 25), (0, 25)], 6: [(0, 5), (8, 15)], 7: [(0, 15), (6, 5)], 8: [(2, 15), (0, 25)], 9: [(0, 15), (6, 15)], 10: [(0, 5), (8, 5)], 11: [(4, 5), (0, 25)], 12: [(0, 25), (6, 25)], 13: [(8, 25), (0, 15)], 14: [(0, 5), (4, 25)], 15: [(0, 5), (4, 15)], 16: [(2, 25), (0, 15)], 17: [(0, 25), (2, 
    # 15)], 18: [(0, 25), (8, 15)], 19: [(0, 5), (8, 5)], 20: [(0, 15), (4, 5)], 21: [(0, 25), (6, 15)], 22: [(0, 15), (2, 5)], 23: [(6, 5), (0, 5)], 24: [(4, 15), (0, 15)], 25: [(0, 25), (4, 25)], 26: [(0, 5), (2, 25)], 27: [(0, 15), (6, 15)], 28: [(0, 25), (6, 5)], 29: [(8, 5), (0, 5)]}

    YT_locations = {0: (2, 17), 1: (4, 7), 2: (6, 7), 3: (0, 7), 4: (4, 17), 5: (8, 7), 6: (6, 17), 7: (0, 17), 8: (2, 7), 9: (8, 27), 10: (8, 17), 11: (6, 27), 12: (2, 27), 13: (0, 27), 14: (4, 27), 15: (4, 27), 16: (6, 27), 17: (6, 17), 18: (0, 17), 19: (4, 17), 20: (4, 7), 21: (2, 27), 22: (8, 27), 23: (0, 7), 24: (2, 7), 25: (8, 7), 26: (0, 27), 27: (2, 17), 28: (6, 7), 29: (8, 17)}
    Job_locations = {0: [(0, 25), (4, 25)], 1: [(0, 5), (8, 15)], 2: [(2, 5), (0, 15)], 3: [(0, 5), (6, 15)], 4: [(0, 15), (8, 5)], 5: [(2, 15), 
    (0, 25)], 6: [(0, 25), (4, 5)], 7: [(6, 25), (0, 15)], 8: [(0, 5), (8, 25)], 9: [(4, 15), (0, 5)], 10: [(2, 25), (0, 25)], 11: [(0, 15), (6, 
    5)], 12: [(6, 25), (0, 25)], 13: [(0, 5), (4, 5)], 14: [(0, 15), (4, 25)], 15: [(6, 5), (0, 5)], 16: [(0, 25), (8, 15)], 17: [(0, 15), (8, 25)], 18: [(0, 5), (8, 5)], 19: [(6, 15), (0, 15)], 20: [(2, 25), (0, 25)], 21: [(2, 5), (0, 25)], 22: [(0, 15), (2, 15)], 23: [(0, 5), (4, 15)], 24: [(0, 25), (4, 5)], 25: [(2, 5), (0, 15)], 26: [(8, 25), (0, 5)], 27: [(8, 5), (0, 25)], 28: [(0, 5), (8, 15)], 29: [(6, 15), (0, 15)]}

    # # Assuming you have YC_locations and QC_locations defined
    # YT_locations = {}
    # Job_locations = {}

    # # Generate a shuffled list of all possible grid locations
    # possible_locations = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
    # random.shuffle(possible_locations)
    # # location_index = 0  # Initialize the index

    # # Create YT locations
    # for i in range(number_of_YT):
    #     YT_location = None
    #     while YT_location is None or grid[YT_location] == -1 or YT_location[1] not in _YT_location_col_index:
    #         # YT_location = possible_locations[location_index]  # Use the current index
    #         if len(possible_locations) > 0:
    #           YT_location = possible_locations.pop()
    #         else:
    #           # print("No more possible YT locations")
    #           possible_locations = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
    #           random.shuffle(possible_locations)
    #           YT_location = possible_locations.pop()

    #     YT_locations[i] = YT_location

    # # Shuffle YC and QC locations for better randomness
    # possible_YC_locations = YC_locations.copy()
    # possible_QC_locations = QC_locations.copy()

    # random.shuffle(possible_YC_locations)
    # random.shuffle(possible_QC_locations)

    # # Create Job locations
    # for j in range(number_of_Job):
    #     # choice random number 0 or 1
    #     random_num = np.random.randint(2)

    #     if(len(possible_YC_locations) > 0):
    #       YC_loc = possible_YC_locations.pop()

    #     else:
    #       # print("No more YC locations")
    #       possible_YC_locations = YC_locations.copy()
    #       random.shuffle(possible_YC_locations)
    #       YC_loc = possible_YC_locations.pop()

    #     if(len(possible_QC_locations) > 0):
    #       QC_loc = possible_QC_locations.pop()

    #     else:
    #       # print("No more QC locations")
    #       possible_QC_locations = QC_locations.copy()
    #       random.shuffle(possible_QC_locations)
    #       QC_loc = possible_QC_locations.pop()

    #     # 0 means Outbound => YC -> QC
    #     if random_num == 0:
    #         Pick_location = YC_loc  # Use random.choice for better randomness
    #         Drop_location = QC_loc
    #     # 1 means Inbound => QC -> YC
    #     else:
    #         Pick_location = QC_loc
    #         Drop_location = YC_loc

    #     Job_locations[j] = [Pick_location, Drop_location]

    # print("YT_locations =", YT_locations)
    # print("Job_locations =", Job_locations)

    number_of_final_route = 3
    alpha1 = 20  # prev counter
    alpha2 = 70  # now counter
    alpha3 = 10  # distance

    # prev_count : t-1시점의 활성화된 A2 + A3의 누적 path정보
    prev_count = np.zeros((len(grid), len(grid[0])))
    prev_count = np.array([[ 3,  3,  3,  3,  3, 11,  9,  9,  9,  9, 11,  3,  3,  3,
                            3, 10,  7,  7,  7,  7, 12,  7,  7,  7,  7, 12,  7,  7,
                            7,  7,  7],
                            [ 3,  0,  0,  0,  0,  0,  0,  0,  0,  0, 10,  0,  0,  0,
                            0,  0,  0,  0,  0,  0, 10,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  7],
                            [ 4,  1,  1,  1,  1,  2,  1,  1,  1,  1, 14,  5,  5,  5,
                            5,  6,  5,  5,  5,  5, 12,  4,  4,  4,  4,  6,  5,  5,
                            5,  5, 11],
                            [ 4,  0,  0,  0,  0,  0,  0,  0,  0,  0, 12,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0,  0,
                            0,  0, 10],
                            [ 5,  3,  3,  3,  3,  4,  3,  3,  3,  3, 14,  2,  2,  2,
                            2,  3,  1,  1,  1,  1,  8,  2,  2,  2,  2,  4,  3,  3,
                            3,  3, 12],
                            [ 3,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  8,  0,  0,  0,  0,  0,  0,  0,
                            0,  0, 11],
                            [ 4,  1,  1,  1,  1,  3,  2,  2,  2,  2, 12,  1,  1,  1,
                            1,  4,  4,  4,  4,  4, 12,  4,  4,  4,  4,  6,  6,  6,
                            6,  6, 13],
                            [ 4,  0,  0,  0,  0,  0,  0,  0,  0,  0, 10,  0,  0,  0,
                            0,  0,  0,  0,  0,  0,  8,  0,  0,  0,  0,  0,  0,  0,
                            0,  0,  9],
                            [ 4,  4,  4,  4,  4,  7,  7,  7,  7,  7, 12,  7,  7,  7,
                            7,  8,  7,  7,  7,  7, 11,  7,  7,  7,  7,  9,  9,  9,
                            9,  9,  9]])

    now_count = np.zeros((len(grid), len(grid[0])))

    processing_time = 150
    time_consumed_per_grid = 1

    ra.set_grid(grid)

    # Create arcs
    arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, now_count = make_arc.create_arcs(
        YT_locations=YT_locations, Job_locations=Job_locations, number_of_final_route=number_of_final_route,
        alpha1=alpha1, alpha2=alpha2, alpha3=alpha3,
        grid=grid, prev_count=prev_count, now_count=now_count, time_consumed_per_grid=time_consumed_per_grid, processing_time=processing_time)

    all_arcs = arcs_YT_to_Pick + arcs_Pick_to_Drop + \
        arcs_Drop_to_Pick + arcs_Drop_to_Sink + arcs_YT_to_Sink





    # arcs_YT_to_Pick을 순회하면서 같은 i, j내의 k개의 arc 중, cost가 가장 작은 arc의 cost를 1000000으로 설정
    for YT_index in range(number_of_YT):
        for Pick_index in range(number_of_Job):
            arcs_in_same_ij = []
            for arc in arcs_YT_to_Pick:
                if arc.i == ['YT', YT_index] and arc.j == ['Pick', Pick_index]:
                    arcs_in_same_ij.append(arc)
            # k가 1개보다 많으면
            if len(arcs_in_same_ij) > 1:
               # arcs_in_same_ij내에서 cost가 가장 작은 arc의 cost를 10000000으로 설정
                min_cost = 10000000
                for arc_ in arcs_in_same_ij:
                    if arc_.cost < min_cost:
                        min_cost = arc_.cost
                for arc__ in arcs_in_same_ij:
                    if arc__.cost == min_cost:
                        arc__.cost = 10000000
                        break

    # arcs_Pick_to_Drop을 순회하면서 같은 i, j내의 k개의 arc 중, cost가 가장 작은 arc의 cost를 1000000으로 설정
    for Pick_index in range(number_of_Job):
        for Drop_index in range(number_of_Job):
            arcs_in_same_ij = []
            for arc in arcs_Pick_to_Drop:
                if arc.i == ['Pick', Pick_index] and arc.j == ['Drop', Drop_index]:
                    arcs_in_same_ij.append(arc)
            # k가 1개보다 많으면
            if len(arcs_in_same_ij) > 1:
               # arcs_in_same_ij내에서 cost가 가장 작은 arc의 cost를 10000000으로 설정
                min_cost = 10000000
                for arc_ in arcs_in_same_ij:
                    if arc_.cost < min_cost:
                        min_cost = arc_.cost
                for arc__ in arcs_in_same_ij:
                    if arc__.cost == min_cost:
                        arc__.cost = 10000000
                        break

    # arcs_Drop_to_Pick을 순회하면서 같은 i, j내의 k개의 arc 중, cost가 가장 작은 arc의 cost를 1000000으로 설정
    for Drop_index in range(number_of_Job):
        for Pick_index in range(number_of_Job):
            arcs_in_same_ij = []
            for arc in arcs_Drop_to_Pick:
                if arc.i == ['Drop', Drop_index] and arc.j == ['Pick', Pick_index]:
                    arcs_in_same_ij.append(arc)
            # k가 1개보다 많으면
            if len(arcs_in_same_ij) > 1:
               # arcs_in_same_ij내에서 cost가 가장 작은 arc의 cost를 10000000으로 설정
                min_cost = 10000000
                for arc_ in arcs_in_same_ij:
                    if arc_.cost < min_cost:
                        min_cost = arc_.cost
                for arc__ in arcs_in_same_ij:
                    if arc__.cost == min_cost:
                        arc__.cost = 10000000
                        break







    # # arcs_YT_to_Pick을 순회하면서 같은 i, j내의 k개의 arc 중, cost가 가장 작은 arc의 cost를 1000000으로 설정
    # for YT_index in range(number_of_YT):
    #     for Pick_index in range(number_of_Job):
    #         arcs_in_same_ij = []
    #         for arc in arcs_YT_to_Pick:
    #             if arc.i == ['YT', YT_index] and arc.j == ['Pick', Pick_index]:
    #                 arcs_in_same_ij.append(arc)
    #         # k가 number_of_final_route개면
    #         if len(arcs_in_same_ij) == number_of_final_route:
    #             # arcs_in_same_ij내에서 cost가 가장 작은 arc의 cost를 10000000으로 설정
    #             min_cost = 10000000
    #             for arc_ in arcs_in_same_ij:
    #                 if arc_.cost < min_cost:
    #                     min_cost = arc_.cost
    #             for arc__ in arcs_in_same_ij:
    #                 if arc__.cost == min_cost:
    #                     arc__.cost = 10000000
    #                     break

    # # arcs_Pick_to_Drop을 순회하면서 같은 i, j내의 k개의 arc 중, cost가 가장 작은 arc의 cost를 1000000으로 설정
    # for Pick_index in range(number_of_Job):
    #     for Drop_index in range(number_of_Job):
    #         arcs_in_same_ij = []
    #         for arc in arcs_Pick_to_Drop:
    #             if arc.i == ['Pick', Pick_index] and arc.j == ['Drop', Drop_index]:
    #                 arcs_in_same_ij.append(arc)
    #         # k가 number_of_final_route개면
    #         if len(arcs_in_same_ij) == number_of_final_route:
    #             # arcs_in_same_ij내에서 cost가 가장 작은 arc의 cost를 10000000으로 설정
    #             min_cost = 10000000
    #             for arc_ in arcs_in_same_ij:
    #                 if arc_.cost < min_cost:
    #                     min_cost = arc_.cost
    #             for arc__ in arcs_in_same_ij:
    #                 if arc__.cost == min_cost:
    #                     arc__.cost = 10000000
    #                     break

    # # arcs_Drop_to_Pick을 순회하면서 같은 i, j내의 k개의 arc 중, cost가 가장 작은 arc의 cost를 1000000으로 설정
    # for Drop_index in range(number_of_Job):
    #     for Pick_index in range(number_of_Job):
    #         arcs_in_same_ij = []
    #         for arc in arcs_Drop_to_Pick:
    #             if arc.i == ['Drop', Drop_index] and arc.j == ['Pick', Pick_index]:
    #                 arcs_in_same_ij.append(arc)
    #         # k가 number_of_final_route개면
    #         if len(arcs_in_same_ij) == number_of_final_route:
    #             # arcs_in_same_ij내에서 cost가 가장 작은 arc의 cost를 10000000으로 설정
    #             min_cost = 10000000
    #             for arc_ in arcs_in_same_ij:
    #                 if arc_.cost < min_cost:
    #                     min_cost = arc_.cost
    #             for arc__ in arcs_in_same_ij:
    #                 if arc__.cost == min_cost:
    #                     arc__.cost = 10000000
    #                     break






    # all arc print
    # print('all_arcs')

    # for arc in all_arcs:
    #   print('arc.i : ', arc.i)
    #   print('arc.j : ', arc.j)
    #   print('arc.k : ', arc.k)
    #   print('arc cost : ', arc.cost)
    #   print('arc path : ', arc.path)
    #   print("")

    objective_value, activated_arcs = network_LP.solve(
        all_arcs, number_of_YT, number_of_Job)

    # activated_arcs들의 각 정보 출력
    # print('activated_arcs')
    # for arc in activated_arcs:
    #     print('arc.i : ', arc.i)
    #     print('arc.j : ', arc.j)
    #     print('arc.k : ', arc.k)
    #     print('arc cost : ', arc.cost)
    #     print('arc path : ', arc.path)
    #     print("")
    print('filename_Truck: ', filename_Truck)
    print('objective_value: ', objective_value)
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

    # 붙여넣기 쉽게 원소사이에 , 추가하여 출력
    print('next_prev_count')
    print(np.array2string(next_prev_count, separator=', ').replace('.', ''))

    # Heatmap을 위한 grid_for_visualization
    # grid_for_visualization = np.zeros((len(grid), len(grid[0])))
    # for arc in activated_arcs:
    #     for i in range(len(arc.path)):
    #         grid_for_visualization[arc.path[i][0]][arc.path[i][1]] += 1

    # print('grid_for_visualization')
    # print(np.array2string(grid_for_visualization, separator=', ').replace('.', ''))

    # Create csv file for Unity simulation/
    make_csv.create_csv(activated_arcs, number_of_YT, grid,
                        filename_Truck, filename_RoutePoints)


if __name__ == "__main__":
    main()
