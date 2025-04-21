import dash
import pandas as pd
import plotly.express as px
import json
import os
import io
import aiohttp
import asyncio
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from dash import html, dcc, callback, Input, Output, State, no_update
from dash.dash_table import DataTable


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


async def fetch_interval_data(intervalo_dias):
    data = []
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        for dia in intervalo_dias:
            url = f'https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/diario/Brasil/focos_diario_br_{dia}.csv'
            for attempt in range(3):
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            csv_data = await response.text()
                            df = pd.DataFrame(pd.read_csv(io.StringIO(csv_data)))
                            df['dia'] = dia
                            data.append(df)
                        break
                except asyncio.TimeoutError:
                    if attempt == 2:
                        print(f"Timeout ao acessar {url}")
    df = pd.DataFrame()
    for d in data:
        df = pd.concat([df, d], ignore_index=True)

    return df

async def fetch_data_consolidados(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)

        dataframes = []
        for response in responses:
            if response.status == 200:
                data = await response.text()
                df = pd.read_csv(io.StringIO(data))
                dataframes.append(df)
        return dataframes

@callback(
    Output('grafico-barras-biomas-consolidado', 'figure'),
    Output('title-grafico-barras-biomas-consolidado', 'children'),
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

        urls = [
            f"https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/diario/Brasil/focos_diario_br_{dia}.csv"
            for dia in intervalo_de_dias
        ]
        dataframes = asyncio.run(fetch_data_consolidados(urls))

        for df in dataframes:
            parsed_df = pd.DataFrame(
                {'bioma': df['bioma'].unique(), 'foco_queimadas_biomas': df['bioma'].value_counts()})
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
            color_continuous_scale="Plasma",
            labels={'foco_queimadas_biomas': 'Focos de Queimadas', 'bioma': 'Bioma'}
        )

        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(
            xaxis_title="Biomas",
            yaxis_title="Número de Focos",
            margin={"r": 0, "t": 100, "l": 0, "b": 0}
        )
        return fig_bar, title
    return no_update

