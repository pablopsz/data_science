# Projeto de Análise de Carros Seminovos

Este repositório contém um projeto para coletar, processar e visualizar dados de carros seminovos. O projeto é dividido em três partes principais: coleta de dados, concatenação de dados e visualização dos dados usando a biblioteca Streamlit.

## Estrutura do Repositório
- dash
- data
- df_main
- get_data
- requirements.txt

Em "**get_data**" é feito um request a uma API utilizada no front-end do catálogo de seminovos da revendedora "Movidas", com o retorno de todos os carros disponíveis do catalogo. Esses dados são armazenados em na pasta "data", com uma coluna identificando o dia em que os dados foram coletados.

Em "**df_main**" todos os dados são concatenados para serem utilizados no Dashboard.

Em "**dash**", temos uma página Home de um dashboard feito utilizando a biblioteca Streamlit, além de subpastas como "**pages**", que contém as páginas de "Estoque" e "Tempo de estoque" do dashboard, e "**utils**" que contém uma classe utilizada no projeto para criar gráficos de forma mais prática.

Em "**requirements.txt**" você pode ver todos os requisitos para utilizar o projeto. Em resumo, são necessárias as bibliotecas "streamlit", "pandas" e "requests".

Nesse repositório, estarei disponibilizando apenas um arquivo do catálogo como exemplo.

## Executando o Projeto

### Coletando os dados
Execute o script "get_api_movidas.py" para coletar os dados diários dos carros seminovos. Os dados serão armazenados na pasta data com a data de coleta. Para um projeto mais robusto, agende a execução do script para que os dados sejam coletados todos os dias.

### Concatenação de Dados
Execute o script "df_concat.py" para concatenar todos os arquivos de dados coletados em um único DataFrame.

### Visualização de Dados
Para inicar o Dashboard, escreva no terminal "streamlit run dash\Home.py (ou o local onde está o arquivo em questão)". Assim, o Dashboard será iniciado em seu navegador.

## Resultado Final
O resultado final é uma visualização conforme mostrado abaixo:

[Dashboard Análise de Seminivos](https://github.com/user-attachments/assets/97fc6d8b-3842-4d89-a703-11c27f90ebe2)


