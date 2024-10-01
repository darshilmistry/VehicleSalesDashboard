# %%
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
import json

# %%
df = pd.read_csv("cleanedData.csv")

# %%
body_mapping = {
    "SUV": "SUV",
    "Sedan": "Sedan",
    "Convertible": "Convertible",
    "Coupe": "Coupe",
    "Wagon": "Wagon",
    "Hatchback": "Hatchback",
    "Crew Cab": "Truck",
    "G Coupe": "Coupe",
    "G Sedan": "Sedan",
    "Elantra Coupe": "Coupe",
    "Genesis Coupe": "Coupe",
    "Minivan": "Minivan",
    "Van": "Van",
    "Double Cab": "Truck",
    "CrewMax Cab": "Truck",
    "Access Cab": "Truck",
    "King Cab": "Truck",
    "SuperCrew": "Truck",
    "CTS Coupe": "Coupe",
    "Extended Cab": "Truck",
    "E-Series Van": "Van",
    "SuperCab": "Truck",
    "Regular Cab": "Truck",
    "G Convertible": "Convertible",
    "Koup": "Coupe",
    "Quad Cab": "Truck",
    "CTS-V Coupe": "Coupe",
    "sedan": "Sedan",
    "G37 Convertible": "Convertible",
    "Club Cab": "Truck",
    "Xtracab": "Truck",
    "Q60 Convertible": "Convertible",
    "CTS Wagon": "Wagon",
    "convertible": "Convertible",
    "G37 Coupe": "Coupe",
    "Mega Cab": "Truck",
    "Cab Plus 4": "Truck",
    "Q60 Coupe": "Coupe",
    "Cab Plus": "Truck",
    "Beetle Convertible": "Convertible",
    "TSX Sport Wagon": "Wagon",
    "Promaster Cargo Van": "Van",
    "GranTurismo Convertible": "Convertible",
    "CTS-V Wagon": "Wagon",
    "Ram Van": "Van",
    "minivan": "Minivan",
    "suv": "SUV",
    "Transit Van": "Van",
    "van": "Van",
    "regular-cab": "Truck",
    "g sedan": "Sedan",
    "g coupe": "Coupe",
    "hatchback": "Hatchback",
    "king cab": "Truck",
    "supercrew": "Truck",
    "g convertible": "Convertible",
    "coupe": "Coupe",
    "crew cab": "Truck",
    "wagon": "Wagon",
    "double cab": "Truck",
    "e-series van": "Van",
    "regular cab": "Truck",
    "quad cab": "Truck",
    "g37 convertible": "Convertible",
    "supercab": "Truck",
    "extended cab": "Truck",
    "crewmax cab": "Truck",
    "genesis coupe": "Coupe",
    "access cab": "Truck",
    "mega cab": "Truck",
    "xtracab": "Truck",
    "beetle convertible": "Convertible",
    "cts coupe": "Coupe",
    "koup": "Coupe",
    "club cab": "Truck",
    "elantra coupe": "Coupe",
    "q60 coupe": "Coupe",
    "cts-v coupe": "Coupe",
    "transit van": "Van",
    "granturismo convertible": "Convertible",
    "tsx sport wagon": "Wagon",
    "promaster cargo van": "Van",
    "q60 convertible": "Convertible",
    "g37 coupe": "Coupe",
    "cab plus 4": "Truck",
    "cts wagon": "Wagon",
}

df["simplifiedbody"] = df["body"].map(body_mapping)

# %%
popurlarBodies = (
    df["vin"]
    .groupby(df["body"])
    .count()
    .sort_values(ascending=False)[:20]
    .sort_values()
)

MostPopularBodyFig = px.bar(popurlarBodies, orientation="h")
MostPopularBodyFig.update_layout(
    title={
        "text": "Most popular vehicle body",
        "xanchor": "left",
        "yanchor": "top",
        "font": {"size": 24},
    },
    title_font_weight=750,
    title_font_family="Courier New",
    width=550,
    height=500,
    showlegend=False,
    margin=dict(l=50, r=50, t=50, b=0),
    yaxis_title="Body type",
    yaxis_title_font={"size": 18},
    xaxis_title="Units sold",
    xaxis_title_font={"size": 18},
)

