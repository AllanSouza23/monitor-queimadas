import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from dash import html, dcc, callback, Input, Output
import reverse_geocode

dash.register_page(__name__)


@callback(
        Output('abc', 'figure'),
        Input('dia', 'value'),
        Input('momento', 'value'),
        Input('botao', 'n_clicks')
)
def grafico_pontos(dia, momento, n):
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
        
        fig = px.bar(new_df, x='estados', y='queimadas_estado', color_continuous_scale="Reds", color='queimadas_estado', title=f'{dia} Queimadas no Brasil {momento}')
        fig.show()
        return fig
        

layout = html.Div([
    html.Br(),
    html.H2("Dados em Tempo Real"),
    html.P("Os Dados em Tempo Real buscam evidenciar focos de queimadas ativos em cada bioma e estado brasileiro, tendo o período de atualização de 10 minutos"),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Input(id="dia"), width="auto"), 
        dbc.Col(dcc.Input(id="momento"), width="auto"),
        dbc.Col(html.Button('click', id="botao", n_clicks=0), width="auto"),
    ]),
    dcc.Loading(dcc.Graph(id="abc"), id="loading-1", overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"}),
    #dcc.Loading([dcc.Graph(id="grafico-estados-mais-afetados")], id="loading-2", overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"})
], className="pad-row")
