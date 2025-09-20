
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

@st.cache_data
def carregar_dados():
    
    try:
        classifica = pd.read_excel(r'C:\Users\fazin\OneDrive\Documents\Nisio\Retorno_Resultados_HVI\Hvi_retorno\RetornosHVI_Testes\Teste-Apresentação.xlsx', sheet_name='Fardos')
        classifica.columns = classifica.iloc[1]
        classifica.drop([0, 1], inplace=True)

        df_clone = pd.DataFrame(
            classifica.loc[:, ['Número', 'Bloco', 'Talhão', 'Data Benef', 'Tipo', 'Peso', 'Variedade']])
        df_clone['Data Benef'] = pd.to_datetime(df_clone['Data Benef'], format='%d/%m/%Y', errors="coerce")
        return df_clone
    except FileNotFoundError:
        st.error("Arquivo Excel não encontrado. Verifique o caminho.")
        st.stop() 
        st.exception(f"Erro ao ler o arquivo Excel: {e}")
        st.stop() 


st.title("Visualizador de Produção")

df_clone = carregar_dados()

col1, col2 = st.columns(2)
with col1:
    data_inicio = st.date_input("Data de Início", value=datetime.date(2025, 7, 1))
with col2:
    data_fim = st.date_input("Data de Fim", value=datetime.date(2025, 7, 31))

tipos_unicos = df_clone['Variedade'].unique()
tipo_selecionado = st.selectbox("Selecione a Variedade", tipos_unicos)

# Converter datas para o formato necessário para o Pandas
data_inicio = pd.to_datetime(data_inicio)
data_fim = pd.to_datetime(data_fim)

#Verificação das datas
if data_inicio > data_fim:
    st.error("A data de início deve ser anterior à data de fim.")
else:
    if 'Data Benef' not in df_clone.columns:
        st.error("A coluna 'Data Benef' não existe no arquivo.")
    elif 'Tipo' not in df_clone.columns:
        st.error("A coluna 'Variedade' não existe no arquivo.")
    elif 'Peso' not in df_clone.columns:
        st.error("A coluna 'Peso' não existe no arquivo.")
    else:
        df_filtrado = df_clone[(df_clone['Data Benef'] >= data_inicio) & (df_clone['Data Benef'] <= data_fim) & (df_clone['Variedade'] == tipo_selecionado)]
    if not df_filtrado.empty:
         
        df_agrupado = df_filtrado.groupby(['Data Benef', 'Variedade'])['Peso'].agg(['sum', 'count']).reset_index()
        df_agrupado.columns = ['Data Benef', 'Variedade', 'Peso Total', 'Quantidade']

        #Criando os gráficos
        st.subheader(f"Peso Total e Quantidade para o Tipo: {tipo_selecionado}")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='Data Benef', y='Peso Total', hue='Variedade', data=df_agrupado, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig) 

        st.subheader("Quantidade por Tipo")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.lineplot(x='Data Benef', y='Quantidade', hue='Variedade', data=df_agrupado, ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)
    else:
        st.warning("Nenhum dado encontrado para este período.")