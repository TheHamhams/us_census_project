import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import codecademylib3_seaborn
import glob

# Turning a number of csv files into a data frame
files = glob.glob("states*.csv")
df_list = []
for filename in files:
  state = pd.read_csv(filename)
  df_list.append(state)
us_census = pd.concat(df_list)
us_census = us_census.drop_duplicates(subset='State')

# Converting the income column into a float
us_census.Income = us_census['Income'].replace('\$', '', regex=True)
us_census.Income = pd.to_numeric(us_census.Income)

# Converting the gender and population column into seperate male and female population columns
gender_split = us_census.GenderPop.str.split('_')
us_census['Men'] = gender_split.str.get(0).replace('M', '', regex=True)
us_census['Women'] = gender_split.str.get(1).replace('F', '', regex=True)

us_census.Men = pd.to_numeric(us_census.Men)
us_census.Women = pd.to_numeric(us_census.Women)
us_census.Women = us_census.Women.fillna(us_census.TotalPop - us_census.Men)

# Converting each race column in to a float
for race in us_census.columns[3:9]:
  us_census[race] = us_census[race].replace('%', '', regex=True)
  us_census[race] = pd.to_numeric(us_census[race])
  #print(us_census[race])

# The Pacific population had some nan values to I replaced them with the mean
us_census.Pacific = us_census.Pacific.fillna(us_census.Pacific.mean())

# Created a scatter plot showing the corralation between the population of women and income fo the state
plt.scatter(us_census.Women, us_census.Income)
plt.xlabel('Women (millions)')
plt.ylabel("Income")
plt.show()
plt.cla()

# Created a histogram for each race showing the percentage of population 
for race in us_census.columns[3:9]:
  plt.hist(us_census[race])
  plt.title(race)
  plt.xlabel("Percentage of Population")
  plt.ylabel("Number of Occurences")
  plt.show()
  plt.cla()
  
print(us_census.head())
print(us_census.dtypes)
#print(us_census.duplicated())
