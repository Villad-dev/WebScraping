import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash import dash_table

df = pd.read_csv("Data.csv", sep=",")

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Dash Graph"),
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="dropdown",
                    children=[
                        html.Label("Model Type:"),
                        dcc.Dropdown(
                            id="model-type",
                            options=[
                                {"label": "Regression", "value": "regression"},
                                {"label": "Classification", "value": "classification"},
                            ],
                            value="regression",
                        ),
                        html.Label("Select Column:"),
                        dcc.Dropdown(
                            id="column-selector",
                            options=[
                                {"label": col, "value": col}
                                for col in df.columns.tolist()
                            ],
                            value="residual sugar",
                        ),
                    ],
                )
            ],
        ),
        dcc.Graph(id="graph", className="graph"),
        html.H2("Data Table"),
        dash_table.DataTable(
            id="data-table",
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),
        ),
    ]
)


@app.callback(
    dash.dependencies.Output("graph", "figure"),
    dash.dependencies.Input("model-type", "value"),
    dash.dependencies.Input("column-selector", "value"),
)
def table_update(model_type, selected_column):
    if model_type == "regression":
        fig = px.scatter(
            df,
            x=selected_column,
            y="pH",
        )
    elif model_type == "classification":
        fig = px.histogram(
            df, x="alcohol", color="target", color_discrete_sequence=["red", "white"]
        )
    else:
        fig = None

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
