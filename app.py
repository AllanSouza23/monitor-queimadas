import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}], prevent_initial_callbacks=True)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Mudanças Climáticas", href="/mudancas-climaticas")),
        dbc.NavItem(dbc.NavLink("Papel da COP", href="/cop")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Dados Consolidados", href="/consolidado"),
                dbc.DropdownMenuItem("Teste", href="/test"),
                dbc.DropdownMenuItem("Agora Refactored", href="/agora-refactored"),
            ],
            nav=True,
            in_navbar=True,
            label="Gráficos",
        ),
        dbc.NavItem(dbc.NavLink("Reportar Problema", href="https://github.com/AllanSouza23/monitor-queimadas/issues/new/choose")),
        
    ],
    brand="Monitor Queimadas",
    brand_href="/",
    color="dark",
    dark=True,
)

github_url = "https://github.com/AllanSouza23/monitor-queimadas"  

footer_style = {
    'border': '1px solid #ccc',
    'text-align': 'center',
    'padding': '20px',
    'background-color': '#212529'
}

app.layout = html.Div(
    [   
        navbar,
        dbc.Container(
            [       
                dash.page_container
            ]
        ),
        html.Br(),
        html.Footer(
        html.A([
            html.I(className="bi bi-github"),
            html.P("AllanSouza23, 2024")
            ],
            href=github_url,
            target="_blank",
            style={
                'text-color': '#FFFFFF',
                'color': '#FFFFFF',
                'text-decoration': 'none'
            }            
        ),
        style=footer_style)
    
])

if __name__ == '__main__':
    app.run(debug=True, dev_tools_serve_dev_bundles=True)
