import numpy as np

def Grid(_grid_length, _grid_height, _block_length, _block_height, _block_num_in_row):
    
    # Grid 생성
    # length by height
    grid = np.zeros((_grid_height, _grid_length), dtype = int)
    
    one_way_index = []
    block_row_index = []


    # Fill in corners with value 4
    for i in range(_grid_height):
        if (i == 0) | (i % (_block_height + 1) == 0):
            grid[i, 0] = 4
            grid[i, -1] = 4

            if (i!=0) & (i!=_grid_height-1):
                one_way_index.append(i)
    
    # Block 행 index
    for i in range(len(one_way_index)):
        block_row_index.append(one_way_index[i] - 1)
        
        if(i == len(one_way_index) - 1):
            block_row_index.append(one_way_index[i] + 1)
            
    # 양방향
    for i in range(_block_num_in_row):
        grid[0, i * _block_length + (i + 1) : (i + 1) * _block_length + (i + 1)] = 2
        grid[-1, i * _block_length + (i + 1) : (i + 1) * _block_length + (i + 1)] = 2
        
        if i != 0:
            grid[0, i * _block_length + i] = 4
            grid[-1, i * _block_length + i] = 4

    
    # 단방향 1
    for i in one_way_index:
        for j in range(_block_num_in_row):
            grid[i, j * _block_length + (j+1) : (j+1) * _block_length + (j+1) ] = 1
            if j != 0:
                grid[i, j*_block_length + j] = 4
    
    # Block 있는 곳은 -1
    for i in block_row_index:
        grid[i, -1] = 2
        for j in range(_block_num_in_row):
            grid[i, j * _block_length + (j+1) : (j+1) * _block_length + (j+1)] = -1
            grid[i, j*_block_length + j] = 2
        
    # block 칸에서 뒤에서 2번째 column에 YT 생성
    YT_location_diff_index = 2
    
    _YT_location_col_index = []
    Job_location_col_index = []
    # _YC_location_row_index = one_way_index + 
    _QC_locations = []
    _YC_locations = []
    
    # index of YT Column and add QC location
    for i in range(_block_num_in_row):
        _YT_location_col_index.append((i+1) * (_block_length + 1) - YT_location_diff_index - 1)
        Job_location_col_index.append((i+1) * (_block_length + 1) - round(_block_length / 2) - 1)
        _QC_locations.append((0, Job_location_col_index[i]))
        
    
    # Add YC location
    for i in block_row_index:
        for j in Job_location_col_index:
            _YC_locations.append((i + 1, j)) 
    
    return grid, _YT_location_col_index, _QC_locations, _YC_locations