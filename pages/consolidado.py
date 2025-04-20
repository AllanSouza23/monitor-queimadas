import dash
import pandas as pd
import plotly.express as px
import json
import os
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from dash import html, dcc, callback, Input, Output, State, no_update


dash.register_page(__name__)

current_dir = os.path.dirname(__file__)

estados = [
            'ACRE', 'ALAGOAS', 'AMAPÁ', 'AMAZONAS', 'BAHIA', 'CEARÁ', 'DISTRITO FEDERAL', 'ESPÍRITO SANTO', 'GOIÁS',
            'MARANHÃO', 'MATO GROSSO', 'MATO GROSSO DO SUL', 'MINAS GERAIS', 'PARÁ', 'PARAÍBA', 'PARANÁ', 'PERNAMBUCO',
            'PIAUÍ', 'RIO DE JANEIRO', 'RIO GRANDE DO NORTE', 'RIO GRANDE DO SUL', 'RONDÔNIA', 'RORAIMA', 'SANTA CATARINA',
            'SÃO PAULO', 'SERGIPE', 'TOCANTINS'
        ]

dicionario_estados = {
            'ACRE': 'AC', 'ALAGOAS': 'AL', 'AMAPÁ': 'AP', 'AMAZONAS': 'AM', 'BAHIA': 'BA', 'CEARÁ': 'CE',
            'DISTRITO FEDERAL': 'DF', 'ESPÍRITO SANTO': 'ES', 'GOIÁS': 'GO', 'MARANHÃO': 'MA', 'MATO GROSSO': 'MT',
            'MATO GROSSO DO SUL': 'MS', 'MINAS GERAIS': 'MG', 'PARÁ': 'PA', 'PARAÍBA': 'PB', 'PARANÁ': 'PR',
            'PERNAMBUCO': 'PE', 'PIAUÍ': 'PI', 'RIO DE JANEIRO': 'RJ', 'RIO GRANDE DO NORTE': 'RN',
            'RIO GRANDE DO SUL': 'RS', 'RONDÔNIA': 'RO', 'RORAIMA': 'RR', 'SANTA CATARINA': 'SC', 'SÃO PAULO': 'SP',
            'SERGIPE': 'SE', 'TOCANTINS': 'TO'
        }

bioma_lista = ['Amazônia', 'Caatinga', 'Cerrado', 'Mata Atlântica', 'Pampa', 'Pantanal']

@callback(
    Output('grafico-barras-biomas-consolidado', 'figure'),
    State('dia-inicio-graficos', 'date'),
    State('dia-fim-graficos', 'date'),
    Input('btn-consolidados', 'n_clicks')
)
def grafico_barras_queimadas_biomas_consolidado(date1, date2, n):
    if n:
        data_inicio = datetime.strptime(date1, "%Y-%m-%d")
        data_fim = datetime.strptime(date2, "%Y-%m-%d")
        diferenca_dias = (data_fim - data_inicio).days
        intervalo_de_dias = []

        df_final = pd.DataFrame({'bioma': bioma_lista, 'foco_queimadas_biomas': [0] * len(bioma_lista)})

        if diferenca_dias == 0:
            intervalo_de_dias.append(data_inicio.strftime("%Y%m%d"))
        else:
            for dia in range(0, diferenca_dias + 1):
                intervalo_de_dias.append((data_fim - timedelta(days=dia)).strftime("%Y%m%d"))

        for dia in intervalo_de_dias:
            url = f"https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/diario/Brasil/focos_diario_br_{dia}.csv"
            df = pd.read_csv(url)
            parsed_df = pd.DataFrame({'bioma': df['bioma'].unique(), 'foco_queimadas_biomas':  df['bioma'].value_counts()})
            parsed_df.reset_index(drop=True, inplace=True)

            parsed_df = parsed_df.sort_values(ascending=True, by='bioma')
            intermediario = pd.merge(parsed_df, df_final, on='bioma', suffixes=('_x', '_y'), how='right')
            intermediario = intermediario.fillna(0)
            df_final['foco_queimadas_biomas'] = intermediario['foco_queimadas_biomas_x'] + intermediario['foco_queimadas_biomas_y']

        df_final = df_final.fillna(0)
        if len(intervalo_de_dias) > 1:
            title=f'Focos de Queimadas Registradas por Bioma de {datetime.strptime(date1, "%Y-%m-%d").strftime("%d/%m/%Y")} até {datetime.strptime(date2, "%Y-%m-%d").strftime("%d/%m/%Y")}'
        else:
            title=f'Focos de Queimadas Registradas por Bioma em {datetime.strptime(date1, "%Y-%m-%d").strftime("%d/%m/%Y")}'
        fig_bar = px.bar(
            df_final,
            x='bioma',
            y='foco_queimadas_biomas',
            color='foco_queimadas_biomas',
            text='foco_queimadas_biomas',
            title=title,
            color_continuous_scale="Plasma",
            labels={'foco_queimadas_biomas': 'Focos de Queimadas', 'bioma': 'Bioma'}
        )
        fig_bar.update_layout(margin={"r": 0, "t": 100, "l": 0, "b": 0})

        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(
            xaxis_title="Biomas",
            yaxis_title="Número de Focos",
        )
        return fig_bar
    return no_update

