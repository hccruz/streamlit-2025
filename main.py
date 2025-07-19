import streamlit as st
import pandas as pd

def calc_general_stats(df:pd.DataFrame):
    df_data = df.groupby(by='Data')[['Valor']].sum()
    df_data['lag_1'] = df_data['Valor'].shift(1)
    df_data['Diferença Mensal Abs.'] = df_data['Valor'] - df_data['lag_1']
    df_data['Média 6M Diferença Mensal Abs.']= df_data['Diferença Mensal Abs.'].rolling(6).mean()
    df_data['Média 12M Diferença Mensal Abs.'] = df_data['Diferença Mensal Abs.'].rolling(12).mean()
    df_data['Média 24M Diferença Mensal Abs.'] = df_data['Diferença Mensal Abs.'].rolling(24).mean()
    
    df_data['Diferença Mensal Rel.'] = df_data['Valor'] / df_data['lag_1'] - 1
    
    df_data['Evolução 6M Total'] = df_data['Valor'].rolling(6).apply(lambda x: x[-1] - x[0])
    df_data['Evolução 12M Total'] = df_data['Valor'].rolling(12).apply(lambda x: x[-1] - x[0])
    df_data['Evolução 24M Total'] = df_data['Valor'].rolling(24).apply(lambda x: x[-1] - x[0])
    
    df_data['Evolução 6M Relativa'] = df_data['Valor'].rolling(6).apply(lambda x: x[-1] / x[0] - 1)
    df_data['Evolução 12M Relativa'] = df_data['Valor'].rolling(12).apply(lambda x: x[-1] / x[0] - 1)
    df_data['Evolução 24M Relativa'] = df_data['Valor'].rolling(24).apply(lambda x: x[-1] / x[0] - 1)
    
    df_data = df_data.drop('lag_1', axis=1)
    
    return df_data

st.set_page_config(page_title='Finanças', page_icon='💰')

st.markdown('''
            # Boas vindas!
            
            ## Nosso APP Financeiro!
            
            Espero que você curta a experiência da nossa solução para organização financeira.
            
            ''')

# Widget de upload de dados
file_upload = st.file_uploader(label='Faça o upload dos dados aqui', type=['csv'])

# Verifica se algum arquivo foi feito o upload
if file_upload:
    
    # Leitura dos dados
    df = pd.read_csv(file_upload)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date
        
    # Exibição dos dados no App
    exp1 = st.expander('Dados Brutos')
    columns_fmt = {'Valor': st.column_config.NumberColumn('Valor', format='R$%d')}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)
    
    # Visão Instituição
    exp2 = st.expander('Instituições')
    df_instituicao = df.pivot_table(index='Data', columns='Instituição', values='Valor')
    
    # Abas para diferentes visualizações
    tab_data, tab_history, tab_share = exp2.tabs(['Dados', 'Histórico', 'Distribuição'])
    
    # Exibe Dataframe
    with tab_data:
        st.dataframe(df_instituicao)
    
    # Exibe Histórico
    with tab_history:
        st.line_chart(df_instituicao)
    
    # Exibe Distribuição
    with tab_share:
        
        # Filtro de data
        date = st.selectbox('Data', options=df_instituicao.index)
        
        # Gráfico de distribuição
        st.bar_chart(df_instituicao.loc[date])
    
    exp3 = st.expander('Estatísticas Gerais')
    tab_stats, tab_abs, tab_rel = exp3.tabs(tabs=['Estatísticas', 'Histórico de Evolução', 'Crescimento Relativo'])
    
    df_stats = calc_general_stats(df)    
    columns_config = {
        'Valor': st.column_config.NumberColumn('Valor', format='R$ %.2f'),
        'Diferença Mensal Abs.': st.column_config.NumberColumn('Diferença Mensal Abs.', format='R$ %.2f'),
        'Média 6M Diferença Mensal Abs.': st.column_config.NumberColumn('Média 6M Diferença Mensal Abs.', format='R$ %.2f'),
        'Média 12M Diferença Mensal Abs.': st.column_config.NumberColumn('Média 12M Diferença Mensal Abs.', format='R$ %.2f'),
        'Média 24M Diferença Mensal Abs.': st.column_config.NumberColumn('Média 24M Diferença Mensal Abs.', format='R$ %.2f'),
        'Diferença Mensal Rel.':st.column_config.NumberColumn('Diferença Mensal Rel.', format='percent'),
        'Evolução 6M Total': st.column_config.NumberColumn('Evolução 6M Total', format='R$ %.2f'),
        'Evolução 12M Total': st.column_config.NumberColumn('Evolução 12M Total', format='R$ %.2f'),
        'Evolução 24M Total': st.column_config.NumberColumn('Evolução 24M Total', format='R$ %.2f'),
        'Evolução 6M Relativa': st.column_config.NumberColumn('Evolução 6M Relativa', format='percent'),
        'Evolução 12M Relativa': st.column_config.NumberColumn('Evolução 12M Relativa', format='percent'),
        'Evolução 24M Relativa': st.column_config.NumberColumn('Evolução 24M Relativa', format='percent')
    }
    
    with tab_stats:
        st.dataframe(df_stats, column_config=columns_config)
    
    with tab_abs:
        abs_col = [
            'Diferença Mensal Abs.',
            'Média 6M Diferença Mensal Abs.',
            'Média 12M Diferença Mensal Abs.',
            'Média 24M Diferença Mensal Abs.'
        ]
        
        st.line_chart(df_stats[abs_col])
    
    with tab_rel:
        rel_col = [
            'Diferença Mensal Rel.',
            'Evolução 6M Relativa',
            'Evolução 12M Relativa',
            'Evolução 24M Relativa'
        ]
        
        st.line_chart(df_stats[rel_col])


# Não tem arquivos...
