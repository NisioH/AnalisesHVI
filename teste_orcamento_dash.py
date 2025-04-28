import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Carregamento das planilhas
sheets = pd.read_excel("./Projeto Orçamento/Planilha Orçamento 24-25(valendo).xlsx", sheet_name=None)
orcado = pd.read_excel("./Projeto Orçamento/Orçado23-24.xlsx", sheet_name="Manutenção")
realizado = pd.read_excel("./Projeto Orçamento/Realizado23-24.xlsx")

# Ajustes nos DataFrames
df_clone_orcado = orcado.loc[:, ['Safra', 'Dt. Mvto', 'Dt.Vcto', 'Doc.Num.', 'Histórico', 'Débito', 'Cliente/Fornecedor']]
realizado.columns = realizado.iloc[1]
realizado.drop([0, 1], inplace=True)
df_clone_realizado = realizado.loc[:, ['Safra', 'Doc.Num.', 'Produto', 'Data Uso', 'Total', 'Valor Total', 'Valor Médio']]

# Processamento das planilhas
for sheet_name, df in sheets.items():
    if sheet_name == "Revisões":
        sheets[sheet_name] = df.drop(index=0, errors="ignore")
    else:
        if len(df) > 2:
            sheets[sheet_name] = df.iloc[2:].reset_index(drop=True)
            sheets[sheet_name].columns = df.iloc[1]
        else:
            sheets[sheet_name] = pd.DataFrame()

# Inicializando o aplicativo Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Análise de Orçamento"),
    dcc.Dropdown(
        id='grafico-selector',
        options=[{'label': desc, 'value': desc} for desc in sheets["Revisões"]["Descrição"].dropna().unique()],
        placeholder="Selecione um gráfico"
    ),
    dcc.Graph(id="grafico"),
    html.H3("Tabela do Gráfico"),
    dash_table.DataTable(id="tabela-grafico"),
    html.H3("Orçado 23-24"),
    dash_table.DataTable(id="orcado-tabela"),
    html.H3("Realizado 23-24"),
    dash_table.DataTable(id="realizado-tabela")
])

@app.callback(
    [Output("grafico", "figure"), 
     Output("tabela-grafico", "data"), Output("tabela-grafico", "columns"),
     Output("orcado-tabela", "data"), Output("orcado-tabela", "columns"),
     Output("realizado-tabela", "data"), Output("realizado-tabela", "columns")],
    [Input("grafico-selector", "value")]
)
def update_content(selecao):
    if not selecao:
        return px.scatter(), [], [], [], [], [], []

    df_filtrado = sheets["Revisões"][sheets["Revisões"]["Descrição"] == selecao]
    df_grafico = df_filtrado.melt(id_vars=["Descrição"], var_name="Meses", value_name="Valores")
    df_grafico = df_grafico[~df_grafico["Meses"].isin(["Quantidade", "VALOR TOTAL"])]

    fig = px.bar(
        df_grafico,
        x="Meses",
        y="Valores",
        title=f"Valores Orçados {selecao} - Safra 24-25",
        labels={"Valores": "Valores (R$)"}
    )

    df_tabela = sheets.get(selecao, pd.DataFrame())
    tabela_grafico_data = df_tabela.to_dict("records")
    tabela_grafico_columns = [{"name": col, "id": col} for col in df_tabela.columns]

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

    orcado_data = total_orcado.to_dict("records")
    orcado_columns = [{"name": col, "id": col} for col in total_orcado.columns]

    realizado_data = total_realizado.to_dict("records")
    realizado_columns = [{"name": col, "id": col} for col in total_realizado.columns]

    return fig, tabela_grafico_data, tabela_grafico_columns, orcado_data, orcado_columns, realizado_data, realizado_columns

if __name__ == '__main__':
    app.run_server(debug=True)