import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')


about = '''
        Este projeto destina-se a auxiliar a visualização de como as queimadas vem avançando no Brasil,
        criando gráficos que utilizam como fonte a base de dados BDQueimadas. 
        '''
how =   '''
        Através de requisições HTTP à base de dados, o monitor recupera informações coletadas pelos
        satélites que atuam como sensores dispostos na área espacial do país, onde transmite dados sobre
        focos de queimadas ativos, biomas afetados, estados com mais incidência, entre outros. 
        '''

issues = f'''
         Caso ao navegar por este portal você tenha encontrado qualquer problema, inconsistência ou informação
         faltando, por favor não deixe de registrar clicando em Reportar Problema na barra superior.
         '''

card_cop = dbc.Card(
    [
        dbc.CardImg(src="/static/images/cop.jpg", top=True),
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
        dbc.CardImg(src="/static/images/mudancas-climaticas.jpg", top=True),
        dbc.CardBody(
            [
                html.H4("Mudanças Climáticas", className="card-title"),
                html.P(
                    "Aqui, você verá uma discussão a respeito das crescentes mudanças climáticas no Brasil",
                    className="card-text",
                ),
                dbc.Button("Acessar", color="primary", href="/mudancas"),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_consolidado = dbc.Card(
    [
        dbc.CardImg(src="/static/images/consolidado.jpg", top=True),
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
        dbc.CardImg(src="/static/images/agora.jpg", top=True),
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
        html.H1('Seja bem-vindo ao Monitor Queimadas!'),
       dbc.Row(
        [dbc.Col(card_mudancas), dbc.Col(card_cop), dbc.Col(card_consolidado), dbc.Col(card_agora)],
        ),
        html.Div([
                html.H4("Perguntas Frequentes"),
                dbc.Accordion([dbc.AccordionItem(title="O que é o projeto Monitor Queimadas?",
                                                 children=about)], active_item=True),
                dbc.Accordion([dbc.AccordionItem(title="Como funciona?", children=how)], active_item=True),
                dbc.Accordion([dbc.AccordionItem(title="Encontrou algum problema?", children=issues)], active_item=True),
        
        ]),
])