import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Análise de Orçamento", layout="wide")

sheets = pd.read_excel("Planilha Orçamento 24-25.xlsx", sheet_name=None)
orcado = pd.read_excel("Orçado23-24.xlsx", sheet_name="Manutenção")
realizado = pd.read_excel("Realizado23-24-08Mai2025.xlsx")

df_clone_orcado = orcado.loc[:, ['Safra', 'Dt. Mvto', 'Dt.Vcto', 'Doc.Num.', 'Histórico', 'Débito', 'Cliente/Fornecedor']]
realizado.columns = realizado.iloc[1]
realizado.drop([0, 1], inplace=True)
df_clone_realizado = realizado.loc[:, ['Safra', 'Doc.Num.', 'Produto', 'Data Uso', 'Total', 'Valor Médio', 'Valor Total']]
df_clone_realizado['Valor Total'] = pd.to_numeric(df_clone_realizado['Valor Total'], errors='coerce').round(2)


for sheet_name, df in sheets.items():
    if sheet_name == "Revisões":
        sheets[sheet_name] = df.drop(index=0, errors="ignore")
    else:
        if len(df) > 2:
            sheets[sheet_name] = df.iloc[2:].reset_index(drop=True)
            sheets[sheet_name].columns = df.iloc[1]
        else:
            sheets[sheet_name] = pd.DataFrame()


st.sidebar.title("Análise de Orçamento")
selecao = st.sidebar.selectbox(
    "Selecione um gráfico:", 
    sheets["Revisões"]["Descrição"].dropna().unique()
)

if selecao:
  
    df_filtrado = sheets["Revisões"][sheets["Revisões"]["Descrição"] == selecao]
    df_grafico = df_filtrado.melt(id_vars=["Descrição"], var_name="Meses", value_name="Valores")
    df_grafico = df_grafico[~df_grafico["Meses"].isin(["Quantidade", "VALOR TOTAL"])]

    fig = px.bar(
        df_grafico,
        x="Meses",
        y="Valores",
        title=f"Valores Orçados {selecao} - Safra 24-25: ",
        labels={"Valores": "Valores (R$)"}
    )

    fig.update_traces(
        text=df_grafico["Valores"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")),
        textposition="outside"
    )

    fig.update_layout(
        yaxis=dict(tickprefix="R$ ", tickformat=",.2f", showgrid=True)
    )

    st.plotly_chart(fig, use_container_width=True)


    df_orcado_filtrado = df_clone_orcado[df_clone_orcado["Doc.Num."].isin(df_filtrado["Descrição"])]
    df_realizado_filtrado = df_clone_realizado[df_clone_realizado["Doc.Num."].isin(df_filtrado["Descrição"])]

    df_orcado_filtrado["Débito"] = pd.to_numeric(df_orcado_filtrado["Débito"], errors="coerce")
    df_realizado_filtrado["Valor Total"] = pd.to_numeric(df_realizado_filtrado["Valor Total"], errors="coerce")

  
    total_orcado = df_orcado_filtrado.copy()
    total_orcado.loc["Total"] = total_orcado.select_dtypes(include=['number']).sum()
    total_orcado.loc["Total", "Doc.Num."] = "TOTAL"

    total_realizado = df_realizado_filtrado.copy()
    total_realizado.loc["Total"] = total_realizado.select_dtypes(include=['number']).sum()
    total_realizado.loc["Total", "Doc.Num."] = "TOTAL"

   
    total_orcado.fillna("", inplace=True)
    total_realizado.fillna("", inplace=True)

   
    def formatar_moeda(valor):
        try:
            return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except ValueError:
            return valor  

    for coluna in ["Débito"]:
        if coluna in total_orcado.columns:
            total_orcado[coluna] = total_orcado[coluna].apply(lambda x: formatar_moeda(x) if pd.notna(x) else "")

    for coluna in ["Valor Total", "Valor Médio"]:
        if coluna in total_realizado.columns:
            total_realizado[coluna] = total_realizado[coluna].apply(lambda x: formatar_moeda(x) if pd.notna(x) else "")

   
    df_tabela = sheets.get(selecao, pd.DataFrame())

    def formatar_valores(valor, coluna):
        if pd.isna(valor):
            return "-"
        elif coluna == "Quantidade" and isinstance(valor, (int, float)):
            return f"{int(valor):,}".replace(",", ".")
        elif isinstance(valor, (int, float)):
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return valor

    if not df_tabela.empty:
        df_formatado = df_tabela.copy()
        for coluna in df_formatado.columns:
            df_formatado[coluna] = df_formatado[coluna].apply(lambda x: formatar_valores(x, coluna))

        st.subheader(f"Tabela {selecao} - Safra: 24-25")
        st.dataframe(df_formatado, hide_index=True)
    else:
        st.subheader("Nenhuma informação disponível.")

    
    st.subheader(f"Orçado {selecao} - Safra: 23-24")
    st.dataframe(total_orcado, hide_index=True)

    st.subheader(f"Realizado {selecao} - Safra: 23-24")
    st.dataframe(total_realizado, hide_index=True)

else:
    st.write("Selecione um gráfico na barra lateral.")