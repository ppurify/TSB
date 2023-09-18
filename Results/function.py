import csv
import os
import matplotlib.pyplot as plt
import re
import pandas as pd

def load_csv_file(file_path):
    data = []

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            data.append(row)

    return data


def load_csv_files_in_folder(folder_path):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    all_csv_data = []

    for csv_file in csv_files:
        csv_path = os.path.join(folder_path, csv_file)
        csv_data = load_csv_file(csv_path)
        all_csv_data.append((csv_file, csv_data))

    return all_csv_data

# ------------------------------------------------------------------------------

# To Variance 
def extract_YT_A_data(data, keyword):
    new_data = []
    
    for row in data:
        if keyword in row:
            new_data.append(row)
    
    return new_data

def create_YT_A_Data(_keyword, _variance_all_csv_data):
    _data_list = []
    
    for csv_file, csv_data in _variance_all_csv_data:
        
        _extract_YT_A_data = extract_YT_A_data(csv_data, _keyword)

        # Extract the number after the first occurrence of "Truck"
        match  = re.search(r"Truck_(\d+)", csv_file)
        if match:
            truck_number = match.group(1)
            # prev 없을 때
            if truck_number == "1":
                truck_number = "0"
            # print("prev Truck Number:", truck_number)
            # print(f"Extracted data from {csv_file} where '{_keyword}' exists:")
            for row in _extract_YT_A_data:
                row[4:] = [float(value) for value in row[4:]]
                new_row = row + [truck_number]
                # print(row) 
                _data_list.append(new_row)
            # print("=" * 80)
            
        else:
            print("Truck number not found.")
            
    original_column_names = _variance_all_csv_data[0][1][0]
    _column_names = [column.strip() for column in original_column_names] + ['prev YT Num']        
    
    return _data_list, _column_names

# ------------------------------------------------------------------------------
def create_congestion_df(_folderPath):
    csv_data = load_csv_files_in_folder(_folderPath)
    folder_name = os.path.basename(os.path.normpath(_folderPath))
    
    prev_truck_num = re.findall(r'prev_(\d+)', folder_name)[0]
    now_truck_num = re.findall(r'now_(\d+)', folder_name)[0]

    columns = ["Prev Truck Number", "Now Truck Number", "repeat_num", "alpha_1", "alpha_2", "alpha_3"] + csv_data[0][1][0]

    wt_data_list = []
    wot_data_list = []


    for file_name, file_data in csv_data:
        
        alphas_match = re.search(r"LP_(\d+)_(\d+)_(\d+)", file_name)
        
        if alphas_match:
            alpha1 = int(alphas_match.group(1))
            alpha2 = int(alphas_match.group(2))
            alpha3 = int(alphas_match.group(3))
            
            alphas = [alpha1, alpha2, alpha3]
            
        # remove .csv
        repeat_time = file_name.split('_')[-1].split('.')[0]
        
        # if repeat_time doesn't contain "rep"
        if "rep" in repeat_time:
            if repeat_time[0] == '0':
                repeat_time = '1'
        
        else:
            repeat_time = '1'
        
        for row in file_data[1:]:
            # print(row)
            row[4:] = [float(value) for value in row[4:]]
            new_row = [prev_truck_num, now_truck_num, repeat_time] + alphas + row
            
            if 'NoCongestions' in file_name:
                wot_data_list.append(new_row)
            else:
                wt_data_list.append(new_row)

    wt_df = pd.DataFrame(wt_data_list, columns=columns)
    wot_df = pd.DataFrame(wot_data_list, columns=columns)
    
    # remove unnecessary columns : "Origin", "Destination", "Route-id"
    wt_df = wt_df.drop(['Origin', 'Destination', 'Route_id'], axis=1)
    wot_df = wot_df.drop(['Origin', 'Destination', 'Route_id'], axis=1)
    
    return wt_df, wot_df


def get_congestion_ratio_df(_folder_path):

    wt_df, wot_df = create_congestion_df(_folder_path)
    # Perform the subtraction and division
    merged_df = wt_df.merge(wot_df, on=['Prev Truck Number', 'Now Truck Number', 'alpha_1', 'repeat_num', 'alpha_2', 'alpha_3', 'Truck_id'], suffixes=('_wt', '_wot'))
    merged_df['Pickup_Congestion_ratio'] = (merged_df['PickupSta AT_wt'] - merged_df['PickupSta AT_wot'])/merged_df['PickupSta AT_wot']
    merged_df['Drop_Congestion_ratio'] = (merged_df['DropSta AT_wt'] - merged_df['DropSta AT_wot'])/merged_df['DropSta AT_wot']
    # alpha값들에 따라서 그룹화를 한후 Pickup_Congestion_ratio, Drop_Congestion_ratio의 전체 평균을 구한다.
    merged_df_congestion_ratio = merged_df.groupby(['alpha_1', 'alpha_2', 'alpha_3'])[['Pickup_Congestion_ratio', 'Drop_Congestion_ratio']].mean()

    # index to column
    merged_df_congestion_ratio = merged_df_congestion_ratio.reset_index()

    # 각 행별로 평균 구하기
    merged_df_congestion_ratio['Congestion_ratio'] = (merged_df_congestion_ratio['Pickup_Congestion_ratio'] + merged_df_congestion_ratio['Drop_Congestion_ratio'])/2
    # drop unnecessary columns
    merged_df_congestion_ratio = merged_df_congestion_ratio.drop(['Pickup_Congestion_ratio', 'Drop_Congestion_ratio'], axis=1)
    return merged_df_congestion_ratio

