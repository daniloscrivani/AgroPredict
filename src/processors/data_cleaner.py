import pandas as pd
import os

def limpar_dados_mestre():
    print("🧼 Iniciando a limpeza e higienização do Dataset Mestre...")
    
    # 1. Carregar a tabela v2 (que contém tudo)
    caminho_entrada = "data/processed/master_data_final.csv"
    if not os.path.exists(caminho_entrada):
        print("❌ Erro: Arquivo master_data_final.csv não encontrado!")
        return

    df = pd.read_csv(caminho_entrada, parse_dates=['Date'])
    
    # 2. Desfragmentação (Resolve o PerformanceWarning)
    df = df.copy()
    
    # 3. Remover Duplicatas
    # Garante que cada data apareça apenas uma vez
    linhas_antes = len(df)
    df = df.drop_duplicates(subset=['Date'], keep='first')
    linhas_depois = len(df)
    
    if linhas_antes != linhas_depois:
        print(f"♻️  Removidas {linhas_antes - linhas_depois} linhas duplicadas.")
    
    # 4. Remover NaNs (Filtro de Qualidade)
    # Removemos qualquer linha que tenha valor vazio em colunas essenciais
    # Como você bem disse, a IA não usará dados incompletos de 2026
    df = df.dropna(subset=['Soja_Chicago', 'Petroleo_WTI', 'Indice_ONI_Clima'])
    
    # 5. Ordenação Final
    df = df.sort_values('Date')
    
    # 6. Salvar o "Golden Dataset"
    # Este é o arquivo que a IA realmente vai ler
    caminho_saida = "data/processed/agro_predict_dataset_v1.csv"
    df.to_csv(caminho_saida, index=False)
    
    print(f"✨ Sucesso! Dataset higienizado salvo em: {caminho_saida}")
    print(f"📊 Total de registros prontos para a IA: {len(df)}")
    print(df.tail())

if __name__ == "__main__":
    limpar_dados_mestre()