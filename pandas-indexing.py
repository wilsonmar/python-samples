#!/usr/bin/env python3
# pandas-indexing.py in https://github.com/bomonike/fullest-stack/blob/main/python/caiq-yaml-gen/pandas-indexing.py
# by Wilson Mar - v0.3 
# based on https://sparkbyexamples.com/pandas/iterate-over-rows-in-pandas-dataframe/
           # (which has an analysis of the efficiency of each method as the dataset gets larger)
# https://www.geeksforgeeks.org/different-ways-to-iterate-over-rows-in-pandas-dataframe/

import pandas as pd
Technologys = ({
    'Courses':["Spark","Spark","PySpark","Hadoop","Python","Pandas","Oracle","Java"],
    'Fee' :[10000,20000,25000,26000,22000,24000,21000,22000],
    'Duration':['15day','30day', '40days' ,'35days', '40days', '60days', '50days', '55days']
              })
df = pd.DataFrame(Technologys)
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
print("\r\n*** print(df) ")
print(df)
print("***\r\n")


print("\r\n*** Using DataFrame.iterrows() - most inefficient? ")
row = next(df.iterrows())[1]
print("Data For First Row :")
print(row)
print("***\r\n")

print("\r\n*** for index, row in df.iterrows()")
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html
for index, row in df.iterrows():
    print (index,row["Fee"], row["Courses"])
print("***\r\n")


print("\r\n*** for index, columns in data.iterrows() ")
# From https://statisticsglobe.com/loop-through-index-pandas-dataframe-python
data = pd.DataFrame({'x1':['a', 'b', 'c', 'd'],    # Create pandas DataFrame
                     'x2':['w', 'x', 'y', 'z']})
print(data) 
for i, row in data.iterrows():                     # Initialize for loop
    print('Index', i, '- Column x1:', row['x1'], '- Column x2:', row['x2'])
# Index 0 - Column x1: a - Column x2: w
# Index 1 - Column x1: b - Column x2: x
# Index 2 - Column x1: c - Column x2: y
# Index 3 - Column x1: d - Column x2: z
print("***\r\n")


print("\r\n*** next(df.itertuples() -- as namedtuples ")
#  iterate over DataFrame rows 
row = next(df.itertuples(index = True, name='Tution'))
print("Data For First Row :")
print(row)
print("***\r\n")


# https://www.w3resource.com/pandas/dataframe/dataframe-itertuples.php
print("\r\n*** for row in df3.itertuples(name='Animal') ")
df3 = pd.DataFrame({'num_legs': [4, 2], 'num_wings': [0, 2]},
                  index=['fox', 'eagle'])
for row in df3.itertuples(name='Animal'):
    print(row)
    # Animal(Index='fox', num_legs=4, num_wings=0)
    # Animal(Index='eagle', num_legs=2, num_wings=2)
print("***\r\n")


print("\r\n*** for row in df.itertuples(index = True) ")
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.itertuples.html
for row in df.itertuples(index = True):
    print (getattr(row,'Index'),getattr(row, "Fee"), getattr(row, "Courses"))
print("***\r\n")


print("\r\n*** df.apply ")
print(df.apply(lambda row: str(row["Fee"]) + " " + str(row["Courses"]), axis = 1))
print("***\r\n")


print("\r\n*** for idx in df.index ")
for idx in df.index:
    print(idx, df['Fee'][idx], df['Courses'][idx])
print("***\r\n")

     
print("\r\n*** for i in range(len(df)) : df.loc ")
for i in range(len(df)) :
    print(df.loc[i, "Fee"], df.loc[i, "Courses"])
print("***\r\n")


print("\r\n*** for i in range(len(df)) : df.iloc ")
for i in range(len(df)) :
    print(df.iloc[i, 0], df.iloc[i, 2])
print("***\r\n")


print("\r\n*** for label, content in df.items() ")
for label, content in df.items():
    print(f'label: {label}')
    print(f'content: {content}', sep='\n')
print("***\r\n")


# And from https://stackoverflow.com/questions/36864690/iterate-through-a-dataframe-by-index
# staticData.apply((lambda x: (x.name, x['exchange'])), axis=1)

# https://stackabuse.com/how-to-iterate-over-rows-in-a-pandas-dataframe/

# https://pandas.pydata.org/docs/reference/api/pandas.Series.iteritems.html

# What I really need: lookup values based on an indexed key, then 
# iterate through all values matching that key found.