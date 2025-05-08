import pandas as pd
import numpy as np
from pathlib import Path

# Configurações
DATA_PATH = Path().resolve() / 'data'
ARQUIVO_AMOSTRA_PATH = DATA_PATH / 'raw' / 'microdados_enem_2023_sample.csv'

# Definição dos tipos
colunas_float = [
    'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT',
    'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4',
    'NU_NOTA_COMP5', 'NU_NOTA_REDACAO'
]

colunas_string = [
    'NU_INSCRICAO', 'CO_MUNICIPIO_ESC', 'CO_MUNICIPIO_PROVA'
]

# Captura os nomes das colunas
colunas = pd.read_csv(ARQUIVO_AMOSTRA_PATH, nrows=0, encoding='latin1').columns.tolist()

# Preparar o dicionário de tipos
dtypes = {}
for col in colunas:
    if col in colunas_float:
        dtypes[col] = 'float32'
    elif col in colunas_string:
        dtypes[col] = 'string'
    else:
        dtypes[col] = 'category'

# Leitura com tipos otimizados
df = pd.read_csv(ARQUIVO_AMOSTRA_PATH, dtype=dtypes, encoding='latin1')

# Exclusoes
del df['NU_INSCRICAO']
del df['TP_FAIXA_ETARIA']
del df['CO_MUNICIPIO_ESC']                         
del df['TP_DEPENDENCIA_ADM_ESC']                   
del df['TP_LOCALIZACAO_ESC']                       
del df['TP_SIT_FUNC_ESC']
del df['TP_ENSINO']
del df['CO_MUNICIPIO_PROVA']

# TP_CONCLUSAO
condicoes = [
    (df['TP_ANO_CONCLUIU'] == '0') & (df['TP_ST_CONCLUSAO'] == '1'),    # Concluido mas sem ano
    (df['TP_ANO_CONCLUIU'] == '0') & (df['TP_ST_CONCLUSAO'] == '2'),    # EM a ser concluido em 2023
    (df['TP_ANO_CONCLUIU'] == '0') & (df['TP_ST_CONCLUSAO'] == '3'),    # EM a ser concluido após 2023
    (df['TP_ANO_CONCLUIU'] == '0') & (df['TP_ST_CONCLUSAO'] == '4'),    # EM não cursado
    (df['TP_ANO_CONCLUIU'] == '1'),                                     # EM concluido em 2022
    (df['TP_ANO_CONCLUIU'].isin(['2', '3', '4', '5'])),                 # EM concluido entre 2021 e 2018
    (df['TP_ANO_CONCLUIU'].isin(['6', '7', '8', '9', '10', '11',
                                    '12', '13', '14', '15', '16'])),    # EM concluido entre 2017 e 2007
    (df['TP_ANO_CONCLUIU'] == '17')                                     # EM concluido após 2007
]

# Valores que serão atribuídos com base nas condições
valores = [1, 2, 3, 4, 5, 6, 7, 8]

df['TP_CONCLUSAO'] =  np.select(condicoes, valores)
df['TP_CONCLUSAO'] = df['TP_CONCLUSAO'].astype('category')

df['TP_CONCLUSAO'] = df['TP_CONCLUSAO'].cat.rename_categories({
    '1.0': '1',
    '2.0': '2',
    '3.0': '3',
    '4.0': '4',
    '6.0': '6',
    '7.0': '7',
    '8.0': '8'
})

del df['TP_ANO_CONCLUIU']
del df['TP_ST_CONCLUSAO'] 

# TP_PRESENCA_DIA1 e TP_PRESENCA_DIA2
df.rename(columns={
    'TP_PRESENCA_CH': 'TP_PRESENCA_DIA1',
    'TP_PRESENCA_CN': 'TP_PRESENCA_DIA2'
}, inplace=True)

del df['TP_PRESENCA_LC']
del df['TP_PRESENCA_MT']

# CO_PROVA_DIA1
condicoes = [
    df['CO_PROVA_CH'].isin(['1191.0', '1192.0', '1193.0', '1194.0']),               # Prova Comum
    df['CO_PROVA_CH'].isin(['1195.0', '1196.0', '1197.0', '1198.0', '1199.0']),     # Prova Adaptada
    df['CO_PROVA_CH'].isin(['1271.0', '1272.0', '1273.0', '1274.0']),               # Prova Reaplicação
    df['CO_PROVA_CH'].isna()                                                        # Ausente
]

# Valores que serão atribuídos com base nas condições
valores = [1, 2, 3, 4]

