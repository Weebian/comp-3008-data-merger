# import pandas and numpy to generate dataframes and perform calculations
import pandas as pd
import numpy as np 
from datetime import datetime

#Variables
scheme_type_1 = 'Image21'
scheme_type_2 = 'Text21'


"""
Function to obtain a dataframe from a csv file

@param csv_file the csv file name
@return the dataframe from the csv file
"""
def csv_to_df(csv_file):
    # generate dataframe from csv
    # sep: Delimiter to use, names: the column headers in order
    df = pd.read_csv(csv_file, sep=',', names=["time", "user", "site", "scheme", "mode", "event", "event details", "data"])

    #drop columns that aren't needed
    df = df.drop(columns=['site', 'data', 'scheme', 'mode'])

    #Remove any rows that are not a login event or enter event with event detail start (event/start and login/success or fail)
    df = df.loc[(df['event'] == 'login') | ((df['event'] == 'enter')  & (df['event details'] == 'start'))]

    return df

"""
Function to generate a new dataframe with the columns userid (the user), login result (success or failure), and time (time taken to complete a login) using a specified dataframe

@param df the dataframe to be used for generating the new one
@return the new dataframe
""" 
def calculate_time_df(df):
    #variables
    start = None # the initial login time
    user = None # The user id of the user for the current login calculation
    temp = [] # list to hold each row of the new dataframe

    # Fill empty dataframe
    for x in df.index: # Iterate through each row
        if df.at[x, "event"] == "enter" and df.at[x, "event details"] == "start": #if the current row is event enter and event detail start
            start = df.at[x, "time"]
            user = df.at[x, "user"]
        else: #Is a login event
            if start != None and user != None:
                if user == df.at[x, "user"]: #ensure that its the same user
                    # convert string to datetime
                    date_time_start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
                    date_time_end = datetime.strptime(df.at[x, "time"], '%Y-%m-%d %H:%M:%S')
                    # obtain the total time taken in seconds
                    total_time = (date_time_end - date_time_start).total_seconds()
                    # create a row with data
                    temp.append((user, df.at[x, "event details"], total_time))
                    
                #Reset start time and current user
                start = None
                user = None

    # Create a dataframe and return it
    return pd.DataFrame(temp, columns = ["userid", "login result", "time"])

"""
Function to generate a dataframe with the number of logins for success, failure, and combined total for each user. Also mean of login time for success and failure for each user.

@param df the dataframe to be used for generating the new one
@return the dataframe with the mean value for success, and mean value for failure for each user
"""
def calculate_stats_df(df):
    #split the dataframe into two dataframes for success and failure
    df_success = df[df["login result"] == "success"]
    df_fail = df[df["login result"] == "failure"]

    #drop result columns
    df = df.drop(['login result'], axis = 1)
    df_success = df_success.drop(['login result'], axis = 1)
    df_fail = df_fail.drop(['login result'], axis = 1)

    #calculate number of logins (create dataframes)
    df_total_count = df.groupby(['userid'], as_index=False).agg({"time":"count"}).rename(columns={"time" : "total logins"})    # total count
    df_success_count = df_success.groupby(['userid'], as_index=False).agg({"time":"count"}).rename(columns={"time" : "successful logins"}) #success count
    df_fail_count = df_fail.groupby(['userid'], as_index=False).agg({"time":"count"}).rename(columns={"time" : "unsuccessful logins"}) #failed count

    # mean of time (create dataframes)
    df_success_mean = df_success.groupby(['userid'], as_index=False).agg({"time":"mean"}).rename(columns={"time" : "avg login time success (s)"})
    df_fail_mean = df_fail.groupby(['userid'], as_index=False).agg({"time":"mean"}).rename(columns={"time" : "avg login time failed (s)"})

    # merge (merge left in case there are empty data)
    resulting_df = df_total_count.merge(df_success_count, how='left', on = "userid").merge(df_fail_count, how='left', on = "userid").merge(df_success_mean, how='left', on = "userid").merge(df_fail_mean, how='left', on = "userid")

    #If there are any Nan values in the number of logins
    resulting_df[["successful logins", "unsuccessful logins"]] = resulting_df[["successful logins", "unsuccessful logins"]].fillna(value = 0)

    return resulting_df

"""
Function to join two dataframes and sort based on userid

@param df1 one of the two dataframes to join
@param df2 one of the two dataframes to join
@return the resulting dataframe after the join and sort
"""
def join_and_sort(df1, df2):
    #join the two dataframes
    df = pd.concat([df1, df2])

    #sort by userid
    return df.sort_values(["userid"])

# Create dataframes out of the two csv files and add their headers
df_image = csv_to_df('imagept21.csv') #image21
df_text = csv_to_df('text21.csv') #text21

# Obtain a data frame with the time taken to complete logins
df_image = calculate_time_df(df_image)
df_text = calculate_time_df(df_text)

# Generate dataframe with mean value for success, and mean value for failure for each user
df_image = calculate_stats_df(df_image)
df_text = calculate_stats_df(df_text)

#add column pwd scheme to the dataframes
#also pass the password scheme as the value for each row
df_image.insert(1, "pwd scheme", scheme_type_1)
df_text.insert(1, "pwd scheme", scheme_type_2)

# join the two dataframes
df_result = join_and_sort(df_image, df_text)

#Generate csv file
df_result.to_csv('combined.csv', index = False, header=True)