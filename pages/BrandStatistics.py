from dash import html, dcc, Input, Output, callback
import dash
import pandas as pd
import plotly.express as px
import json

df = pd.read_csv("cleanedVehicleSet.csv")

df.dropna(inplace=True)

brands = df["make"].sort_values().unique().tolist()
models = df["model"].where(df["make"] == brands[0]).sort_values().unique().tolist()

geodata = json.load(open("north_america_states.json"))

salesPerState = df["vin"].groupby(df["state"]).count().to_frame().reset_index()

state_abbreviations = {
    "Alabama": "AL",
    "Alberta": "AB",
    "Arizona": "AZ",
    "California": "CA",
    "Colorado": "CO",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Illinois": "IL",
    "Indiana": "IN",
    "Louisiana": "LA",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "Nova Scotia": "NS",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Ontario": "ON",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Quebec": "QC",
    "South Carolina": "SC",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Virginia": "VA",
    "Washington": "WA",
    "Wisconsin": "WI",
}

brandSales = (
    df[["vin", "make", "model"]].groupby(["make", "model"]).count().reset_index()
)
brandSales.columns = ["make", "model", "sales"]
brandSales["sales"] = (brandSales["sales"] / 1000).round(1)
marketSharesFig = px.treemap(
    brandSales,
    path=[px.Constant("All Brands"), "make", "model"],
    values=brandSales["sales"]
)

marketSharesFig.update_layout(
    width=650,
    height=950,
    title={
        "text": "Market-shares of different manufacturers",
        "xanchor": "right",
        "yanchor": "top",
        "x": 0.895,
    },
    title_font=dict(size=24),
    title_font_weight=750,
    title_font_family="Courier New",
    margin={"l": 0, "r": 0, "t": 80, "b": 0},
)

marketSharesFig.update_traces(
    hovertemplate="<b>%{value}k cars<b>",
    hoverlabel=dict(bgcolor="white", font=dict(color="black")),
)


@callback(
    Output("output-div", "children"),
    Output("modelSelector", "options"),
    Output("modelSelector", "value"),
    Input("brandSelector", "value"),
)
def update_graph_and_additional_content(selected_option):

    model_counts = (
        df["vin"]
        .where(df["make"] == selected_option)
        .groupby(df["model"])
        .count()
        .sort_values(ascending=False)[:20]
        .sort_values()
        .loc[lambda x: x > 0]
    )

    ModelCountFig = px.bar(x=model_counts.values, y=model_counts.index, orientation="h")

    ModelCountFig.update_layout(
        width=900,
        height=475,
        title={
            "text": "Most Purchased Models",
            "xanchor": "left",
            "yanchor": "top",
            "x": 0,
        },
        title_font={"size": 24},
        yaxis_title="Model",
        yaxis_title_font={"size": 18},
        xaxis_title="Units Sold",
        xaxis_title_font={"size": 18},
    )

    ModelCountFig.update_traces(
        hovertemplate="%{y}: %{x}",
        marker_line_width=1.5,
    )

    additional_content = html.Div(
        [
            html.Div(id="model-specific-div", children="Select a model"),
        ],
    )

    models = (
        df["model"].where(df["make"] == selected_option).sort_values().unique().tolist()
    )

    return [
        html.Div(
            [
                dcc.Graph(figure=ModelCountFig),
                additional_content,
            ]
        ),
        models,
        models[0],
    ]


@callback(
    Output("model-specific-div", "children"),
    Input("modelSelector", "value"),
    Input("brandSelector", "value"),
)
def update_Model_Specific_Stuff(selected_model="CL", selected_brand="Acura"):

    MostPopularTrims = (
        df[["vin", "model", "trim"]]
        .where(df["make"] == selected_brand)
        .where(df["model"] == selected_model)
        .dropna()
        .groupby(["model", "trim"])
        .count()
        .reset_index()
    )

    MostPopularTrimsFig = px.sunburst(
        MostPopularTrims,
        path=["model", "trim"],
        values="vin",
        custom_data=["model", "trim", "vin"],
    )

    MostPopularTrimsFig.update_layout(
        title={"text": "Most popular trims"},
        width=400,
        height=400,
        margin={"l": 10, "r": 10, "t": 50, "b": 10},
        title_font=dict(size=24),
        title_font_weight=750,
        title_font_family="Courier New",
    )

    MostPopularTrimsFig.update_traces(
        hovertemplate="<b>%{customdata[2]} cars</b>",
        hoverlabel=dict(bgcolor="white", font=dict(color="black")),
    )

    stateSaleCounts = (
        df["vin"][df["make"] == selected_brand]
        .where(df["model"] == selected_model)
        .dropna()
        .groupby(df["state"])
        .count()
        .sort_values(ascending=False)
        .reset_index()
    )

    stateSaleCounts["Abbreviation"] = stateSaleCounts["state"].map(state_abbreviations)

    stateSaleCountsFig = px.choropleth(
        data_frame=stateSaleCounts,
        locations="Abbreviation",
        geojson=geodata,
        color="vin",
        scope="north america",
        width=500,
        height=400,
        hover_name="vin",
        hover_data={"vin": False, "Abbreviation": False},
    )

    stateSaleCountsFig.update_geos(
        projection_scale=1.7,
        center={"lat": 40, "lon": -120},
    )

    titleText = f"Sales in different regions <br>{selected_brand} | {selected_model}"

    stateSaleCountsFig.update_layout(
        title={
            "text": titleText,
            "xanchor": "left",
            "yanchor": "top",
            "x": 0.042,
        },
        title_font=dict(size=24),
        title_font_weight=750,
        title_font_family="Courier New",
        margin=dict(l=10, r=10, t=50, b=10),
    )

    stateSaleCountsFig.update_traces(
        hovertemplate="<b>%{customdata[0]}:</b> %{z}<extra></extra>",
        customdata=stateSaleCounts[["state"]],
    )

    return html.Div(
        [dcc.Graph(figure=MostPopularTrimsFig), dcc.Graph(figure=stateSaleCountsFig)],
        style={"display": "flex", "flex-direction": "row"},
    )

dash.register_page(__name__, name="Brand Statistics")

layout = html.Div(
    [
        dcc.Graph(figure=marketSharesFig),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            brands,
                            brands[0],
                            id="brandSelector",
                            searchable=False,
                            style={"width": 300},
                        ),
                        dcc.Dropdown(
                            models,
                            models[0],
                            id="modelSelector",
                            searchable=False,
                            style={"width": 300},
                        ),
                    ],
                    style={"display": "flex", "flex-direction": "row", "gap": 10},
                ),
                html.Div(id="output-div"),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-left": "10px",
            },
        ),
    ],
    style={"display": "flex", "flex-direction": "row"},
)