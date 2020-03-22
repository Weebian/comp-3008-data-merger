# import pandas and numpy to generate dataframes and perform calculations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Function to split a dataframe into the two types of password scheme

@param df the dataframe to get the statistics from
@return an array of dataframes
"""
def split_df(df):
    #First split dataframe on pwd scheme
    df_1 = df[df["pwd scheme"] == "Image21"]
    df_2 = df[df["pwd scheme"] == "Text21"]

    #Drop pwd scheme column
    df_1 = df_1.drop(['pwd scheme'], axis = 1)
    df_2 = df_2.drop(['pwd scheme'], axis = 1)

    return [df_1, df_2]

"""
Function to generate a dataframe with the mean, median and standard deviation for number of logins and login time per user

@param df the dataframe to get the statistics from
"""
def get_stat(df, pwd_scheme, name, indices):
    #variables
    temp = [] #hold onto each row for a new dataframe

    #Calculate stats (uses sample standard deviation)
    for i in indices:
        temp.append((df[i].mean(), df[i].std(), df[i].median()))

    #Create resulting dataframe
    #Columns: mean. standard deviation, median
    #Rows: total login, sucessful logins, uncessful logins,  avg
    df_stat = pd.DataFrame(temp, columns = ["mean", "standard deviation", "median"], index=indices)
    df_stat.to_csv(pwd_scheme + " " + name + ' stats.csv', index = True, header=True)

#Obtain data from csv file
df = pd.read_csv('combined.csv', sep=',')

#Split in terms of pwd scheme
df_list = split_df(df)
image_df = df_list[0]
text_df = df_list[1]

#First generate the Mean, standard deviation, and median of number of logins per user (total, successful, and unsuccessful).
get_stat(image_df, "Image21", "number of logins per user", ["total logins", "successful logins", "unsuccessful logins"])
get_stat(image_df, "Image21", "login time per user", ["avg login time success (s)", "avg login time failed (s)"])
get_stat(text_df, "Text21", "number of logins per user", ["total logins", "successful logins", "unsuccessful logins"])
get_stat(text_df, "Text21", "login time per user", ["avg login time success (s)", "avg login time failed (s)"])