@callback(
    Output('grafico-estados-mais-afetados', 'figure'),
    Output('title-grafico-estados-mais-afetados', 'children'),
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

        df = asyncio.run(fetch_interval_data(intervalo_de_dias))

        parsed_df = pd.DataFrame(
            {'estado': df['estado'].unique(), 'foco_queimadas_estados': df['estado'].value_counts()})
        parsed_df.reset_index(drop=True, inplace=True)
        parsed_df = parsed_df.sort_values(ascending=True, by='estado')
        intermediario = pd.merge(parsed_df, df_final, on='estado', suffixes=('_x', '_y'), how='right')
        intermediario = intermediario.fillna(0)
        df_final['foco_queimadas_estados'] = intermediario['foco_queimadas_estados_x'] + intermediario['foco_queimadas_estados_y']

        df_final = df_final.fillna(0)
        df_final['estado'] = df_final['estado'].map(dicionario_estados)

        title = f"Estados mais afetados pelas queimadas de {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}" \
            if len(intervalo_de_dias) > 1 else f"Estados mais afetados pelas queimadas em {data_inicio.strftime('%d/%m/%Y')}"

        path_geojson = os.path.join(current_dir, '../resources/brasil_estados.json')

        with open(path_geojson, 'r') as f:
            geojson = json.load(f)

        df_final.rename(columns={'estado': 'estados'}, inplace=True)

        fig_map = px.choropleth(df_final, geojson=geojson, locations='estados', color='foco_queimadas_estados',
                                color_continuous_scale="Plasma",
                                range_color=(0, df_final['foco_queimadas_estados'].max()),
                                scope='south america',
                                labels={'foco_queimadas_estados': 'Focos de Queimadas'}
                          )

        fig_map.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
        fig_map.update_geos(
            fitbounds="locations",
            visible=True,
            lataxis_range=[-35, 5],
            lonaxis_range=[-75, -30],
        )
        return fig_map, title
    return no_update

@callback(
    Output('tabela-queimadas', 'data'),
    Output('title-tabela-dinamica-estados', 'children'),
    Input('ordenar-por', 'value'),
    State('dia-inicio-graficos', 'date'),
    State('dia-fim-graficos', 'date'),
    Input('btn-consolidados', 'n_clicks')
)
def atualizar_tabela(ordenar_por, date1, date2, n):
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

        df = asyncio.run(fetch_interval_data(intervalo_de_dias))

        parsed_df = pd.DataFrame(
            {'estado': df['estado'].unique(), 'foco_queimadas_estados': df['estado'].value_counts()})
        parsed_df.reset_index(drop=True, inplace=True)

        parsed_df = parsed_df.sort_values(ascending=True, by='estado')
        intermediario = pd.merge(parsed_df, df_final, on='estado', suffixes=('_x', '_y'), how='right')
        intermediario = intermediario.fillna(0)
        df_final['foco_queimadas_estados'] = intermediario['foco_queimadas_estados_x'] + intermediario['foco_queimadas_estados_y']

        df_final = df_final.fillna(0)
        df_final.rename(columns={'estado': 'Estado', 'foco_queimadas_estados': 'Número de Queimadas'}, inplace=True)

        if len(intervalo_de_dias) > 1:
            title = f"Tabela Dinâmica de Queimadas por Estado entre {data_inicio.strftime('%d/%m/%Y')} e {data_fim.strftime('%d/%m/%Y')}"
        else:
            title = f"Tabela Dinâmica de Queimadas por Estado em {data_inicio.strftime('%d/%m/%Y')}"

        if ordenar_por == 'desc':
            df_ordenado = df_final.sort_values(by='Número de Queimadas', ascending=False).reset_index(drop=True)
        elif ordenar_por == 'asc':
            df_ordenado = df_final.sort_values(by='Número de Queimadas', ascending=True).reset_index(drop=True)
        elif ordenar_por == 'z-a':
            df_ordenado = df_final.sort_values(by='Estado', ascending=False).reset_index(drop=True)
        else:
            df_ordenado = df_final.sort_values(by='Estado', ascending=True).reset_index(drop=True)
        df_ordenado['Posição'] = df_ordenado.index + 1

        return df_ordenado.to_dict('records'), title
    return no_update

@callback(
    Output('grafico-linha-queimadas', 'figure'),
    Output('title-grafico-linha-queimadas', 'children'),
    State('dia-inicio-graficos', 'date'),
    State('dia-fim-graficos', 'date'),
    Input('btn-consolidados', 'n_clicks')
)
def grafico_linha_queimadas(date1, date2, n):
    if n:
        data_inicio = datetime.strptime(date1, "%Y-%m-%d")
        data_fim = datetime.strptime(date2, "%Y-%m-%d")
        diferenca_dias = (data_fim - data_inicio).days
        intervalo_de_dias = []

        if diferenca_dias == 0:
            intervalo_de_dias.append(data_inicio.strftime("%Y%m%d"))
        else:
            for dia in range(0, diferenca_dias + 1):
                intervalo_de_dias.append((data_fim - timedelta(days=dia)).strftime("%Y%m%d"))

        dataframes = pd.DataFrame(asyncio.run(fetch_interval_data(intervalo_de_dias)))

        df_final = dataframes.groupby('dia').size().reset_index(name='total_queimadas')

        # total_queimadas_por_dia.append({'dia': intervalo_de_dias[index], 'total_queimadas': len(dataframes[index])})

        # df_final = pd.DataFrame(total_queimadas_por_dia)
        df_final['dia'] = pd.to_datetime(df_final['dia'], format='%Y%m%d')

        title = f"Variação de Queimadas de {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}" \
            if len(intervalo_de_dias) > 1 else f"Variação de Queimadas em {data_inicio.strftime('%d/%m/%Y')}"

        fig_line = px.line(
            df_final,
            x='dia',
            y='total_queimadas',
            labels={'dia': 'Intervalo de Dias', 'total_queimadas': 'Total de Queimadas'},
            markers=True
        )

        fig_line.update_xaxes(dtick="D1", tickformat="%d/%m")
        fig_line.update_layout(
            xaxis_title="Dia",
            yaxis_title="Total de Queimadas",
            margin={"r": 0, "t": 50, "l": 0, "b": 0}
        )

        return fig_line, title
    return no_update

layout = html.Div([
    html.Br(),
    html.H2("Dados Consolidados", style={"textAlign": "center", "margin-bottom": "20px"}),
    html.P(
        "Os Dados Consolidados tratam-se de um conjunto de dados vindos dos registros do BDQueimadas, "
        "a fim de melhor visualizar dentro do intervalo máximo de aproximadamente um mês, quais os biomas e estados "
        "mais afetados por focos de queimadas.",
        style={"textAlign": "center", "margin-bottom": "30px"}
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(html.B("Selecione um intervalo para visualização"), width=12, style={"textAlign": "center", "margin-bottom": "10px"}),
        dbc.Col([
            html.B("Data de início: "),
            dcc.DatePickerSingle(id='dia-inicio-graficos', date=datetime.today().date(), display_format="DD/MM/YYYY")
        ], width=4, style={"textAlign": "center"}),
        dbc.Col([
            html.B("Data de fim: "),
            dcc.DatePickerSingle(id='dia-fim-graficos', date=datetime.today().date(), display_format="DD/MM/YYYY")
        ], width=4, style={"textAlign": "center"}),
        dbc.Col([
            dbc.Button("Gerar Gráficos", id="btn-consolidados", color="primary", className="mt-1")
        ], width=4, style={"textAlign": "center"}),
    ], justify="center", style={"margin-bottom": "30px"}),
    dcc.Loading([
        html.Br(),
        html.H4(id="title-grafico-barras-biomas-consolidado", style={"textAlign": "center", "margin-bottom": "20px"}),
        dcc.Graph(id="grafico-barras-biomas-consolidado", style={"margin-bottom": "30px"})
    ], id="loading-3", type="circle"),
    dcc.Loading([
        html.Br(),
        html.H4(id="title-grafico-estados-mais-afetados", style={"textAlign": "center", "margin-bottom": "20px"}),
        dcc.Graph(id="grafico-estados-mais-afetados", style={"margin-bottom": "30px"})
    ], id="loading-4", type="circle"),
    dcc.Loading([
        html.Br(),
        html.H4(id="title-grafico-linha-queimadas", style={"textAlign": "center", "margin-bottom": "20px"}),
        dcc.Graph(id="grafico-linha-queimadas", style={"margin-bottom": "30px"})
    ], id="loading-5", type="circle"),
    dcc.Loading([
        html.Br(),
        html.H4(id="title-tabela-dinamica-estados", style={"textAlign": "center", "margin-bottom": "20px"}),
        dcc.Dropdown(
            id='ordenar-por',
            options=[
                {'label': 'Número de Queimadas (Decrescente)', 'value': 'desc'},
                {'label': 'Número de Queimadas (Crescente)', 'value': 'asc'},
                {'label': 'Estados (Z-A)', 'value': 'z-a'},
                {'label': 'Estados (A-Z)', 'value': 'a-z'}
            ],
            value='desc',
            placeholder="Ordenar por...",
            style={'margin-bottom': '10px', "width": "60%"}
        ),
        DataTable(
            id='tabela-queimadas',
            columns=[
                {'name': 'Posição', 'id': 'Posição'},
                {'name': 'Estado', 'id': 'Estado'},
                {'name': 'Número de Queimadas', 'id': 'Número de Queimadas'}
            ],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '10px'},
            style_header={'fontWeight': 'bold', 'backgroundColor': '#f8f9fa'},
            style_data={'backgroundColor': '#ffffff', 'border': '1px solid #dee2e6'},
        )
    ], id="loading-6", type="circle"),
], className="pad-row", style={"padding": "20px"})
