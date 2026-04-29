import pandas as pd
import os

def unificar_dados():
    print("🔗 Iniciando a unificação dos dados (Mercado + Clima)...")
    
    # 1. Carregar os dados
    df_mercado = pd.read_csv("data/raw/market_essentials.csv", parse_dates=['Date'])
    df_clima = pd.read_csv("data/raw/oni_index_history.csv")
    
    # 2. Preparar o Clima (ONI) para o casamento
    # O ONI usa 'YR' (Ano) e 'SEAS' (Estação/Mês). Vamos simplificar para facilitar o cruzamento.
    # Criamos uma coluna de data simplificada no clima
    meses_map = {'DJF': 1, 'JFM': 2, 'FMA': 3, 'MAM': 4, 'AMJ': 5, 'MJJ': 6, 
                 'JJA': 7, 'JAS': 8, 'ASO': 9, 'SON': 10, 'OND': 11, 'NDJ': 12}
    
    df_clima['Month'] = df_clima['SEAS'].map(meses_map)
    
    # 3. Criar colunas temporárias no mercado para o cruzamento
    df_mercado['Year'] = df_mercado['Date'].dt.year
    df_mercado['Month'] = df_mercado['Date'].dt.month
    
    # 4. O "Casamento" (Merge)
    # Vamos trazer a coluna 'ANOM' (que é o índice do El Niño) para a tabela de mercado
    df_final = pd.merge(df_mercado, df_clima[['YR', 'Month', 'ANOM']], 
                        left_on=['Year', 'Month'], 
                        right_on=['YR', 'Month'], 
                        how='left')
    
    # 5. Limpeza Final
    df_final.drop(columns=['YR', 'Year', 'Month'], inplace=True)
    df_final.rename(columns={'ANOM': 'Indice_ONI_Clima'}, inplace=True)
    
    # Salvar o resultado na pasta 'processed'
    caminho_saida = "data/processed/master_data.csv"
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df_final.to_csv(caminho_saida, index=False)
    
    print(f"✅ Sucesso! Tabela mestre criada com {len(df_final)} linhas.")
    print(df_final.tail())

if __name__ == "__main__":
    unificar_dados()