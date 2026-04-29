import pandas as pd
import requests
import zipfile
import io
import os

def baixar_cot_historico():
    print("📦 Iniciando coleta de dados do COT - Versão Auditoria Total...")
    
    anos = list(range(2000, 2027))
    dfs = []

    for ano in anos:
        try:
            url = f"https://www.cftc.gov/files/dea/history/deacot{ano}.zip"
            r = requests.get(url)
            
            if r.status_code == 200:
                print(f"📥 Processando ano {ano}...")
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    filename = z.namelist()[0]
                    with z.open(filename) as f:
                        # CFTC costuma usar vírgula, mas às vezes o delimitador varia
                        temp_df = pd.read_csv(f, low_memory=False)
                        
                        # Limpeza radical de colunas
                        temp_df.columns = [str(c).strip() for c in temp_df.columns]
                        
                        # Localizar a coluna de Mercado por palavra-chave (case insensitive)
                        col_mercado = next((c for c in temp_df.columns if 'MARKET' in c.upper() and 'NAME' in c.upper()), None)
                        
                        if col_mercado:
                            # Filtro resiliente para SOYBEANS
                            soja_filtro = temp_df[temp_df[col_mercado].astype(str).str.contains('SOYBEANS', na=False, case=False)].copy()
                            
                            if not soja_filtro.empty:
                                # Padronizar nome para o merge futuro
                                soja_filtro.rename(columns={col_mercado: 'Market_Name'}, inplace=True)
                                
                                # Localizar a coluna de Data por palavra-chave
                                col_data = next((c for c in temp_df.columns if 'DATE' in c.upper()), None)
                                if col_data:
                                    soja_filtro.rename(columns={col_data: 'Date'}, inplace=True)
                                
                                dfs.append(soja_filtro)
            else:
                if ano < 2026: print(f"⚠️ Link indisponível para {ano}")
        except Exception as e:
            print(f"❌ Erro no ano {ano}: {e}")

    if dfs:
        df_completo = pd.concat(dfs, ignore_index=True, sort=False)
        df_completo['Date'] = pd.to_datetime(df_completo['Date'], errors='coerce')
        df_completo = df_completo.sort_values('Date').dropna(subset=['Date'])

        os.makedirs("data/raw", exist_ok=True)
        df_completo.to_csv("data/raw/cot_soybeans_raw.csv", index=False)
        print(f"✅ Sucesso! {len(df_completo)} registros salvos.")
    else:
        print("❌ Falha: O padrão dos arquivos da CFTC mudou drasticamente.")

if __name__ == "__main__":
    baixar_cot_historico()