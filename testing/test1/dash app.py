# import packages
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# initialize the app with stylesheets
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# data sets
pbc_df = pd.read_csv('data.csv')
iris = pd.DataFrame(pbc_df).sort_values(by='month')
gapminder = px.data.gapminder()
tips = px.data.tips()
carshare = px.data.carshare()

df = pd.DataFrame(dict(
    r=[1, 5, 2, 2, 3],
    theta=['processing cost','mechanical properties','chemical stability',
           'thermal stability', 'device integration']))


nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Active", active=True, href="#")),
        dbc.NavItem(dbc.NavLink("A link", href="#")),
        dbc.NavItem(dbc.NavLink("Another link", href="#")),
        dbc.NavItem(dbc.NavLink("Disabled", disabled=True, href="#")),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Item 1"), dbc.DropdownMenuItem("Item 2")],
            label="Dropdown",
            nav=True,
        ),
    ]
)

    
breadcrumb = dbc.Breadcrumb(
    items=[
        {"label": "Docs", "href": "/docs", "external_link": True},
        {
            "label": "Components",
            "href": "/docs/components",
            "external_link": True,
        },
        {"label": "Breadcrumb", "active": True},
    ],
)

figure_templates = [
    "plotly",
    "ggplot2",
    "seaborn",
    "simple_white",
    "plotly_white",
    "plotly_dark",
    "presentation",
    "xgridoff",
    "ygridoff",
    "gridon",
    "none",
]

header = html.Div(
    [
        html.Div(html.H1('Dashboard')),
    ],
)

change_figure_template = html.Div(
    [
        html.Div("Change figure template"),
        dcc.Dropdown(figure_templates, figure_templates[0], id="template"),
    ],
    className="pb-4",
)


app.layout = dbc.Container(
    [   
        dbc.Row(dbc.Col(header, width='auto')),            
        dbc.Row(dbc.Col(breadcrumb, lg=6)),
        dbc.Row(dbc.Col(change_figure_template, lg=6)),
        dbc.Row(dbc.Col(nav, lg=6)),
        dbc.Row(dbc.Col(html.Div(id="graphs"))),
    ],
    className="dbc p-4",
    fluid=True,
)


@app.callback(
    Output("graphs", "children"),
    Input("template", "value"),
)

def update_graph_theme(template):
    graph1 = dcc.Graph(
        figure=px.line(
            iris,
            x="month",
            y="profit",
            # color="ee",
            title=f"Iris <br>{template} figure template",
            template=template,
        ),
        className="border",
    )
    graph2 = dcc.Graph(
        figure=px.scatter(
            gapminder,
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            hover_name="country",
            animation_frame="year",
            animation_group="country",
            log_x=True,
            size_max=60,
            title=f"Gapminder <br>{template} figure template",
            template=template,
        ),
        className="border",
    )
    graph3 = dcc.Graph(
        figure=px.violin(
            tips,
            y="tip",
            x="smoker",
            color="sex",
            box=True,
            points="all",
            hover_data=tips.columns,
            title=f"Tips <br>{template} figure template",
            template=template,
        ),
        className="border",
    )
    graph4 = dcc.Graph(
        figure=px.scatter_mapbox(
            carshare,
            lat="centroid_lat",
            lon="centroid_lon",
            color="peak_hour",
            size="car_hours",
            size_max=15,
            zoom=10,
            mapbox_style="carto-positron",
            title=f"Carshare <br> {template} figure template",
            template=template,
        ),
        className="border",
    )
    graph5 = dcc.Graph(
        figure = px.line_polar(
            df, r='r',
            theta='theta', 
            line_close=True
            ),
    )

    return [
        dbc.Row([dbc.Col(graph1, lg=6), dbc.Col(graph2, lg=6)]),
        dbc.Row([dbc.Col(graph3, lg=6), dbc.Col(graph4, lg=6)], className="mt-4"),
        dbc.Row([dbc.Col(graph5, lg=6), dbc.Col()])
    ]


if __name__ == "__main__":
    app.run_server(debug=True)
