import numpy as np

import make_arc
# import network_LP_final
import route_algorithm as ra

def main():

    # Parameter

    YT_locations = {0 : (4,2)}
    Job_locations = {0 : [(2,4), (5,6)], 1 : [(4,2), (8,0)]}
    number_of_final_route = 3
    alpha1 = 0.4
    alpha2 = 0.4
    alpha3 = 0.2
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
    grid = ra.grid
    now_count = np.zeros((len(grid), len(grid[0])))

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
    arcs_YT_to_Pick, arcs_Pick_to_Drop, arcs_Drop_to_Pick, arcs_Drop_to_Sink, arcs_YT_to_Sink = make_arc.create_arcs(
        YT_locations=YT_locations,
        Job_locations=Job_locations,
        number_of_final_route=number_of_final_route,
        alpha1=alpha1,
        alpha3=alpha3,
        prev_count=prev_count,
        grid=grid,
    )

    # print(arcs_Drop_to_Pick[2].path)
    for i in range(len(arcs_YT_to_Pick)):
        print(arcs_YT_to_Pick[i].index)

    # Run network_LP_final
    # network_LP_final.run(
    #     arcs_YT_to_Pick,
    #     arcs_Pick_to_Drop,
    #     arcs_Drop_to_Pick,
    #     arcs_Drop_to_Sink,
    #     arcs_YT_to_Sink,
    # )









if __name__ == "__main__":
    main()