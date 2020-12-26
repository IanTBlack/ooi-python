import pandas as pd
import re

def get_deployment(filename):
    deployment_pattern = '(deployment.*?)_'
    deployment = re.findall(deployment_pattern,filename).pop()
    return deployment

def ds2df(dataset,variables,close=False):
    '''A function that takes a 1D data from an xarray dataset and puts it into
    a dataframe.
    @param dataset -- a xarray dataset.
    @param variables -- a tuple or list of variable names.
    '''
    
    df = pd.DataFrame()
    for variable in variables:
        column = pd.DataFrame(data = {variable:dataset[variable]})
        df = pd.concat([df,column],axis = 1)
    if close is True:
        dataset.close()
    return df


def sort_df(df,variable='time'):
    '''A function that sorts a dataframe by the prescribed variable.
    Variable must be numeric or a datetime. Sorting is descending.
    @param df -- a pandas dataframe.
    @param variable -- the variable to sort by.
    '''
    
    df = df.sort_values(variable,axis=0,kind = 'mergesort')
    return df

def df_drop_range(df,variable,minimum,maximum):
    df = df[df[variable] > minimum]
    df = df[df[variable] < maximum]
    return df

def time_avg_df(df,avg='1S'):
    '''A function that time averages the entire dataframe given an input.
        Rows with nans are removed.
    @param df -- a pandas dataframe, must have a 'time' column.
    @param avg -- a pd.resample() valid value.
    '''
    
    df.index = pd.DatetimeIndex(df.time)
    df = df.resample('1S').mean().dropna()
    return df


def json2df(json):
    df = pd.read_json(json)
    return df