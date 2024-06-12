import dash
import pandas as pd
import numpy as np
import plotly.express as px
import json
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from dash import html, dcc, callback, Input, Output


dash.register_page(__name__)


@callback(
    Output('grafico-barras-biomas', 'figure'),
    Input('dia-inicio-graficos', 'date'),
    Input('dia-fim-graficos', 'date')
)
def grafico_barras_queimadas_intervalo_de_dias(date1, date2):
    data_inicio = datetime.strptime(date1, "%Y-%m-%d")
    data_fim = datetime.strptime(date2, "%Y-%m-%d")
    
    bioma_lista = ['Amazônia', 'Mata Atlântica', 'Cerrado', 'Pantanal', 'Pampa', 'Caatinga']


    diferenca_dias = (data_fim - data_inicio).days
    intervalo_de_dias = []
    biomas = pd.DataFrame({'bioma': ['Amazônia', 'Mata Atlântica', 'Cerrado', 'Pantanal', 'Pampa', 'Caatinga']})

    for dia in range(0, diferenca_dias + 1):
        intervalo_de_dias.append((data_inicio - timedelta(days=dia)).strftime("%Y%m%d"))
    
    df_final = pd.DataFrame({'bioma': bioma_lista, 'foco_queimadas': [0, 0, 0, 0, 0, 0]})

    for dia in intervalo_de_dias:
        df = pd.read_csv(f"https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/diario/Brasil/focos_diario_br_{dia}.csv")

        new_df = pd.DataFrame({'bioma': df['bioma'].unique(), 'foco_queimadas':  df['bioma'].value_counts()})
        
        new_df.reset_index(drop = True, inplace = True)
        biomas.reset_index(drop = True, inplace = True)        

        new_df = pd.merge(new_df, biomas, how='right', on='bioma')
        for item in range(0, len(new_df['foco_queimadas'])):
            if np.isnan(new_df['foco_queimadas'][item]):
                new_df.loc[item, ['foco_queimadas']] = [0]

        for item in range(0, len(df_final['foco_queimadas'])):
            df_final.loc[item, ['foco_queimadas']] = [df_final['foco_queimadas'][item] + new_df['foco_queimadas'][item]]
        
    if len(intervalo_de_dias) > 1: 
        title=f'Focos de Queimadas Registradas por Bioma de {datetime.strptime(date1, "%Y-%m-%d").strftime("%d/%m/%Y")} até {datetime.strptime(date2, "%Y-%m-%d").strftime("%d/%m/%Y")}'
    else: 
        title=f'Focos de Queimadas Registradas por Bioma em {datetime.strptime(date1, "%Y-%m-%d").strftime("%d/%m/%Y")}'

    df_final = df_final.sort_values(by='foco_queimadas')
    return px.bar(df_final, x='bioma', y='foco_queimadas', color='foco_queimadas', title=title, color_continuous_scale="Reds")


@callback(
    Output('grafico-estados-mais-afetados', 'figure'),
    Input('dia-inicio-graficos', 'date'),
    Input('dia-fim-graficos', 'date')
)
def grafico_barras_queimadas_intervalo_de_dias(date1, date2):
    data_inicio = datetime.strptime(date1, "%Y-%m-%d")
    data_fim = datetime.strptime(date2, "%Y-%m-%d")
    
    estados = ['ACRE', 'ALAGOAS', 'AMAPÁ', 'AMAZONAS', 'BAHIA', 'CEARÁ', 'DISTRITO FEDERAL', 'ESPÍRITO SANTO', 'GOIÁS', 'MARANHÃO',
    'MATO GROSSO', 'MATO GROSSO DO SUL', 'MINAS GERAIS', 'PARÁ', 'PARAÍBA', 'PARANÁ', 'PERNAMBUCO', 'PIAUÍ', 'RIO DE JANEIRO', 
    'RIO GRANDE DO NORTE', 'RIO GRANDE DO SUL', 'RONDÔNIA', 'RORAIMA', 'SANTA CATARINA', 'SÃO PAULO', 'SERGIPE', 'TOCANTINS']

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

    diferenca_dias = (data_fim - data_inicio).days
    intervalo_de_dias = []
    
    for dia in range(0, diferenca_dias + 1):
        intervalo_de_dias.append((data_inicio - timedelta(days=dia)).strftime("%Y%m%d"))
    
    df_final = pd.DataFrame({'estados': estados, 'queimadas_estado': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})
    

    for dia in intervalo_de_dias:
        df = pd.read_csv(f"https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/diario/Brasil/focos_diario_br_{dia}.csv")
        df['queimadas_estado'] = 1
        
        new_df = df[['estado', 'queimadas_estado']].groupby('estado').sum().reset_index()  
        new_df.rename(columns={'estado': 'estados'}, inplace=True)

        df_final = pd.merge(new_df, df_final, how='right', on='estados')

        for item in range(0, len(df_final['queimadas_estado_x'])):
            if np.isnan(df_final['queimadas_estado_x'][item]):
                df_final.loc[item, ['queimadas_estado_x']] = [0]
        
        for item in range(0, len(df_final['queimadas_estado_x'])):
            df_final.loc[item, ['queimadas_estado']] = [df_final['queimadas_estado_x'][item] + df_final['queimadas_estado_y'][item]]
        
        df_final.drop('queimadas_estado_x', inplace=True, axis=1)
        df_final.drop('queimadas_estado_y', inplace=True, axis=1)

    if len(intervalo_de_dias) > 1: 
        title=f'Estados mais afetados pelas queimadas de {datetime.strptime(date1, "%Y-%m-%d").strftime("%d/%m/%Y")} até {datetime.strptime(date2, "%Y-%m-%d").strftime("%d/%m/%Y")}'
    else: 
        title=f'Estados mais afetados pelas queimadas em {datetime.strptime(date1, "%Y-%m-%d").strftime("%d/%m/%Y")}'

    df_final['estados'] = df_final['estados'].map(dicionario_estados)

    geojson = json.load(open('./local_resources/brasil_estados.json'))
    return px.choropleth(df_final, geojson=geojson, locations='estados', scope='south america', color_continuous_scale="Reds", color='queimadas_estado', width=700, height=900, title=title)
    

layout = html.Div([
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
    dcc.Graph(id="grafico-barras-biomas"),
    dcc.Graph(id="grafico-estados-mais-afetados", style={"align": "center"})

], className="pad-row")


