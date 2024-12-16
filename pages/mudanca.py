import dash
from dash import html

dash.register_page(__name__, path='/mudancas-climaticas')

p1 = '''O Brasil, como um país de dimensões continentais, possui como característica marcante uma vasta biodiversidade, seja relativa 
à fauna, com grande variedade de animais ao longo de cada região, bem como no tocante à flora, que constitui cada um dos seis 
distintos biomas brasileiros.
'''

p2 = '''As queimadas ainda são amplamente utilizadas no Brasil para limpar a vegetação natural e preparar a terra para cultivos e 
pastagens. Inicialmente, parece que as queimadas beneficiam as plantações, pois as cinzas aumentam os nutrientes no solo. No entanto, 
os prejuízos superam os benefícios, pois o fogo destrói nutrientes, microrganismos, insetos e resíduos vegetais, causando vários 
impactos negativos, como desequilíbrios nos ecossistemas, extinção de espécies nativas, redução da qualidade do ar e emissão de gases 
de efeito estufa. (RAMOS et al., 2015).'''

p3 = '''Dentre os principais agentes para fiscalizar, coibir, estabelecer regulamentações e punições àqueles que deterioram o 
meio-ambiente são os órgãos governamentais. Um exemplo disto é a Lei nº 12.651/2012, que estabelece que o Governo Federal deve 
implementar uma Política Nacional de Manejo e Controle de Queimadas, visando substituir o uso do fogo no meio rural e melhorar a 
prevenção e combate aos incêndios florestais. (SOUSA, BASTOS, 2020).'''

p4 = '''Atualmente existem implementações de sistemas de monitoramento e programas que fornecem informações sobre o desmatamento, 
potencializado também por queimadas, como os projetos PRODES e DETER, ambos mantidos pelo Instituto Nacional de Pesquisas Espaciais 
(INPE). A legislação brasileira aponta que a geração de danos ao meio ambiente como o desmatamento é considerada como crime, como 
também provocar incêndio em mata ou floresta, extração ilegal de recursos naturais, e o uso não autorizado de motosserras.'''

layout = html.Div([
    html.Br(),
    html.H1('Qual o impacto das Queimadas?'),
    html.Br(),
    html.Article(p1),
    html.Br(),
    html.Article(p2),
    html.Br(),
    html.Article(p3),
    html.Br(),
    html.Div(html.Img(src='../static/images/mudancas-climaticas.jpg', alt='Foco de queimada registrado em Roraima'), style={'textAlign': 'center'}),
    html.Br(),
    html.Article(p4),
    html.Br(),
    html.H4("Referências", style={'text-align': 'center'}),
    html.Br(),
    html.Ol([
        html.Li("RAMOS, R. C. et al. Análise das áreas queimadas na região sul do Maranhão no ano de 2013. In: Simpósio Brasileiro de Sensoriamento Remoto - SBSR, 17, 2015, João Pessoa-PB. Anais... João Pessoa: INPE: 2015"),
        html.Li(html.A("SOUSA, C. T. C.; BASTOS, A. T. Queimadas no Brasil e o direito ao meio ambiente ecologicamente equilibrado. Intraciência Uniesp, Guarujá, v.19, p. 1- 13, 2020.", href="https://uniesp.edu.br/sites/_biblioteca/revistas/20200522115203.pdf"))
    ])
])
