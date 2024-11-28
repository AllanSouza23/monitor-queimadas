# import dash
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn import model_selection
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
# from dash import html, callback, dcc, Input

# dash.register_page(__name__)


# @callback(
#     Input('btn-novo', 'n_clicks')
# )
# def teste(n):
#     print('aa')
#     if n:
#         df = pd.read_csv('https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/mensal/Brasil/focos_mensal_br_202405.csv')
#         # df.drop('id', inplace=True, axis=1)
#         # df.drop('municipio_id', inplace=True, axis=1)
#         # df.drop('estado_id', inplace=True, axis=1)
#         # df.drop('pais_id', inplace=True, axis=1)
#         # df.drop('precipitacao', inplace=True, axis=1)
#         # df.drop('numero_dias_sem_chuva', inplace=True, axis=1)
#         # df.drop('frp', inplace=True, axis=1)
#         # df.drop('lat', inplace=True, axis=1)
#         # df.drop('lon', inplace=True, axis=1)
#         # df.drop('satelite', inplace=True, axis=1)
#         # df.drop('risco_fogo', inplace=True, axis=1)
#         # df.drop('pais', inplace=True, axis=1)

#         # print(df.info())
#         return

# layout = html.Div([
#     html.H1('This is our Previsao page'),
#     html.Div('This is our Previsao page content.'),
#     html.Button(id="btn-novo", value='teste', n_clicks=0)
# ])