MostPopularBodyFig.update_traces(hovertemplate="%{y}: %{x}<extra></extra>")

# %%
transmissionTypes = df["vin"].groupby(df["transmission"]).count().sort_values()


TransmissionTypeFig = go.Figure(
    data=[
        go.Pie(
            labels=transmissionTypes.index,
            values=transmissionTypes.values,
            hovertemplate="<b>%{label}:</b> %{value}<extra></extra>",
            rotation=90,
            textinfo="label+percent",
            insidetextorientation="radial",
            showlegend=False,
        )
    ]
)

TransmissionTypeFig.update_layout(
    title={
        "text": "Transmission types",
        "xanchor": "left",
        "yanchor": "top",
        "y": 0.95,
        "font": {"size": 24},
    },
    title_font_weight=750,
    title_font_family="Courier New",
    width=500,
    height=450,
    margin=dict(l=25, r=25, t=75, b=25),
)

TransmissionTypeFig.update_traces(
    hoverlabel=dict(bgcolor="white", font=dict(color="black")),
)

# %%
PriceScatterFig = px.scatter(
    data_frame=df.where(df["sellingprice"] > 50000),
    x="condition",
    y="sellingprice",
    color="simplifiedbody",
    custom_data=["sellingprice", "condition", "simplifiedbody", "make", "model"],
)

PriceScatterFig.update_layout(
    title={
        "text": "Variation in selling price with condition and body.",
        "xanchor": "left",
        "yanchor": "top",
        "font": {"size": 24},
    },
    title_font_weight=750,
    title_font_family="Courier New",
    legend_title_text="Body Type",
    width=1000,
    height=350,
    xaxis_title="Condition",
    xaxis_title_font={"size": 18},
    yaxis_title="Selling Price",
    yaxis_title_font={"size": 18},
    margin=dict(l=50, r=50, t=50, b=50),
)

PriceScatterFig.update_traces(
    hovertemplate="<b> %{customdata[3]} %{customdata[4]} </b> <br> %{x}/100 | $%{y}<extra></extra>",
    hoverlabel=dict(
        bgcolor="white", font=dict(color="black")  # Background color  # Text color
    ),
)

# %%
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

salesPerState["Abbreviation"] = salesPerState["state"].map(state_abbreviations)

state_count_map = dict(zip(salesPerState["Abbreviation"], salesPerState["vin"]))

salesPerStateFig = px.choropleth(
    data_frame=salesPerState,
    locations="Abbreviation",
    geojson=geodata,
    color="vin",
    scope="north america",
    width=800,
    height=600,
    hover_name="vin",
    hover_data={"vin": False, "Abbreviation": False},
)

salesPerStateFig.update_geos(
    projection_scale=1.7,
    center={"lat": 40, "lon": -120},
)

salesPerStateFig.update_layout(
    title={
        "text": "Number of vehicles sold in different States.",
        "xanchor": "left",
        "yanchor": "top",
    },
    title_font_weight=750,
    title_font_family="Courier New",
    title_font={"size": 24},
    margin=dict(l=10, r=10, t=50, b=10),
    coloraxis_colorbar=dict(
        title="Cars sold",
    ),
)

salesPerStateFig.update_traces(
    hovertemplate="<b>%{customdata[0]}</b>: %{z}<extra></extra>",
    hoverlabel=dict(bgcolor="white", font=dict(color="black")),
    customdata=salesPerState[["state"]],
)

# %%
import plotly.graph_objects as go

# Number of squares per column
n = 10

# Define numbers and colors for the first column
numbers_column1 = list(range(1, n + 1))
colors_column1 = [
    "#000000",
    "#808080",
    "#F5F5DC",
    "#D2B48C",
    "#8B4513",
    "#FF0000",
    "#C0C0C0",
    "#0000FF",
    "#F8F8FF",
    "#FFD700",
]
color_names_column1 = [
    "Black",
    "Gray",
    "Beige",
    "Tan",
    "Brown",
    "Red",
    "Silver",
    "Blue",
    "Off-white",
    "Gold",
]

