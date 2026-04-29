import pandas as pd
import os

def unificar_dados_mestre():
    print("🔗 Iniciando a SUPER UNIFICAÇÃO (Mercado + Clima + COT)...")
    
    # 1. Carregar Mercado (Preços Diários)
    df_mercado = pd.read_csv("data/raw/market_essentials.csv", parse_dates=['Date'])
    
    # 2. Carregar Clima (Índice ONI Mensal)
    df_clima = pd.read_csv("data/raw/oni_index_history.csv")
    meses_map = {'DJF': 1, 'JFM': 2, 'FMA': 3, 'MAM': 4, 'AMJ': 5, 'MJJ': 6, 
                 'JJA': 7, 'JAS': 8, 'ASO': 9, 'SON': 10, 'OND': 11, 'NDJ': 12}
    df_clima['Month'] = df_clima['SEAS'].map(meses_map)
    
    # 3. Carregar Sentimento (COT Semanal)
    # Usamos a coluna 'As of Date in Form YYYY-MM-DD' que está correta
    df_cot = pd.read_csv("data/raw/cot_soybeans_raw.csv", low_memory=False)
    df_cot['Date_COT'] = pd.to_datetime(df_cot['As of Date in Form YYYY-MM-DD'])
    
    # Selecionamos as colunas fundamentais para o Cluster 6
    colunas_cot = {
        'Date_COT': 'Date',
        'Noncommercial Positions-Long (All)': 'COT_Spec_Comprados',
        'Noncommercial Positions-Short (All)': 'COT_Spec_Vendidos',
        'Open Interest (All)': 'COT_Open_Interest'
    }
    df_cot = df_cot[list(colunas_cot.keys())].rename(columns=colunas_cot)
    
    # Cálculo de Auditoria: Posição Líquida (Net Position)
    df_cot['COT_Posicao_Liquida'] = df_cot['COT_Spec_Comprados'] - df_cot['COT_Spec_Vendidos']

    # --- INÍCIO DO CRUZAMENTO ---
    
    # Criar colunas de apoio para o clima
    df_mercado['Year'] = df_mercado['Date'].dt.year
    df_mercado['Month'] = df_mercado['Date'].dt.month
    
    # Join 1: Mercado + Clima
    df_final = pd.merge(df_mercado, df_clima[['YR', 'Month', 'ANOM']], 
                        left_on=['Year', 'Month'], right_on=['YR', 'Month'], how='left')
    df_final.rename(columns={'ANOM': 'Indice_ONI_Clima'}, inplace=True)
    
    # Join 2: Mercado/Clima + COT
    # Como o COT é semanal, fazemos um merge_asof (típico de mercado financeiro)
    # Ele busca a última informação disponível do COT para cada data de mercado
    df_final = df_final.sort_values('Date')
    df_cot = df_cot.sort_values('Date')
    
    df_final = pd.merge_asof(df_final, df_cot, on='Date', direction='backward')
    
    # 4. Limpeza e Salvamento
    df_final.drop(columns=['YR', 'Year', 'Month'], inplace=True)
    
    caminho_saida = "data/processed/master_data_final.csv"
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df_final.to_csv(caminho_saida, index=False)
    
    print(f"✅ Sucesso Total! Tabela Mestre criada com {len(df_final)} linhas.")
    print("📋 Colunas finais:", df_final.columns.tolist())
    print(df_final.tail(10))

if __name__ == "__main__":
    unificar_dados_mestre()