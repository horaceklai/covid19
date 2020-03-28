import os.path
import pandas as pd
import math
import plotly
import plotly.graph_objects as go

# File locations
data_file_path = os.path.join(
    "john_hopkins_data",
    "csse_covid_19_data",
    "csse_covid_19_time_series",
    "time_series_covid19_deaths_global.csv"
)
population_data_file = 'pop_data.csv'


# Load data
data = pd.read_csv(data_file_path, ',')
pop_data = pd.read_csv(population_data_file, ',')


# Merge data
data.set_index(['Province/State', 'Country/Region'], inplace=True)
pop_data.set_index(['Province/State', 'Country/Region'], inplace=True)
merged_data = data.merge(pop_data, on=['Province/State', 'Country/Region'])


# Calculate deaths per million people
all_columns = list(merged_data.columns)
all_dates = [x for x in all_columns if x not in ['Lat', 'Long', 'Population'] ]
merged_data[all_dates] = merged_data[all_dates].div(merged_data['Population'], axis='index').mul(1000000)


# Squeeze all deaths data into 1 array
merged_data['Death Array'] = merged_data[all_dates].values.tolist()
# Remove leading numbers that are < 1
def reduce(row):
    return [x for x in row if x >= 1]
merged_data['Death Array'] = [reduce(row) for row in merged_data['Death Array']]


## Plot the death arrays
fig = go.Figure()
for idx in merged_data.index:
    if type(idx[0]) != str:
        name_str = idx[1]
    else:
        name_str = idx[0] + ', ' + idx[1]

    fig.add_trace(go.Scatter(
        x=list(range(len(merged_data['Death Array'][idx]))),
        y=merged_data['Death Array'][idx],
        mode='lines',
        name=name_str
    ))

plotly.offline.plot(fig, filename='deaths_per_million_from_day0.html')