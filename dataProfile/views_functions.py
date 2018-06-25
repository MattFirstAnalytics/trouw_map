from django.utils.safestring import mark_safe
import pandas as pd
import numpy as np
import glob
import os
import json


# helper functions
def read_csv(file_path, name):
    df = pd.read_csv(file_path)
    columns = df.columns
    values = df.values.tolist()
    return {name: {'columns': columns, 'values': values}}


def append_csv(file_path, name, data_dictionary):
    # reads in the data
    df = pd.read_csv(file_path)
    columns = df.columns
    values = df.values.tolist()

    # appends it to the dictionary
    data_dictionary[name] = {'columns': columns, 'values': values}
    return data_dictionary


def load_preview_data(file_path, range_start, range_end, name, data_dictionary):
    # reads in the data
    df = pd.read_csv(file_path, skiprows=range(1, int(range_start)), nrows=int(range_end) - int(range_start))
    columns = df.columns
    values = df.values.tolist()

    # appends it to the dictionary
    data_dictionary[name] = {'columns': columns, 'values': values}
    return data_dictionary


def append_json(file_path, name, data_dictionary):
    with open(file_path, 'r') as f:
        json_str = f.read()
    json_data = json.loads(json_str)
    data_dictionary[name] = json_data
    return data_dictionary


def append_json_columns(file_path, name, data_dictionary):
    with open(file_path, 'r') as f:
        json_str = f.read()
    json_data = json.loads(json_str)

    # function for checking the data
    def data_check(v):
        if type(v) is str:
            return True
        else:
            return np.isnan(v) == False

    json_data['values'] = [x for x in json_data['values'] if data_check(x)]
    data_dictionary[name] = json_data
    return data_dictionary


# gets the data for the scatter plot
def get_scatter_data(data_source, x, y, z):
    df_x = json.load(open(os.getcwd() + '/dataProfile/static/data/output/' + data_source + '/variable_' + x + '.json'))
    df_y = json.load(open(os.getcwd() + '/dataProfile/static/data/output/' + data_source + '/variable_' + y + '.json'))

    df = pd.DataFrame(df_x['values'], columns=['x'])
    df['y'] = df_y['values']

    # checks what we want the z variable to be
    if z == "N Observations":
        # if z is blank then we use the count as the size or z value
        # remove any missing values
        df = df.loc[(pd.notnull(df['x']) & pd.notnull(df['y'])), :]
        df = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0:'count'})
        df.columns = ['x', 'y', 'z']
    else:
        df_z = json.load(open(os.getcwd() + '/dataProfile/static/data/output/' + data_source + '/variable_' + z + '.json'))
        df['z'] = df_z['values']
        # remove any missing values
        df = df.loc[(pd.notnull(df['x']) & pd.notnull(df['y']) & pd.notnull(df['z'])), :]

    # sorts by size
    df = df.sort_values(['z'], ascending=False)
    dict_temp = df.to_dict(orient='record')
    dict_res = {}
    dict_res['values'] = dict_temp

    # appends the min and max stats
    dict_res['x_min'] = df['x'].min().item()
    dict_res['x_max'] = df['x'].max().item()
    dict_res['y_min'] = df['y'].min().item()
    dict_res['y_max'] = df['y'].max().item()
    dict_res['z_min'] = df['z'].min().item()
    dict_res['z_max'] = df['z'].max().item()

    return json.dumps(dict_res)


# gets data for the preview based on what was selected in the scatter plot
def load_preview_from_scatter(file_path, scatter_data, name, data_dictionary):
    scatter_data = json.loads(scatter_data)
    x_list = [i['x'] for i in scatter_data["scatter_data"]]
    y_list = [i['y'] for i in scatter_data["scatter_data"]]
    z_list = [i['z'] for i in scatter_data["scatter_data"]]

    # reads in the data
    df = pd.read_csv(file_path)
    # checks if we need to sort by z
    if scatter_data['z'] == 'N Observations':
        df = df.loc[(df[scatter_data['x']].isin(x_list)) & (df[scatter_data['y']].isin(y_list)), :]
    else:
        df = df.loc[(df[scatter_data['x']].isin(x_list)) & (df[scatter_data['y']].isin(y_list)) & (df[scatter_data['z']].isin(z_list)), :]

    # does the filtering
    columns = df.columns
    values = df.values.tolist()

    # appends it to the dictionary
    data_dictionary[name] = {'columns': columns, 'values': values}
    return data_dictionary


def get_unique_lists(file_name):
    res = {}
    df = pd.read_csv('/home/matt/FirstAnalytics/trouw/webapp/dataProfile/static/data/BEA.csv')
    df = df.drop('Invoiced Quantity Kgs', axis=1)
    for c in df.columns:
        res[c.replace(' ', '_')] = list(df[c].unique())
    # print(res)
    return(res)
    # print(df.head())