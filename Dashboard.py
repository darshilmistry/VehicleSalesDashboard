from dash import Dash, html, dcc
import dash
from PIL import Image

logo = Image.open("./logo.png")

app = Dash(__name__, use_pages=True)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Img(src=logo, alt="the logo was \n supposed to be here 😅"),
                html.H1("Vehicle Sales 2014/15"),
                html.Div(
                    [
                        dcc.Link(
                            page["name"],
                            href=page["path"],
                            style={
                                "font-size": "24px",
                                "font-weight": "bold",
                                "color": "black",
                                "text-decoration": "none",
                                "margin-top": "10px",
                                "padding": "4px",
                            },
                        )
                        for page in dash.page_registry.values()
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "width": "15%",
            },
        ),
        dash.page_container,
    ],
    style={
        "display": "flex",
        "flex": "row",
        "height": "98vh",
        "font-family": "Comfortaa, monospace",
    },
)


if __name__ == "__main__":
    app.run_server(use_reloader=True)
