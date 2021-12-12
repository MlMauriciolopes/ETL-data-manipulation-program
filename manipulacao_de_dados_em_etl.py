#!/usr/bin/env python
# coding: utf-8

# In[4]:


# Importando as bibliotecas
import pandas as pd


# In[5]:


# Pegar o tamanho/posição das colunas 
# Nomes dados a essas colunas
# Criar listas com nome de colunas e lista com os nomes dos campos

#3.2 Registro - 01- Cotacções históricas por papel-mercado =

def read_files(path, name_file, year_date, type_file ):
    
    _file = f'{path}{name_file}{year_date}.{type_file}'
    
    colspecs = [(2,10),  # Data do pregão (3,10)
                (10,12), # CODBDI - código BDI (11,12)
                (12,24), # CODNEG - Código de negociação de papel (13,24)
                (27,39), # NONAMES - Nome resumido da empresa emissora do papel (28,39)
                (56,69), # PREABE - Preço de abertura do papel - mercado no pregão
                (69,82), # PREMAX - Preço máximo do papel - mercado de pregão
                (82,95), # PREMIN - Preço mínimo do papel - mercado de pregão
                (108,121), # PREULT - Preço do último negócio do papel  - mercado no pregão
                (152,170), # QUATOT - Quantidade total de títulos negociados neste papel - mercado
                (170,188) #VOLTOT - Volume total de títulos negociados neste papel - mercado
    ]

    names = ['data_pregao', 'cod_bdi', 'sigla_acao', 'nome_acao', 'preco_abertura','preco_maximo', 'preco_minimo', 'preco_fechamento', 'qtd_negocios','volume_negocios']

    #df = pd.read_fwf('C:/Users/mlsil/OneDrive/Área de Trabalho/manipulacao_dados_bovespa/COTAHIST_A2020.txt', colspecs = colspecs, names = names, skiprows = 1)
    df = pd.read_fwf(_file, colspecs = colspecs, names = names, skiprows = 1)
    
    return df

#df


# In[6]:


# Filtrar o lote padrão / filtrar ações
def filter_stocks(df):
    df = df [df['cod_bdi'] == 2]
    df = df.drop(['cod_bdi'], 1)
    
    return df


# In[7]:


# Ajuste campo de data
def parse_date(df):
    df['data_pregao'] = pd.to_datetime(df['data_pregao'], format = '%Y%m%d')
    return df


# In[8]:


# Ajuste dos campos numéricos

def parse_values(df):
    df['preco_abertura'] = (df['preco_abertura'] /100).astype(float)
    df['preco_maximo'] = (df['preco_maximo'] /100).astype(float)
    df['preco_minimo'] = (df['preco_minimo'] /100).astype(float)
    df['preco_fechamento'] = (df['preco_fechamento'] /100).astype(float)

    return df


# In[9]:


# Juntando os arquivos
def concat_files(path, name_file, name_date, type_file, final_file):
    for i, y in enumerate(year_date):
        df = read_files(path, name_file, y, type_file)
        df = filter_stocks(df)
        df = parse_date(df)
        df = parse_values(df)
        
        if i == 0:
            df_final = df
        else:
            df_final = pd.concat([df_final, df])
    
    df_final.to_csv(f'{path}//{final_file}', index = False)


# In[10]:


# Executando programa  de etl

year_date = ['2018', '2019', '2020']

path = f'C:/Users/mlsil/OneDrive/Área de Trabalho/manipulacao_dados_bovespa/'

name_file = 'COTAHIST_A'

type_file = 'txt'

final_file = 'all_bovespa.csv'

concat_files(path, name_file, year_date, type_file, final_file)


# In[ ]:




