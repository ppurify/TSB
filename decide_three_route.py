import numpy as np
import matplotlib.pyplot as plt
import time

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




start = (0,6)
finish = (0,4)
path = []
route = []




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

move(start, finish, grid, path, route)

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


number_of_YT = 5
number_of_job = 5000

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

before_grid = np.array([
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

parameter1 = 0.4
parameter2 = 0.3
parameter3 = 0.3







grid_for_count = np.zeros_like(grid)

#현재 시각
start_time = time.time()

for i in range(number_of_job) :
    start = None
    finish = None

    while start is None or grid[start] == -1 or finish is None or grid[finish] == -1 or finish == start:
        start = (np.random.randint(9), np.random.randint(7))
        finish = (np.random.randint(9), np.random.randint(7))
    print()
    print("start : ", start)
    print("finish : ", finish)

    path = []
    route = []
    current = start
    move(current, finish, grid, path, route)

    if len(route) > 3:
        # 아크로 선정될 3개의 경로 추리기
        pass
    else:
        # 발견된 루트 다 arc로 반영. 모자랑 arc는 cost inf로 정해서 dummy arc 생성
        pass
    print('Number of completed paths : ', len(route))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    

# start = (6,2)
# finish = (6,5)

# path = []
# rout = []
# current = start
# move(current, finish, grid, path, route)
# for i in range(len(route)):
#     print(route[i])
#     print()
# print('Number of completed paths : ', len(route))





    for path in route:
        for point in path:
            grid_for_count[point] += 1

    print(grid_for_count)





end_time = time.time()
print("소요시간 : ", end_time - start_time)









# def move(current, finish, grid, path):
#     if current == finish:
#         return path

#     color = grid[current]
#     visited = set(path)

#     if color == 1: # blue
#         candidate = blue(current, finish, grid)
    
#     elif color == 2: # purple
#         candidate = purple(current, finish, grid)

#     elif color == 3: # green
#         candidate = green(current, finish, grid)

#     elif color == 4: # orange
#         candidate = orange(current, finish, grid)

#     paths = []
#     for c in candidate:
#         if c not in visited:
#             new_path = path.copy()
#             new_path.append(current)
#             sub_path = move(c, finish, grid, new_path)
#             if sub_path:
#                 paths.append(sub_path)

#     return paths









# def move(current, finish, grid, path, route):
#     if current == finish:
#         route.append(path[:]) # append a copy of the path list to the route list
#         return

#     color = grid[current]
#     candidates = []
#     if color == 1:
#         candidates = blue(current, finish, grid)
#     elif color == 2:
#         candidates = purple(current, finish, grid)
#     elif color == 3:
#         candidates = green(current, finish, grid)
#     elif color == 4:
#         candidates = orange(current, finish, grid)

#     for candidate in candidates:
#         if candidate not in path: # check if candidate is not visited before
#             path.append(candidate) # append current coordinates to path list
#             move(candidate, finish, grid, path, route) # recursively traverse the candidate
#             path.pop() # remove current coordinates from path list after traversing it










# def move(current, finish, grid, path):
#     if current == finish:
#         routes.append(path.copy())
#         return
#     for candidate in blue(current, finish, grid) + purple(current, finish, grid) + green(current, finish, grid) + orange(current, finish, grid):
#         if candidate not in path:
#             move(candidate, finish, grid, path + [candidate])









# def move(current, finish, grid, visited, path, routes):
#     # Get the possible directions based on the current block color.
#     color = grid[current]
#     if color == 1:
#         candidate = blue(current, finish, grid)
#     elif color == 2:
#         candidate = purple(current, finish, grid)
#     elif color == 3:
#         candidate = green(current, finish, grid)
#     elif color == 4:
#         candidate = orange(current, finish, grid)
#     else:
#         print('Invalid block color!')
#         return

#     # Append the current coordinates to the path list.
#     path.append(current)

#     # Recursively execute the move function by traversing the returned candidates.
#     for coord in candidate:
#         if coord not in visited:
#             # Create a copy of the path list to avoid modifying it for other traversals.
#             path_copy = path.copy()
#             # Recursively execute the move function with the new coordinates.
#             move(coord, finish, grid, visited + [current], path_copy, routes)

#     # When current coordinates are equals to finish coordinates, end the while loop and insert the path list so far into route list.
#     if current == finish:
#         routes.append(path)












# def move(current, finish, grid, path, visited, route):
#     if current == finish:
#         path.append(current)
#         route.append(path)
#         return
#     visited.add(current)
#     for candidate in get_candidates(current, finish, grid, visited):
#         new_path = path + [current]
#         move(candidate, finish, grid, new_path, visited, route)

# def get_candidates(current, finish, grid, visited):
#     color = grid[current]
#     if color == 1: # red
#         return []
#     elif color == 2: # blue
#         return blue(current, finish, grid, visited)
#     elif color == 3: # purple
#         return purple(current, finish, grid, visited)
#     elif color == 4: # green
#         return green(current, finish, grid, visited)
#     elif color == 5: # orange
#         return orange(current, finish, grid, visited)

# def blue(current, finish, grid, visited):
#     candidate = []
#     x, y = current
#     if y > 0 and grid[x, y-1] != -1 and (x, y-1) not in visited:
#         candidate.append((x, y-1))
#     return candidate

# def purple(current, finish, grid, visited):
#     temp_candidate = []
#     candidate = []
#     distances = []

#     for i in range(4):
#         nx = current[0] + dx[i]
#         ny = current[1] + dy[i]
#         if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1 and (nx, ny) not in visited:
#             if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
#                 temp_candidate.append((nx, ny))
#                 distances.append(abs(nx - finish[0]) + abs(ny - finish[1]))

#     min_distance = min(distances)

#     for i in range(len(temp_candidate)):
#         if distances[i] == min_distance:
#             candidate.append(temp_candidate[i])
#     return candidate

# def green(current, finish, grid, visited):
#     temp_candidate = []
#     candidate = []
#     distances = []

#     for i in range(4):
#         nx = current[0] + dx[i]
#         ny = current[1] + dy[i]
#         if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1 and (nx, ny) not in visited:
#             if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
#                 temp_candidate.append((nx, ny))
#                 distances.append(abs(nx - finish[0])+abs(ny - finish[1]))

