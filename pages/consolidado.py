import dash
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta, time
from dash import html, dcc, callback, Input, Output


dash.register_page(__name__)

bioma_lista = ['Amazônia', 'Mata Atlântica', 'Cerrado', 'Pantanal', 'Pampa', 'Caatinga']

@callback(
    Output('grafico-span-tempo', 'figure'),
    Input('dia-inicio-span-tempo', 'date'),
    Input('dia-fim-span-tempo', 'date')
)
def get_last_week_values(date1, date2):
    data_inicio = datetime.strptime(date1, "%Y-%m-%d")
    data_fim = datetime.strptime(date2, "%Y-%m-%d")
    
    diferenca_dias = (data_fim - data_inicio).days
    intervalo_de_dias = []
    biomas = pd.DataFrame({'bioma': ['Amazônia', 'Mata Atlântica', 'Cerrado', 'Pantanal', 'Pampa', 'Caatinga']})

    for dia in range(0, diferenca_dias + 1):
        intervalo_de_dias.append((data_inicio - timedelta(days=dia)).strftime("%Y%m%d"))
    
    df_final = pd.DataFrame({'bioma': bioma_lista, 'queimadas_registradas': [0, 0, 0, 0, 0, 0]})

    print(intervalo_de_dias)
    for dia in intervalo_de_dias:
        df = pd.read_csv(f"https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/diario/Brasil/focos_diario_br_{dia}.csv")

        new_df = pd.DataFrame({'bioma': df['bioma'].unique(), 'queimadas_registradas':  df['bioma'].value_counts()})
        
        new_df.reset_index(drop = True, inplace = True)
        biomas.reset_index(drop = True, inplace = True)
        print(f'new_df\n {new_df}')
            

        new_df = pd.merge(new_df, biomas, how='right', on='bioma')
        for item in range(0, len(new_df['queimadas_registradas'])):
            print(f"debug: {new_df['bioma'][item]}, valor: {new_df['queimadas_registradas'][item]}")
                
            if np.isnan(new_df['queimadas_registradas'][item]):
                new_df.loc[item, ['queimadas_registradas']] = [0]

        for item in range(0, len(df_final['queimadas_registradas'])):
            df_final.loc[item, ['queimadas_registradas']] = [df_final['queimadas_registradas'][item] + new_df['queimadas_registradas'][item]]

    print(f'df_final\n {df_final}')
        
    return px.bar(df_final, x='bioma', y='queimadas_registradas', color='bioma', title=f'Queimadas Registradas por Bioma de {datetime.strptime(date1, "%Y-%m-%d").strftime("%d/%m/%Y")} até {datetime.strptime(date2, "%Y-%m-%d").strftime("%d/%m/%Y")}')

@callback(
    Output('grafico-consolidado-queimadas-por-bioma-em-um-dia', 'figure'),
    Input('dia-selecionado-queimadas-por-bioma', 'date')
)

def update_chart_queimadas_bioma_dia(date):
    dia = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
 
    df = pd.read_csv(f"https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/diario/Brasil/focos_diario_br_{dia}.csv")

    biomas = pd.DataFrame({'bioma': ['Amazônia', 'Mata Atlântica', 'Cerrado', 'Pantanal', 'Pampa', 'Caatinga']})
    
    new_df = pd.DataFrame({'bioma': df['bioma'].unique(), 'queimadas_registradas':  df['bioma'].value_counts()})
    biomas.reset_index(drop = True, inplace = True)
    new_df.reset_index(drop = True, inplace = True)

    new_df = pd.merge(new_df, biomas, how='right', on='bioma')

    for item in range(0, len(new_df['queimadas_registradas']) - 1):
        if np.isnan(new_df['queimadas_registradas'][item]):
            new_df.loc[item, ['queimadas_registradas']] = [0]

    
    return px.bar(new_df, x='bioma', y='queimadas_registradas', color='bioma', title=f'Queimadas Registradas por Bioma em {datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")}')
   
layout = html.Div([
    html.H4("Nesta seção, encontram-se gráficos com dados consolidados registrados até o dia corrente"),
    html.Br(),
    html.B("Selecione o dia para visualização: "),
    dcc.DatePickerSingle(id='dia-selecionado-queimadas-por-bioma', date=datetime.today().date(), display_format="DD/MM/YYYY"),
    dcc.Graph(id="grafico-consolidado-queimadas-por-bioma-em-um-dia"),
    html.Hr(),
    dcc.DatePickerSingle(id='dia-inicio-span-tempo', date=datetime.today().date(), display_format="DD/MM/YYYY"),
    dcc.DatePickerSingle(id='dia-fim-span-tempo', date=datetime.today().date(), display_format="DD/MM/YYYY"),
    dcc.Graph(id="grafico-span-tempo")
])


