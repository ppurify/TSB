import numpy as np


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

    current = (current[0], current[1]-1)
    candidate.append(current)

    return candidate


# 최단거리 , 이미간길 고려순서 !!!!!!!!
def purple(current, finish, grid, path):
    temp_candidate = []
    candidate = []
    distances = []

    # start가 purple grid에 있을 때, 일단 모든 candidate 고려
    # if len(path) == 1:
    for i in range(4):
        nx = current[0] + dx[i]
        ny = current[1] + dy[i]
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1:
            if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
                temp_candidate.append((nx, ny))
                distances.append(abs(nx - finish[0]) + abs(ny - finish[1]))

    # finish와 거리가 가장 가까운 candidate만 남기기 다시말해, finish와 가까운 좌표만 남김
    min_distance = min(distances)

    for i in range(len(temp_candidate)):
        if distances[i] == min_distance and temp_candidate[i] not in path:
            candidate.append(temp_candidate[i])
    
    # 가는도중, 이전 위치 파악하여 이동방향대로 한칸 이동
    # else:
    #     previous = path[-2]
    #     direction = (current[0]-previous[0], current[1]-previous[1])
    #     current = (current[0]+direction[0], current[1]+direction[1])
    #     candidate.append(current)

    return candidate



def green(current, finish, grid, path):
    temp_candidate = []
    candidate = []
    distances = []

    for i in range(4):
        nx = current[0] + dx[i]
        ny = current[1] + dy[i]
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1:
            # 역주행으로 blue로 가는 경우 제외
            if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
                temp_candidate.append((nx, ny))
                distances.append(abs(nx - finish[0])+abs(ny - finish[1]))

    min_distance = min(distances)

    for i in range(len(temp_candidate)):
        if distances[i] == min_distance and temp_candidate[i] not in path:
            candidate.append(temp_candidate[i])    

    return candidate



# 무조건 갈래길 다 candidate
def orange(current, finish, grid, path):
    candidate = []

    for i in range(4):
        nx = current[0] + dx[i]
        ny = current[1] + dy[i]
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1:
            # 역주행으로 blue로 가는 경우 제외
            if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
                if (nx, ny) not in path:
                    candidate.append((nx, ny))
    
    return candidate



# 1. 밟았던건 안밟게 !! path 리스트 활용
# 2. if current == 왼쪽 가장자리 쪽 or 교차로 등이면 소요시간 변화 등 속성
# 3. finish에 도착하면 끝내기
# def move(start, finish, grid):
#     path = [start]
#     route = []
#     current = start

    
#     while current != finish:
#         if grid[current] == 1:
#             candidate = blue(current, finish, grid)
#         elif grid[current] == 2:
#             candidate = purple(current, finish, grid)
#         elif grid[current] == 3:
#             candidate = green(current, finish, grid)
#         elif grid[current] == 4:
#             candidate = orange(current, finish, grid)

#         # 도착하면(current == finish) 종료
#         for i in range(len(candidate)):
#             if candidate[i] == finish:
#                 path.append(candidate[i])
#                 break
    
#     return candidate




start = (0,6)
finish = (2,4)
path = []
route = []
current = start



def move(current, finish, grid, path, route):
    print('current : ', current)
    path.append(current)
    # if len(path)>= 25: # 무한루프 방지
    #     return
    print('path : ', path)

    # Get possible moves based on color of current cell
    color = grid[current[0], current[1]]
    print('color : ', color)
    if color == 1:
        candidate = blue(current, finish, grid, path)
    elif color == 2:
        candidate = purple(current, finish, grid, path)
    elif color == 3:
        candidate = green(current, finish, grid, path)
    elif color == 4:
        candidate = orange(current, finish, grid, path)
    else:
        print('Invalid color')
        return
    print('candidate : ', candidate)

    # 갈곳 없으면 종료
    if len(candidate) == 0 :
        return
    



    # candidate 방문
    for next_move in candidate:
        if next_move == finish:
            # If next_move is finish, add completed path to route
            route.append(path + [finish])
        else:
            # Continue recursively visiting candidate
            new_path = path.copy()
            move(next_move, finish, grid, new_path, route)

            
    # # 각 candidate 방문
    # for i in range(len(candidate)):
    #     next_move = candidate[i]
    #     # candidate가 finish면 종료
    #     if next_move == finish:
    #         route.append(path + [next_move])
    #         print('route complete. next_move : ', next_move)
    #         print('route : ', route)
    #         continue

    #     # 경로 이동
    #     move(next_move, finish, grid, path, route)
   
    return
