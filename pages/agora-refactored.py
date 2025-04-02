import dash
import pandas as pd
import plotly.express as px
import io
import os
import reverse_geocode
from datetime import datetime
from dash import html, dcc, callback, Input, Output, State
import aiohttp
import asyncio
import geopandas as gpd
from shapely.geometry import Point

dash.register_page(__name__)

dicionario_horarios = {
    '00:00': '0300', '00:10': '0310', '00:20': '0320', '00:30': '0330', '00:40': '0340', '00:50': '0350',
    '01:00': '0400', '01:10': '0410', '01:20': '0420', '01:30': '0430', '01:40': '0440', '01:50': '0450',
    '02:00': '0500', '02:10': '0510', '02:20': '0520', '02:30': '0530', '02:40': '0540', '02:50': '0550',
    '03:00': '0600', '03:10': '0610', '03:20': '0620', '03:30': '0630', '03:40': '0640', '03:50': '0650',
    '04:00': '0700', '04:10': '0710', '04:20': '0720', '04:30': '0730', '04:40': '0740', '04:50': '0750',
    '05:00': '0800', '05:10': '0810', '05:20': '0820', '05:30': '0830', '05:40': '0840', '05:50': '0850',
    '06:00': '0900', '06:10': '0910', '06:20': '0920', '06:30': '0930', '06:40': '0940', '06:50': '0950',
    '07:00': '1000', '07:10': '1010', '07:20': '1020', '07:30': '1030', '07:40': '1040', '07:50': '1050',
    '08:00': '1100', '08:10': '1110', '08:20': '1120', '08:30': '1130', '08:40': '1140', '08:50': '1150',
    '09:00': '1200', '09:10': '1210', '09:20': '1220', '09:30': '1230', '09:40': '1240', '09:50': '1250',
    '10:00': '1300', '10:10': '1310', '10:20': '1320', '10:30': '1330', '10:40': '1340', '10:50': '1350',
    '11:00': '1400', '11:10': '1410', '11:20': '1420', '11:30': '1430', '11:40': '1440', '11:50': '1450',
    '12:00': '1500', '12:10': '1510', '12:20': '1520', '12:30': '1530', '12:40': '1540', '12:50': '1550',
    '13:00': '1600', '13:10': '1610', '13:20': '1620', '13:30': '1630', '13:40': '1640', '13:50': '1650',
    '14:00': '1700', '14:10': '1710', '14:20': '1720', '14:30': '1730', '14:40': '1740', '14:50': '1750',
    '15:00': '1800', '15:10': '1810', '15:20': '1820', '15:30': '1830', '15:40': '1840', '15:50': '1850',
    '16:00': '1900', '16:10': '1910', '16:20': '1920', '16:30': '1930', '16:40': '1940', '16:50': '1950',
    '17:00': '2000', '17:10': '2010', '17:20': '2020', '17:30': '2030', '17:40': '2040', '17:50': '2050',
    '18:00': '2100', '18:10': '2110', '18:20': '2120', '18:30': '2130', '18:40': '2140', '18:50': '2150',
    '19:00': '2200', '19:10': '2210', '19:20': '2220', '19:30': '2230', '19:40': '2240', '19:50': '2250',
    '20:00': '2300', '20:10': '2310', '20:20': '2320', '20:30': '2330', '20:40': '2340', '20:50': '2350',
    '21:00': '0000', '21:10': '0010', '21:20': '0020', '21:30': '0030', '21:40': '0040', '21:50': '0050',
    '22:00': '0100', '22:10': '0110', '22:20': '0120', '22:30': '0130', '22:40': '0140', '22:50': '0150',
    '23:00': '0200', '23:10': '0210', '23:20': '0220', '23:30': '0230', '23:40': '0240', '23:50': '0250'
}

