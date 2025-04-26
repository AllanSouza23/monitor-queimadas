import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')


about = '''
        Este projeto destina-se a auxiliar a visualização de como as queimadas vem avançando no Brasil,
        criando gráficos que utilizam como fonte a base de dados disponibilizadas pelo INPE. 
        '''
how =   '''
        Através de requisições e consulta à base de dados, o monitor recupera informações coletadas pelos
        satélites que atuam como sensores dispostos na área espacial do país, e transmite dados sobre
        focos de queimadas ativos, biomas afetados e estados com maior incidência. 
        '''

issues = f'''
         Caso ao navegar por este app você tenha encontrado qualquer problema, inconsistência ou informação
         faltando, por favor registre clicando em Reportar Problema na barra superior.
         '''

card_cop = dbc.Card(
    [
        dbc.CardImg(src="/static/images/cop.jpg", top=True, style={"height": "12rem"}),
        dbc.CardBody(
            [
                html.H4("COP", className="card-title"),
                html.P(
                    "Nesta página, você poderá conhecer um pouco da história e do papel da Conferência das Partes",
                    className="card-text",
                ),
                dbc.Button("Acessar", color="primary", href="/cop"),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_mudancas = dbc.Card(
    [
        dbc.CardImg(src="/static/images/mudancas-climaticas.jpg", top=True, style={"height": "12rem"}),
        dbc.CardBody(
            [
                html.H4("Mudanças Climáticas", className="card-title"),
                html.P(
                    "Aqui, você verá uma discussão a respeito das crescentes mudanças climáticas no Brasil",
                    className="card-text",
                ),
                dbc.Button("Acessar", color="primary", href="/mudancas-climaticas"),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_consolidado = dbc.Card(
    [
        dbc.CardImg(src="/static/images/icone-grafico-barras.png", top=True, style={"height": "12rem"}),
        dbc.CardBody(
            [
                html.H4("Dados Consolidados", className="card-title"),
                html.P(
                    "Nesta página, você poderá ver um recorte agregado de dados em um determinado período",
                    className="card-text",
                ),
                dbc.Button("Acessar", color="primary", href="/consolidado"),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_agora = dbc.Card(
    [
        dbc.CardImg(src="/static/images/clock.jpg", top=True, style={"height": "12rem"}),
        dbc.CardBody(
            [
                html.H4("Agora", className="card-title"),
                html.P(
                    "Nesta aba, você consegue observar como estão gráficos da situação atual",
                    className="card-text",
                ),
                dbc.Button("Acessar", color="primary", href="/agora"),
            ]
        ),
    ],
    style={"width": "18rem"},
)

layout = html.Div([
        html.Br(),
        html.H1('Seja bem-vindo ao Monitor Queimadas!'),
        html.Br(),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(card_mudancas, md=6, lg=3),
                        dbc.Col(card_cop, md=6, lg=3),
                        dbc.Col(card_agora, md=6, lg=3),
                        dbc.Col(card_consolidado, md=6, lg=3),
                    ],
                    justify="center",
                    className="mb-4",
                )
            ]
        ),
        html.Br(),
        html.Div([
                html.H4("Perguntas Frequentes"),
                dbc.Accordion([dbc.AccordionItem(title="O que é o projeto Monitor Queimadas?",
                                                 children=about)], active_item=True),
                dbc.Accordion([dbc.AccordionItem(title="Como funciona?", children=how)], active_item=True),
                dbc.Accordion([dbc.AccordionItem(title="Encontrou algum problema?", children=issues)], active_item=True),

        ]),
])
