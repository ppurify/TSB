import numpy as np

import make_arc
import network_LP
import route_algorithm as ra
import make_csv
import os

import make_grid
import random

def generate_locations(grid, number_of_YT, number_of_Job, _YT_location_col_index, QC_locations, YC_locations):
    # Assuming you have YC_locations and QC_locations defined
    YT_locations = {}
    Job_locations = {}

    # Generate a shuffled list of all possible grid locations
    possible_locations = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
    random.shuffle(possible_locations)
    # location_index = 0  # Initialize the index

    # Create YT locations
    for i in range(number_of_YT):
        YT_location = None
        while YT_location is None or grid[YT_location] == -1 or YT_location[1] not in _YT_location_col_index:
            # YT_location = possible_locations[location_index]  # Use the current index
            if len(possible_locations) > 0:
              YT_location = possible_locations.pop()
            else:
              # print("No more possible YT locations")
              possible_locations = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
              random.shuffle(possible_locations)
              YT_location = possible_locations.pop()

        YT_locations[i] = YT_location

    # Shuffle YC and QC locations for better randomness
    possible_YC_locations = YC_locations.copy()
    possible_QC_locations = QC_locations.copy()

    random.shuffle(possible_YC_locations)
    random.shuffle(possible_QC_locations)

    # Create Job locations
    for j in range(number_of_Job):
        # choice random number 0 or 1
        random_num = np.random.randint(2)

        if(len(possible_YC_locations) > 0):
          YC_loc = possible_YC_locations.pop()

        else:
          # print("No more YC locations")
          possible_YC_locations = YC_locations.copy()
          random.shuffle(possible_YC_locations)
          YC_loc = possible_YC_locations.pop()

        if(len(possible_QC_locations) > 0):
          QC_loc = possible_QC_locations.pop()

        else:
          # print("No more QC locations")
          possible_QC_locations = QC_locations.copy()
          random.shuffle(possible_QC_locations)
          QC_loc = possible_QC_locations.pop()

        # 0 means Outbound => YC -> QC
        if random_num == 0:
            Pick_location = YC_loc  # Use random.choice for better randomness
            Drop_location = QC_loc
        # 1 means Inbound => QC -> YC
        else:
            Pick_location = QC_loc
            Drop_location = YC_loc

        Job_locations[j] = [Pick_location, Drop_location]

    return YT_locations, Job_locations


def main(number_of_YT, number_of_Job, casename, time, prev_count, alpha1, alpha2, alpha3, rep):

    # 가로로 3개
    block_num_in_row = 3
    block_length = 9
    block_height = 1
    grid_length = 31
    grid_height = 9
    grid, _YT_location_col_index, QC_locations, YC_locations = make_grid.Grid(
        grid_length, grid_height, block_length, block_height, block_num_in_row)

    filename_Truck = 'Model-DH/Result-DH/'+str(casename)+'/'+ str(time) + '_Truck_'+str(number_of_YT)+'_LP_'+str(alpha1)+'_'+str(alpha2)+'_'+str(alpha3)+'_'+str(rep)+'rep'+'.csv'
    filename_RoutePoints = 'Model-DH/Result-DH/'+str(casename)+'/'+ str(time) + '_RoutePoints_'+str(number_of_YT)+'_LP_'+str(alpha1)+'_'+str(alpha2)+'_'+str(alpha3)+'_'+str(rep)+'rep'+'.csv'


    YT_locations, Job_locations = generate_locations(grid, number_of_YT, number_of_Job, _YT_location_col_index, QC_locations, YC_locations)

    # print("YT_locations =", YT_locations)
    # print("Job_locations =", Job_locations)

    number_of_final_route = 3
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


    objective_value, activated_arcs = network_LP.solve(
        all_arcs, number_of_YT, number_of_Job)
    print('objective_value: ', objective_value)

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

    # Create csv file for Unity simulation/
    make_csv.create_csv(activated_arcs, number_of_YT, grid, filename_Truck, filename_RoutePoints)

    return next_prev_count


