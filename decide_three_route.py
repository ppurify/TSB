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

# start, finish 위치 랜덤 생성 + 블럭위치에는 생성 안되게
start = None
while start is None or grid[start] == -1:
    start = (np.random.randint(9), np.random.randint(7))

finish = None
while finish is None or grid[finish] == -1 or finish == start:
    finish = (np.random.randint(9), np.random.randint(7))

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

path = [start]
route = []
current = start
print(grid.shape)




def blue(current, finish, grid):
    candidate = []

    current = (current[0], current[1]-1)
    candidate.append(current)

    return candidate


def purple(current, finish, grid):
    candidate = []

    # start가 purple grid에 있을 때, 일단 모든 candidate 고려
    if len(path) == 1:
        for i in range(4):
            nx = current[0] + dx[i]
            ny = current[1] + dy[i]
            if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[current[0]+dx[i], current[1]+dy[i]] != -1:
                candidate.append((current[0]+dx[i], current[1]+dy[i]))
        
        # finish와 거리가 가장 가까운 candidate만 남기기
        distances = []
        for i in range(len(candidate)):
            distances.append(abs(candidate[i][0]-finish[0])+abs(candidate[i][1]-finish[1]))
        min_distance = min(distances)
        
        

    # 가는도중, 이전 위치 파악하여 이동방향대로 한칸 이동
    else:
        previous = path[-2]
        direction = (current[0]-previous[0], current[1]-previous[1])
        current = (current[0]+direction[0], current[1]+direction[1])
        candidate.append(current)

    return candidate



print(blue(current=current, finish=finish, grid=grid))















def green(current, finish, grid):
    candidate = []
    

    return candidate











def orange(current, finish, grid):
    candidate = []

    return candidate
    

# def move(start, finish, grid):
#     current = start

#     # if current == 왼쪽 가장자리 쪽 or 교차로 등이면 소요시간 변화 등 속성

#     while current != finish:
#         # Check the value of the current position in the grid
#         if grid[current] == 1:
#             current = (current[0], current[1]-1)
#         elif grid[current] == 2:
#             current = (current[0]+1, current[1])
#         elif grid[current] == 3:
#             current = (current[0], current[1]-1)
#         elif grid[current] == 4:
#             current = (current[0]-1, current[1])
#         else:
#             break
            
#     return current


# def move(start, finish, grid):
#     current = start
#     paths = [] # list to save different paths from start to finish
#     previous = None # variable to save the previous location

#     while current != finish:
#         # Save current location and update previous
#         paths.append(current)
#         previous = current

#         # Check the value of the current position in the grid
#         if grid[current] == 1:
#             current = (current[0], current[1]-1)

#         elif grid[current] == 2:
#             if previous[0] < current[0]:
#                 current = (current[0]+1, current[1])
#             elif previous[0] > current[0]:
#                 current = (current[0]-1, current[1])

#         elif grid[current] == 3:
#             if current[0] < finish[0]:
#                 current = (current[0]+1, current[1])
#             elif current[0] > finish[0]:
#                 current = (current[0]-1, current[1])
#             elif current[1] < finish[1]:
#                 current = (current[0], current[1]+1)
#             elif current[1] > finish[1]:
#                 current = (current[0], current[1]-1)

#         elif grid[current] == 4:
#             if previous[0] < current[0]:
#                 current = (current[0]+1, current[1])
#             elif previous[0] > current[0]:
#                 current = (current[0]-1, current[1])
#             elif current[1] < finish[1]:
#                 current = (current[0], current[1]+1)
#             elif current[1] > finish[1]:
#                 current = (current[0], current[1]-1)
                
#         elif grid[current] == -1:
#             print('start generated on blcok grid.')
#             break
#         else:
#             break
            
#     # Add the final location to the path and return the list of paths
#     paths.append(current)
#     return paths