numbers_column2 = list(range(1, n + 1))
colors_column2 = [
    "#000000",
    "#FFFFFF",
    "#C0C0C0",
    "#808080",
    "#0000FF",
    "#FF0000",
    "#FFD700",
    "#008000",
    "#800020",
    "#F5F5DC",
]
color_names_column2 = [
    "Black",
    "White",
    "Silver",
    "Gray",
    "Blue",
    "Red",
    "Gold",
    "Green",
    "Burgundy",
    "Beige",
]

popularColorsFig = go.Figure()

for i in range(n):

    popularColorsFig.add_trace(
        go.Scatter(
            x=[0.3],
            y=[n - i],
            mode="text",
            text=str(numbers_column1[i]),
            textposition="middle right",
            showlegend=False,
            hoverinfo="none",
        )
    )

    popularColorsFig.add_trace(
        go.Scatter(
            x=[0.8],
            y=[n - i],
            mode="markers",
            marker=dict(
                size=25,
                color=colors_column1[i],
                symbol="square",
                line=dict(
                    color="black",
                    width=1.75,
                ),
            ),
            hovertemplate=f"{color_names_column1[i]}<extra></extra>",
            showlegend=False,
        )
    )

for i in range(n):

    popularColorsFig.add_trace(
        go.Scatter(
            x=[1.2],
            y=[n - i],
            mode="text",
            text=str(numbers_column2[i]),
            textposition="middle right",
            showlegend=False,
            hoverinfo="none",
        )
    )

    popularColorsFig.add_trace(
        go.Scatter(
            x=[1.7],
            y=[n - i],
            mode="markers",
            marker=dict(
                size=25,
                color=colors_column2[i],
                symbol="square",
                line=dict(
                    color="black",
                    width=1.75,
                ),
            ),
            hovertemplate=f"{color_names_column2[i]}<extra></extra>",
            showlegend=False,
        )
    )

popularColorsFig.update_layout(
    title={
        "text": "Popular <br>color options",
        "xanchor": "left",
        "yanchor": "top",
        "x": 0.1,
        "font": {"size": 24},
    },
    title_font_weight=750,
    title_font_family="Courier New",
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[0, 2.2],
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[0, n + 0.5],
    ),
    plot_bgcolor="white",
    height=600,
    width=220,
    margin=dict(l=10, r=10, t=100, b=0),
    annotations=[
        dict(
            x=0.6,
            y=n + 0.5,
            text="Interior",
            showarrow=False,
            font=dict(size=16, color="black", family="Arial", weight="bold"),
            align="center",
        ),
        dict(
            x=1.53,
            y=n + 0.5,
            text="Exterior",
            showarrow=False,
            font=dict(size=16, color="black", family="Arial", weight="bold"),
            align="center",
        ),
    ],
)

# %%
layout = html.Div(
    [
        html.Div(
            [
                html.H1("Vehicle Sales 2014/15"),
                html.P(
                    """
                    This is a dataset I found on kaggle and now I have created a data dashboard out of it. 
                    Initially I had to do quiet a bit of data cleaning, but here are the results, my efforts payed off.
                    More details would be added soon and the dashboard would be posted on a hosting service within a few days.\n
                    As of now this image is all I can present, but please not that all graphs in the dashboard are fully interactive.
                    """
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "width": "15%",
            },
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(figure=MostPopularBodyFig),
                        html.Br(),
                        dcc.Graph(figure=TransmissionTypeFig),
                    ],
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(figure=salesPerStateFig),
                                dcc.Graph(figure=popularColorsFig),
                            ],
                            style={"display": "flex", "flex-direction": "row"},
                        ),
                        html.Br(),
                        dcc.Graph(figure=PriceScatterFig),
                    ],
                ),
            ],
            style={"display": "flex", "flex": "row"},
        ),
    ],
    style={"display": "flex", "flex": "row", "height": "100%"},
)

# %%
app = Dash(__name__)
app.layout = layout

if __name__ == "__main__":
    app.run_server()


