import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np  # Importação necessária para a máscara
import os

def realizar_eda():
    print("📊 Iniciando Análise Exploratória (EDA) com Seaborn...")
    
    # 1. Carregar o dataset higienizado
    file_path = "data/processed/agro_predict_dataset_v1.csv"
    if not os.path.exists(file_path):
        print("❌ Erro: O dataset final não foi encontrado em data/processed/!")
        return
        
    df = pd.read_csv(file_path, parse_dates=['Date'])
    
    # 2. Preparar dados (remover colunas não numéricas para correlação)
    df_numeric = df.drop(columns=['Date'])
    corr = df_numeric.corr()

    # --- VISUALIZAÇÃO 1: HEATMAP ---
    plt.figure(figsize=(12, 8))
    sns.set_theme(style="white")
    
    # Criando a máscara para esconder a parte repetida (triângulo superior)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Mapa de calor profissional
    sns.heatmap(corr, annot=True, cmap='RdYlGn', center=0, fmt='.2f', 
                linewidths=0.5, mask=mask)
    
    plt.title('Mapa de Correlação AgroPredict (Cluster 1 a 6)', fontsize=15)
    
    # Garantir que a pasta de relatórios exista
    os.makedirs("reports/figures", exist_ok=True)
    
    plt.savefig('reports/figures/correlation_heatmap.png')
    print("✅ Heatmap salvo em reports/figures/correlation_heatmap.png")

    # --- VISUALIZAÇÃO 2: SOJA vs SENTIMENTO (COT) ---
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='COT_Posicao_Liquida', y='Soja_Chicago', 
                scatter_kws={'alpha':0.2, 'color':'teal'}, 
                line_kws={'color':'red', 'label':'Tendência'})
    
    plt.title('Influência do Sentimento dos Fundos (COT) no Preço', fontsize=14)
    plt.xlabel('Posição Líquida (Contratos Comprados - Vendidos)')
    plt.ylabel('Preço Soja Chicago (US$/bu)')
    plt.savefig('reports/figures/soja_vs_cot.png')

    # --- VISUALIZAÇÃO 3: SOJA vs CLIMA (ONI) ---
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='Indice_ONI_Clima', y='Soja_Chicago', 
                scatter_kws={'alpha':0.2, 'color':'blue'}, 
                line_kws={'color':'orange'})
    
    plt.title('Impacto do Índice ONI (Clima) no Preço', fontsize=14)
    plt.xlabel('Anomalia ONI (Negativo = La Niña / Positivo = El Niño)')
    plt.ylabel('Preço Soja Chicago (US$/bu)')
    plt.savefig('reports/figures/soja_vs_oni.png')

    print("🚀 Análise concluída! Verifique a pasta reports/figures/")
    
    # Mostrar as correlações diretas com a Soja no Terminal
    print("\n📈 Ranking de Correlação Direta com a Soja (Chicago):")
    print(corr['Soja_Chicago'].sort_values(ascending=False))

if __name__ == "__main__":
    realizar_eda()