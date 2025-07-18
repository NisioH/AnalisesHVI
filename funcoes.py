import pandas as pd

class Funcoes:

    @staticmethod
    def mic_fora_padrao_baixa_resistencia(df_clone):
        # Filtra as amostras que estão fora do padrão de Micronaire e que apresentam resistência abaixo de 28.

        Mic_fora_padrao_baixa_resistencia = (df_clone['Mic_fora_padrao'] == True) & (df_clone['baixa_resistencia'] == True)
        Mic_fora_padrao_baixa_resistencia = df_clone.loc[Mic_fora_padrao_baixa_resistencia, ['Tp.Visual', 'UN']]

        totais_por_visual = Mic_fora_padrao_baixa_resistencia['Tp.Visual'].value_counts().sort_index()

        detalhamento = Mic_fora_padrao_baixa_resistencia.groupby(['Tp.Visual', 'UN']).size().sort_index()


        for tp_visual in totais_por_visual.index:
            print(f"{tp_visual}\t{totais_por_visual[tp_visual]}")
            un_grupo = detalhamento.loc[tp_visual]
            if isinstance(un_grupo, pd.Series):  # múltiplos UNs
                for un, contagem in un_grupo.items():
                    print(f"{un}\t{contagem}")
            else:  # apenas um UN
                print(f"{un_grupo.name}\t{un_grupo}")
            print()
               
        
    @staticmethod
    def mic_padrao_baixa_resistencia(df_clone ):

        Mic_padrao_baixa_resistencia = (df_clone['Mic_fora_padrao'] == False) & (df_clone['baixa_resistencia'] == True)
        Mic_padrao_baixa_resistencia = df_clone.loc[Mic_padrao_baixa_resistencia, ['Tp.Visual', 'UN']]


        totais_por_visual = Mic_padrao_baixa_resistencia['Tp.Visual'].value_counts().sort_index()

        detalhamento = Mic_padrao_baixa_resistencia.groupby(['Tp.Visual', 'UN']).size().sort_index()

        for tp_visual in totais_por_visual.index:
            print(f"{tp_visual}\t{totais_por_visual[tp_visual]}")
            un_grupo = detalhamento.loc[tp_visual]
            if isinstance(un_grupo, pd.Series):  # múltiplos UNs
                for un, contagem in un_grupo.items():
                    print(f"{un}\t{contagem}")
            else:  # apenas um UN
                print(f"{un_grupo.name}\t{un_grupo}")
            print()
    

    @staticmethod
    def mic_fora_padrao_boa_resistencia(df_clone):

        Mic_fora_padrao_resistencia = (df_clone['Mic_fora_padrao'] == True) & (df_clone['baixa_resistencia'] == False)
        Mic_fora_padrao_resistencia = df_clone.loc[Mic_fora_padrao_resistencia, ['Tp.Visual', 'UN']]


        totais_por_visual = Mic_fora_padrao_resistencia['Tp.Visual'].value_counts().sort_index()

        detalhamento = Mic_fora_padrao_resistencia.groupby(['Tp.Visual', 'UN']).size().sort_index()

        for tp_visual in totais_por_visual.index:
            print(f"{tp_visual}\t{totais_por_visual[tp_visual]}")
            un_grupo = detalhamento.loc[tp_visual]
            if isinstance(un_grupo, pd.Series):  # múltiplos UNs
                for un, contagem in un_grupo.items():
                    print(f"{un}\t{contagem}")
            else:  # apenas um UN
                print(f"{un_grupo.name}\t{un_grupo}")
            print()

    
    @staticmethod
    def mic_padrao_boa_resistencia(df_clone):
        # Filtra amostras com Micronaire dentro do padrão e resistência >= 28
        filtro = (df_clone['Mic_fora_padrao'] == False) & (df_clone['baixa_resistencia'] == False)
        dados_filtrados = df_clone.loc[filtro, ['Tp.Visual', 'UN']]

        # Conta totais por Tp.Visual
        totais_por_visual = dados_filtrados['Tp.Visual'].value_counts().sort_index()

        # Agrupa por Tp.Visual e UN
        detalhamento = dados_filtrados.groupby(['Tp.Visual', 'UN']).size().sort_index()

        # Impressão formatada
        for tp_visual in sorted(totais_por_visual.index):
            print(f"{tp_visual}\t{totais_por_visual[tp_visual]}")
            un_grupo = detalhamento.loc[tp_visual]
            if isinstance(un_grupo, pd.Series):  # múltiplos UNs
                for un, contagem in un_grupo.items():
                    print(f"\t{un}\t{contagem}")
            else:  # apenas um UN
                print(f"\t{un_grupo.name}\t{un_grupo}")
            print()
    

    @staticmethod
    def mic_fora_padrao_variedade(df_clone):

        # Filtra as variedades das amostras que estão fora do padrão de Micronaire.

        Mic_fora_padrao_variedade = (df_clone['Mic_fora_padrao'] == True)
        Mic_fora_padrao_variedade = df_clone.loc[Mic_fora_padrao_variedade, ['Variedade']]
                                                 
        totais_por_visual = Mic_fora_padrao_variedade['Variedade'].value_counts()
        print(totais_por_visual)
    

    @staticmethod
    def mic_padrao_variedade(df_clone):
        # Filtra as variedades das amostras que estão dentro do padrão de Micronaire.

        Mic_padrao_variedade = (df_clone['Mic_fora_padrao'] == False)
        Mic_padrao_variedade = df_clone.loc[Mic_padrao_variedade, ['Variedade']]
                                                 
        totais_por_visual = Mic_padrao_variedade['Variedade'].value_counts()
        print(totais_por_visual)

       

            