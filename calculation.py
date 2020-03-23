# import pandas and numpy to generate dataframes and perform calculations
import pandas as pd
import numpy as np
import matplotlib
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

"""
Function to generate a histogram

@param df the dataframe that the histogram will be generated from
@param pwd_scheme the current password scheme
@param column the column from the dataframe that we will be calculating with
@param x_text extra text for the x-axis
"""
def generate_hist(df, pwd_scheme, column, x_text):
    #Drop any empty value
    if column == "avg login time success (s)" or column == "avg login time failed (s)":
        df.dropna(subset=[column], inplace=True)
        #Set bin to 4 (due to large distance between values)
        bin_list = [x for x in range(0, df[column].astype(int).max() + 4) if x%4 == 0]
    else:
        #Set bin to 1
        bin_list = range(df[column].astype(int).min(), df[column].astype(int).max() + 2)

    #generate figure
    _f, ax = plt.subplots(1,1, figsize=(10, 10))

    #convert to histogram
    _count, bins, _patches = ax.hist(df[column], bins=bin_list, edgecolor='black', linewidth=1.2, alpha=0.5, align='mid')

    #adjust x-axis
    xa = ax.get_xaxis()
    xa.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    plt.xticks(bins)

    #add labels
    plt.title(pwd_scheme + ": " + column + ' histogram')
    plt.xlabel(x_text + " " + column)
    plt.ylabel('Num of Users')
    
    #save as png
    plt.savefig(pwd_scheme + " " + column + ' histogram.png', bbox_inches='tight')
    #clear plot
    plt.close('all')

"""
Function to generate a box plot

@param df the dataframe that the boxplot will be generated from
@param pwd_scheme the current password scheme
@param column the column from the dataframe that we will be calculating with
"""
def generate_box(df, pwd_scheme, column1, column2):
    #drop any empty values
    df.dropna(subset=[column1], inplace=True)
    df.dropna(subset=[column2], inplace=True)

    #generate figure
    plt.subplots(1,1, figsize=(10, 10))

    #generate boxplot
    df.boxplot(column=[column1, column2])

    #add labels
    plt.title(pwd_scheme + ": Avg time box plot")
    plt.ylabel('Num of Users')

    #show
    plt.savefig(pwd_scheme + ' box plot.png', bbox_inches='tight')

    #clear plot
    plt.close("all")


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


#generate histograms for the number of logins (per user, total, successful, and unsuccessful)
generate_hist(image_df, "Image21", "total logins", "Num of")
generate_hist(image_df, "Image21", "successful logins", "Num of")
generate_hist(image_df, "Image21", "unsuccessful logins", "Num of")
generate_hist(text_df, "Text21", "total logins", "Num of")
generate_hist(text_df, "Text21", "successful logins", "Num of")
generate_hist(text_df, "Text21", "unsuccessful logins", "Num of")

#generate histograms for the login time per user, successful, and unsuccessful
generate_hist(image_df, "Image21", "avg login time success (s)", "")
generate_hist(image_df, "Image21", "avg login time failed (s)", "")
generate_hist(text_df, "Text21", "avg login time success (s)", "")
generate_hist(text_df, "Text21", "avg login time failed (s)", "")

#generate boxplots for the login time per user, successful, and unsuccessful
generate_box(image_df, "Image21", "avg login time success (s)", "avg login time failed (s)")
generate_box(text_df, "Text21", "avg login time success (s)", "avg login time failed (s)")