if __name__ == "__main__":

    #casename에 해당하는 폴더가 없다면 생성

    if not os.path.exists('Model-DH/Result-DH/Congestion'):
        os.makedirs('Model-DH/Result-DH/Congestion')
    casename = 'Congestion'
    Prev_number_of_YT = 30
    Prev_number_of_Job = 30
    Now_number_of_YT = 35
    Now_number_of_Job = 35

    reps = 1

    alphas = [[0, 80, 70, 60, 50, 40, 30, 20, 10],
              [0, 10, 20, 30, 40, 50, 60, 70, 80],
              [100, 10, 10, 10, 10, 10, 10, 10, 10]]
    
    for i in range(len(alphas[0])):
        alpha1 = alphas[0][i]
        alpha2 = alphas[1][i]
        alpha3 = alphas[2][i]
        for rep in range(reps):
            # Prev
            prev_count = np.zeros((9, 31),dtype=np.int8)
            next_prev_count = main(Prev_number_of_YT, Prev_number_of_Job, casename, 'Prev', prev_count, alpha1, alpha2, alpha3, rep)
            # Now
            prev_count = next_prev_count
            next_prev_count = main(Now_number_of_YT, Now_number_of_Job, casename, 'Now', prev_count, alpha1, alpha2, alpha3, rep)



# def change_min_arcs_cost_to_bignumber(arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink, number_of_YT, number_of_Job):
#     """페어 당 가장작은 코스트의 아크의 코스트를 1000000으로 설정"""
#     # arcs_YT_to_Pick을 순회하면서 같은 i, j내의 k개의 arc 중, cost가 가장 작은 arc의 cost를 1000000으로 설정
#     for YT_index in range(number_of_YT):
#         for Pick_index in range(number_of_Job):
#             arcs_in_same_ij = []
#             for arc in arcs_YT_to_Pick:
#                 if arc.i == ['YT', YT_index] and arc.j == ['Pick', Pick_index]:
#                     arcs_in_same_ij.append(arc)
#             # k가 1개보다 많으면
#             if len(arcs_in_same_ij) > 1:
#                # arcs_in_same_ij내에서 cost가 가장 작은 arc의 cost를 10000000으로 설정
#                 min_cost = 10000000
#                 for arc_ in arcs_in_same_ij:
#                     if arc_.cost < min_cost:
#                         min_cost = arc_.cost
#                 for arc__ in arcs_in_same_ij:
#                     if arc__.cost == min_cost:
#                         arc__.cost = 10000000
#                         break

#     # arcs_Pick_to_Drop을 순회하면서 같은 i, j내의 k개의 arc 중, cost가 가장 작은 arc의 cost를 1000000으로 설정
#     for Pick_index in range(number_of_Job):
#         for Drop_index in range(number_of_Job):
#             arcs_in_same_ij = []
#             for arc in arcs_Pick_to_Drop:
#                 if arc.i == ['Pick', Pick_index] and arc.j == ['Drop', Drop_index]:
#                     arcs_in_same_ij.append(arc)
#             # k가 1개보다 많으면
#             if len(arcs_in_same_ij) > 1:
#                # arcs_in_same_ij내에서 cost가 가장 작은 arc의 cost를 10000000으로 설정
#                 min_cost = 10000000
#                 for arc_ in arcs_in_same_ij:
#                     if arc_.cost < min_cost:
#                         min_cost = arc_.cost
#                 for arc__ in arcs_in_same_ij:
#                     if arc__.cost == min_cost:
#                         arc__.cost = 10000000
#                         break

#     # arcs_Drop_to_Pick을 순회하면서 같은 i, j내의 k개의 arc 중, cost가 가장 작은 arc의 cost를 1000000으로 설정
#     for Drop_index in range(number_of_Job):
#         for Pick_index in range(number_of_Job):
#             arcs_in_same_ij = []
#             for arc in arcs_Drop_to_Pick:
#                 if arc.i == ['Drop', Drop_index] and arc.j == ['Pick', Pick_index]:
#                     arcs_in_same_ij.append(arc)
#             # k가 1개보다 많으면
#             if len(arcs_in_same_ij) > 1:
#                # arcs_in_same_ij내에서 cost가 가장 작은 arc의 cost를 10000000으로 설정
#                 min_cost = 10000000
#                 for arc_ in arcs_in_same_ij:
#                     if arc_.cost < min_cost:
#                         min_cost = arc_.cost
#                 for arc__ in arcs_in_same_ij:
#                     if arc__.cost == min_cost:
#                         arc__.cost = 10000000
#                         break
# def change_second_min_arcs_cost_to_bignumber(arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, number_of_YT, number_of_Job, number_of_final_route):

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