import dash
import pandas as pd
import numpy as np
import plotly.express as px
import json
import dash_bootstrap_components as dbc
import reverse_geocode
from datetime import datetime
from dash import html, dcc, callback, Input, Output, State


dash.register_page(__name__)


@callback(
        Output('graph', 'figure'),
        #Input('dia1', 'value'),
        State('graph', 'figure'),
        Input('botao1', 'n_clicks')
)
def grafico_linha(fig, n):
    dia = '20240612'
    momento = '0220'
    if n:
        dicionario_estados = {
            'ACRE': 'AC',
            'ALAGOAS': 'AL',
            'AMAPÁ': 'AP',
            'AMAZONAS': 'AM',
            'BAHIA': 'BA',
            'CEARÁ': 'CE',
            'DISTRITO FEDERAL': 'DF',
            'ESPÍRITO SANTO': 'ES',
            'GOIÁS': 'GO',
            'MARANHÃO': 'MA',
            'MATO GROSSO': 'MT',
            'MATO GROSSO DO SUL': 'MS',
            'MINAS GERAIS': 'MG',
            'PARÁ': 'PA',
            'PARAÍBA': 'PB',
            'PARANÁ': 'PR',
            'PERNAMBUCO': 'PE',
            'PIAUÍ': 'PI',
            'RIO DE JANEIRO': 'RJ',
            'RIO GRANDE DO NORTE': 'RN',
            'RIO GRANDE DO SUL': 'RS',
            'RONDÔNIA': 'RO',
            'RORAIMA': 'RR',
            'SANTA CATARINA': 'SC',
            'SÃO PAULO': 'SP',
            'SERGIPE': 'SE',
            'TOCANTINS': 'TO'
        }
        url = f'https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/10min/focos_10min_{dia}_{momento}.csv'
        print(url)
        df = pd.read_csv(url)
        pais = []
        estado = []
        for i, infos in df.iterrows():
            loc = reverse_geocode.search([(infos.lat, infos.lon)])[0]
            p = loc.get('country')
            e = str(loc.get('state')).upper()
            pais.append(p)
            estado.append(e)
            

        df = df.assign(pais=pais)
        df = df.assign(estados=estado)
        df = df[df['pais'] == 'Brazil']
        df['pais'] = 'Brasil'
        df['estados'] = df['estados'].map(dicionario_estados)
        df.assign(queimadas_estado=1)
        df['queimadas_estado'] = 1
        new_df = df[['estados', 'queimadas_estado']].groupby('estados').sum().reset_index()  

        
        print(new_df)
        new_df = new_df.sort_values(by="queimadas_estado")
        
        return px.bar(new_df, x='estados', y='queimadas_estado', color_continuous_scale="Reds", color='queimadas_estado')

layout = html.Div([
    html.Br(),
    html.H2("Dados Consolidados"),
    html.P("Os Dados Consolidados tratam-se de um conjunto de dados vindos dos registros do BDQueimadas, a fim de melhor visualizar dentro do intervalo máximo de aproximadamente um mês, quais os biomas e estados mais afetados por focos de queimadas"),
    html.Br(),
    dbc.Col(html.B("Selecione um intervalo para visualização"), style={"margin-bottom": "0.5em"}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.B("Data de início: "),
            dcc.DatePickerSingle(id='dia-inicio-graficos', date=datetime.today().date(), display_format="DD/MM/YYYY")
            ], width="auto"),
        dbc.Col([
            html.B("Data de fim: "),
            dcc.DatePickerSingle(id='dia-fim-graficos', date=datetime.today().date(), display_format="DD/MM/YYYY")
            ], width="auto"),
        ]),
    dcc.Loading([dcc.Graph(id="grafico-barras-biomas1")], id="loading-3", overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"}),
    dcc.Loading([dcc.Graph(id="grafico-estados-mais-afetados1")], id="loading-4", overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"}),
    dcc.Loading([dcc.Graph(id="graph")], id="loading-5", overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"}),
    dbc.Row([
        #dbc.Col(dcc.Input(id="dia1"), width="auto"), 
        #dbc.Col(dcc.Input(id="momento1"), width="auto"),
        dbc.Col(html.Button('click', id="botao1", n_clicks=0), width="auto"),
    ]),
], className="pad-row")


