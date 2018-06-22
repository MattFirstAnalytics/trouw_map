# generates the stats for the summary statistics
import os
import time
import json
import pandas as pd
import numpy as np
from scipy import stats


def generate_profile(file_name):

    data_type_dict = {'int64': 'Numeric', 'float64': 'Numeric',
                      'object': 'Categorical', 'bool': 'Boolean'}
    data_type_index = ['Numeric', 'Categorical', 'Date', 'Boolean', 'Misc']

    print('------------------')
    print('Starting Profiler')

    output_path = os.getcwd() + '/dataProfile/static/data/output/' + \
        os.path.basename(file_name).replace('.csv', '')
    data_summary_path = output_path + '/summary.csv'
    column_summary_path = output_path + '/summary.csv'
    variable_summary_path = output_path + '/variable_summary.csv'
    json_test = output_path + '/variables.json'
    corr_path = output_path + '/correlation.csv'
    missing_count_path = output_path + '/missing_count.csv'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    df = pd.read_csv(file_name)
    print('Data Loaded')
    print('Data Shape')
    print(df.shape)

    # generates the summary
    print('Generating Summary')
    df_res = pd.DataFrame(index=[
                          'File Name', 'Rows', 'Variable', 'Created', 'Last Modified'], columns=['values'])
    df_res.loc['File Name', 'values'] = os.path.basename(file_name)
    df_res.loc['Rows', 'values'] = df.shape[0]
    df_res.loc['Variable', 'values'] = df.shape[1]
    df_res.loc['Created', 'values'] = time.ctime(os.path.getmtime(file_name))
    df_res.loc['Last Modified', 'values'] = time.ctime(
        os.path.getctime(file_name))

    df_res = df_res.reset_index()
    df_res.columns = ['Metric', 'Value']
    df_res.to_csv(data_summary_path, index=False)

    # generates the variable summary
    print('Generating Variable Summary')
    df_res = pd.DataFrame(index=data_type_index)
    df_res['values'] = 0
    types = df.dtypes
    for t in types:
        df_res.loc[data_type_dict[str(
            t)], 'values'] = df_res.loc[data_type_dict[str(t)], 'values'] + 1

    df_res = df_res.reset_index()
    df_res.columns = ['Metric', 'Value']
    df_res.to_csv(variable_summary_path, index=False)

    # saves the varialbe names and data type
    json_res = []
    for c in df.columns:
        # unique
        values = list(df.loc[:, c].values)
        if df[c].dtype in ['int64', 'bool']:
            # converts the values to python types (needed to save as json)
            values = [v.item() for v in values]
        n_unique = len(set(values))
        percent_unique = str(int(n_unique / len(values) * 100)) + '%'

        # missing
        n_missing = sum(df[c].isnull()).item()
        percent_missing = str(int(n_missing / len(values) * 100)) + '%'

        # data type
        if percent_unique == '100%':
            data_type = 'Unique'
        else:
            data_type = data_type_dict[str(df[c].dtype)]

        json_res.append({'name': c.replace('_', ' '),
                         'name_underscore': c.replace(' ', '_'),
                         'n_unique': n_unique,
                         'percent_unique': percent_unique,
                         'n_missing': n_missing,
                         'percent_missing': percent_missing,
                         'type': data_type})

    json_res = {'variables': json_res}
    with open(json_test, 'w') as f:
        json.dump(json_res, f)

    # makes the correlation table
    print('Generating Correlation Values')
    df_res = df.copy()
    df_res = df_res.corr()

    # remove the main diagonal
    rem_list = []
    for c1 in df_res.columns:
        df_res.loc[c1, c1] = np.nan
        for c2 in df_res.columns:
            if [c1, c2] not in rem_list and [c2, c1] not in rem_list:
                df_res.loc[c1, c2] = np.nan
                rem_list.append([c1, c2])

    # melts the dataframe
    c = df_res.columns
    df_res = df_res.reset_index()
    df_res = pd.melt(df_res, id_vars=['index'], value_vars=c)
    df_res = df_res.loc[pd.notnull(df_res['value']), :]

    # sorts the values
    df_res['corr_squared'] = df_res['value'] ** 2
    df_res = df_res.sort_values('corr_squared', ascending=False)

    # clean up
    df_res = df_res.drop('corr_squared', 1)
    df_res.columns = ['var_1', 'var_2', 'corr']
    df_res = df_res.reset_index(drop=True)

    # saves the results
    df_res.to_csv(corr_path, index=False)

    # makes missing data stats
    print('Generating Missing Summary')
    columns = df.columns
    df_res = pd.DataFrame(columns)
    df_res.columns = ['Variable Name']
    df_res['n Missing'] = "NA"
    df_res['% Missing'] = "NA"
    for c in df.columns:
        print('    ' + c)
        n_missing = sum(df[c].isnull())
        df_res.loc[df_res['Variable Name'] == c, 'n Missing'] = n_missing
        df_res.loc[df_res['Variable Name'] == c, '% Missing'] = str(
            int((n_missing / df.shape[0]) * 100)) + '%'

    df_res = df_res.sort_values(by=['n Missing'], ascending=False)
    df_res.to_csv(missing_count_path, index=False)

    # saves stats on each column
    print('Saving Variable Data')
    for c in df.columns:
        print('    ' + c)
        dict_res = {}

        # the object type
        dict_temp = {}
        dict_temp['Type'] = str(df[c].dtype)

        # unique
        values = list(df.loc[:, c].values)
        if df[c].dtype in ['int64', 'bool']:
            # converts the values to python types (needed to save as json)
            values = [v.item() for v in values]
        dict_temp['Unique n'] = len(set(values))
        dict_temp['Unique %'] = str(
            int(dict_temp['Unique n'] / len(values) * 100)) + '%'

        # missing
        dict_temp['Missing n'] = sum(df[c].isnull()).item()
        dict_temp['Missing %'] = str(
            int(dict_temp['Missing n'] / len(values) * 100)) + '%'

        # min mean max
        if dict_temp['Type'] != 'object':
            dict_temp['Min'] = min(values)
            dict_temp['Mean'] = np.mean(values)
            dict_temp['Max'] = max(values)
            # dict_temp['Mode'] = stats.mode(df[c])[0][0].item()

        # appends the properties
        dict_res['Properties'] = dict_temp

        # gets the values
        dict_res['values'] = values

        # file_name = c.replace(' ', '_')
        file_name = output_path + '/variable_' + c + '.json'

        with open(file_name, 'w') as f:
            json.dump(dict_res, f)


# file_path = 'C:/Users/Matth/OneDrive - First Analytics/Repos/datachar/dataProfile/static/data/input/Titanic.csv'
# generate_profile(file_path)
