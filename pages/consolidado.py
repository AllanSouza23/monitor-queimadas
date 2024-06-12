import dash
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from dash import html, dcc, callback, Input, Output


dash.register_page(__name__)

bioma_lista = ['Amazônia', 'Mata Atlântica', 'Cerrado', 'Pantanal', 'Pampa', 'Caatinga']

@callback(
    Output('grafico-span-tempo', 'figure'),
    Input('dia-inicio-span-tempo', 'date'),
    Input('dia-fim-span-tempo', 'date')
)
def grafico_barras_queimadas_intervalo_de_dias(date1, date2):
    data_inicio = datetime.strptime(date1, "%Y-%m-%d")
    data_fim = datetime.strptime(date2, "%Y-%m-%d")
    
    diferenca_dias = (data_fim - data_inicio).days
    intervalo_de_dias = []
    biomas = pd.DataFrame({'bioma': ['Amazônia', 'Mata Atlântica', 'Cerrado', 'Pantanal', 'Pampa', 'Caatinga']})

    for dia in range(0, diferenca_dias + 1):
        intervalo_de_dias.append((data_inicio - timedelta(days=dia)).strftime("%Y%m%d"))
    
    df_final = pd.DataFrame({'bioma': bioma_lista, 'queimadas_registradas': [0, 0, 0, 0, 0, 0]})

    for dia in intervalo_de_dias:
        df = pd.read_csv(f"https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/diario/Brasil/focos_diario_br_{dia}.csv")

        new_df = pd.DataFrame({'bioma': df['bioma'].unique(), 'queimadas_registradas':  df['bioma'].value_counts()})
        
        new_df.reset_index(drop = True, inplace = True)
        biomas.reset_index(drop = True, inplace = True)        

        new_df = pd.merge(new_df, biomas, how='right', on='bioma')
        for item in range(0, len(new_df['queimadas_registradas'])):
            print(f"debug: {new_df['bioma'][item]}, valor: {new_df['queimadas_registradas'][item]}")
                
            if np.isnan(new_df['queimadas_registradas'][item]):
                new_df.loc[item, ['queimadas_registradas']] = [0]

        for item in range(0, len(df_final['queimadas_registradas'])):
            df_final.loc[item, ['queimadas_registradas']] = [df_final['queimadas_registradas'][item] + new_df['queimadas_registradas'][item]]
        
    if len(intervalo_de_dias) > 1: 
        title=f'Queimadas Registradas por Bioma de {datetime.strptime(date1, "%Y-%m-%d").strftime("%d/%m/%Y")} até {datetime.strptime(date2, "%Y-%m-%d").strftime("%d/%m/%Y")}'
    else: 
        title=f'Queimadas Registradas por Bioma em {datetime.strptime(date1, "%Y-%m-%d").strftime("%d/%m/%Y")}'

    return px.bar(df_final, x='bioma', y='queimadas_registradas', color='bioma', title=title)


layout = html.Div([
    html.H4("Nesta seção, encontram-se gráficos com dados consolidados registrados até o dia corrente"),
    html.Br(),
    dbc.Col(html.B("Selecione o intervalo para visualização"), style={"margin-bottom": "0.5em"}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.B("Data de início: "),
            dcc.DatePickerSingle(id='dia-inicio-span-tempo', date=datetime.today().date(), display_format="DD/MM/YYYY")
            ], width="auto"),
        dbc.Col([
            html.B("Data de fim: "),
            dcc.DatePickerSingle(id='dia-fim-span-tempo', date=datetime.today().date(), display_format="DD/MM/YYYY")
            ], width="auto"),
        ]),
    dcc.Graph(id="grafico-span-tempo", responsive=True)
], className="pad-row")


