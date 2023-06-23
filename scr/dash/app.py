import dash
import base64
import requests
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output




df = pd.read_csv('Formated.csv', sep=',', low_memory=False)

app = dash.Dash(__name__)

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

total_fatalities = df['Fatalities'].sum()
category_counts = df['Category'].value_counts()

country_deaths = df.groupby('Country')['Fatalities'].sum().reset_index()
country_deaths = country_deaths.sort_values('Fatalities', ascending=False)

bar_chart = px.bar(country_deaths, x='Country', y='Fatalities', title='Total Fatalities by Crash Location(Country)')

history = {
    'A': 'Accident',
    'I': 'Incident',
    'H': 'Hijacking',
    'C': 'Criminal occurrence (sabotage, shoot down)',
    'O': 'Other occurrence (ground fire, sabotage)',
    'U': 'Type of occurrence unknown',
    '1': 'Hull-loss',
    '2': 'Repairable damage'
}

category_dropdown ={
    "Category",
    "Phase",
    "Nature"
}

regression_dropdown =[
    "Index",
    "Date",
    "Fatalities",
    "Crew",
    "Crew Fatalities",
    "Passengers",
    "Passengers Fatalities",
    "Total Fatalities",
    "Total airframe hrs"
]


app.layout = html.Div(children=[
    html.H1(children='Airplane Accidents Statistics'),

    html.Div(children=[
        html.H3(children='Total Fatalities'),
        html.P(children=
            "From 1919 till 2023 there were " + '{:,}'.format(total_fatalities) + " deaths in flight accidents which is about "+ '{:.2%}'.format(total_fatalities/(3700*365*104)) + " of chance to be in a car accident with a fatal ending"
        ),
    ], className='statistic-card'),

    html.Div(children=[
        html.Div(children=[
            html.Label('Select Year Range:')
        ], className='slider-label'),

        dcc.RangeSlider(
            id='year-range-slider',
            marks={str(year): str(year) for year in df['Date'].dt.year.unique()},
            min=df['Date'].dt.year.min(),
            max=df['Date'].dt.year.max(),
            value=[df['Date'].dt.year.min(), df['Date'].dt.year.max()],
            className='year-range-slider',
            step=1
        ),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': col, 'value': col} for col in category_dropdown],
            value = 'Category',
            placeholder='Select Category'
        ),
        html.Div(children=[
            html.Div(children=[
                dcc.Graph(id='category-pie'),#, figure=category_pie),
            ], className='chart-container'),

            html.Div(children=[
                html.P(id= 'pie-label',
                       children='Category'),
                html.Ul([html.Li(f'{key} = {value}') for key, value in history.items()])
            ], className='explanation-container')
        ], className='graph-card')
    ], className='container'),

    html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Dropdown(
                        id='x-axis-dropdown',
                        options=[{'label': col, 'value': col} for col in regression_dropdown],
                        value="Index",
                        placeholder='Select x-axis column'
                    ),
                    dcc.Dropdown(
                        id='y-axis-dropdown',
                        options=[{'label': col, 'value': col} for col in regression_dropdown],
                        value="Fatalities",
                        placeholder='Select Y-axis column'
                    )
                ],
                className='dropdown-container'
            ),
            dcc.Graph(id='line-graph'),
            html.Img(id='hover-image', style={'padding': '10px', 'margin' : '10px'}),
            html.Div(id='hover-data', style={'padding': '10px'})
        ],
        className='graph-container'
    ),
    dcc.Graph(id='fatalities-bar', figure=bar_chart),
    html.Div([
        html.H3('Classification'),
        html.Img(src=app.get_asset_url('Classification with prediction.png')),
    ], className='plot-card'),

    html.H2("Data Table"),
    dash_table.DataTable(
        id='dash-table',
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict('records'),
    )
])

@app.callback(
    [Output('category-pie', 'figure'),
     Output('pie-label', 'children')],
    [Output('line-graph', 'figure')],
     Output('hover-image', 'src'),
    [Input('year-range-slider', 'value'),
     Input('category-dropdown', 'value')],
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')],
     Input("line-graph", "hoverData"),
)
def update_charts(year_range, category, x_axis, y_axis, hover_info):
    #print(hover_info)
    pie_chart, pie_label = update_pie_chart(year_range, category)
    regression_graph = update_regression_graph(x_axis, y_axis)
    img = display_hover_image(hover_info)
    return pie_chart, pie_label, regression_graph, img

def update_pie_chart(year_range, category):
    filtered_data = df[(df['Date'].dt.year >= year_range[0]) & (df['Date'].dt.year <= year_range[1])]
    category_counts = filtered_data[category].value_counts()
    pie_chart = px.pie(category_counts, values=category_counts.values, names=category_counts.index,
                       title=category)
    pie_chart.update_traces(textposition='inside', textinfo='label+percent')
    pie_label = f"Selected category: {category}"
    return pie_chart, pie_label

def update_regression_graph(x_axis_name, y_axis_name):
    regression_graph = px.scatter(df, x=x_axis_name, y=y_axis_name, trendline='ols', title='Regression Graph', hover_data=['Image link', 'Narrative', 'Aircraft damage', 'Departure airport', 'Destination airport', 'Type'])
    regression_graph.update_traces(hovertemplate="<b>" + x_axis_name + ": %{x}</b><br>" + y_axis_name + ": %{y}<br><b>Type: %{customdata[5]}<br></b><b>Departure airport: %{customdata[3]}<br></b><b>Destination airport: %{customdata[4]}<br></b><b>Aircraft damage: %{customdata[2]}<br></b><b>Narrative: %{customdata[1]}<br></b><img src='%{customdata[0]}'>")
    return regression_graph

def display_hover_image(hover_data):
    if hover_data is not None:
        image_url = hover_data['points'][0]['customdata'][0]
        if image_url:
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    encoded_image = base64.b64encode(requests.get(image_url).content)
                    return f'data:image/gif;base64,{encoded_image.decode()}'
            except requests.exceptions.RequestException:
                pass
    return ''



if __name__ == '__main__':
    app.run_server(debug=True)