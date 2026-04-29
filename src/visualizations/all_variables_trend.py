import pandas as pd
import matplotlib.pyplot as plt
import os

def gerar_tendencia_global():
    print("📈 Gerando Gráfico de Tendências Normalizadas (Todas as Variáveis)...")
    
    # 1. Carregar o dataset
    file_path = "data/processed/agro_predict_dataset_v1.csv"
    if not os.path.exists(file_path):
        print("❌ Erro: Dataset não encontrado!")
        return
        
    df = pd.read_csv(file_path, parse_dates=['Date'])
    
    # 2. Selecionar colunas para comparar
    colunas_interesse = [
        'Soja_Chicago', 
        'Petroleo_WTI', 
        'COT_Posicao_Liquida', 
        'Indice_ONI_Clima'
    ]
    
    # 3. Normalização Min-Max (Transforma tudo para escala 0-1)
    df_norm = df[['Date']].copy()
    for col in colunas_interesse:
        min_val = df[col].min()
        max_val = df[col].max()
        df_norm[col] = (df[col] - min_val) / (max_val - min_val)

    # 4. Criar o Gráfico
    plt.figure(figsize=(15, 8))
    
    plt.plot(df_norm['Date'], df_norm['Soja_Chicago'], label='SOJA (Alvo)', color='green', linewidth=2.5, zorder=5)
    plt.plot(df_norm['Date'], df_norm['Petroleo_WTI'], label='Petróleo (Energia)', color='red', alpha=0.6, linewidth=1)
    plt.plot(df_norm['Date'], df_norm['COT_Posicao_Liquida'], label='Fundos (Sentimento)', color='blue', alpha=0.5, linewidth=1)
    plt.plot(df_norm['Date'], df_norm['Indice_ONI_Clima'], label='Clima (ONI)', color='orange', alpha=0.5, linestyle='--')

    # Estilização
    plt.title('Tendência Global Normalizada: O que move a Soja? (2000-2026)', fontsize=16)
    plt.xlabel('Linha do Tempo (Anos)', fontsize=12)
    plt.ylabel('Escala Normalizada (0 a 1)', fontsize=12)
    plt.legend(loc='upper left', frameon=True)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Salvar e Mostrar
    os.makedirs("reports/historical", exist_ok=True)
    plt.savefig('reports/historical/tendencia_global_normalizada.png')
    
    print("✅ Gráfico gerado! Abrindo janela...")
    plt.show()

if __name__ == "__main__":
    gerar_tendencia_global()