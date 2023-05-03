import numpy as np
import matplotlib.pyplot as plt
import time

import heapq

# parameter(have to set by yourself)
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

# start, finish 위치 랜덤 생성 + 블럭위치에는 생성 안되게 + start, finish가 같지 않게
start = None
finish = None

while start is None or grid[start] == -1 or finish is None or grid[finish] == -1 or finish == start:
    start = (np.random.randint(9), np.random.randint(7))
    finish = (np.random.randint(9), np.random.randint(7))

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

to_right = (0,1)


def blue(current, finish, grid, path):
    candidate = []

    nx = current[0]
    ny = current[1] - 1
    if (nx,ny) not in path and 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1:
        candidate.append((nx, ny))

    return candidate


# 최단거리 , 이미간길 고려순서 !!!!!!!!
# def purple(current, finish, grid, path):
#     temp_candidate = []
#     candidate = []
#     distances = []

#     # start가 purple grid에 있을 때, 일단 모든 candidate 고려
#     # if len(path) == 1:
#     for i in range(4):
#         nx = current[0] + dx[i]
#         ny = current[1] + dy[i]1. 
#         # 그리드 범위 안에 있고, Block이 아니고, 이미 간 길이 아닌 경우만
#         if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1 and (nx, ny) not in path:
#             # 역주행으로 blue로 가는 경우 제외
#             if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
#                 temp_candidate.append((nx, ny))
#                 distances.append(abs(nx - finish[0]) + abs(ny - finish[1]))

#     # finish와 거리가 가장 가까운 candidate만 남기기 다시말해, finish와 가까운 좌표만 남김
#     min_distance = min(distances)

#     for i in range(len(temp_candidate)):
#         if distances[i] == min_distance:
#             candidate.append(temp_candidate[i])
    
#     # 가는도중, 이전 위치 파악하여 이동방향대로 한칸 이동
#     # else:
#     #     previous = path[-2]
#     #     direction = (current[0]-previous[0], current[1]-previous[1])
#     #     current = (current[0]+direction[0], current[1]+direction[1])
#     #     candidate.append(current)

#     return candidate



def purple(current, finish, grid, path):
    temp_candidate = []
    distances = []

    # start가 purple grid에 있을 때, 일단 모든 candidate 고려
    for i in range(4):
        nx = current[0] + dx[i]
        ny = current[1] + dy[i]
        # 그리드 범위 안에 있고, Block이 아니고, 이미 간 길이 아닌 경우만
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1 and (nx, ny) not in path:
            # 역주행으로 blue로 가는 경우 제외
            if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
                temp_candidate.append((nx, ny))
                distances.append(abs(nx - finish[0]) + abs(ny - finish[1]))

    # finish와 거리가 가장 가까운 candidate만 남기기 다시말해, finish와 가까운 좌표만 남김
    if len(temp_candidate) == 0:
        candidate = []
    else:
        min_distance = min(distances)
        candidate = [c for i, c in enumerate(temp_candidate) if distances[i] == min_distance]

    return candidate



def green(current, finish, grid, path):
    temp_candidate = []
    distances = []

    for i in range(4):
        nx = current[0] + dx[i]
        ny = current[1] + dy[i]
        # 그리드 범위 안에 있고, Block이 아니고, 이미 간 길이 아닌 경우만
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1 and (nx, ny) not in path:
            # 역주행으로 blue로 가는 경우 제외
            if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
                temp_candidate.append((nx, ny))
                distances.append(abs(nx - finish[0])+abs(ny - finish[1]))
                
    # finish와 거리가 가장 가까운 candidate만 남기기 다시말해, finish와 가까운 좌표만 남김
    if len(temp_candidate) == 0:
        candidate = []
    else:
        min_distance = min(distances)
        candidate = [c for i, c in enumerate(temp_candidate) if distances[i] == min_distance]

    return candidate



# 무조건 갈래길 다 candidate
def orange(current, finish, grid, path):
    candidate = []

    for i in range(4):
        nx = current[0] + dx[i]
        ny = current[1] + dy[i]
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1 and (nx, ny) not in path:
            # 역주행으로 blue로 가는 경우 제외
            if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
                candidate.append((nx, ny))
    
    return candidate




# start = (0,6)
# finish = (0,4)
# path = []
# route = []




