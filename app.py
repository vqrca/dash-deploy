from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import joblib
import pandas as pd
import dash_bootstrap_components as dbc
import dash

# Carrega o modelo treinado
modelo = joblib.load('modelo_xgboost.pkl')

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

# Definição do layout do aplicativo Dash
app.layout = dbc.Container([
    html.H1('Previsão de Doença Cardíaca',className='text-center mt-5'),
    html.P('Informe os dados do paciente e clique em prever para receber a previsão.', className='text-center mb-5'),
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Label('Idade'),
                dbc.Input(id='idade', type='number', placeholder='Idade'),
            ],className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Sexo biológico'),
                dbc.Select(
                    id='sexo',
                    options=[
                        {'label': 'Masculino', 'value': 1},
                        {'label': 'Feminino', 'value': 0},
                    ],
                ),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Tipo de Dor no Peito'),
                dbc.Select(
                    id='cp',
                    options=[
                        {'label': 'Angina típica', 'value': 1},
                        {'label': 'Angina atípica', 'value': 2},
                        {'label': 'Não angina', 'value': 3},
                        {'label': 'Angina assintomática', 'value': 4},
                    ],
                ),
            ],className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Pressão Sanguínea em Repouso'),
                dbc.Input(id='trestbps', type='number', placeholder='Pressão Sanguínea em Repouso'),
            ],className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Colesterol sérico'),
                dbc.Input(id='chol', type='number', placeholder='Colesterol sérico'),
            ],className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Glicose em Jejum > 120 mg/dl'),
                dbc.Select(
                    id='fbs',
                    options=[
                        {'label': 'Não', 'value': 0},
                        {'label': 'Sim', 'value': 1},
                    ],
                ),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Resultados Eletrocardiográficos em Repouso'),
                dbc.Select(
                    id='restecg',
                    options=[
                        {'label': 'Normal', 'value': 0},
                        {'label': 'Anormalidade de ST-T', 'value': 1},
                        {'label': 'Hipertrofia Ventricular Esquerda', 'value': 2},
                    ],
                ),
            ], className='mb-3'),
        ], md=5),
        dbc.Col([
            dbc.CardGroup([
                dbc.Label('Frequência Cardíaca Máxima'),
                dbc.Input(id='thalach', type='number', placeholder='Frequência Cardíaca Máxima'),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Angina Induzida por Exercício'),
                dbc.Select(
                    id='exang',
                    options=[
                        {'label': 'Não', 'value': 0},
                        {'label': 'Sim', 'value': 1},
                    ],
                ),
            ],className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Depressão de ST Induzida por Exercício'),
                dbc.Input(id='oldpeak', type='number', placeholder='Depressão de ST Induzida por Exercício'),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Inclinação do Segmento ST no Pico do Exercício'),
                dbc.Select(
                    id='slope',
                    options=[
                        {'label': 'Inclinação para Cima', 'value': 1},
                        {'label': 'Plano', 'value': 2},
                        {'label': 'Inclinação para Baixo', 'value': 3},
                    ],
                ),
            ],className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Número de Vasos Principais Coloridos por Fluoroscopia (0 a 3)'),
                dbc.Input(id='ca', type='number', placeholder='Número de Vasos Principais Coloridos por Fluoroscopia (0 a 3)'),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label('Cintilografia do miocárdio com tálio'),
                dbc.Select(
                    id='thal',
                    options=[
                        {'label': 'Normal', 'value': 3},
                        {'label': 'Defeito Fixo', 'value': 6},
                        {'label': 'Defeito Reversível', 'value': 7},
                    ],
                ),
            ]),
            dbc.Button('Prever', id='prever', color='success', n_clicks=0, className='mt-5 mb-5'),
        ], md=6),
    ]),
    html.Div(id='resultado'),
    html.Div(className='mb-5'),
], fluid=True, className='px-5')

# Carrega as medianas dos campos
medianas = joblib.load('medianas.pkl')

@app.callback(
    Output('resultado', 'children'),
    [Input('prever', 'n_clicks')],
    [State('idade', 'value'),
     State('sexo', 'value'),
     State('cp', 'value'),
     State('trestbps', 'value'),
     State('chol', 'value'),
     State('fbs', 'value'),
     State('restecg', 'value'),
     State('thalach', 'value'),
     State('exang', 'value'),
     State('oldpeak', 'value'),
     State('slope', 'value'),
     State('ca', 'value'),
     State('thal', 'value')]
)


def prever_doenca_cardiaca(n_clicks, idade, sexo, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    if n_clicks > 0:
        # Cria um DataFrame com as entradas do usuário
        entradas_usuario = pd.DataFrame(
            data=[[idade, sexo, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]],
            columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        )

        # Preenche os valores vazios com as medianas
        entradas_usuario.fillna(medianas, inplace=True)

        entradas_usuario['sex'] = entradas_usuario['sex'].astype(int)
        entradas_usuario['cp'] = entradas_usuario['cp'].astype(int)
        entradas_usuario['trestbps'] = entradas_usuario['trestbps'].astype(float)  # Se espera um número inteiro ou flutuante
        entradas_usuario['chol'] = entradas_usuario['chol'].astype(float)  # Se espera um número inteiro ou flutuante
        entradas_usuario['fbs'] = entradas_usuario['fbs'].astype(int)
        entradas_usuario['restecg'] = entradas_usuario['restecg'].astype(int)
        entradas_usuario['thalach'] = entradas_usuario['thalach'].astype(float)  # Se espera um número inteiro ou flutuante
        entradas_usuario['exang'] = entradas_usuario['exang'].astype(int)
        entradas_usuario['oldpeak'] = entradas_usuario['oldpeak'].astype(float)  # Se espera um número inteiro ou flutuante
        entradas_usuario['slope'] = entradas_usuario['slope'].astype(int)
        entradas_usuario['ca'] = entradas_usuario['ca'].astype(int)
        entradas_usuario['thal'] = entradas_usuario['thal'].astype(int)
        
        # Faz a predição com os dados do usuário
        predicao = modelo.predict(entradas_usuario)[0]
        
        return f'O modelo previu que o paciente {"tem" if predicao else "não tem"} doença cardíaca.'
    #return 'Informe seus dados e clique em prever para receber a previsão.'


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)
