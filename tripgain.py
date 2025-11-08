import pandas as pd

df = pd.read_csv(r"C:\Users\lakshay pandey\Desktop\matches.csv")



# Q1. Load the dataset into a pandas DataFrame and show:
# Total number of matches
total_number_of_matches = int(df['id'].count())
print(f'{total_number_of_matches = }\n')

# Column names
column_names = list(df.columns)
print(f'{column_names = }\n')

# First 5 rows of data
print(df.head(5), '\n')

# Describe the data
print(df.describe(), '\n')

# Q2. Which player has won the most “Player of the Match” awards in games decided on the final ball? (i.e., matches won by just 1 run or 1 wicket).
d = {}
j = 0
for i in df['win_by_runs']:
    d[j] = [i]
    j += 1

k = 0
for i in df['win_by_wickets']:
    d[k].append(i)
    k += 1 

counter = {}
for k, v in d.items():
    if v[0] == 1 or v[1] == 1:
        counter[k] = counter.get(k, 0) + 1
    
i = 0
arr = []
for j in df['player_of_match']:
    if i in counter:
        arr.append(j)
    i += 1

print('player of matches: ', arr)





