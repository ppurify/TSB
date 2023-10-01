import os
import re
import csv
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

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

def get_dfs_by_folder(_directory_path, _y_value_col, nooutlier = True):
    dfs = {}
    folder_names = []

    for folder_name in os.listdir(_directory_path):
        # 확장자 얻기
        extension = os.path.splitext(folder_name)[-1]
        
        # .csv 파일만 가져오기
        if extension != '.meta':
            folder_names.append(folder_name)

            folder_path = os.path.join(_directory_path, folder_name)
            
            if os.path.isdir(folder_path):
                all_csv_data = load_csv_files_in_folder(folder_path)
                prev_truck_num = re.findall(r'prev_(\d+)', folder_name)[0]
                now_truck_num = re.findall(r'now_(\d+)', folder_name)[0]
                df_col = ["Prev Truck Number", "Now Truck Number", "alpha_1", "alpha_2", "alpha_3", "repeat_num", _y_value_col]
                data_list = []

                for file, file_data in all_csv_data:
                    file_name = file.name
                        
                    alphas_match = re.search(r"LP_(\d+)_(\d+)_(\d+)", file_name)
                        
                    if alphas_match:
                        alpha1 = int(alphas_match.group(1))
                        alpha2 = int(alphas_match.group(2))
                        alpha3 = int(alphas_match.group(3))
                            
                        alphas = [alpha1, alpha2, alpha3]
                        
                    # rep 글자 앞에 있는 숫자만 가져오기
                    repeat_time = int(re.search(r'(\d+)rep', file_name).group(1))
                        
                    df = pd.DataFrame(file_data[1:], columns = file_data[0])
                    y_col_value = df[df[_y_value_col].notna()][_y_value_col].astype(float).values.tolist()
                    for y_value in y_col_value:
                        result_df_data_row = [prev_truck_num , now_truck_num] + alphas + [repeat_time, y_value]
                        data_list.append(result_df_data_row)
                # 첫번째 열부터 5번째 열까지 기준으로 정렬
                data_list.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4], x[5]))
                
                # Create a DataFrame from the data_list
                now_df = pd.DataFrame(data_list, columns=df_col)
                
                if nooutlier:
                    
                    # Remove outliers from the 'y_value_col' column
                    df_no_outliers = remove_outliers(df, _y_value_col)
                    
                    # Sort the DataFrame by the specified columns
                    df_no_outliers.sort_values(by=df_col[:-1], inplace=True)
                    
                    dfs[folder_name] = df_no_outliers
                    
                else:
                    dfs[folder_name] = now_df
    
    # Sort the dfs dictionary by keys
    dfs = sorted(dfs.items(), key=lambda x: (int(re.search(r'prev_(\d+)', x[0]).group(1)), int(re.search(r'now_(\d+)', x[0]).group(1))))
    
    return dfs
                
def remove_outliers(df, col):
    # Calculate the IQR for the specified column
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define the lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filter out rows with values outside the bounds
    df_no_outliers = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    
    return df_no_outliers


def boxsubplot(_dfs, x_col, y_col, col_num, y_lim, title, fig_size):
    folder_num = len(_dfs)

    if folder_num % col_num == 0:
        row_num = folder_num // col_num
    else:
        row_num = folder_num // col_num + 1
        
    fig, axes = plt.subplots(nrows=row_num, ncols=col_num, figsize=fig_size)

    for (key, value), ax in zip(_dfs, axes.ravel()):
        subplot_title = title + '(' + key + ')'
        sns.boxplot(data=value, x=x_col, y=y_col, ax=ax, color='white')
        ax.set_title(subplot_title)
        ax.set_ylim(y_lim)
        
    # Display the plot
    plt.show()

def lineplot(_dfs, x_col, y_col, y_lim, _title):
    keys = []
    for key, value in _dfs:

        keys.append(key)
        # get average of group by alpha_1, alpha_2, alpha_3
        df = value.groupby([x_col])[y_col].mean().reset_index()
        
        x_value = df[x_col]
        y_value = df[y_col]
        
        # draw line plot
        plt.plot(x_value, y_value, marker='o')    
        # set y limit
        plt.ylim(y_lim)
        
    plt.title(_title)
    plt.xlabel(x_col, fontsize = 9)
    plt.ylabel(y_col, fontsize = 9)
    plt.legend(keys, fontsize = 7, loc = 'upper right')

    for key, value in _dfs:
        df = value.groupby([x_col])[y_col].mean().reset_index()
        y_value = df[y_col]
        plt.axhline(y=y_value[0], color='gray', linestyle='--', alpha = 0.5)

def scatterplot(_dfs, _x_value, x_label, y_col, y_lim, _title):

    x_index = 0
    keys = []
    
    for key, value in _dfs.items():
        x_value = _x_value[x_index]
        y_value = value[y_col]
        keys.append(key)
        plt.scatter([x_value] * len(y_value), y_value, label=key, alpha = 0.5)
        
        x_index += 1
        
    # # set y limit
    plt.ylim(y_lim)    
    plt.title(_title)
    plt.xlabel(x_label, fontsize = 9)
    plt.ylabel(y_col, fontsize = 9)
    plt.legend(keys, fontsize = 7, loc = 'upper right')

    plt.show()