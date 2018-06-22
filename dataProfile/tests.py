import os
import json
import pandas as pd


# Create your tests here.
# gets the data for the scatter plot
def get_scatter_data(data_source, x, y, z):
    df_x = json.load(open(os.getcwd() + '/static/data/output/' +
                          data_source + '/variable_' + x + '.json'))
    df_y = json.load(open(os.getcwd() + '/static/data/output/' +
                          data_source + '/variable_' + y + '.json'))

    df = pd.DataFrame(df_x['values'], columns=['x'])
    df['y'] = df_y['values']

    # remove any missing values
    df = df.loc[(pd.notnull(df['x']) & pd.notnull(df['y'])), :]
    df = df.groupby(df.columns.tolist()).size(
    ).reset_index().rename(columns={0: 'count'})
    # x = df['x'].values
    # y = df['y'].values
    # z = df['count'].values
    #
    # dict_res = []
    # for i in range(len(x)):
    #     dict_res.append({"x": x[i], "y": y[i], "z": z[i]})

    # if z is blank then we use the count as the size or z value
    dict_res = df.to_dict(orient='record')
    print(dict_res)
    return json.dumps(dict_res)


get_scatter_data('Titanic', 'Age', 'Fare_Ammount', '')
