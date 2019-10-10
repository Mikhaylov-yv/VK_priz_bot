import pandas as pd

csv_path = 'Посты — копия.csv'
pd.set_option('display.max_columns', 16)
df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
print(df)
df = df.drop_duplicates(subset='post', keep='first')
print(df)
file_name = csv_path
df.to_csv(file_name, sep=';', encoding='utf-8', index=False, header=True)
