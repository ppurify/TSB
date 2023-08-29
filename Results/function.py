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
def create_congestion_df(csv_data):
    columns = ['Truck_num', 'Repeat_time'] + csv_data[0][1][0]

    data_list = []

    for file_name, file_data in csv_data:
        truck_num = file_name.split('_')[2]
        # remove .csv
        repeat_time = file_name.split('_')[-1].split('.')[0]
        
        if repeat_time == '100' :
            repeat_time == '1'
            
        for row in file_data[1:]:
            # print(row)
            row[4:] = [float(value) for value in row[4:]]
            new_row = [truck_num, repeat_time] + row
            data_list.append(new_row)

    df = pd.DataFrame(data_list, columns=columns)
    return df

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
    

def merge_df(df1, df2):
    merged_df = pd.merge(df1, df2, on=['Truck_num', 'Truck_id'], suffixes=('_wt', '_wot'))
    return merged_df