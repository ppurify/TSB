import numpy as np
import matplotlib.pyplot as plt


def set_grid(input_grid):
    global grid
    grid = input_grid

# parameter
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
to_right = (0,1)


# Type1 : one_way
def one_way(current, finish, grid, path):
    candidate = []

    nx = current[0]
    ny = current[1] - 1
    if (nx,ny) not in path and 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1:
        candidate.append((nx, ny))
    return candidate


# Type2 : Two_way
def two_way(current, finish, grid, path):
    candidate = []

    # start가 two_way grid에 있을 때, 일단 모든 candidate 고려
    for i in range(4):
        nx = current[0] + dx[i]
        ny = current[1] + dy[i]
        # 그리드 범위 안에 있고, Block이 아니고, 이미 간 길이 아닌 경우만
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1 and (nx, ny) not in path:
            # 역주행으로 one_way로 가는 경우 제외
            if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
                candidate.append((nx, ny))
    return candidate


# Type3 : Intersection
def intersection(current, finish, grid, path):
    candidate = []

    for i in range(4):
        nx = current[0] + dx[i]
        ny = current[1] + dy[i]
        # 그리드 범위 안에 있고, Block이 아니고, 이미 간 길이 아닌 경우만
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != -1 and (nx, ny) not in path:
            # 역주행으로 one_way로 가는 경우 제외
            if not ((nx - current[0], ny - current[1]) == to_right and grid[nx, ny]) == 1:
                candidate.append((nx, ny))
    return candidate



# 1. 밟았던건 안밟게. path 리스트 활용
# 2. 추후 if current == 왼쪽 가장자리 쪽 or 교차로 등이면 소요시간 변화 등 속성
# 3. current = finish면 route에 current좌표만 추가하고 종료
# 4. To do : path 라는 변수 없이 move 함수 내에서 path 리스트 만들어서 재귀적으로 돌리기
def move(current, finish, grid, path, route):
    if current == finish:
        route = [[current]]
        return route
    
    
    #print('current : ', current)

    path.append(current)
    #print('path : ', path)

    color = grid[current[0], current[1]]
    #print('color : ', color)
    if color == 1:
        candidate = one_way(current, finish, grid, path)
    elif color == 2:
        candidate = two_way(current, finish, grid, path)
    elif color == 3:
        candidate = intersection(current, finish, grid, path)
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
            route.append(path + [next_move])
        else:
            # Continue recursively visiting candidate
            new_path = path.copy()
            move(next_move, finish, grid, new_path, route)

    return route