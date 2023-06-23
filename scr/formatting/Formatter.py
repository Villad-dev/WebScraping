import pandas as pd
from dateutil import parser

df = pd.read_csv("data.csv", index_col=False, low_memory=False)

#Colomn names

column_no_semicolomn = [name.replace(":", "") for name in df.columns]
df.rename(columns=dict(zip(df.columns, column_no_semicolomn)), inplace=True)

#Index

df["Index"] = df["Index"].astype(int)

substring = "xx xxx"
substring1 = "xx"
substring2 = "XX XXX"
substring3 = "XX"

#Date
# Replace the rows containing the substring "xx xxx" and "xx" with 31 December and 31

df.loc[df["Date"].str.contains(substring), "Date"] = "Tuesday 31 December " + df.loc[df["Date"].str.contains(substring), "Date"].str[-4:]
df.loc[df["Date"].str.contains(substring1), "Date"] = "Monday 01 June" + df.loc[df["Date"].str.contains(substring1), "Date"].str[-4:]
df.loc[df["Date"].str.contains(substring2), "Date"] = "Tuesday 31 December " + df.loc[df["Date"].str.contains(substring2), "Date"].str[-4:]
df.loc[df["Date"].str.contains(substring3), "Date"] = "Monday 01 June" + df.loc[df["Date"].str.contains(substring3), "Date"].str[-4:]

df["Date"] = df["Date"].apply(parser.parse)

#Time

df["Time"] = df["Time"].str.strip()
df["Time"] = df["Time"].str.findall(r"\d{2}:\d{2}").str[0]
df['Time'] = df['Time'].fillna('00:00')

#Useless colomns with small amount of data

drop_columns = ["Unknown","Crash site elevation","Ground casualties","Collision casualties","Unnamed 30", "Unnamed 31", "Unnamed 32", "Unnamed 33", "Unnamed 34", "Unnamed 35", "Unnamed 36", "Unnamed 37"]
df = df.drop(columns=drop_columns)

#Narrative
df["Narrative"] = df["Narrative"].apply(lambda x: x[:97] + "..." if len(x) > 100 else x)

#Country

df["Country"] = df["Location"].str.extract(r"\(([^()]+)\)[^()]*$")
df["Country"] = df["Country"].str.strip()
columns = df.columns.tolist()
columns.insert(3, "Country")
df = df[columns]

#Fatalities

def parse_fatalities(value):
    if value.strip() == '':
        return 0
    elif '+' in value:
        parts = value.split('+')
        return sum(int(part) for part in parts)
    else:
        return int(value)

df['Fatalities'] = df['Fatalities'].apply(parse_fatalities)
df['Fatalities'] = df['Fatalities'].astype(int)

#First flight

def parse_first_flight(value):
    if value.strip() == '':
        return -1
    elif '(' in value:
        year_str = value.split('(')[0].strip()
    else:
        year_str = value.strip()

    if '-' in year_str:
        year_str = year_str.split('-')[0].strip()

    return int(year_str)

df['First flight'] = df['First flight'].apply(parse_first_flight)
df['Fatalities'] = df['Fatalities'].astype(int)

#Crew

df['Crew Fatalities'] = df['Crew'].str.extract(r'Fatalities:\s*(\d+)')
df['Crew Fatalities'] = pd.to_numeric(df['Crew Fatalities'], errors='coerce').fillna(0).astype(int)
df['Crew Fatalities'].fillna(0, inplace=True)

df['Crew'] = df['Crew'].str.extract(r'Occupants:\s*(\d+)')
df['Crew'] = pd.to_numeric(df['Crew'], errors='coerce').fillna(0).astype(int)
df['Crew'].fillna(0, inplace=True)

#Passengers

df['Passengers Fatalities'] = df['Passengers'].str.extract(r'Fatalities:\s*(\d+)')
df['Passengers Fatalities'] = pd.to_numeric(df['Passengers Fatalities'], errors='coerce').fillna(0).astype(int)
df['Passengers Fatalities'].fillna(0, inplace=True)

df['Passengers'] = df['Passengers'].str.extract(r'Occupants:\s*(\d+)')
df['Passengers'] = pd.to_numeric(df['Passengers'], errors='coerce').fillna(0).astype(int)
df['Passengers'].fillna(0, inplace=True)

#Total

df['Total Fatalities'] = df['Total'].str.extract(r'Fatalities:\s*(\d+)')
df['Total Fatalities'] = pd.to_numeric(df['Total Fatalities'], errors='coerce').fillna(0).astype(int)
df['Total Fatalities'].fillna(0, inplace=True)

df['Total'] = df['Total'].str.extract(r'Occupants:\s*(\d+)')
df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0).astype(int)
df['Total'].fillna(0, inplace=True)


print(df.dtypes)
#print(df)
df.to_csv("Formated.csv", index=False, encoding="utf-8")

