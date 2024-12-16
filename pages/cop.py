import dash
from dash import html

dash.register_page(__name__)

p1 = '''A Conferência das Partes (em inglês, Conference of the Parties ou COP) é o nome dado ao principal órgão da Convenção-Quadro 
das Nações Unidas sobre Mudanças Climáticas (em inglês, United Nations Framework Convention on Climate Change ou UNFCCC). A UNFCCC 
entrou em vigor em março de 1995, a partir do reconhecimento de que o clima é um recurso global e compartilhado, que pode ser 
comprometido por atividades humanas que emitem gases de efeito estufa e causam o aquecimento do planeta.'''

p2 = '''A COP é um evento anual que reúne os países que aderiram à UNFCCC e ao Protocolo de Kyoto. Esse evento é essencial para a 
negociação de acordos e elaboração de estratégias para enfrentar desafios ambientais. As decisões são tomadas coletivamente e 
validadas se aceitas por unanimidade, sendo obrigatórias para todos os países signatários. Os países membros se reuniram 29 vezes 
até a presente data, tendo dois desses encontros um maior destaque: a COP-3 e COP-21.'''

p3 = '''A COP-3, realizada em Kyoto, Japão, em 1997, resultou na adoção do Protocolo de Kyoto, que estabelece metas de redução de 
emissões de gases de efeito estufa para os países desenvolvidos. Os Estados Unidos não ratificaram o acordo, sob a justificativa de 
que cumprir as metas estabelecidas comprometeria seu desenvolvimento econômico e deixaram o acordo em 2001. Para entrar em vigor, o 
Protocolo dependia da ratificação por 55 países, o que foi alcançado em 2005, após a Rússia concordar.'''

p4 = '''A COP-21, realizada em Paris, em 2015, alcançou um acordo que envolveu quase todos os países do mundo em esforços para 
reduzir as emissões de carbono e combater os impactos do aquecimento global, que ficou conhecido como Acordo de Paris. Um total de 
195 países membros da Convenção do Clima da ONU, juntamente com a União Europeia, ratificaram o documento. O objetivo de longo prazo 
do acordo é manter o aquecimento global abaixo de 2ºC, considerado o limite crítico para evitar efeitos catastróficos, como eventos 
climáticos extremos. O acordo também menciona esforços para limitar o aumento da temperatura a 1,5ºC e estabelece revisões a cada 
cinco anos para acompanhar o progresso em direção às metas climáticas.'''

p5 = '''Apesar de sua grande importância para auxiliar a tomada de decisão a respeito dos passos a seguir para tentar mitigar um 
possível agravamento da situação global, infelizmente nem sempre ocorre de acordo com o proposto em reuniões da COP. Como apontado 
por Dryzek em "The Politics of the Earth: Environmental Discourses" (2013, p.47, em tradução livre do autor), “[...] Quase todos os países do mundo enviam representantes (para a COP). Mas 
um acordo tem se tornado inatingível; e diversos países parecem estar lutando pelos seus interesses econômicos próprios, apenas 
falando da boca para fora a respeito das preocupações climáticas mundiais.”.'''

p6 = '''O Brasil foi eleito o país-sede da COP-30, em 2025, devendo ocorrer na capital do Pará, Belém. A escolha da sede foi 
motivada pelo interesse em destacar a importância da Amazônia no debate climático e permitir que os participantes conheçam a região 
e suas riquezas naturais, como os rios, as florestas e a fauna local, além de levantar discussões sobre questões locais, como a 
questão dos povos indígenas e ribeirinhos.'''

layout = html.Div([
    html.Br(),
    html.H1('Qual o Papel da Conferência das Partes?'),
    html.Br(),
    html.Article(p1),
    html.Br(),
    html.Article(p2),
    html.Br(),
    html.Div(html.Img(src='../static/images/cop.jpg', alt='Primeira Conferência das Partes, realizada em Berlim, 1995'), style={'textAlign': 'center'}),
    html.Br(),
    html.Article(p3),
    html.Br(),
    html.Article(p4),
    html.Br(),
    html.Article(p5),
    html.Br(),
    html.Article(p6),
    html.Br(),
    html.H4("Referências", style={'text-align': 'center'}),
    html.Br(),
    html.Ol([
        html.Li(html.A("BRASIL. Ministério do Meio Ambiente. Convenção-Quadro das Nações Unidas sobre Mudança do Clima (UNFCCC). Ministério do Meio Ambiente, [2024].", href="https://antigo.mma.gov.br/clima/convencao-das-nacoes-unidas.html")),
        html.Li(html.A("BRASIL. Ministério do Meio Ambiente. Conferência das Partes. Ministério do Meio Ambiente, [2024].", href="https://antigo.mma.gov.br/clima/convencao-das-nacoes-unidas/conferencia-das-partes.html")),
        html.Li(html.A("BRASIL. Presidência da República. COP 30 no Brasil. Portal do Planalto, [2024].", href="https://www.gov.br/planalto/pt-br/agenda-internacional/missoes-internacionais/cop28/cop-30-no-brasil#:~:text=O%20estado%20do%20Par%C3%A1%20se,os%20principais%20dias%20da%20Confer%C3%AAncia")),
        html.Li(html.A("DRYZEK, J. S. The Politics of the Earth: Environmental Discourses. OUP Oxford, 2013.", href="https://books.google.com.br/books?id=EJM1OTeZ0sgC")),
        html.Li(html.A("FUNDAÇÃO AMAZÔNIA SUSTENTÁVEL. O caminho até Dubai: confira o histórico de COP desde 1995. Fundação Amazônia Sustentável, 2023.", href="https://fas-amazonia.org/blog-da-fas/2023/11/17/o-caminho-ate-dubai-confira-o-historico-de-cop-desde-1995")),
        html.Li(html.A("UNFCCC SECRETARIAT. Conference of the Parties (COP). 2023.", href="https://unfccc.int/process/bodies/supreme-bodies/conference-of-the-parties-cop"))
    ])
])