dicionario_estados = {
    'ACRE': 'AC', 'ALAGOAS': 'AL', 'AMAPÁ': 'AP', 'AMAZONAS': 'AM', 'BAHIA': 'BA', 'CEARÁ': 'CE',
    'DISTRITO FEDERAL': 'DF', 'ESPÍRITO SANTO': 'ES', 'GOIÁS': 'GO', 'MARANHÃO': 'MA', 'MATO GROSSO': 'MT',
    'MATO GROSSO DO SUL': 'MS', 'MINAS GERAIS': 'MG', 'PARÁ': 'PA', 'PARAÍBA': 'PB', 'PARANÁ': 'PR',
    'PERNAMBUCO': 'PE', 'PIAUÍ': 'PI', 'RIO DE JANEIRO': 'RJ', 'RIO GRANDE DO NORTE': 'RN', 'RIO GRANDE DO SUL': 'RS',
    'RONDÔNIA': 'RO', 'RORAIMA': 'RR', 'SANTA CATARINA': 'SC', 'SÃO PAULO': 'SP', 'SERGIPE': 'SE', 'TOCANTINS': 'TO'
}

async def fetch_data():
    # Obtém a data atual no formato YYYYMMDD
    dia = datetime.now().strftime('%Y%m%d')

    # Obtém o horário atual no formato HH:MM
    hora_atual = datetime.now().strftime('%H:%M')

    # Converte o horário atual usando o dicionário
    momento = dicionario_horarios.get(hora_atual, '0000')
    url = f'https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/10min/focos_10min_{dia}_{momento}.csv'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            return pd.read_csv(io.StringIO(data))

@callback(
    Output('ultima-atualizacao', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_ultima_atualizacao(n):
    now = datetime.now().strftime("Última atualização: %d/%m/%Y às %H:%M:%S")
    return now

@callback(
    Output('graph2', 'figure'),
    Input('interval-component', 'n_intervals')
)
def grafico_pizza(n):
    df = asyncio.run(fetch_data())
    pais = []
    estado = []
    for i, infos in df.iterrows():
        loc = reverse_geocode.search([(infos.lat, infos.lon)])[0]
        p = loc.get('country')
        e = str(loc.get('state')).upper()
        pais.append(p)
        estado.append(e)

    print (df)
    df = df.assign(pais=pais)
    df = df.assign(estados=estado)
    df = df[df['pais'] == 'Brazil']
    df['pais'] = 'Brasil'
    df['estados'] = df['estados'].map(dicionario_estados)
    df.assign(queimadas_estado=1)
    df['queimadas_estado'] = 1
    new_df = df[['estados', 'queimadas_estado']].groupby('estados').sum().reset_index()

    new_df = new_df.sort_values(by="queimadas_estado")
    return px.pie(new_df, names='estados', values='queimadas_estado', color_discrete_sequence=px.colors.sequential.Inferno_r, title='Queimadas por Estado')

@callback(
    Output('queimadas-contagem', 'figure'),
    Input('interval-component', 'n_intervals')
)
def queimadas_contagem(n):
    df = asyncio.run(fetch_data())
    return 'Queimadas registradas: ' + str(len(df))

layout = html.Div([
    html.Br(),
    html.H2("Dados em Tempo Real"),
    html.P("Os Dados em Tempo Real buscam evidenciar focos de queimadas ativos em cada bioma e estado brasileiro, tendo o período de atualização de 10 minutos."),
    html.P(id='ultima-atualizacao'),
    html.Br(),
    html.P(id="queimadas-contagem"),
    html.Br(),
    dcc.Loading([dcc.Graph(id="grafico-barras-biomas1")], id="loading-3", overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"}),
    dcc.Loading([dcc.Graph(id="grafico-estados-mais-afetados1")], id="loading-4", overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"}),
    dcc.Loading([dcc.Graph(id="graph2")], id="loading-5", overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"}),
    dcc.Interval(
        id='interval-component',
        interval=0.175*60*1000,  # Atualiza a cada 10 minutos
        n_intervals=0
    ),
], className="pad-row")