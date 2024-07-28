import os
import pandas as pd

dfs = []

diretorio = 'E:\\Workspace\\analise_seminovos\\data'

for arquivo in os.listdir(diretorio):
    if arquivo.startswith('all_cars') and arquivo.endswith('.json'):
        data_atual = arquivo.replace('all_cars', '').replace('.json', '')

        if data_atual[2:4] == "03" or data_atual[2:4] == "04":
            df = pd.read_json(os.path.join(diretorio, arquivo))
        
            df['data_atual'] = data_atual
            
            dfs.append(df)


df = pd.concat(dfs, ignore_index=True)

df['lat'] = df['localizacao'].apply(lambda x: x.split(',')[0])
df['lon'] = df['localizacao'].apply(lambda x: x.split(',')[1])

df.to_csv('E:\\Workspace\\analise_seminovos\\df_main\\df_consol.csv', encoding='utf-8', index=False)