# The main changes to the function include:

# Adding the path and route parameters. path keeps track of the visited coordinates in the current path, and route is a list of all the valid paths found so far.
# Recursively calling move() for each candidate and updating path and route accordingly.
# Checking if the candidate has already been visited in the path and skipping it if so.
# If the candidate is the finish, adding the current path to route.
# Removing the return statement as the function no longer needs to return anything.


move(current = current, finish = finish, grid = grid, path = path, route = route)

# print(current)
# print(finish)
# print(grid)
# print(path)
for i in range(len(route)):
    print(route[i])
    print()

print(len(route))






def move(current, finish, grid, path):
    if current == finish:
        return path

    color = grid[current]
    visited = set(path)

    if color == 1: # blue
        candidate = blue(current, finish, grid)
    
    elif color == 2: # purple
        candidate = purple(current, finish, grid)

    elif color == 3: # green
        candidate = green(current, finish, grid)

    elif color == 4: # orange
        candidate = orange(current, finish, grid)

    paths = []
    for c in candidate:
        if c not in visited:
            new_path = path.copy()
            new_path.append(current)
            sub_path = move(c, finish, grid, new_path)
            if sub_path:
                paths.append(sub_path)

    return paths



# # The changes I made are as follows:

# # The function is now recursive, so when there are multiple candidates, it calls itself for each of them and combines the resulting paths into a list of paths.
# # The function now takes an additional argument, path, which is a list of coordinates visited so far. This list is appended with the current coordinates but is checked to avoid visiting previously visited coordinates again.
# # When the current coordinates are equal to the finish coordinates, the function returns the path visited so far and doesn't continue the recursive call. The path visited so far is also appended to the list of possible paths, which will be later sorted by length to get the shortest path.
















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

# # In the above code, the move function now takes two additional arguments - path and route. path is a list that stores the coordinates visited so far, and route is a list that stores all the paths from start to finish. The move function recursively traverses the candidates returned by each color function. Before traversing each candidate, the move function checks if the candidate has not been visited before (i.e., not in the path list). If the candidate is not visited, it appends the current coordinates to the path list and recursively traverses the candidate. After traversing the candidate, the move function removes the current coordinates from the path list. If the current coordinates are equal to the finish coordinates, the move function appends a copy of the path list to the route list.

















# def move(current, finish, grid, path):
#     if current == finish:
#         routes.append(path.copy())
#         return
#     for candidate in blue(current, finish, grid) + purple(current, finish, grid) + green(current, finish, grid) + orange(current, finish, grid):
#         if candidate not in path:
#             move(candidate, finish, grid, path + [candidate])


# # Here's a brief explanation of the changes made:

# # Instead of using a while loop, the move function is now defined recursively. This means that the function calls itself with a new set of arguments until the current coordinates equal the finish coordinates.
# # The path parameter is passed to the function and is used to keep track of the current path taken to reach the current coordinates. This is a list of tuples, where each tuple represents the coordinates of a cell on the grid. The path is initially an empty list [], but as the function is called recursively, the path is appended with new coordinates at each step. The path parameter is also checked to make sure that the current coordinates have not already been visited. If the candidate coordinates are already in the path list, they are skipped and not considered as possible candidates for the next step.
# # If the current coordinates equal the finish coordinates, the path list is appended to the routes list of all possible routes.
# # Instead of returning the list of candidates, the move function now loops over the candidates returned by each of the four direction functions (blue, purple, green, and orange) and calls itself recursively with the new candidate coordinates and the updated path list. Note that the path list passed to the recursive call is a new list created by appending the candidate to the previous path. This ensures that the previous path list is not modified by the recursive call, which could cause issues when backtracking.












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


# # Here are the changes I made to the original function:

# # I added visited parameter to the function to keep track of the visited coordinates. This will be used to avoid revisiting the same coordinate again.
# # I added path parameter to the function to keep track of the path list.
# # Instead of returning the candidate list, I used a loop to traverse the returned candidates and recursively execute the move function with the new coordinates.
# # I created a copy of the path list before recursively executing the move function with the new coordinates to avoid modifying it for other traversals.
# # I added a condition to check if the current coordinates are equal to the finish coordinates. If so, I appended the path list so far into the route list.

















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

