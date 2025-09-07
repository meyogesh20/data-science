# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px


# -------------------------------
# Load Dataset
# -------------------------------
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()


# -------------------------------
# Dropdown Options
# -------------------------------
options = [
    {"label": "All Sites", "value": "ALL"},
    {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
    {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
    {"label": "KSC LC-39A", "value": "KSC LC-39A"},
    {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
]

# Grouped data (note: your renaming was overwriting columns)
spacex_all = spacex_df.groupby("Launch Site")["class"].value_counts().reset_index()
spacex_all.columns = ["Launch Site", "class", "count"]

# Slider marks
marks = {0: "0", 2500: "2500", 5000: "5000", 7500: "7500", 10000: "10000"}


# -------------------------------
# Initialize Dash App
# -------------------------------
app = dash.Dash(__name__)


# -------------------------------
# App Layout
# -------------------------------
app.layout = html.Div(
    children=[
        # Title
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Dropdown
        dcc.Dropdown(
            id="site-dropdown",
            value="ALL",
            options=options,
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Pie Chart
        html.Div(
            dcc.Graph(
                id="success-pie-chart",
                figure=px.pie(
                    spacex_all,
                    names="class",
                    title="Total Success Launches for All Sites",
                ),
            )
        ),
        html.Br(),
        # TASK 3: Range Slider
        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks=marks,
            value=[min_payload, max_payload],
        ),
        # TASK 4: Scatter Plot
        html.Div(
            dcc.Graph(
                id="success-payload-scatter-chart",
                figure=px.scatter(
                    spacex_df,
                    x="Payload Mass (kg)",
                    y="class",
                    color="Booster Version Category",
                    title="Correlation between Payload and Success for all Sites",
                ),
            )
        ),
    ]
)


# -------------------------------
# TASK 2: Callback for Pie Chart
# -------------------------------
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def update_pie_chart(selected_site):
    df_render = spacex_df

    if selected_site == "ALL":
        fig = px.pie(
            spacex_all,
            names="class",
            values="class",  # ⚠ Placeholder (incomplete logic from your code)
            title="Total Success Launches for All Sites",
        )
    else:
        df_render = spacex_df[spacex_df["Launch Site"] == selected_site]
        pie_data = df_render["class"].value_counts().reset_index()
        pie_data.columns = ["index", "class"]

        fig = px.pie(
            pie_data,
            names="index",
            values="class",
            title=f"Total Success Launches for site {selected_site}",
        )

    return fig


# -------------------------------
# TASK 4: Callback for Scatter Plot
# -------------------------------
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def update_scatter_chart(selected_site, payload_range):
    df_render = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= payload_range[0])
        & (spacex_df["Payload Mass (kg)"] <= payload_range[1])
    ]

    if selected_site == "ALL":
        fig = px.scatter(
            df_render,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for all Sites",
        )
    else:
        df_render = df_render[df_render["Launch Site"] == selected_site]
        fig = px.scatter(
            df_render,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Correlation between Payload and Success for site {selected_site}",
        )

    return fig


# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run()
