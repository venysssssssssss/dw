import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Obter as variáveis do arquivo .env
DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

# Criar a URL de conexão do banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

commodities = ['CL=F', 'GC=F', 'SI=F']

def buscar_dados_de_comodities(simbolo, periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    dados['simbolo'] = simbolo
    return dados


def buscar_todos_dados_de_commodities(commodities):
    todos_os_dados = []
    for simbolo in commodities:
        dados = buscar_dados_de_comodities(simbolo)
        todos_os_dados.append(dados)
    return pd.concat(todos_os_dados)


def salvar_no_postgres(df, schema='public'):
    df.to_sql('commodities', engine, if_exists='replace', index=True, index_label='Date', schema=schema)
    print(f"Dados salvos no schema '{schema}' do banco de dados PostgreSQL")


if __name__ == '__main__':
    dados_concatenados = buscar_todos_dados_de_commodities(commodities)
    salvar_no_postgres(dados_concatenados, schema=DB_SCHEMA)