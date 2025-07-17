import pandas as pd

class Funcoes:

    @staticmethod
    def mic_fora_padrao_baixa_resistencia(df_clone):
        # Filtra as amostras que estão fora do padrão de Micronaire e que apresentam resistência abaixo de 28.

        Mic_fora_padrao_baixa_resistencia = (df_clone['Mic_fora_padrao'] == True) & (df_clone['baixa_resistencia'] == True)
        Mic_fora_padrao_baixa_resistencia = df_clone.loc[Mic_fora_padrao_baixa_resistencia, ['Tp.Visual', 'UN']]

        totais_por_visual = Mic_fora_padrao_baixa_resistencia['Tp.Visual'].value_counts()

        detalhamento = Mic_fora_padrao_baixa_resistencia.groupby(['Tp.Visual', 'UN']).size()


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


        totais_por_visual = Mic_padrao_baixa_resistencia['Tp.Visual'].value_counts()

        detalhamento = Mic_padrao_baixa_resistencia.groupby(['Tp.Visual', 'UN']).size()

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


        totais_por_visual = Mic_fora_padrao_resistencia['Tp.Visual'].value_counts()

        detalhamento = Mic_fora_padrao_resistencia.groupby(['Tp.Visual', 'UN']).size()

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
        
        Mic_padrao_resistencia = (df_clone['Mic_fora_padrao'] == False) & (df_clone['baixa_resistencia'] == False)
        Mic_padrao_resistencia = df_clone.loc[Mic_padrao_resistencia, ['Tp.Visual', 'UN']]


        totais_por_visual = Mic_padrao_resistencia['Tp.Visual'].value_counts()

        detalhamento = Mic_padrao_resistencia.groupby(['Tp.Visual', 'UN']).size()

        for tp_visual in totais_por_visual.index:
            print(f"{tp_visual}\t{totais_por_visual[tp_visual]}")
            un_grupo = detalhamento.loc[tp_visual]
            if isinstance(un_grupo, pd.Series):  # múltiplos UNs
                for un, contagem in un_grupo.items():
                    print(f"{un}\t{contagem}")
            else:  # apenas um UN
                print(f"{un_grupo.name}\t{un_grupo}")
            print()