# 1. 밟았던건 안밟게. path 리스트 활용
# 2. 추후 if current == 왼쪽 가장자리 쪽 or 교차로 등이면 소요시간 변화 등 속성
# 3. 
def move(current, finish, grid, path, route):
    #print('current : ', current)

    path.append(current)
    #print('path : ', path)

    color = grid[current[0], current[1]]
    #print('color : ', color)
    if color == 1:
        candidate = blue(current, finish, grid, path)
    elif color == 2:
        candidate = purple(current, finish, grid, path)
    elif color == 3:
        candidate = green(current, finish, grid, path)
    elif color == 4:
        candidate = orange(current, finish, grid, path)
    else:
        print('Invalid color. terminating.')
        return
    #print('candidate : ', candidate)

    # 갈곳 없으면 종료
    if len(candidate) == 0 :
        #print('This path is dead end.', 'path : ', path)
        return

    # candidate 방문
    for next_move in candidate:
        if next_move == finish:
            # If next_move is finish, add completed path to route
            #print('got finish, completed path : ', path + [next_move]) 
            route.append(path + [next_move])
        else:
            # Continue recursively visiting candidate
            new_path = path.copy()
            move(next_move, finish, grid, new_path, route)

    return

# print(move(start, finish, grid, path, route))

# for i in range(len(grid)):
#     for j in range(len(grid[0])):
#         for k in range(len(grid)):
#             for p in range(len(grid[0])):
#                 start = (i,j)
#                 finish = (k,p)
#                 path = []
#                 route = []
#                 current = start
#                 if grid[start[0], start[1]] == -1 or grid[finish[0], finish[1]] == -1:
#                     continue
#                 move(current, finish, grid, path, route)
#                 print('start : ', start, 'finish : ', finish)
#                 print('Number of completed paths : ', len(route))


# for i in range(len(route)):
#     print(route[i])
#     print()

# print(route)




# for i in range(number_of_YT):
#     while YT_location is None or grid[YT_location] == -1:
#         YT_location = (np.random.randint(9), np.random.randint(7))

#     for j in range(number_of_job) : 
#         start = None
#         finish = None

#         while start is None or grid[start] == -1 or finish is None or grid[finish] == -1 or YT_location == start or start == finish :
#             start = (np.random.randint(9), np.random.randint(7))
#             finish = (np.random.randint(9), np.random.randint(7))

#         print("YT_location : ", YT_location)
#         print("start : ", start)
#         print("finish : ", finish)


#         path = []
#         route = []
#         current = YT_location
#         move(current, finish, grid, path, route)
#         print('Number of completed paths : ', len(route))
#         print()




def penalty(prev_grid, route, alpha1, alpha3):
    penalty_list = []

    for i in range(len(route)):
        
        sum_of_counter_of_prev_grid = 0
        sum_of_move = len(route[i])
        for j in range(len(route[i])):
            sum_of_counter_of_prev_grid += prev_grid[(route[i][j][0], route[i][j][1])]

        # 각 경로의 penalty 산출하여 리스트에 저장
        penalty_list.append((alpha1 * sum_of_counter_of_prev_grid) + (alpha3 * sum_of_move))

    # penalty가 가장 작은 3개의 경로의 인덱스를 추출하여 final_three_route 리스트에 저장
    final_three_route_idx = heapq.nsmallest(3, range(len(penalty_list)), key=penalty_list.__getitem__)
    final_three_route = [route[i] for i in final_three_route_idx]

    print(penalty_list)
    print(final_three_route)

    return final_three_route



