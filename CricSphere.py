# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 20:40:38 2025

@author: HP V15 (493178410)
"""

import pandas as pd
import re
  
df = pd.read_csv(r"C:/Users/HP V15 (493178410)/OneDrive/Desktop/dapl/Players_Info_2024.csv")
df_matches = pd.read_csv('C:/Users/HP V15 (493178410)/OneDrive/Desktop/dapl/team_performance_dataset_2008to2024.csv')

def clean_salary(salary):
    if pd.isna(salary): 
        return None   
    salary = str(salary).encode('utf-8').decode('utf-8')  
    salary = re.sub(r'[^\d\.crorelakh]', '', salary) 

    match = re.search(r'(\d+\.?\d*)\s*(crore|lakh)?', salary, re.IGNORECASE)
    if match:
        value, unit = match.groups()
        value = float(value)
        if unit == "crore":
            return int(value * 10000000)  
        elif unit == "lakh":
            return int(value * 100000)  
        return int(value)  
    return None

df["Cleaned Salary"] = df["Player Salary"].apply(clean_salary)

df.to_csv("cleaned_Players_Info_2024.csv", index=False)

print(df.isnull().sum())
df['IPL Debut'] = df['IPL Debut'].fillna('Unknown')
df['Cleaned Salary'] = df['Cleaned Salary'].fillna(df['Cleaned Salary'].mean())
df['Date of Birth'] = df['Date of Birth'].fillna('11-Apr-02')
print(df.isnull().sum())
print(df.head())
print(df.describe())
print(df.info())
print(df.columns.tolist())
print(df_matches.columns.tolist())

###

import pandas as pd

df_matches['Date'] = pd.to_datetime(df_matches['Date'], errors='coerce')
df_matches['Year'] = df_matches['Date'].dt.year
output_file_path = 'year_team_performance.csv' 
df_matches.to_csv(output_file_path, index=False)

print(f"Year extracted and saved to {output_file_path}")
print(df_matches.columns.tolist())


df_matches[['Team1', 'Team2']] = df_matches['Teams'].str.split(' vs ', expand=True)
output_file_path = 'year_team_performance.csv'  
df_matches.to_csv(output_file_path, index=False)
print(f"Teams extracted and saved to {output_file_path}")





