df['CO_PROVA_DIA1'] =  np.select(condicoes, valores)
df['CO_PROVA_DIA1'] = df['CO_PROVA_DIA1'].astype('category')
del df['CO_PROVA_CH']
del df['CO_PROVA_LC'] 

# CO_PROVA_DIA2
condicoes = [
    df['CO_PROVA_CN'].isin(['1221.0', '1222.0', '1223.0', '1224.0']),               # Prova Comum
    df['CO_PROVA_CN'].isin(['1225.0', '1226.0', '1227.0', '1228.0', '1229.0']),     # Prova Adaptada
    df['CO_PROVA_CN'].isin(['1301.0', '1302.0', '1303.0', '1304.0']),               # Prova Reaplicação
    df['CO_PROVA_CN'].isna()                                            # Ausente
]

# Valores que serão atribuídos com base nas condições
valores = [1, 2, 3, 4]

df['CO_PROVA_DIA2'] = np.select(condicoes, valores)
df['CO_PROVA_DIA2'] = df['CO_PROVA_DIA2'].astype('category')
del df['CO_PROVA_CN']
del df['CO_PROVA_MT'] 

# ESC_MAE, ESC_PAI, INTERNET
df.rename(columns={
    'Q001': 'ESC_PAI',
    'Q002': 'ESC_MAE',
    'Q025': 'INTERNET'
}, inplace=True)

# RENDA
condicoes = [
    df['Q006'] == 'A',
    df['Q006'] == 'B',
    df['Q006'].isin(['C', 'D']),
    df['Q006'].isin(['E', 'F']),
    df['Q006'] == 'G',
    df['Q006'].isin(['H', 'I']),
    df['Q006'].isin(['J', 'K', 'L', 'M']),
    df['Q006'].isin(['N', 'O']),
    df['Q006'] == 'P',
    df['Q006'] == 'Q'
]

valores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

df['RENDA'] = np.select(condicoes, valores)
df['RENDA'] = df['RENDA'].astype(int).astype('category')

del df['Q006']

# TP_STATUS_REDACAO

condicoes = [
    df['TP_STATUS_REDACAO'] == '1.0',
    df['TP_STATUS_REDACAO'] == '2.0',
    df['TP_STATUS_REDACAO'] == '3.0',
    df['TP_STATUS_REDACAO'] == '4.0',
    df['TP_STATUS_REDACAO'] == '6.0',
    df['TP_STATUS_REDACAO'] == '7.0',
    df['TP_STATUS_REDACAO'] == '8.0',
    df['TP_STATUS_REDACAO'] == '9.0',
    df['TP_STATUS_REDACAO'].isna(),
]

valores = [1, 2, 3, 4, 6, 7, 8, 9, 10]

df['TP_STATUS_REDACAO'] =  np.select(condicoes, valores)
df['TP_STATUS_REDACAO'] = df['TP_STATUS_REDACAO'].astype('category')

# Transformacao das variaveis numericas em categoricas, segunda as faixas estipuladas

colunas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT',  'NU_NOTA_REDACAO',
           'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5']

for col in colunas:
    media = df[col].mean()
    std = df[col].std()

    if col not in ['NU_NOTA_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5']:
        condicoes = [
            df[col].isna(),
            df[col] == 0,
            df[col] < media - std,
            df[col] <= media + std,
            df[col] <= media + 2*std,
            df[col] > media + 2*std
        ]
    elif col == 'NU_NOTA_REDACAO': 
        condicoes = [
            df[col].isna(),
            df[col] == 0,
            df[col] < media - std,
            df[col] <= media + std,
            (df[col] > media + std) & (df[col] < 900),
            df[col] >= 900
        ]
    else:
        condicoes = [
            df[col].isna(),
            df[col] == 0,
            df[col] < media - std,
            df[col] <= media + std,
            (df[col] > media + std) & (df[col] < 200),
            df[col] == 200
        ]

    valores = [0, 1, 2, 3, 4, 5]

    df[col] =  np.select(condicoes, valores)
    df[col] = df[col].astype('category')

# Proporcao das faixas das notas

print("\n:")

colunas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO',
           'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5']
contagens = {}
percentual = {}

for col in colunas:
    
    contagens[f'tp_{col}'] = df[col].value_counts(dropna=False)
    percentual[f'tp_{col}_pct'] = df[col].value_counts(normalize=True, dropna=False) * 100

    resultado = pd.DataFrame({
        'Frequência': contagens[f'tp_{col}'],
        'Percentual (%)': percentual[f'tp_{col}_pct'].round(2)
    })
    
    print(resultado, '\n')