# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label':'All Sites', 'value':'ALL'},
                                                    {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                    {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                                    {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                                    {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                                ],
                                                value='ALL',
                                                placeholder='Select a launch site here',
                                                searchable=True
                                                ),




                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0:'0',
                                                100:'100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id="success-pie-chart", component_property="figure"),
              Input(component_id="site-dropdown", component_property="value"))

def get_pie_chart(entered_site):
    new_df = spacex_df.groupby(["Launch Site","class"]) ["class"].count().reset_index(name='cnt')
    #pvt = pd.pivot_table(new_df, values='cnt', index='Launch Site', columns=['class'])
    pvt = pd.pivot_table(new_df, values="cnt", index="Launch Site", columns=["class"])
    pvt.rename(columns={0:'F', 1:'S'}, inplace=True)
    #filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = pvt
        fig = px.pie(filtered_df, 
        values="S", 
        names=filtered_df.index, 
        title="Launch Success Rate")
        return fig
    else:
        filtered_df = pvt.loc[entered_site]       
        fig = px.pie(values = filtered_df, 
        names=["Failure","Success "],
        title='Launch Success Rate')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))

def get_scatter_chart(entered_site, payld):
    #filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = spacex_df
        low, high = payld
        mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
        fig = px.scatter(filtered_df[mask],
        x='Payload Mass (kg)', 
        y='class', 
        color='Booster Version Category')
        return fig

    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        low, high = payld
        mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
        fig = px.scatter(filtered_df[mask], 
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category')
        return fig
        # return the outcomes piechart for a selected site



# Run the app
if __name__ == '__main__':
    app.run_server()