prev_grid = np.array([
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

alpha1 = 0.4
alpha2 = 0.3
alpha3 = 0.3


number_of_YT = 1
number_of_job = 1


YT_position = None
Pick_position = None
Drop_position = None




# route = [[(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (7, 6), (6, 6), (6, 5), (6, 4), (5, 4), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6)],
#          [(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (7, 6), (6, 6), (5, 6)],
#          [(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (7, 4), (6, 4), (5, 4), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6)],
#          [(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6)],
#          [(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (2, 5), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (8, 5), (8, 6), (7, 6), (6, 6), (5, 6)],
#          [(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (8, 5), (8, 6), (7, 6), (6, 6), (5, 6)],
#          [(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6)],
#          [(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (4, 5), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (8, 5), (8, 6), (7, 6), (6, 6), (5, 6)],
#          [(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (2, 5), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (8, 5), (8, 6), (7, 6), (6, 6), (5, 6)],
#          [(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (8, 5), (8, 6), (7, 6), (6, 6), (5, 6)]]

# for i in range(len(penalty(prev_grid=prev_grid, route=route, alpha1=0.5, alpha3=0.3))):
#     print(penalty(prev_grid=prev_grid, route=route, alpha1=0.5, alpha3=0.3)[i])

# penalty(prev_grid=prev_grid, route=route, alpha1=0.5, alpha3=0.3)


YT_positions = {}
Job_positions = {}



# 스케줄링 대상 YT 생성
for i in range(number_of_YT):
    while YT_position is None or grid[YT_position] == -1:
        YT_position = (np.random.randint(9), np.random.randint(7))
    YT_positions[i] = YT_position

# 스케줄링 대상 작업 생성
for j in range(number_of_job):
    while Pick_position is None or grid[Pick_position] == -1 or Drop_position is None or grid[Drop_position] == -1 or finish == start:
        Pick_position = (np.random.randint(9), np.random.randint(7))
        Drop_position = (np.random.randint(9), np.random.randint(7))
    Job_positions[j] = [Pick_position, Drop_position]
  
  
# print('YT_positions : ', YT_positions)
# print('Job_positions : ', Job_positions[0][1])


for i in range(number_of_YT):
    for j in range(number_of_job):
        YT_position = YT_positions[i]
        Pick_position = Job_positions[j][0]
        Drop_position = Job_positions[j][1]

        path_YT_to_Pick = []
        route_YT_to_Pick = []

        path_Pick_to_Drop = []
        route_Pick_to_Drop = []

        move(YT_position, Pick_position, grid, path_YT_to_Pick, route_YT_to_Pick)
        move(Pick_position, Drop_position, grid, path_Pick_to_Drop, route_Pick_to_Drop)

        print('length of route_YT_to_Pick : ', route_YT_to_Pick)
        # print('route_YT_to_Pick : ', route_YT_to_Pick)
        print('')
        print('length of route_Pick_to_Drop : ', route_Pick_to_Drop)
        # print('route_Pick_to_Drop : ', route_Pick_to_Drop)


        # 경로 수가 3개보다 많으면 패널티 함수 통해 3개로 줄이기
        if len(route_YT_to_Pick) > 3 :
            final_route_YT_to_Pick = penalty(prev_grid, route_YT_to_Pick, alpha1=alpha1, alpha3=alpha3)
        # 그렇지 않으면 (더미 추가했지만 더미 경로 내용 안정해줌 !!)
        else:
            number_of_route_YT_to_Pick = len(route_YT_to_Pick)
            for i in range(3 - number_of_route_YT_to_Pick):
                route_YT_to_Pick.append(route_YT_to_Pick[-1])

            final_route_YT_to_Pick = route_YT_to_Pick

        if len(route_Pick_to_Drop) > 3 :
            final_route_Pick_to_Drop = penalty(prev_grid, route_Pick_to_Drop, alpha1=alpha1, alpha3=alpha3)
        
        # 그렇지 않으면 (더미 추가했지만 더미 경로 내용 안정해줌 !!)
        else:
            number_of_route_Pick_to_Drop = len(route_Pick_to_Drop)
            for i in range(3 - number_of_route_Pick_to_Drop):
                route_Pick_to_Drop.append(route_Pick_to_Drop[-1])

            final_route_Pick_to_Drop = route_Pick_to_Drop

        

        












# now_grid = np.zeros_like(grid)

# #현재 시각
# start_time = time.time()

# for i in range(number_of_job) :
#     start = None
#     finish = None

#     while start is None or grid[start] == -1 or finish is None or grid[finish] == -1 or finish == start:
#         start = (np.random.randint(9), np.random.randint(7))
#         finish = (np.random.randint(9), np.random.randint(7))
#     print()
#     print("start : ", start)
#     print("finish : ", finish)

#     path = []
#     route = []
#     current = start
#     move(current, finish, grid, path, route)

#     if len(route) > 3:
#         # 아크로 선정될 3개의 경로 추리기
#         pass
#     else:
#         # 발견된 루트 다 arc로 반영. 모자랑 arc는 cost inf로 정해서 dummy arc 생성
#         pass
#     print('Number of completed paths : ', len(route))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    

# # start = (6,2)
# # finish = (6,5)

# # path = []
# # rout = []
# # current = start.
# # move(current, finish, grid, path, route)
# # for i in range(len(route)):
# #     print(route[i])
# #     print()
# # print('Number of completed paths : ', len(route))


#     for path in route:
#         for point in path:
#             now_grid[point] += 1

#     print(now_grid)





# end_time = time.time()
# print("소요시간 : ", end_time - start_time)







