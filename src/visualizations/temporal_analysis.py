import pandas as pd
import matplotlib.pyplot as plt
import os

def gerar_analise_historica():
    print("⏳ Gerando Análise Temporal Completa (2000-2026)...")
    
    # 1. Carregar o dataset
    file_path = "data/processed/agro_predict_dataset_v1.csv"
    df = pd.read_csv(file_path, parse_dates=['Date'])
    
    # Garantir pasta de saída
    os.makedirs("reports/historical", exist_ok=True)

    # --- GRÁFICO 1: O GRANDE HISTÓRICO (SOJA vs PETRÓLEO) ---
    # Usamos dois eixos (Y) porque os preços são em escalas diferentes
    fig, ax1 = plt.subplots(figsize=(14, 7))

    color = 'tab:green'
    ax1.set_xlabel('Anos')
    ax1.set_ylabel('Preço Soja Chicago (US$/bu)', color=color, fontsize=12)
    ax1.plot(df['Date'], df['Soja_Chicago'], color=color, label='Soja', linewidth=1.5)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # Cria o segundo eixo Y
    color = 'tab:red'
    ax2.set_ylabel('Preço Petróleo WTI (US$/barril)', color=color, fontsize=12)
    ax2.plot(df['Date'], df['Petroleo_WTI'], color=color, label='Petróleo', alpha=0.5, linewidth=1)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Série Histórica: Soja vs. Petróleo (2000-2026)', fontsize=16)
    fig.tight_layout() # Garante que nada seja cortado
    plt.grid(True, alpha=0.3)
    plt.savefig('reports/historical/historico_soja_petroleo.png')

    # --- GRÁFICO 2: CICLOS CLIMÁTICOS POR ANO ---
    # Vamos ver a média anual do preço da soja versus o Índice ONI
    df['Year'] = df['Date'].dt.year
    anual = df.groupby('Year').agg({'Soja_Chicago':'mean', 'Indice_ONI_Clima':'mean'}).reset_index()

    fig, ax1 = plt.subplots(figsize=(14, 7))

    ax1.bar(anual['Year'], anual['Soja_Chicago'], color='gray', alpha=0.4, label='Preço Médio Anual')
    ax1.set_ylabel('Média Anual Soja (US$/bu)')
    ax1.set_xlabel('Ano')

    ax2 = ax1.twinx()
    ax2.plot(anual['Year'], anual['Indice_ONI_Clima'], color='blue', marker='o', label='Índice ONI (Clima)')
    ax2.axhline(0, color='black', linestyle='--', linewidth=1) # Linha do neutro
    ax2.fill_between(anual['Year'], 0, anual['Indice_ONI_Clima'], where=(anual['Indice_ONI_Clima'] >= 0), color='red', alpha=0.2, label='El Niño')
    ax2.fill_between(anual['Year'], 0, anual['Indice_ONI_Clima'], where=(anual['Indice_ONI_Clima'] < 0), color='blue', alpha=0.2, label='La Niña')
    ax2.set_ylabel('Intensidade do Clima (ONI)')

    plt.title('Médias Anuais: Preço da Soja vs. Ciclos Climáticos', fontsize=16)
    fig.tight_layout()
    plt.savefig('reports/historical/historico_clima_anual.png')

    print("🚀 Gráficos históricos gerados sem cortes em reports/historical/")

if __name__ == "__main__":
    gerar_analise_historica()