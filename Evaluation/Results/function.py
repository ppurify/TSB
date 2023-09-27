import os
import csv
import re
import pandas as pd

def load_csv_files_in_folder(folder_path):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    all_csv_data = []

    for csv_file in csv_files:
        csv_path = os.path.join(folder_path, csv_file)
        data = []

        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            for row in csv_reader:
                data.append(row)
                
        all_csv_data.append((csv_file, data))

    return all_csv_data



#------- File 기준 --------- ex) prev_25_now_25 > prev_rep_1, now_rep_1 ...
def create_subplot(_directory_path, _x_value_col, _y_value_col, _title, _col_num, _y_lim, _fig_size):
    
    folder_list = []
    folder_name_list = []
    
    for folder_name in os.listdir(_directory_path):
        
        # 확장자 얻기
        extension = os.path.splitext(folder_name)[-1]
        # .csv 파일만 가져오기
        if extension != '.meta':
            folder_path = os.path.join(_directory_path, folder_name)
            if os.path.isdir(folder_path):
                
                print(folder_path)
                all_csv_data = load_csv_files_in_folder(folder_path)
                
                folder_name = os.path.basename(os.path.normpath(folder_path))
                prev_truck_num = re.findall(r'prev_(\d+)', folder_name)[0]
                now_truck_num = re.findall(r'now_(\d+)', folder_name)[0]

                df_col = ["Prev Truck Number", "Now Truck Number", "repeat_num", "alpha_1", "alpha_2", "alpha_3", _y_value_col]
                data_list = []
                
                for file, file_data in all_csv_data:
                    
                    file_name = file.name
                    alphas_match = re.search(r"LP_(\d+)_(\d+)_(\d+)", file_name)
                    
                    if alphas_match:
                        alpha1 = int(alphas_match.group(1))
                        alpha2 = int(alphas_match.group(2))
                        alpha3 = int(alphas_match.group(3))
                        
                        alphas = [alpha1, alpha2, alpha3]
                 
                    
                    repeat_time = file_name.split('_')[-1].split('.')[0]
                    
                    df = pd.DataFrame(file_data[1:], columns = file_data[0])
                    result_df_data_row = [prev_truck_num , now_truck_num] + alphas + [df[_y_value_col].astype(float)[0]]
                    data_list.append(result_df_data_row)
                
                # Create the DataFrame from the 2D list
                # result_df = pd.DataFrame(data_list, columns=df_col)
                    # result_df = pd.DataFrame(, columns=columns)
                    # print(result_df)
             
        # folder_name_list.append(folder_name)
        # folder_list.append(csv_data)

                
                
            # if os.path.isdir(folder_path):
            #     merged_df = get_congestion_ratio_df(folder_path, _prev_or_now)
                
            #     dfs = {}
    
            #     unique_values = merged_df['repeat_num'].unique()
            #     for value in unique_values:
            #         df = merged_df[merged_df['repeat_num'] == value]
            #         grouped_df = df.groupby(['alpha_1', 'alpha_2', 'alpha_3'])['Congestion_ratio'].mean().reset_index()
            #         dfs[value] = grouped_df
            
            #     folder_num = len(dfs)
            #     if folder_num % _col_num == 0:
            #         _row_num = folder_num // _col_num
            #     else:
            #         _row_num = folder_num // _col_num + 1
                
            #     create_subplot(dfs, folder_name, _row_num, _col_num, _x_label, _y_label, _title, _y_lim, _fig_size)
                    
            # else:
            #     print(folder_name + " is not a directory")