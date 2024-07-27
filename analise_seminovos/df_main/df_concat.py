import os
import pandas as pd


# Lista para armazenar todos os DataFrames
dfs = []

# Diretório onde os arquivos estão armazenados
diretorio = 'E:\\Workspace\\analise_seminovos\\data'

# Iterar sobre todos os arquivos no diretório
for arquivo in os.listdir(diretorio):
    if arquivo.startswith('all_cars') and arquivo.endswith('.json'):
        # Extrair a data do nome do arquivo
        data_atual = arquivo.replace('all_cars', '').replace('.json', '')
        
        # Carregar o arquivo JSON em um DataFrame
        df = pd.read_json(os.path.join(diretorio, arquivo))
        
        # Adicionar uma coluna com a data atual
        df['data_atual'] = data_atual
        
        # Adicionar este DataFrame à lista
        dfs.append(df)

# Concatenar todos os DataFrames da lista em um único DataFrame
df = pd.concat(dfs, ignore_index=True)

df['lat'] = df['localizacao'].apply(lambda x: x.split(',')[0])
df['lon'] = df['localizacao'].apply(lambda x: x.split(',')[1])

df.to_csv('E:\\Workspace\\analise_seminovos\\df_main\\df_consol.csv', encoding='utf-8', index=False)