def group_folders_by_truck_numbers(_directory_path):
    folder_groups = {}
    
    for folder_name in os.listdir(_directory_path):
        extension = os.path.splitext(folder_name)[-1]
        
        # .csv 파일만 가져오기\n",
        if extension != '.meta':
            folder_path = os.path.join(_directory_path, folder_name)
            # list to tuple
            key = tuple(map(int, re.findall('(d+\)', folder_name)[:2]))
            congestion_df = get_congestion_ratio_df(folder_path)
            if key in folder_groups:
                folder_groups[key].append(congestion_df)
            else:
                folder_groups[key] = [congestion_df]
    return folder_groups

def create_completion_df(csv_data):
    columns = ["Prev Truck Number", "Now Truck Number", "alpha_1", "alpha_2", "alpha_3"] + csv_data[0][1][0]

    data_list = []

    for file_name, file_data in csv_data:
        
        # Extract numbers after "Truck_"
        truck_numbers = re.findall(r'Truck_(\d+)', file_name)
        
        alphas_match = re.search(r"LP_(\d+)_(\d+)_(\d+)", file_name)
        
        if alphas_match:
            alpha1 = int(alphas_match.group(1))
            alpha2 = int(alphas_match.group(2))
            alpha3 = int(alphas_match.group(3))
            
            alphas = [alpha1, alpha2, alpha3]
        
        for row in file_data[1:]:
            # print(row)
            row[4:] = [float(value) for value in row[4:]]
            new_row = truck_numbers + alphas + row
            data_list.append(new_row)

    df = pd.DataFrame(data_list, columns=columns)

    return df


def draw_plot(_x_values, _y_values, _title_name, x_label, y_label):
    plt.figure(figsize=(5,3))
    plt.plot(_x_values, _y_values , marker='o', linestyle='-', color = 'navy')
    plt.title(_title_name, fontsize=9, ha='center')

    plt.yticks(range(int(_y_values.min()) - 30, int(_y_values.max()) + 10, 50))
    plt.xlabel(x_label, fontsize=9)
    plt.ylabel(y_label, fontsize=9)
    # plt.xticks(range(0, x_values.max() + 10, 10))

    plt.grid(True)
    plt.show()


def draw_plot_congestion(_df, _x_label, _y_label):

    # 현재 스케줄링 대상 트럭
    x_value_2 = _df["alpha_1"]
    y_value_2 = _df["Congestion_ratio"]

    # 그래프 그리기
    plt.figure(figsize=(5,3))
    # plt.plot(x_value_1, y_value_1 , marker='o', linestyle='-', color = 'steelblue')
    plt.plot(x_value_2, y_value_2 , marker='o', linestyle='-', color = 'blue')

    plt.xlabel(_x_label, fontsize=9)
    plt.ylabel(_y_label, fontsize=9)

    # plt.ylim(int(y_value_2.min()) - 0.05, int(y_value_2.max()) + 0.05)
    
    plt.axhline(y=y_value_2.iloc[0], color='gray', linestyle='--')

    plt.show()


