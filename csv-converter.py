from scipy.io import arff
import pandas as pd

data, meta = arff.loadarff('Training Dataset.arff')

df = pd.DataFrame(data)

print('Cleaning Data...')
str_df = df.select_dtypes([object])
str_df = str_df.stack().str.decode('utf-8').unstack()

for col in str_df:
    df[col] = str_df[col]

print('saving to CSV..')
df.to_csv('phishing.csv', index=False)

print("Success! File Saved as 'phishing.csv'")