@callback(
    Output('grafico-estados-mais-afetados', 'figure'),
    State('dia-inicio-graficos', 'date'),
    State('dia-fim-graficos', 'date'),
    Input('btn-consolidados', 'n_clicks')
)
def grafico_estados_mais_afetados(date1, date2, n):
    if n:
        data_inicio = datetime.strptime(date1, "%Y-%m-%d")
        data_fim = datetime.strptime(date2, "%Y-%m-%d")
        diferenca_dias = (data_fim - data_inicio).days
        intervalo_de_dias = []

        df_final = pd.DataFrame({'estado': estados, 'foco_queimadas_estados': [0] * len(estados)})

        if diferenca_dias == 0:
            intervalo_de_dias.append(data_inicio.strftime("%Y%m%d"))
        else:
            for dia in range(0, diferenca_dias + 1):
                intervalo_de_dias.append((data_fim - timedelta(days=dia)).strftime("%Y%m%d"))

        for dia in intervalo_de_dias:
            url = f"https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/diario/Brasil/focos_diario_br_{dia}.csv"
            df = pd.read_csv(url)
            parsed_df = pd.DataFrame(
                {'estado': df['estado'].unique(), 'foco_queimadas_estados': df['estado'].value_counts()})
            parsed_df.reset_index(drop=True, inplace=True)

            parsed_df = parsed_df.sort_values(ascending=True, by='estado')
            intermediario = pd.merge(parsed_df, df_final, on='estado', suffixes=('_x', '_y'), how='right')
            intermediario = intermediario.fillna(0)
            df_final['foco_queimadas_estados'] = intermediario['foco_queimadas_estados_x'] + intermediario[
                'foco_queimadas_estados_y']

        df_final = df_final.fillna(0)
        df_final['estado'] = df_final['estado'].map(dicionario_estados)

        title = f"Estados mais afetados pelas queimadas de {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}" \
            if len(intervalo_de_dias) > 1 else f"Estados mais afetados pelas queimadas em {data_inicio.strftime('%d/%m/%Y')}"

        path_geojson = os.path.join(current_dir, '../local_resources/old_brasil_estados.json')

        with open(path_geojson, 'r') as f:
            geojson = json.load(f)

        df_final.rename(columns={'estado': 'estados'}, inplace=True)

        fig_map = px.choropleth(df_final, geojson=geojson, locations='estados', color='foco_queimadas_estados',
                                color_continuous_scale="Plasma",
                                range_color=(0, df_final['foco_queimadas_estados'].max()),
                                scope='south america',
                                title=title,
                                labels={'foco_queimadas_biomas': 'Focos de Queimadas'}
                          )

        fig_map.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
        fig_map.update_geos(fitbounds="locations", visible=True)
        return fig_map
    return no_update

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
        dbc.Col([
            html.Button("Gerar Gráficos", id="btn-consolidados"),
        ], width="auto"),
        ]),
    dcc.Loading([dcc.Graph(id="grafico-barras-biomas-consolidado")], id="loading-1", type="circle", overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white", "filter": "blur(2px)"}),
    dcc.Loading([dcc.Graph(id="grafico-estados-mais-afetados")], id="loading-1", type="circle", overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white", "filter": "blur(2px)"}),
], className="pad-row")