def subplot_congestion_avg(_directory_path, _x_label, _y_label, _title, row_num, col_num, fig_size):
    f, axes = plt.subplots(row_num, col_num)
    # 격자 크기 설정
    f.set_size_inches(fig_size)
    
    # 격자 여백 설정
    plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
    
    row_index = 0
    col_index = 0
    
    grouped_data = group_folders_by_truck_numbers(_directory_path)
    
    for i in range(len(grouped_data)):
        # get first key
        key = list(grouped_data.keys())[i]
        # 행별로 각 데이터프레임의 Congestion_ratio 열의 합계를 초기화\n",
        sum_congestion = pd.Series(0.0, index=grouped_data[key][0].index)
    
        # 데이터프레임 리스트를 순회하면서 행별로 Congestion_ratio 열을 합산
        for df in grouped_data[key]:
            sum_congestion += df['Congestion_ratio']

        # 데이터프레임의 개수로 나누어 각 행별 평균을 계산\n",
        average_congestion = sum_congestion / len(grouped_data[key])
    
        # 결과를 새로운 데이터프레임으로 생성\n",
        result_df = pd.DataFrame({'alpha_1' : df['alpha_1'].values, 'alpha_2' : df['alpha_2'].values, 'alpha_3' : df['alpha_3'].values, 'Congestion_ratio_mean': average_congestion})
        x_value_1 = result_df[i]['alpha_1']
        y_value_1 = result_df[i]['Congestion_ratio_mean']

        if row_num == 1:
            plt.subplot(1, col_num, col_index + 1)
            plt.plot(x_value_1, y_value_1 , marker='o', linestyle='-', color = 'steelblue')

            plt.xlabel(_x_label, fontsize=9, ha='center')
            plt.ylabel(_y_label, fontsize=9)
            # x축 10 단위로 표시
            # plt.xticks(range(x_value_1.min(), x_value_1.max() + 10, 10))
            plt.title(_title + ' (prev_' + key[0] + '_now_' + key[1] +')', fontsize=9, ha='center')
            plt.axhline(y=y_value_1.iloc[0], color='gray', linestyle='--')
                
        else:
            # x축 10 단위로 표시
            # axes[row_index, col_index].set_xticks(range(x_value_1.min(), x_value_1.max() + 10, 10))
            axes[row_index, col_index].plot(x_value_1, y_value_1 , marker='o', linestyle='-', color = 'steelblue')
            axes[row_index, col_index].axhline(y=y_value_1.iloc[0], color='gray', linestyle='--')
            
            # title_name = "Completion Time by alpha_1 (prev_20_now_20)"
            title_name = _title +  ' (prev_' + key[0] + '_now_' + key[1] +')'
            
            axes[row_index, col_index].set_xlabel(_x_label, fontsize=9, ha='center')
            axes[row_index, col_index].set_ylabel(_y_label, fontsize=9)
            axes[row_index, col_index].set_title(title_name, fontsize=9, ha='center')

            col_index += 1
            if(col_index == col_num):
                col_index = 0
                row_index += 1
            
        plt.show()
        

def Create_subplot_congestion(_directory_path, _x_label, _y_label, _title, row_num, col_num, fig_size):
    
    folder_name_list = []
    congestion_df_list = []
    
    for folder_name in os.listdir(_directory_path):
        
        # 확장자 얻기
        extension = os.path.splitext(folder_name)[-1]

        # .csv 파일만 가져오기
        if extension != '.meta':
            folder_path = os.path.join(_directory_path, folder_name)
            
            if os.path.isdir(folder_path):
                folder_name_list.append(folder_name)
                
                congestion_df = get_congestion_ratio_df(folder_path)
                congestion_df_list.append(congestion_df)
                            
            else:
                print("Please Check Directory Path")
    
    f, axes = plt.subplots(row_num, col_num)
    
    # 격자 크기 설정
    f.set_size_inches(fig_size)

    # 격자 여백 설정
    plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
    
    row_index = 0
    col_index = 0
    
    for i in range(len(congestion_df_list)):

        x_value_1 = congestion_df_list[i]["alpha_1"]
        y_value_1 = congestion_df_list[i]['Congestion_ratio']
        
        if row_num == 1:
            plt.subplot(1, col_num, col_index + 1)
            plt.plot(x_value_1, y_value_1 , marker='o', linestyle='-', color = 'steelblue')

            plt.xlabel(_x_label, fontsize=9, ha='center')
            plt.ylabel(_y_label, fontsize=9)
            # x축 10 단위로 표시
            # plt.xticks(range(x_value_1.min(), x_value_1.max() + 10, 10))
            plt.title(_title + ' (' + folder_name_list[i] + ')', fontsize=9, ha='center')
            plt.axhline(y=y_value_1.iloc[0], color='gray', linestyle='--')
            
        else:
            # x축 10 단위로 표시
            # axes[row_index, col_index].set_xticks(range(x_value_1.min(), x_value_1.max() + 10, 10))
            axes[row_index, col_index].plot(x_value_1, y_value_1 , marker='o', linestyle='-', color = 'steelblue')
            axes[row_index, col_index].axhline(y=y_value_1.iloc[0], color='gray', linestyle='--')
            
            # title_name = "Completion Time by alpha_1 (prev_20_now_20)"
            title_name = _title +  ' (' + folder_name_list[i] + ')'
            
            axes[row_index, col_index].set_xlabel(_x_label, fontsize=9, ha='center')
            axes[row_index, col_index].set_ylabel(_y_label, fontsize=9)
            axes[row_index, col_index].set_title(title_name, fontsize=9, ha='center')

        col_index += 1
        if(col_index == col_num):
            col_index = 0
            row_index += 1
        
    plt.show()
    
    
def merge_df(df1, df2):
    merged_df = pd.merge(df1, df2, on=['Truck_num', 'Truck_id'], suffixes=('_wt', '_wot'))
    return merged_df