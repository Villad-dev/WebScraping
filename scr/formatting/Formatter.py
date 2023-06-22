import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')

drop_columns = ['Image link', 'Location accident']
df = df.drop(columns=drop_columns)
df = df.rename(columns={'Registration': 'Image', 'Category': 'Accident Location', 'MSN': 'Operator', 'First flight':'Registration'})
df = df.replace('', np.nan)
df = df.replace('registration unknown', np.nan)

#df['Fatalities'] = df['Fatalities'].str.split('+').str[0]


#df[['Index', 'Fatalities', 'Crew', 'Passengers', 'Total']] = df[
#    ['Index', 'Fatalities', 'Crew', 'Passengers', 'Total']].replace(' ', '0').astype(float).astype(int)

#df[['Index', 'Fatalities', 'First flight', 'Crew', 'Passengers', 'Total']] = df[
#   ['Index', 'Fatalities', 'First flight', 'Crew', 'Passengers', 'Total']].astype(float).astype(int)

#df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

#df[['Operator', 'Location accident', 'Category', 'Registration', 'MSN', 'Engines', 'Aircraft damage', 'Aircraft fate', 'Location', 'Phase', 'Nature', 'Departure airport', 'Destination airport', 'Image link']] = df[
#    ['Operator', 'Location accident', 'Category', 'Registration', 'MSN', 'Engines', 'Aircraft damage', 'Aircraft fate', 'Location', 'Phase', 'Nature', 'Departure airport', 'Destination airport', 'Image link']].fillna('Unknown')
df.to_csv('Formatet.csv', index=False, encoding='utf-8')
print(df)