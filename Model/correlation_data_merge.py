import os
import pandas as pd

# corrlation_data csv를 불러옴
csv_path = os.path.join(os.getcwd(), 'Model', 'corrlation_data.csv')

# corrlation_data csv를 dataframe으로 변환
df = pd.read_csv(csv_path)

print(df)