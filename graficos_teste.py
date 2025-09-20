
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

classifica = pd.read_excel('/home/nisiohelande/Documents/Teste-Apresentação.xlsx')


classifica.columns = classifica.iloc[1]
classifica.drop([0, 1], inplace=True)


df_clone = pd.DataFrame(classifica.loc[:, ['Número', 'Bloco', 'Talhão', 'Data Benef', 'Tipo',  'Variedade']])
df_clone['Data Benef'] = pd.to_datetime(df_clone['Data Benef'], format='%d/%m/%Y', errors="coerce")


st.title("Visualizador de Produção")

# Seleção de período com Streamlit
col1, col2 = st.columns(2)
with col1:
    data_inicio = st.date_input("Data de Início", value=datetime.date(2024, 1, 1))
with col2:
    data_fim = st.date_input("Data de Fim", value=datetime.date(2024, 1, 31))


# Converter datas para o formato necessário para o Pandas
data_inicio = pd.to_datetime(data_inicio)
data_fim = pd.to_datetime(data_fim)

#Verificação das datas
if data_inicio > data_fim:
    st.error("Data de início deve ser anterior à data de fim.")
else:
    df_filtrado = df[(df['Data Benef'] >= data_inicio) & (df['Data Benef'] <= data_fim)]
    if not df_filtrado.empty:
        df_agrupado = df_filtrado.groupby(['Data Benef', 'Tipo'])['Peso'].agg(['sum', 'count']).reset_index()
        df_agrupado.columns = ['Data Benef', 'Tipo', 'Peso Total', 'Quantidade']

        #Criando os gráficos
        st.subheader("Peso Total por Tipo")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x='Data Benef', y='Peso Total', hue='Tipo', data=df_agrupado, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.subheader("Quantidade por Tipo")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.lineplot(x='Data Benef', y='Quantidade', hue='Tipo', data=df_agrupado, ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)
    else:
        st.warning("Nenhum dado encontrado para este período.")