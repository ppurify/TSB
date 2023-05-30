import numpy as np
import pandas as pd

import make_arc
import network_LP_final
import route_algorithm as ra

def main():
    # Parameter
    YT_locations = {0 : (4,2), 1 : (8,0)}
    Job_locations = {0 : [(2,4), (5,6)], 1 : [(4,2), (8,0)]}
    number_of_final_route = 3
    alpha1 = 0.4
    alpha2 = 0.4
    alpha3 = 0.3
    prev_count = np.array([
    [4, 2, 3, 2, 3, 2, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 1, 3, 1, 3, 1, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 1, 3, 1, 3, 1, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 1, 3, 1, 3, 1, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 2, 3, 2, 3, 2, 4],
    ])

    grid = np.array([
    [4, 2, 3, 2, 3, 2, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 1, 3, 1, 3, 1, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 1, 3, 1, 3, 1, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 1, 3, 1, 3, 1, 4],
    [2, -1, 2, -1, 2, -1, 2],
    [4, 2, 3, 2, 3, 2, 4],
    ])

    # grid = np.array([
    #     [4, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 4],
    #     [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
    #     [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
    #     [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
    #     [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
    #     [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
    #     [4, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 4],
    #     [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
    #     [4, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2 ,3, 2, 2, 2, 2, 2, 4]
    # ])

    ra.set_grid(grid)
    now_count = np.zeros((len(grid), len(grid[0])))

    number_of_YT = len(YT_locations)
    number_of_Job = len(Job_locations)

    # # 스케줄링 대상 YT 생성
    # for i in range(number_of_YT):
    #     YT_location = None
    #     while YT_location is None or grid[YT_location] == -1:
    #         YT_location = (np.random.randint(9), np.random.randint(7))
    #     YT_locations[i] = YT_location
        
    # # 스케줄링 대상 작업 생성
    # for j in range(number_of_job):
    #     Pick_location = None
    #     Drop_location = None
    #     while Pick_location is None or grid[Pick_location] == -1 or Drop_location is None or grid[Drop_location] == -1 or Pick_location == Drop_location:
    #         Pick_location = (np.random.randint(9), np.random.randint(7))
    #         Drop_location = (np.random.randint(9), np.random.randint(7))
    #     Job_locations[j] = [Pick_location, Drop_location]

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

    # Run network_LP_final
    objective_value, activated_arcs = network_LP_final.solve(all_arcs, number_of_YT, number_of_Job)
    
    # print('objective_value: ', objective_value)
    # print('activated_arcs: ', activated_arcs)


    # 각 YT들이 어떤 경로로 이동하는지 저장하는 dictionary
    YT_traversing_arc = {}

    arcs_for_YT_traverse = activated_arcs.copy()

    # 딕셔너리에 key로 YT들 먼저 추가
    for _ in range(number_of_YT):
        for arc in arcs_for_YT_traverse:
        # 만약 arc의 i에 YT가 포함되고 아직 YT_traversing_arc에 추가되지 않았다면
            if (arc.i == ['YT', _]) and tuple(arc.i) not in YT_traversing_arc.keys():
                YT_traversing_arc[tuple(arc.i)] = [arc]
                arcs_for_YT_traverse.remove(arc)
                break


    # arcs_for_YT_traverse에 원소가 남아있는 동안
    while arcs_for_YT_traverse != []:
        for arc in arcs_for_YT_traverse:
             # YT_traversing_arc의 모든 value를 돌면서
            for values in YT_traversing_arc.values():
                for value in values:
                    # 만약 arc의 i가 value의 j와 같다면
                    if arc.i == value.j:
                        # 해당 value 뒤에 해당 arc를 추가
                        values.append(arc)
                        arcs_for_YT_traverse.remove(arc)
                        break

    # for v in YT_traversing_arc.values():
    #     for arc in v:
    #         print(arc.i, arc.j)

if __name__ == "__main__":
    main()